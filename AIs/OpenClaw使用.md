# OpenClaw 使用指南

> 一个开源的 AI 助手网关，可以接入各种渠道（iMessage、Telegram、Discord、Signal 等）和各类大模型。

官方网站：[openclaw.ai](https://openclaw.ai) · 文档：[docs.openclaw.ai](https://docs.openclaw.ai)

---

## 一、安装

### macOS / Linux

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

### 验证安装

```bash
openclaw --version
```

---

## 二、初始化配置

### 首次设置（推荐）

```bash
openclaw onboard --install-daemon
```

这会交互式引导你完成：
- 选择 AI 模型（OpenAI、Ollama 本地模型、Claude、DeepSeek 等）
- 设置工作区
- 安装守护进程（后台自动运行）

### 中文引导

```bash
OPENCLAW_LOCALE=zh-CN openclaw onboard
```

### 重新配置

```bash
openclaw configure
```

---

## 三、启动与运行

### 检查网关状态

```bash
openclaw gateway status
```

### 终端聊天（TUI，推荐）

```bash
openclaw tui
```

### 简易聊天模式

```bash
openclaw chat
```

### 网页控制面板

```bash
openclaw dashboard
```

浏览器打开 `http://localhost:19525` 即可访问。

---

## 四、工作区（Workspace）

所有配置文件在 `~/.openclaw/workspace/`：

```
workspace/
├── AGENTS.md      # Agent 行为规则（告诉 AI 怎么表现）
├── SOUL.md        # AI 人格设定
├── USER.md        # 用户信息（你的名字、偏好等）
├── TOOLS.md       # 本地工具配置
├── HEARTBEAT.md   # 后台定时任务清单
├── IDENTITY.md    # 身份标识
├── MEMORY.md      # 长期记忆（AI 会读写）
└── memory/        # 每日日记文件夹
    └── YYYY-MM-DD.md
```

> 💡 **重要**：这些文件是 AI 的"大脑"——想让它记住什么，就写进文件里。AI 每次启动都会读这些文件。

---

## 五、连接 AI 模型

### 使用 Ollama（本地模型）

确保 Ollama 已运行：

```bash
curl http://localhost:11434/v1/models
```

然后在 `openclaw onboard` 中选择 Ollama provider。

### 使用云端模型

支持的提供商：
- **OpenAI**（GPT-4o、GPT-4 等）
- **Anthropic Claude**
- **DeepSeek**
- **Google Gemini**
- **Groq**
- 以及兼容 OpenAI API 接口的任何服务

配置时会要求输入 API Key。

### 切换模型

```bash
openclaw configure
```

或在聊天中使用指令 `/model <model-name>` 临时切换。

---

## 六、接入聊天渠道

OpenClaw 的一大特色是可以绑定各种聊天软件，让 AI 在手机上和你聊天。

### Telegram（最快捷）

1. 在 Telegram 中搜索 @BotFather，创建新 Bot 获取 token
2. 配置：

```bash
openclaw configure
```

3. 选择 Channels → Telegram，填入 token

### iMessage（macOS）

安装后自动支持 Mac 上的 iMessage，通过 `openclaw onboard` 配置即可。

### Discord

通过 Bot Token 接入 Discord 服务器。

### 其他渠道

支持 Signal、WhatsApp、Slack 等，详见文档：[docs.openclaw.ai/channels](https://docs.openclaw.ai/channels)

---

## 七、Agent（智能体）

### 查看现有 Agent

```bash
openclaw agents list
```

### 添加新 Agent

```bash
openclaw agents add <name>
```

每个 Agent 可以有不同的：
- 绑定的模型（如一个用 GPT-4，一个用 Claude）
- 工作区和配置文件
- 接入的聊天渠道

---

## 八、常用指令

在聊天中可以使用：

| 指令 | 作用 |
|------|------|
| `/help` | 显示帮助 |
| `/status` | 查看当前会话状态 |
| `/model <name>` | 切换模型 |
| `/reasoning` | 开启/关闭思维链显示 |
| `/reset` | 重置当前会话 |
| `/clear` | 清空聊天记录 |

---

## 九、Skill（技能）

OpenClaw 的技能系统让 AI 能做特定任务：

- **天气查询**：获取天气预报
- **搜索网页**：联网搜索信息
- **管理日历**：查看/添加日程
- **发送邮件**：需授权
- **操作文件**：读写文件、运行脚本

技能文件在 `/opt/homebrew/lib/node_modules/openclaw/skills/` 下。

自定义技能参考：[docs.openclaw.ai/skills](https://docs.openclaw.ai/skills)

---

## 十、记忆与持久化

AI 默认每次对话都是"全新"的，但 OpenClaw 通过文件系统实现记忆：

- **每日日记**：`memory/YYYY-MM-DD.md` — 记录每天的对话和事件
- **长期记忆**：`MEMORY.md` — AI 会主动读写，记住重要信息
- **定期回顾**：AI 会在后台（Heartbeat）整理记忆，把重要的提炼到 MEMORY.md

想要 AI 记住什么 → 直接告诉它"记住这个"或写进工作区文件。

---

## 十一、Cron 定时任务

可以用 cron 设置提醒、定时任务：

```bash
# 在终端配置
openclaw cron
```

示例：每天早上 8 点推送天气简报，或 30 分钟后提醒你做事。

---

## 十二、更新

```bash
openclaw update
```

---

## 十三、故障排查

### 网关没启动

```bash
openclaw gateway status
openclaw gateway start
```

### 模型连接失败

检查 API Key 是否正确，或 Ollama 是否在运行：

```bash
curl http://localhost:11434/v1/models
```

### 日志查看

```bash
openclaw logs
```

### 诊断工具

```bash
openclaw doctor
```

---

## 十四、常用命令速查

```bash
openclaw gateway status      # 查看网关状态
openclaw gateway start       # 启动网关
openclaw gateway stop        # 停止网关
openclaw dashboard           # 打开网页控制台
openclaw tui                 # 终端聊天界面
openclaw chat                # 简易聊天
openclaw configure           # 重新配置
openclaw agents list         # 查看所有 Agent
openclaw agents add <name>   # 添加新 Agent
openclaw update              # 更新
openclaw doctor              # 诊断问题
openclaw logs                # 查看日志
```

---

## 附：官方资源

- 安装脚本：`curl -fsSL https://openclaw.ai/install.sh | bash`
- 文档首页：[docs.openclaw.ai](https://docs.openclaw.ai)
- 快速开始：[docs.openclaw.ai/start/getting-started](https://docs.openclaw.ai/start/getting-started)
- 配置参考：[docs.openclaw.ai/configuration](https://docs.openclaw.ai/configuration)
- GitHub：[github.com/openclaw/openclaw](https://github.com/openclaw/openclaw)
