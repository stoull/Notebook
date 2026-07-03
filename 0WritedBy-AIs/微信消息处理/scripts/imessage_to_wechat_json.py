#!/usr/bin/env python3
"""
将 imessage-extractor 的 export-all JSON 中单个会话转为 export_chat 兼容格式。

用法:
  python imessage_to_wechat_json.py <all_conversations.json> <filter> <output.json>

<filter>: 匹配 participants、chat_identifier、display_name 的子串（如 +86138、user@icloud.com）
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def parse_timestamp(ts: Any) -> int:
    """转为 Unix 秒。"""
    if ts is None:
        return 0
    if isinstance(ts, (int, float)):
        # 已是 Unix 秒或毫秒
        if ts > 1e12:
            return int(ts / 1000)
        if ts > 1e10:
            return int(ts)
        # Apple Cocoa 纳秒（2001-01-01）
        if ts > 1e15:
            return int(ts / 1_000_000_000) + 978307200
        return int(ts)
    if isinstance(ts, str):
        s = ts.replace("Z", "+00:00")
        try:
            dt = datetime.fromisoformat(s)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return int(dt.timestamp())
        except ValueError:
            return 0
    return 0


def normalize_conversations(data: Any) -> list[dict]:
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        if "conversations" in data:
            return data["conversations"]
        if "chats" in data:
            return data["chats"]
        # 单会话
        if "messages" in data:
            return [data]
    raise ValueError("无法识别的 JSON 结构，需要 conversations 列表或含 messages 的对象")


def match_conversation(conv: dict, needle: str) -> bool:
    needle = needle.lower()
    for key in ("display_name", "chat_identifier", "chat_guid"):
        v = conv.get(key)
        if v and needle in str(v).lower():
            return True
    for p in conv.get("participants") or []:
        if needle in str(p).lower():
            return True
    return False


def pick_peer_name(conv: dict, filter_str: str) -> str:
    for p in conv.get("participants") or []:
        if filter_str.lower() not in str(p).lower():
            return str(p)
    return conv.get("display_name") or conv.get("chat_identifier") or "PEER"


def convert_message(msg: dict, peer_label: str) -> dict:
    from_me = msg.get("from_me") in (True, 1, "1")
    text = msg.get("text") or msg.get("body") or ""
    item_type = msg.get("item_type") or msg.get("type") or 0

    out: dict[str, Any] = {
        "local_id": msg.get("id") or msg.get("ROWID") or 0,
        "timestamp": parse_timestamp(msg.get("timestamp") or msg.get("date")),
        "sender": "me" if from_me else peer_label,
        "source": "imessage",
        "service": msg.get("service") or "iMessage",
    }

    if text:
        out["content"] = text.strip()
    else:
        out["type"] = "imessage_other"
        out["content"] = f"[iMessage item_type={item_type}]"

    if msg.get("attachments"):
        out["attachments"] = [
            {k: a.get(k) for k in ("name", "mime_type", "path") if a.get(k)}
            for a in msg["attachments"]
        ]

    return out


def main(inp: Path, filter_str: str, outp: Path) -> None:
    data = json.loads(inp.read_text(encoding="utf-8"))
    conversations = normalize_conversations(data)
    matched = [c for c in conversations if match_conversation(c, filter_str)]
    if not matched:
        print(f"未找到匹配 '{filter_str}' 的会话。可用字段: display_name, participants, chat_identifier")
        sys.exit(1)
    if len(matched) > 1:
        print(f"警告: 匹配到 {len(matched)} 个会话，将合并消息（按时间排序）")
    peer_label = pick_peer_name(matched[0], filter_str)
    all_msgs: list[dict] = []
    for conv in matched:
        for msg in conv.get("messages") or []:
            all_msgs.append(convert_message(msg, peer_label))

    all_msgs.sort(key=lambda m: m.get("timestamp") or 0)

    identifier = matched[0].get("chat_identifier") or matched[0].get("chat_guid") or filter_str
    out = {
        "chat": matched[0].get("display_name") or peer_label,
        "username": f"imessage:{identifier}",
        "platform": "imessage",
        "exported_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "message_count": len(all_msgs),
        "messages": all_msgs,
    }
    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {outp} ({len(all_msgs)} messages)")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(1)
    main(Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3]))
