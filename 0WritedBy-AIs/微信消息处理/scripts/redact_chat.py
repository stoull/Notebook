#!/usr/bin/env python3
"""对 export_chat 导出的 JSON 做本地脱敏。"""
import json
import re
import sys
from pathlib import Path

PHONE_RE = re.compile(r"1[3-9]\d{9}")
EMAIL_RE = re.compile(r"[\w.-]+@[\w.-]+\.\w+")
URL_RE = re.compile(r"https?://\S+")
ID_CARD_RE = re.compile(r"\d{17}[\dXx]|\d{15}")
WXID_RE = re.compile(r"wxid_[a-zA-Z0-9_-]+", re.I)


def redact_text(s: str) -> str:
    if not s:
        return s
    s = WXID_RE.sub("[WXID]", s)
    s = PHONE_RE.sub("[PHONE]", s)
    s = EMAIL_RE.sub("[EMAIL]", s)
    s = URL_RE.sub("[URL]", s)
    s = ID_CARD_RE.sub("[ID]", s)
    return s


def main(inp: Path, outp: Path) -> None:
    data = json.loads(inp.read_text(encoding="utf-8"))
    peer = data.get("username", "unknown")
    data["username"] = "USER_PEER"
    data["chat"] = "[PEER]"
    for key in ("contact_remark", "contact_nick_name", "contact_memo"):
        if key in data:
            data[key] = "[REDACTED]"

    for msg in data.get("messages", []):
        sender = msg.get("sender")
        if sender == "me":
            msg["sender"] = "USER_ME"
        elif sender and sender not in ("", "USER_ME"):
            msg["sender"] = "PEER"
        if msg.get("content"):
            msg["content"] = redact_text(str(msg["content"]))
        if msg.get("transcription"):
            msg["transcription"] = redact_text(str(msg["transcription"]))

    meta = {
        "source_peer_hash": str(hash(peer))[-8:],
        "message_count": len(data.get("messages", [])),
    }
    data["_redaction_meta"] = meta
    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {outp} ({meta['message_count']} messages)")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python redact_chat.py <input.json> <output.json>")
        sys.exit(1)
    main(Path(sys.argv[1]), Path(sys.argv[2]))
