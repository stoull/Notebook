
## wechat-decrypt 解密微信数据库密码

[项目地址：https://github.com/ylytdeng/wechat-decrypt](https://github.com/ylytdeng/wechat-decrypt)


### 操作步骤

#### 0. 环境
* `xcode-select --install`          # 若未装 Command Line Tools
* `python3 -m venv .venv && source .venv/bin/activate`

	确保使用的是的python10的版本: `/opt/homebrew/bin/python3.13 -m venv .venv`

* `pip install -r requirements.txt`

#### 1. 重签（微信退出时做）
* `killall WeChat`
* `sudo codesign --force --deep --sign - /Applications/WeChat.app`

#### 2. 启动微信并登录，保持运行

#### 3. 编译 + root 扫密钥
* `cc -O2 -o find_all_keys_macos find_all_keys_macos.c -framework Foundation`
* `sudo ./find_all_keys_macos`	 # 扫描内存提取密钥

#### 4. 后续解密/导出（一般不用 sudo）
* `python3 decrypt_db.py`	# 解密所有数据库
* `python3 export_all_chats.py -t`     # 导出全部聊天并转录语音



