# Z shell-zsh配置文件的加载

Starting with macOS Catalina, your Mac uses zsh as the default login shell and interactive shell. 

* `zsh` (Z shell) is the default shell for all newly created user accounts, starting with macOS Catalina.
* `bash` is the default shell in macOS Mojave and earlier.

自2019年起，macOS的默认Shell已从Bash改为Zsh。

[Z shell - WiKi](https://zh.wikipedia.org/zh-cn/Z_shell)

[Use zsh as the default shell on your Mac](https://support.apple.com/en-us/102360)

[What should/shouldn't go in .zshenv, .zshrc, .zlogin, .zprofile, .zlogout?](https://unix.stackexchange.com/questions/71253/what-should-shouldnt-go-in-zshenv-zshrc-zlogin-zprofile-zlogout)


Here is a non-exhaustive list, in execution-order, of what each file tends to contain:

* `.zshenv` is always sourced. It often contains exported variables that should be available to other programs. For example, $PATH, $EDITOR, and $PAGER are often set in .zshenv. Also, you can set $ZDOTDIR in .zshenv to specify an alternative location for the rest of your zsh configuration.
* `.zprofile` is for login shells. It is basically the same as .zlogin except that it's sourced before .zshrc whereas .zlogin is sourced after .zshrc. According to the zsh documentation, ".zprofile is meant as an alternative to .zlogin for ksh fans; the two are not intended to be used together, although this could certainly be done if desired."
* `.zshrc` is for interactive shells. You set options for the interactive shell there with the setopt and unsetopt commands. You can also load shell modules, set your history options, change your prompt, set up zle and completion, et cetera. You also set any variables that are only used in the interactive shell (e.g. $LS_COLORS).
* `.zlogin` is for login shells. It is sourced on the start of a login shell but after .zshrc, if the shell is also interactive. This file is often used to start X using startx. Some systems start X on boot, so this file is not always very useful.
* `.zlogout` is sometimes used to clear and reset the terminal. It is called when exiting, not when opening.



# zsh配置文件的加载顺序是？

Zsh 的配置文件加载机制比 Bash 更复杂但也更灵活。以下是详细说明：

## Zsh 配置文件列表

Zsh 有 **5 个主要配置文件**：

1. **~/.zshenv** - 环境变量
2. **~/.zprofile** - 登录时的配置
3. **~/.zshrc** - 交互式 shell 配置
4. **~/.zlogin** - 登录后的配置
5. **~/.zlogout** - 登出时的配置

## 加载顺序（完整版）

### **Login Shell（登录式）**
```
1. /etc/zshenv
2. ~/.zshenv
3. /etc/zprofile
4. ~/.zprofile
5. /etc/zshrc
6. ~/.zshrc
7. /etc/zlogin
8. ~/.zlogin
   
   [使用 shell...]
   
9. ~/.zlogout
10. /etc/zlogout
```

### **Interactive Non-login Shell（交互式非登录）**
```
1. /etc/zshenv
2. ~/.zshenv
3. /etc/zshrc
4. ~/.zshrc
```

### **Non-interactive Shell（非交互式，如脚本）**
```
1. /etc/zshenv
2. ~/.zshenv
```

## 各文件的用途和特点

### **1. ~/.zshenv**
```bash
# ~/. zshenv
# ✓ 总是被加载（login、non-login、脚本都会读取）
# ✓ 适合：基础环境变量
# ✗ 避免：输出内容、耗时操作

export EDITOR=vim
export LANG=en_US.UTF-8
export PATH="$HOME/bin:$PATH"
```

**特点**：
- 每次启动 zsh 都会读取（包括脚本）
- 应该保持简洁，避免副作用
- ⚠️ 不要在这里设置 PATH 的复杂逻辑

### **2. ~/.zprofile**
```bash
# ~/.zprofile
# ✓ Login shell 时加载
# ✓ 适合：登录时需要运行一次的命令
# ≈ 等同于 Bash 的 ~/. bash_profile

# 启动 SSH agent
if [ -z "$SSH_AUTH_SOCK" ]; then
    eval "$(ssh-agent -s)"
fi

# 设置复杂的 PATH
export PATH="$HOME/. local/bin:$HOME/. cargo/bin:$PATH"

# 加载敏感信息
[ -f ~/. secrets ] && source ~/.secrets
```

### **3. ~/.zshrc**
```bash
# ~/.zshrc
# ✓ 交互式 shell 时加载
# ✓ 适合：别名、函数、提示符、插件
# ≈ 等同于 Bash 的 ~/.bashrc

# 这是最常用的配置文件！

# Oh My Zsh
export ZSH="$HOME/.oh-my-zsh"
ZSH_THEME="robbyrussell"
plugins=(git docker kubectl)
source $ZSH/oh-my-zsh.sh

# 别名
alias ll='ls -lah'
alias gs='git status'

# 自动补全
autoload -Uz compinit
compinit

# 历史记录
HISTSIZE=10000
SAVEHIST=10000
HISTFILE=~/.zsh_history

# 提示符
PS1='%n@%m:%~%# '
```

### **4. ~/.zlogin**
```bash
# ~/.zlogin
# ✓ Login shell 时加载（在 . zshrc 之后）
# ✓ 适合：欢迎信息、检查邮件等

# 显示系统信息
echo "Welcome back, $USER!"
uptime

# 检查更新
[ -x /usr/bin/checkupdates ] && checkupdates | wc -l
```

**注意**：`~/.zprofile` 和 `~/.zlogin` 功能类似，通常只选一个使用

### **5. ~/.zlogout**
```bash
# ~/.zlogout
# ✓ Login shell 退出时执行
# ✓ 适合：清理工作

# 清理临时文件
rm -f /tmp/my-temp-files-*

# 停止 SSH agent
[ -n "$SSH_AGENT_PID" ] && kill $SSH_AGENT_PID
```

## 对比 Bash vs Zsh

| 用途 | Bash | Zsh |
|------|------|-----|
| **所有 shell** | - | `~/.zshenv` |
| **Login shell 环境** | `~/.bash_profile` | `~/.zprofile` |
| **交互式 shell** | `~/.bashrc` | `~/.zshrc` |
| **Login 后执行** | - | `~/.zlogin` |
| **退出时执行** | `~/.bash_logout` | `~/.zlogout` |

## 实际使用建议

### **最小化配置（推荐新手）**

只使用 `~/.zshrc`：
```bash
# ~/.zshrc
# 所有配置都放这里

# 环境变量
export EDITOR=vim
export PATH="$HOME/bin:$PATH"

# 敏感信息
[ -f ~/.secrets ] && source ~/.secrets

# 别名和函数
alias ll='ls -lah'

# Oh My Zsh（如果使用）
source ~/. oh-my-zsh/oh-my-zsh.sh
```

### **标准配置（推荐）**

```bash
# ~/.zshenv
# 最基础的环境变量
export EDITOR=vim
export LANG=en_US.UTF-8

# ~/. zprofile
# PATH 设置
export PATH="$HOME/. local/bin:$HOME/bin:$PATH"

# 加载敏感信息
if [ -f ~/.secrets ]; then
    chmod 600 ~/.secrets  # 确保权限
    source ~/.secrets
fi

# ~/. zshrc
# 所有交互式配置
# Oh My Zsh
export ZSH="$HOME/.oh-my-zsh"
source $ZSH/oh-my-zsh.sh

# 别名
alias ll='ls -lah'

# 历史记录
HISTSIZE=10000
SAVEHIST=10000
HISTFILE=~/.zsh_history
```

### **密码配置放哪里？**

```bash
# 方案 1：放在 ~/.zshenv（所有 shell 都能用）
# ~/. zshenv
source ~/.secrets 2>/dev/null

# 方案 2：放在 ~/.zprofile（只在登录时加载一次，更安全）
# ~/.zprofile
if [ -f ~/.secrets ]; then
    source ~/.secrets
fi

# 方案 3：放在 ~/.zshrc（最常用）
# ~/.zshrc
[ -f ~/.secrets ] && source ~/. secrets
```

**推荐**：对于密码等敏感信息，放在 `~/.zprofile` 或 `~/.zshrc` 中，并从独立的 `~/.secrets` 文件加载。

## 调试配置加载

```bash
# 查看当前 shell 类型
echo $ZSH_VERSION  # 确认是 zsh

# 检查是否为 login shell
[[ -o login ]] && echo "login shell" || echo "non-login shell"

# 检查是否为交互式 shell
[[ -o interactive ]] && echo "interactive" || echo "non-interactive"

# 追踪配置文件加载
zsh -xl  # 启动 zsh 并显示所有执行的命令
```

## 常见问题

### **为什么我的 PATH 设置不生效？**
- 检查是否在多个文件中重复设置
- 确保 `~/.zprofile` 在 `~/.zshrc` 之前加载
- macOS Terminal 默认启动 login shell，读取 `~/.zprofile`

### **Oh My Zsh 应该放哪里？**
```bash
# ~/.zshrc（推荐）
export ZSH="$HOME/.oh-my-zsh"
ZSH_THEME="robbyrussell"
plugins=(git docker)
source $ZSH/oh-my-zsh.sh
```

### **如何让配置立即生效？**
```bash
source ~/.zshrc     # 重新加载 zshrc
exec zsh            # 重启 zsh（更彻底）
```

总结：对于大多数用户，**把主要配置放在 `~/.zshrc`** 就足够了，这是最常用和最直观的方式。