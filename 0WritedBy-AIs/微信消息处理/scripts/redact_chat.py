#!/usr/bin/env python3
"""对 export_chat / merge 导出的 JSON 做本地脱敏，支持 name_map.json 人名映射。"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

PHONE_RE = re.compile(r"1[3-9]\d{9}")
EMAIL_RE = re.compile(r"[\w.-]+@[\w.-]+\.\w+")
URL_RE = re.compile(r"https?://\S+")
ID_CARD_RE = re.compile(r"\d{17}[\dXx]|\d{15}")
WXID_RE = re.compile(r"wxid_[a-zA-Z0-9_-]+", re.I)

META_KEY_PREFIX = ("_", "$")
# 手写 JSON 常见：最后一项后多逗号
_TRAILING_COMMA_RE = re.compile(r",(\s*[}\]])")


def load_json_object(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    try:
        data = json.loads(text)
    except json.JSONDecodeError as err:
        fixed = _TRAILING_COMMA_RE.sub(r"\1", text)
        if fixed != text:
            try:
                data = json.loads(fixed)
                print(f"  提示: {path} 含尾随逗号，已自动修正后加载", file=sys.stderr)
            except json.JSONDecodeError:
                data = None
        else:
            data = None
        if data is None:
            raise ValueError(
                f"name_map JSON 解析失败: {path}\n"
                f"  {err.msg}（约第 {err.lineno} 行第 {err.colno} 列）\n"
                "  请检查：最后一项后不能有逗号；键名与字符串必须用双引号。"
            ) from err
    if not isinstance(data, dict):
        raise ValueError(f"name_map 必须是 JSON 对象 {{...}}: {path}")
    return data


def load_name_map(path: Path | None) -> tuple[dict[str, str], dict[str, str]]:
    """
    读取 name_map.json。
    返回 (content_map, role_defaults)。
    - content_map: 用于正文/备注里的称呼替换
    - role_defaults: $me / $peer / $other 等发送者默认代号
    """
    role_defaults = {
        "me": "USER_ME",
        "peer": "USER_PEER",
        "other": "OTHER_PERSON",
    }
    content_map: dict[str, str] = {}

    if path is None or not path.exists():
        return content_map, role_defaults

    raw = load_json_object(path)

    for key, value in raw.items():
        if not isinstance(value, str):
            continue
        if key.startswith("$"):
            role_key = key[1:].lower()
            if role_key in role_defaults:
                role_defaults[role_key] = value
            continue
        if key.startswith("_"):
            continue
        content_map[key] = value

    return content_map, role_defaults


def resolve_map_path(explicit: Path | None, inp: Path) -> Path | None:
    if explicit:
        return explicit
    candidates = [
        inp.parent / "name_map.json",
        inp.parent.parent / "name_map.json",
        Path(__file__).resolve().parent.parent / "work" / "name_map.json",
    ]
    for p in candidates:
        if p.exists():
            return p
    return None


def apply_name_map(text: str, name_map: dict[str, str]) -> str:
    """按最长优先替换正文中的称呼，避免短名误伤长名的一部分。"""
    if not text or not name_map:
        return text
    for name in sorted(name_map.keys(), key=len, reverse=True):
        if name:
            text = text.replace(name, name_map[name])
    return text


def redact_text(s: str, name_map: dict[str, str]) -> str:
    if not s:
        return s
    s = apply_name_map(str(s), name_map)
    s = WXID_RE.sub("[WXID]", s)
    s = PHONE_RE.sub("[PHONE]", s)
    s = EMAIL_RE.sub("[EMAIL]", s)
    s = URL_RE.sub("[URL]", s)
    s = ID_CARD_RE.sub("[ID]", s)
    return s


def redact_sender(
    sender: str | None,
    name_map: dict[str, str],
    role_defaults: dict[str, str],
    peer_aliases: set[str],
) -> str:
    if not sender:
        return sender or ""
    if sender == "me":
        return role_defaults["me"]

    if sender in name_map:
        return name_map[sender]

    if sender in peer_aliases:
        return role_defaults["peer"]

    return role_defaults["other"]


def collect_peer_aliases(data: dict, name_map: dict[str, str]) -> set[str]:
    """从顶层字段推断「主对话对象」可能出现的称呼。"""
    aliases: set[str] = set()
    for key in ("chat", "contact_remark", "contact_nick_name"):
        val = data.get(key)
        if isinstance(val, str) and val.strip():
            aliases.add(val.strip())
    for alias, token in name_map.items():
        if token == "USER_PEER" or token.endswith("_PEER"):
            aliases.add(alias)
    return aliases


def redact_top_level(data: dict, role_defaults: dict[str, str]) -> None:
    data["username"] = role_defaults["peer"]
    data["chat"] = role_defaults["peer"]
    for key in ("contact_remark", "contact_nick_name", "contact_memo"):
        if key in data:
            data[key] = "[REDACTED]"


def main(inp: Path, outp: Path, map_path: Path | None) -> None:
    if inp.resolve() == outp.resolve():
        raise SystemExit(
            "输入与输出路径相同，会覆盖原始文件。请指定不同输出，例如 ./chat_redacted.json"
        )
    resolved_map = resolve_map_path(map_path, inp)
    name_map, role_defaults = load_name_map(resolved_map)

    data = json.loads(inp.read_text(encoding="utf-8"))
    peer_raw = data.get("username", "unknown")
    peer_aliases = collect_peer_aliases(data, name_map)

    redact_top_level(data, role_defaults)

    for msg in data.get("messages", []):
        msg["sender"] = redact_sender(
            msg.get("sender"),
            name_map,
            role_defaults,
            peer_aliases,
        )
        if msg.get("content"):
            msg["content"] = redact_text(str(msg["content"]), name_map)
        if msg.get("transcription"):
            msg["transcription"] = redact_text(str(msg["transcription"]), name_map)

    meta = {
        "source_peer_hash": str(hash(peer_raw))[-8:],
        "message_count": len(data.get("messages", [])),
        "name_map_file": str(resolved_map) if resolved_map else None,
        "name_map_entries": len(name_map),
        "role_defaults": role_defaults,
    }
    data["_redaction_meta"] = meta

    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {outp} ({meta['message_count']} messages)")
    if resolved_map:
        print(f"  name_map: {resolved_map} ({len(name_map)} 条称呼映射)")
    else:
        print("  name_map: 未找到（可用 --map 指定；示例见 work/name_map.example.json）")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="脱敏聊天 JSON（支持 name_map.json）")
    parser.add_argument("input", type=Path, help="输入 JSON")
    parser.add_argument("output", type=Path, help="输出 JSON")
    parser.add_argument(
        "--map",
        type=Path,
        default=None,
        help="name_map.json 路径（默认同目录或 work/name_map.json）",
    )
    args = parser.parse_args()
    main(args.input, args.output, args.map)
