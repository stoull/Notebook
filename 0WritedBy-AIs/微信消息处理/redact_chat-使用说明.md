# redact_chat.py 使用说明

对 **wechat-decrypt** 的 `export_chat.py`、或 **merge_chat_exports.py** 合并后的聊天 JSON 做本地脱敏，支持通过 **`name_map.json`** 统一替换对话中的人名与发送者代号。

---

## 一、适用场景

| 场景 | 输入文件示例 |
|------|----------------|
| 微信单聊导出 | `work/raw/chat_wechat.json` |
| 语音转录后 | `work/raw/chat_transcribed.json` |
| 微信 + iMessage 合并后 | `work/raw/chat_merged.json` |

**输出**：结构与输入相同，字段已替换为代号，可继续用于 `chunk_by_month.py`、本地摘要或（仅摘要）上传云端。

---

## 二、环境要求

- Python **3.10+**
- 无需额外 pip 包（仅标准库）

工作目录建议为项目根目录：

```text
/Users/hut/Documents/AI-playground/
```

---

## 三、快速开始

### 3.1 准备人名映射（首次）

```bash
cd /Users/hut/Documents/AI-playground

cp work/name_map.example.json work/name_map.json
```

编辑 `work/name_map.json`：把对话里会出现的**备注名、昵称、常叫法**写成键，值用**稳定代号**（同一人始终同一个值）。

### 3.2 执行脱敏

```bash
python3 scripts/redact_chat.py \
  work/raw/chat_transcribed.json \
  work/redacted/chat_redacted.json \
  --map work/name_map.json
```

### 3.3 成功输出示例

```text
Wrote work/redacted/chat_redacted.json (15234 messages)
  name_map: work/name_map.json (8 条称呼映射)
```

---

## 四、命令行参数

```bash
python3 scripts/redact_chat.py <输入.json> <输出.json> [--map <name_map.json>]
```

| 参数 | 必填 | 说明 |
|------|------|------|
| `input` | 是 | 原始聊天 JSON 路径 |
| `output` | 是 | 脱敏后输出路径（目录不存在会自动创建） |
| `--map` | 否 | `name_map.json` 路径；省略则自动查找（见第五节） |

查看帮助：

```bash
python3 scripts/redact_chat.py --help
```

---

## 五、name_map.json 自动查找顺序

未指定 `--map` 时，按顺序查找**第一个存在的文件**：

1. `<输入文件同目录>/name_map.json`  
   例：输入 `work/raw/chat.json` → `work/raw/name_map.json`
2. `<输入文件上级目录>/name_map.json`  
   例：`work/name_map.json`
3. `<项目根>/work/name_map.json`

都找不到时：**仍会脱敏**（手机号、wxid、URL 等），但正文中的自定义人名映射不会生效；终端会提示使用 `--map` 或参考 `work/name_map.example.json`。

---

## 六、name_map.json 格式说明

### 6.1 示例文件

路径：`work/name_map.example.json`（复制为 `work/name_map.json` 后修改）

```json
{
  "_comment": "以下划线开头的键仅作说明，不会参与替换",
  "$me": "USER_ME",
  "$peer": "USER_PEER",
  "$other": "OTHER_PERSON",
  "张三": "USER_PEER",
  "三哥": "USER_PEER",
  "李四": "PERSON_001",
  "王五": "PERSON_002"
}
```

### 6.2 特殊键（以 `$` 开头）

| 键 | 作用 |
|----|------|
| `$me` | `sender` 为 `"me"` 时替换成的代号（默认 `USER_ME`） |
| `$peer` | 主对话对象的代号（默认 `USER_PEER`） |
| `$other` | 未匹配到 map、且不属于 peer 的发送者（默认 `OTHER_PERSON`，如群成员） |

### 6.3 普通人名键

