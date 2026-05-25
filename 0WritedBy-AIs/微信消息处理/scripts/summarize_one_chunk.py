#!/usr/bin/env python3
"""单块聊天 → Ollama 摘要 → Markdown。"""
import json
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

PROMPT_HEADER = """你正在处理一段已脱敏的两人私聊记录（微信），仅用于个人复盘。
要求：
1. 只根据下文归纳，不要编造未出现的事件、人物、地点。
2. 输出简体中文，使用 Markdown 小标题。
3. 若信息不足，写「本块未体现」。

请输出：
## 时间范围
## 主要话题
## 沟通氛围
## 关键节点
## 代表性表述
## 待追问点

---
对话记录：
"""


def format_messages(chunk: dict, max_lines: int = 800) -> str:
    lines = []
    for m in chunk.get("messages", [])[:max_lines]:
        ts = m.get("timestamp") or 0
        t = datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")
        body = m.get("content") or m.get("transcription")
        if not body:
            body = f"[{m.get('type', 'unknown')}]"
        lines.append(f"{t} {m.get('sender', '')}: {body}")
    return "\n".join(lines)


def ollama_generate(prompt: str, model: str = "qwen2.5:7b-instruct") -> str:
    payload = json.dumps({"model": model, "prompt": prompt, "stream": False}).encode()
    req = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=600) as resp:
        return json.load(resp)["response"]


def main(chunk_path: Path, out_path: Path, model: str) -> None:
    chunk = json.loads(chunk_path.read_text(encoding="utf-8"))
    text = format_messages(chunk)
    prompt = PROMPT_HEADER + text
    print(f"Calling Ollama ({model}), ~{len(prompt)} chars ...")
    result = ollama_generate(prompt, model=model)
    header = f"# {chunk.get('chunk_id')} ({chunk.get('period')})\n\n"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(header + result, encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python summarize_one_chunk.py <chunk.json> <out.md> [ollama_model]")
        sys.exit(1)
    model = sys.argv[3] if len(sys.argv) > 3 else "qwen2.5:7b-instruct"
    main(Path(sys.argv[1]), Path(sys.argv[2]), model)
