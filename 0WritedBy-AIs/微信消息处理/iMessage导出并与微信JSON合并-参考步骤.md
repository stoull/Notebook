# iMessage 导出 JSON 并与 wechat-decrypt 合并（参考步骤）

> 环境：Mac mini M2。微信侧已用 [wechat-decrypt](https://github.com/ylytdeng/wechat-decrypt) 的 `export_chat.py` 得到 JSON。  
> 目标：把 **iMessage** 记录也变成 **同一套消息结构**，按时间合并，供后续脱敏 / 分块摘要使用。

---

## 一、先弄清：iPhone 上的 iMessage 数据在哪

| 情况 | 数据位置 | 推荐做法 |
|------|----------|----------|
| **Mac 已登录同一 Apple ID，并开启「信息」iCloud 同步** | Mac 上 `~/Library/Messages/chat.db` | 在 Mac 上直接导出（最简单） |
| **只有 iPhone，Mac 上没有同步** | iPhone 本地；Mac 上看不到完整库 | 用 **Finder 加密备份** + 读备份里的 `sms.db`，或先在 Mac 登录 iCloud 信息并等待同步 |
| **仅 SMS/部分会话** | 仍在 `chat.db`，`service` 字段为 SMS | 导出工具一般可同时导出，合并时可用 `source` 区分 |

**结论：** 在 Mac 上能打开「信息」App 且能看到与 iPhone 相同的对话，优先用 **`chat.db` 导出**；否则先做 iCloud 同步或 iPhone 备份。

---

## 二、Mac 导出 iMessage → JSON

### 2.1 系统权限

1. **系统设置 → 隐私与安全性 → 完全磁盘访问权限**  
2. 勾选 **终端**（或 iTerm、Cursor 内置终端）  
3. 否则无法复制 `~/Library/Messages/chat.db`

### 2.2 复制数据库（勿直接查正在使用的库）

```bash
mkdir -p ~/imessage_export/db
cp ~/Library/Messages/chat.db ~/imessage_export/db/
cp ~/Library/Messages/chat.db-wal ~/imessage_export/db/ 2>/dev/null || true
cp ~/Library/Messages/chat.db-shm ~/imessage_export/db/ 2>/dev/null || true
```

### 2.3 方式 A：`imessage-extractor`（推荐，一次导出全部）

```bash
brew install pipx   # 若未安装
pipx install imessage-extractor

imessage-extractor export-all \
  -d ~/imessage_export/db/chat.db \
  -o ~/imessage_export/all_conversations.json
```

输出为 **所有会话** 的 JSON 数组/对象（含 `chat_guid`、`participants`、`messages[]` 等）。  
单聊会从该文件中 **按手机号/邮箱筛选** 再转换（见第四节脚本）。

项目：<https://github.com/scotm/imessage-extractor>

### 2.4 方式 B：`imessage-exporter`（Python，按联系人分文件）

```bash
git clone https://github.com/VasimPatel/imessage-exporter.git
cd imessage-exporter
mkdir -p messages
cp ~/Library/Messages/chat.db messages/

pip install -r requirements.txt   # 若有 requirements
python imessage_export.py --db-path messages/chat.db --format json --output-dir ~/imessage_export/per_contact
```

### 2.5 方式 C：仅 iPhone 备份（Mac 无同步时）

使用 [ReagentX/imessage-exporter](https://github.com/ReagentX/imessage-exporter) 的 **iOS 备份** 模式（需 Finder 备份 iPhone）：

```bash
# 示例：备份根目录因系统而异，需指向含 sms.db 的备份
imessage-exporter -f txt -a iOS -p /path/to/Backup -o ~/imessage_export/ios
```

再视工具是否支持 JSON；或从备份中的 `sms.db` 用与 `chat.db` 相同结构的 SQL 查询。  
**操作成本高于「Mac 开 iCloud 信息同步」。**

---

## 三、wechat-decrypt 的 JSON 长什么样

`export_chat.py` 单聊文件（与 `docs/chat_export_format.md` 一致）：

```json
{
  "chat": "显示名",
  "username": "wxid_xxx",
  "exported_at": "2026-05-25 12:00:00",
  "messages": [
    {
      "local_id": 1,
      "timestamp": 1713000000,
      "sender": "me",
      "content": "你好"
    },
    {
      "local_id": 2,
      "timestamp": 1713000060,
      "sender": "对方备注",
      "type": "voice",
      "transcription": "明天见"
    }
  ]
}
```

- `timestamp`：**Unix 秒**  
- `sender`：`"me"` 或对方显示名  
- `type` / `content`：可选，缺省视为文本  

---

## 四、转换：iMessage → 与微信同结构的 JSON

本仓库提供脚本（需先安装 `imessage-extractor` 或自备兼容 JSON）：

```bash
# 从 export-all 的大 JSON 里抽出与某人（手机号或邮箱）的会话
python3 scripts/imessage_to_wechat_json.py \
  ~/imessage_export/all_conversations.json \
  "+8613800138000" \
  work/raw/imessage_peer.json

# 第二个参数支持子串匹配 participants / chat_identifier
```

输出格式与 `export_chat.py` 对齐，并增加：

- `username`: `imessage:<identifier>`  
- `platform`: `"imessage"`  
- 每条消息带 `"source": "imessage"`、`"service": "iMessage"`（或 SMS）

---

## 五、合并：微信 JSON + iMessage JSON

### 5.1 何时合并、何时分开

| 场景 | 建议 |
|------|------|
| 同一人既用微信又用 iMessage | 合并为 **一条时间线**（需确认是同一个人） |
| 不同人 | 各保留独立 JSON，分析时各跑脱敏/摘要 |
| 仅想「所有对话进同一个分析流水线」 | 用 **目录 + manifest**，不必物理合并成一个文件 |

### 5.2 合并脚本（按时间排序）

```bash
python3 scripts/merge_chat_exports.py \
  work/raw/chat_wechat.json \
  work/raw/imessage_peer.json \
  -o work/raw/chat_merged.json
```

合并后结构示例：

```json
{
  "chat": "对方（微信+ iMessage）",
  "username": "wxid_xxx",
  "platforms": ["wechat", "imessage"],
  "exported_at": "2026-05-25 15:00:00",
  "messages": [
    {
      "local_id": "wx-100",
      "timestamp": 1713000000,
      "sender": "me",
      "content": "微信上说的",
      "source": "wechat"
    },
    {
      "local_id": "im-200",
      "timestamp": 1713003600,
      "sender": "me",
      "content": "iMessage 上说的",
      "source": "imessage",
      "service": "iMessage"
    }
  ]
}
```

- `local_id` 加前缀 `wx-` / `im-`，避免冲突  
- 按 `timestamp` **全局排序**  
- 后续 **脱敏 / 切块 / 摘要** 可直接沿用《微信聊天-本地脱敏与分块摘要-参考步骤.md》，把输入换成 `chat_merged.json`

### 5.3 同一人映射（手动）

微信里是备注名，iMessage 里是 `+86…` 或 Apple ID 邮箱，脚本 **不会自动认定是同一人**。  
合并前请自行确认，必要时在脱敏脚本里把 iMessage 的 `chat` 改成与微信相同的 `[PEER]` 标签。

---

## 六、推荐目录结构

```text
work/
├── raw/
│   ├── chat_wechat.json      # export_chat.py
│   ├── imessage_peer.json    # imessage_to_wechat_json.py
│   └── chat_merged.json      # merge_chat_exports.py（可选）
├── redacted/
│   └── chat_merged_redacted.json
├── chunks/
└── summaries/
```

---

## 七、完整命令速查

```bash
cd /Users/hut/Documents/AI-playground

# --- iMessage ---
mkdir -p ~/imessage_export/db work/raw
cp ~/Library/Messages/chat.db* ~/imessage_export/db/
pipx run imessage-extractor export-all -d ~/imessage_export/db/chat.db -o ~/imessage_export/all.json

# 换成对方手机号或邮箱（与 all.json 里 participants 一致）
python3 scripts/imessage_to_wechat_json.py \
  ~/imessage_export/all.json "+86xxxxxxxxxx" work/raw/imessage_peer.json

# --- 微信（在 wechat-decrypt 目录已导出则复制过来）---
# cp /path/to/wechat-decrypt/exported/某人.json work/raw/chat_wechat.json

# --- 合并 ---
python3 scripts/merge_chat_exports.py \
  work/raw/chat_wechat.json \
  work/raw/imessage_peer.json \
  -o work/raw/chat_merged.json

# --- 后续：脱敏 / 切块（见另一份文档）---
python3 scripts/redact_chat.py work/raw/chat_merged.json work/redacted/chat_merged_redacted.json
python3 scripts/chunk_by_month.py work/redacted/chat_merged_redacted.json work/chunks
```

---

## 八、限制与注意

1. **已删除 / 未同步的消息**：`chat.db` 里有什么就导出什么；iPhone 有而 Mac 没有的，需先同步。  
2. **反应（点赞）、贴纸、定位**：iMessage 的 `item_type` 非纯文本时，转换脚本会标为 `type: "imessage_other"`，正文可能为空。  
3. **附件**：默认只导出文本；图片路径在 iMessage JSON 的 `attachments` 里，合并进微信 JSON 需另写逻辑。  
4. **隐私**：`chat.db` 含全部会话，导出前确认 `all.json` 存放位置，勿上传云端。  
5. **法律与伦理**：仅处理 **本人有权查看** 的通信记录；涉及他人隐私时合并分析需格外谨慎。

---

## 九、相关文档

| 文档 | 说明 |
|------|------|
| `微信聊天-本地脱敏与分块摘要-参考步骤.md` | 合并后的 JSON 如何脱敏与摘要 |
| `微信 4.x 解密后数据库速查说明.md` | 微信库与 export 说明 |

---

*文档版本：2026-05*