- **键**：对话正文、`sender` 字段、或你在 map 里列出的任何称呼字符串。  
- **值**：脱敏后的代号，如 `USER_PEER`、`PERSON_001`、`FAMILY_MOTHER`。  
- **规则**：同一真实身份在全文件中应使用**同一个值**。  
- **替换顺序**：按名称**长度从长到短**替换，减少短名误伤（如先「张三丰」再「张三」）。

### 6.4 忽略的键

- 以 **`_`** 开头的键（如 `_comment`、`_usage`）：仅作文档说明。  
- 非字符串的值：跳过。

### 6.5 微信 + iMessage 合并时

同一个人在两边称呼不同，应都指向同一代号，例如：

```json
{
  "张三": "USER_PEER",
  "三哥": "USER_PEER",
  "+8613800138000": "USER_PEER"
}
```

---

## 七、脚本会做哪些脱敏

### 7.1 顶层字段

| 字段 | 处理后 |
|------|--------|
| `username` | 设为 `$peer` 对应代号（默认 `USER_PEER`） |
| `chat` | 同上 |
| `contact_remark` / `contact_nick_name` / `contact_memo` | `[REDACTED]` |

### 7.2 每条消息 `messages[]`

| 字段 | 处理 |
|------|------|
| `sender` | `me` → `$me`；在 name_map 中 → 对应代号；属于主聊对象别名 → `$peer`；否则 → `$other` |
| `content` | 先按 name_map 替换人名，再替换手机号、邮箱、URL、身份证、wxid |
| `transcription` | 与 `content` 相同（语音转录文本） |

### 7.3 正则替换（正文与转录）

| 模式 | 替换为 |
|------|--------|
| 大陆 11 位手机号 | `[PHONE]` |
| 邮箱 | `[EMAIL]` |
| `http(s)://...` | `[URL]` |
| 15/18 位身份证 | `[ID]` |
| `wxid_...` | `[WXID]` |

### 7.4 元数据 `_redaction_meta`

输出 JSON 末尾会写入（便于追溯）：

```json
"_redaction_meta": {
  "source_peer_hash": "12345678",
  "message_count": 15234,
  "name_map_file": "/path/to/work/name_map.json",
  "name_map_entries": 8,
  "role_defaults": {
    "me": "USER_ME",
    "peer": "USER_PEER",
    "other": "OTHER_PERSON"
  }
}
```

---

## 八、发送者（sender）判定逻辑

```text
sender == "me"  ──────────────────────────►  $me（默认 USER_ME）
sender 在 name_map 的键中  ────────────────►  name_map 中的值
sender 等于顶层 chat / contact_remark 等  ─►  $peer
sender 在 name_map 里映射为 USER_PEER 的键 ►  也视为 peer 别名（用于 sender 匹配）
其它  ─────────────────────────────────────►  $other
```

**说明**：顶层 `chat` 在输出里会被改成 `USER_PEER`，但处理消息时仍会先用**原始** `chat`、备注名收集 peer 别名，因此对方用备注名当 `sender` 时仍能识别为主对话对象。

---

## 九、完整流程示例

### 9.1 仅微信

```bash
cd /Users/hut/Documents/AI-playground

# 假设已在 wechat-decrypt 目录执行过 export_chat.py，并复制到 work/raw/
python3 scripts/redact_chat.py \
  work/raw/chat_wechat.json \
  work/redacted/chat_wechat_redacted.json \
  --map work/name_map.json

python3 scripts/chunk_by_month.py \
  work/redacted/chat_wechat_redacted.json \
  work/chunks
```

### 9.2 微信 + iMessage 合并后再脱敏

```bash
python3 scripts/merge_chat_exports.py \
  work/raw/chat_wechat.json \
  work/raw/imessage_peer.json \
  -o work/raw/chat_merged.json

python3 scripts/redact_chat.py \
  work/raw/chat_merged.json \
  work/redacted/chat_merged_redacted.json \
  --map work/name_map.json
```

