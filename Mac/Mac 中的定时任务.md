# Mac 中的定时任务



Mac OS launchd

不用想， 定时器不会被执行的，crontab 已经被 Mac OS废弃了，替代品就是 launchd


我来帮你创建一个 macOS LaunchAgents 的 plist 文件，让任务在每小时的 5 分钟倍数执行（0、5、10、15、20... 55分钟）。

```
xml name=com.example.task. plist
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <!-- 任务标识符，应该是唯一的 -->
    <key>Label</key>
    <string>com.example.task</string>
    
    <!-- 要执行的程序路径 -->
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/你的用户名/scripts/your_script.py</string>
        <!-- 或者执行 shell 脚本:  -->
        <!-- <string>/bin/bash</string> -->
        <!-- <string>/Users/你的用户名/scripts/your_script.sh</string> -->
    </array>
    
    <!-- 定时执行设置：每5分钟执行一次 -->
    <key>StartCalendarInterval</key>
    <array>
        <dict>
            <key>Minute</key>
            <integer>0</integer>
        </dict>
        <dict>
            <key>Minute</key>
            <integer>5</integer>
        </dict>
        <dict>
            <key>Minute</key>
            <integer>10</integer>
        </dict>
        <dict>
            <key>Minute</key>
            <integer>15</integer>
        </dict>
        <dict>
            <key>Minute</key>
            <integer>20</integer>
        </dict>
        <dict>
            <key>Minute</key>
            <integer>25</integer>
        </dict>
        <dict>
            <key>Minute</key>
            <integer>30</integer>
        </dict>
        <dict>
            <key>Minute</key>
            <integer>35</integer>
        </dict>
        <dict>
            <key>Minute</key>
            <integer>40</integer>
        </dict>
        <dict>
            <key>Minute</key>
            <integer>45</integer>
        </dict>
        <dict>
            <key>Minute</key>
            <integer>50</integer>
        </dict>
        <dict>
            <key>Minute</key>
            <integer>55</integer>
        </dict>
    </array>
    
    <!-- 标准输出日志文件 -->
    <key>StandardOutPath</key>
    <string>/Users/你的用户名/Library/Logs/task.log</string>
    
    <!-- 标准错误日志文件 -->
    <key>StandardErrorPath</key>
    <string>/Users/你的用户名/Library/Logs/task_error.log</string>
    
    <!-- 即使之前执行失败也继续运行 -->
    <key>KeepAlive</key>
    <false/>
    
    <!-- 在用户登录时运行 -->
    <key>RunAtLoad</key>
    <false/>
</dict>
</plist>
```

## 使用步骤：

1. **修改配置**：
   - 将 `com.example.task` 改为你的任务标识符
   - 修改 `ProgramArguments` 中的脚本路径
   - 修改日志文件路径中的用户名

2. **保存文件**：

   ```
   bash
   # 保存到 LaunchAgents 目录
   ~/Library/LaunchAgents/com.example.task.plist
   ```
2.1  **验证 plist 文件是否有效**

`plutil -lint ~/Library/LaunchAgents/com.example.task.plist`

3. **设置权限**：

   ```
   bash
   chmod 644 ~/Library/LaunchAgents/com.example.task.plist
   ```

4. **加载任务**：

   ```
   bash
   launchctl load ~/Library/LaunchAgents/com.example.task.plist
   ```
  路径必须是绝对路径，不能使用 ~ 或相对路径

5. **查看任务状态**：

   ```
   bash
   launchctl list | grep com.example.task
   ```
   
   例如：`launchctl list | grep 'com.hut'`

## 其他有用的命令：

```

bash
# 卸载任务
launchctl unload ~/Library/LaunchAgents/com.example.task. plist

# 启动任务（立即执行一次）
launchctl start com.example.task

# 停止任务
launchctl stop com.example.task

```

## 注意事项：

- plist 文件必须是有效的 XML 格式
- 脚本路径必须使用绝对路径
- 如果脚本需要特定环境变量，可以添加 `EnvironmentVariables` 键
- 日志目录必须存在且有写入权限

这样配置后，你的任务就会在每小时的 0、5、10、15... 55 分钟时自动执行！