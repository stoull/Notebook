#!/usr/bin/env python3
"""按消息 timestamp 的月份切块。"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path


def resolve_input(path: Path) -> Path:
    path = path.expanduser()
    if path.is_file():
        return path.resolve()
    if not path.is_absolute():
        cwd_candidate = (Path.cwd() / path).resolve()
        if cwd_candidate.is_file():
            return cwd_candidate
    raise FileNotFoundError(
        f"找不到输入文件: {path}\n"
        f"  当前工作目录: {Path.cwd()}\n"
        "  请确认脱敏后的 JSON 路径。常见情况：\n"
        "    - 输出在 scripts/ 下: ./chat_xxx_redacted.json\n"
        "    - 输出在 work/redacted/ 下: work/redacted/chat_redacted.json\n"
        "  可先执行: ls -la work/redacted/ 或 ls -la *.json"
    )


def main(inp: Path, out_dir: Path) -> None:
    inp = resolve_input(inp)
    out_dir = out_dir.expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    data = json.loads(inp.read_text(encoding="utf-8"))
    messages = data.get("messages", [])
    if not messages:
        print(f"警告: {inp} 中 messages 为空", file=sys.stderr)

    by_month: dict[str, list] = defaultdict(list)
    skipped_ts = 0
    for m in messages:
        ts = m.get("timestamp") or 0
        if ts <= 0:
            skipped_ts += 1
            key = "unknown-date"
        else:
            key = datetime.fromtimestamp(ts).strftime("%Y-%m")
        by_month[key].append(m)

    if skipped_ts:
        print(f"警告: {skipped_ts} 条消息无有效 timestamp，归入 unknown-date", file=sys.stderr)

    index = []
    for i, (month, msgs) in enumerate(sorted(by_month.items()), start=1):
        chunk_id = f"chunk_{i:03d}"
        chunk = {
            "chunk_id": chunk_id,
            "period": month,
            "message_count": len(msgs),
            "messages": msgs,
        }
        path = out_dir / f"{chunk_id}.json"
        path.write_text(json.dumps(chunk, ensure_ascii=False, indent=2), encoding="utf-8")
        index.append({
            "chunk_id": chunk_id,
            "period": month,
            "file": path.name,
            "message_count": len(msgs),
        })

    index_path = out_dir.parent / "index.json"
    index_path.write_text(
        json.dumps(
            {
                "source": str(inp),
                "chunks": index,
                "total_messages": len(messages),
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"输入: {inp}")
    print(f"Created {len(index)} chunks under {out_dir}")
    print(f"索引: {index_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="按月份切分脱敏后的聊天 JSON")
    parser.add_argument("input", type=Path, help="脱敏后的 JSON（如 work/redacted/chat_redacted.json）")
    parser.add_argument("chunks_dir", type=Path, help="切块输出目录（如 work/chunks）")
    args = parser.parse_args()
    try:
        main(args.input, args.chunks_dir)
    except FileNotFoundError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