### 9.3 不使用 name_map（仅默认代号 + 正则）

```bash
python3 scripts/redact_chat.py \
  work/raw/chat.json \
  work/redacted/chat_redacted.json
```

---

## 十、脱敏后检查清单

在 `work/redacted/` 下打开输出 JSON，建议搜索：

- [ ] 真实姓名、备注名是否还残留  
- [ ] `wxid_`、11 位手机号  
- [ ] `@chatroom`（若误导出群聊）  
- [ ] `sender` 是否已为 `USER_ME` / `USER_PEER` / `PERSON_xxx` 等代号  

可用命令辅助（将 `chat_redacted.json` 换成你的文件）：

```bash
rg -i 'wxid_|1[3-9][0-9]{9}' work/redacted/chat_redacted.json | head
```

---

## 十一、常见问题

### Q1：`JSONDecodeError: Illegal trailing comma`

**原因**：`name_map.json` 里某一行**最后一个字段后面多了逗号**（标准 JSON 不允许）。报错里的行号（如 line 22）即问题位置。

**错误示例：**

```json
{
  "张三": "USER_PEER",
}
```

**正确写法：**

```json
{
  "张三": "USER_PEER"
}
```

新版 `redact_chat.py` 会尝试自动去掉 `,}` / `,]` 形式的尾随逗号；若仍失败，请用编辑器打开 `name_map.json` 按行号修改。

### Q2：提示「未找到 name_map」

**原因**：未传 `--map`，且自动查找路径下没有 `name_map.json`。  
**处理**：`cp work/name_map.example.json work/name_map.json` 并编辑，或显式 `--map work/name_map.json`。

### Q3：输入与输出路径相同

**现象**：`redact_chat.py a.json a.json`  
**处理**：输出请用新文件名，例如 `chat_redacted.json`，避免覆盖未脱敏的原件。

### Q4：正文里还有人名没换掉

**原因**：该称呼未写在 `name_map.json` 里。  
**处理**：把出现的写法（全称、昵称、错别字）都加进 map，指向同一代号。

### Q5：群聊里所有人都变成 USER_PEER

**原因**：未配置 `$other`，或误把群成员昵称都映射成了 `USER_PEER`。  
**处理**：群成员单独映射为 `PERSON_001`…，或依赖默认 `$other` → `OTHER_PERSON`。

### Q6：输入 JSON 格式不对

**要求**：与 `export_chat.py` 一致，至少包含：

```json
{
  "chat": "...",
  "username": "...",
  "messages": [
    { "local_id": 1, "timestamp": 1713000000, "sender": "me", "content": "..." }
  ]
}
```

### Q7：name_map.json 能否提交 Git？

**不要**。其中是真名。建议将 `work/name_map.json` 加入 `.gitignore`，仅提交 `name_map.example.json`。

---

## 十二、相关文件与文档

| 路径 | 说明 |
|------|------|
| `scripts/redact_chat.py` | 本工具 |
| `work/name_map.example.json` | 映射表模板 |
| `work/name_map.json` | 你的真实映射（本地自建，勿外传） |
| `scripts/chunk_by_month.py` | 脱敏后按月切块 |
| `scripts/merge_chat_exports.py` | 合并微信与 iMessage JSON |
| `微信聊天-本地脱敏与分块摘要-参考步骤.md` | 脱敏 → 摘要完整流水线 |
| `iMessage导出并与微信JSON合并-参考步骤.md` | iMessage 导出与合并 |

---

## 十三、安全提示

- 脱敏可降低风险，**不能**保证绝对匿名；罕见组合（公司名+地名+事件）仍可能被推断。  
- `work/raw/` 与 `name_map.json` 含敏感信息，勿上传网盘、勿提交公开仓库。  
- 仅处理**本人有权分析**的聊天记录。

---

*文档版本：2026-05，对应 `scripts/redact_chat.py` 当前实现。*
