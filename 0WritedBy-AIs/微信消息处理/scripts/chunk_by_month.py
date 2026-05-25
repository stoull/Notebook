#!/usr/bin/env python3
"""按消息 timestamp 的月份切块。"""
import json
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path


def main(inp: Path, out_dir: Path) -> None:
    data = json.loads(inp.read_text(encoding="utf-8"))
    messages = data.get("messages", [])
    by_month: dict[str, list] = defaultdict(list)
    for m in messages:
        ts = m.get("timestamp") or 0
        key = datetime.fromtimestamp(ts).strftime("%Y-%m")
        by_month[key].append(m)

    out_dir.mkdir(parents=True, exist_ok=True)
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
        json.dumps({"chunks": index, "total_messages": len(messages)}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Created {len(index)} chunks under {out_dir}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python chunk_by_month.py <redacted.json> <chunks_dir>")
        sys.exit(1)
    main(Path(sys.argv[1]), Path(sys.argv[2]))
