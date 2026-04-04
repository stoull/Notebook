



[Get Claude Code](https://claude.com/product/claude-code)

[Claude Code Docs](https://code.claude.com/docs/en/overview)

Mac上一键安装：`curl -fsSL https://claude.ai/install.sh | bash`


### Claude Code 的配置文件

配置文件路径：

* **Windows：** `C:\Users\你的用户名\.claude\settings.json`
* **macOS/Linux：** `~/.claude/settings.json`


Claude Code 接入自定的语言模型 `~/.claude/settings.json`的配置：

```
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "sk-xxx",
    "ANTHROPIC_BASE_URL": "https://api.anthropic.com",
    "ANTHROPIC_MODEL": "claude-3-sonnet-20240229",
    "ANTHROPIC_MAX_TOKENS": 4096,
    "ANTHROPIC_TEMPERATURE": 0.7
  },
  "theme": "dark",
  "autoApprove": false,
  "readOnly": false
}
```

关键参数说明：

* `ANTHROPIC_AUTH_TOKEN`：必填，你的 API Key
* `ANTHROPIC_BASE_URL`：API 地址（默认即可，第三方代理需修改）
* `ANTHROPIC_MODEL`：模型选择（opus/sonnet/haiku）
* `ANTHROPIC_MAX_TOKENS`：单次响应最大 token（建议 4096）
* `ANTHROPIC_TEMPERATURE`：创意度（0 严谨，1 灵活）
* `autoApprove`：是否自动批准文件修改（false 更安全）
* `readOnly`：只读模式（仅查看，不修改代码）

例如如接入阿里百练的大语言模型 中 `~/.claude/settings.json`的配置：

```
{    
    "env": {
        "ANTHROPIC_AUTH_TOKEN": "sk-865a9...d81",
        "ANTHROPIC_BASE_URL": "https://dashscope.aliyuncs.com/apps/anthropic",
        "ANTHROPIC_MODEL": "qwen3.5-plus"
    }
}
```

付费订阅版本：

```
{    
    "env": {
        "ANTHROPIC_AUTH_TOKEN": "sk-sp-865a9...d81",
        "ANTHROPIC_BASE_URL": "https://coding.dashscope.aliyuncs.com/apps/anthropic",
        "ANTHROPIC_MODEL": "qwen2.5-coder-14b-instruct"
    }
}
```

qwen3.5-plus


你当前使用的兼容模式地址（.../apps/anthropic）是一个“翻译层”，它只接受阿里云预设的几个模型别名（如 qwen3.5-plus）。要使用具体的模型 ID，你需要绕过这个翻译层，直接调用阿里云的原生 API。

```
{    
    "env": {
        "ANTHROPIC_AUTH_TOKEN": "sk-865a9...d81",
        "ANTHROPIC_BASE_URL": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "ANTHROPIC_MODEL": "qwen2.5-coder-14b-instruct"
    }
}
```



或者环境变量将 必要变量传入bash环境变量，在`~/.zshrc`文件中配置到环境变量中

* `export ANTHROPIC_AUTH_TOKEN="sk-865a9...d81"`
* `export ANTHROPIC_BASE_URL="https://dashscope.aliyuncs.com/apps/anthropic"`
* `export ANTHROPIC_MODEL="qwen2.5-coder-14b-instruct"`



### Claude 使用

1. 进入项目目录
2. 使用`claude`指令进入对话框
3. 使用`/status`查看状态，使用的模型等


Claude Code 的命令主要分为**终端 CLI 命令**（启动和配置工具）和**交互式斜杠命令**（在会话中控制 AI）。以下是日常使用频率最高的核心指令整理：

### ⚡ 核心 CLI 命令（终端启动时使用）
| 命令/标志 | 功能说明 |
| :--- | :--- |
| `claude` | 在当前目录启动交互式会话  |
| `claude -p "问题"` | 一次性查询，执行后自动退出（适合脚本） |
| `claude -c` | 继续当前目录最近一次的对话  |
| `claude -r "会话ID"` | 恢复指定的历史会话  |
| `claude --model sonnet` | 指定启动时使用的模型  |
| `claude update` | 将 Claude Code 更新到最新版本  |

### 🛠️ 高频斜杠命令（交互会话中输入 `/` 使用）
| 类别 | 命令 | 功能说明 |
| :--- | :--- | :--- |
| **项目初始化** | `/init` | 自动生成 `CLAUDE.md` 记忆文件，让 AI 记住项目规则  |
| | `/memory` | 直接编辑 `CLAUDE.md` 文件，即时生效  |
| | `/status` | 确认模型、Base URL、API Key 是否配置正确  |
| **会话与上下文** | `/clear` | 清空当前对话历史（硬重置） |
| | `/compact` | 压缩对话上下文（总结摘要），节省 Token 用量  |
| | `/rewind` | 撤销上一次对话或代码更改（救命键） |
| **模型与费用** | `/model` | 切换模型（Sonnet/Opus/Haiku） |
| | `/cost` | 查看当前会话的 Token 消耗和预估费用  |
| | `/context` | 查看当前上下文窗口的占用百分比  |
| **辅助开发** | `/review` / `/simplify` | 对当前代码进行审查或简化分析  |
| | `/todos` | 显示跨会话持久化的任务列表  |
| **诊断与配置** | `/doctor` | 诊断安装和环境问题（网络、Token、Node 版本） |
| | `/config` | 打开配置菜单（主题、权限等） |

### ⌨️ 必备键盘快捷键
| 快捷键 | 功能说明 |
| :--- | :--- |
| `Ctrl + C` | 取消当前 AI 的生成或运行（跑偏时刹车） |
| `Shift + Tab` | 切换权限模式（Normal / Auto-Accept / Plan） |
| `Esc` `Esc`（双击） | 打开回退菜单，撤销文件改动  |
| `Ctrl + R` | 搜索命令历史  |
| `Ctrl + O` | 切换详细输出模式，查看 AI 思考过程  |

### ✨ 扩展与自定义
- **自定义斜杠命令**：将 `.md` 文件放入 `.claude/commands/` 目录，即可创建专属命令（如 `/review-pr`）。
- **引用文件与执行 Shell**：在对话中输入 `@文件名` 引用代码，输入 `! 命令` 执行终端指令 。
- **MCP 集成**：通过 `/mcp` 配置外部工具（如数据库、浏览器）。

### 💡 快速上手建议
1. **新项目先跑 `/init`**，让 AI 建立长期记忆。
2. **遇到长会话或忘记前文**时，使用 `/compact` 压缩上下文。
3. **重大改动前**使用 `Shift+Tab` 切换至 **Plan Mode**（计划模式），审阅后再执行，避免误操作。
4. **改错代码**立刻双击 `Esc` 撤销。

希望这份清单能帮助你更高效地使用 Claude Code！




