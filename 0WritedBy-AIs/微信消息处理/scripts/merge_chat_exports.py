#!/usr/bin/env python3
"""
合并多个 export_chat 兼容 JSON（如微信 + iMessage），按 timestamp 排序。

用法:
  python merge_chat_exports.py <wechat.json> <imessage.json> [more.json ...] -o <merged.json>
  python merge_chat_exports.py a.json b.json -o out.json
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any


def load_messages(path: Path, source: str) -> tuple[dict, list[dict]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    platform = data.get("platform") or source
    prefix = "wx" if platform == "wechat" or "wxid" in str(data.get("username", "")) else "im"
    if "wechat" in path.name.lower():
        prefix = "wx"
    if "imessage" in path.name.lower() or data.get("platform") == "imessage":
        prefix = "im"

    rows: list[dict] = []
    for msg in data.get("messages") or []:
        m = dict(msg)
        lid = m.get("local_id", len(rows))
        m["local_id"] = f"{prefix}-{lid}"
        m.setdefault("source", platform if platform != "unknown" else source)
        rows.append(m)
    return data, rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Merge chat export JSON files by timestamp")
    parser.add_argument("inputs", nargs="+", type=Path, help="Input JSON files (wechat, imessage, ...)")
    parser.add_argument("-o", "--output", type=Path, required=True, help="Merged output path")
    args = parser.parse_args()

    metas: list[dict] = []
    all_msgs: list[dict] = []
    platforms: list[str] = []
    chat_names: list[str] = []
    usernames: list[str] = []

    for i, path in enumerate(args.inputs):
        if not path.exists():
            raise SystemExit(f"文件不存在: {path}")
        meta, msgs = load_messages(path, source=f"file{i}")
        metas.append(meta)
        all_msgs.extend(msgs)
        if meta.get("platform"):
            platforms.append(meta["platform"])
        if meta.get("chat"):
            chat_names.append(meta["chat"])
        if meta.get("username"):
            usernames.append(meta["username"])

    all_msgs.sort(key=lambda m: m.get("timestamp") or 0)

    primary = metas[0]
    merged: dict[str, Any] = {
        "chat": " / ".join(dict.fromkeys(chat_names)) if chat_names else primary.get("chat", "merged"),
        "username": primary.get("username", "merged"),
        "platforms": list(dict.fromkeys(platforms or ["wechat", "imessage"])),
        "merged_from": [str(p) for p in args.inputs],
        "exported_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "message_count": len(all_msgs),
        "messages": all_msgs,
    }
    if len(usernames) == 1:
        merged["username"] = usernames[0]
    elif usernames:
        merged["usernames"] = usernames

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Merged {len(args.inputs)} files → {args.output} ({len(all_msgs)} messages)")


if __name__ == "__main__":
    main()
