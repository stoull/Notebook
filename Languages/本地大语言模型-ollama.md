# Ollama-大语言模型Runner


## 安装

[Ollama官网](https://ollama.com)

Windows和Mac直接下载安装

[Ollama on Linux](https://github.com/ollama/ollama/blob/main/docs/linux.md)

Linux下载及更新：

`curl -fsSL https://ollama.com/install.sh | sh`

## ollama存储目录

* macOS: `~/.ollama/`
* Linux: `/usr/share/ollama/.ollama/`
* Windows: `C:\Users\<username>\.ollama\`

### `ollama` Command

```
ollama --help
Large language model runner

Usage:
  ollama [flags]
  ollama [command]

Available Commands:
  serve       Start ollama
  create      Create a model from a Modelfile
  show        Show information for a model
  run         Run a model
  pull        Pull a model from a registry
  push        Push a model to a registry
  list        List models
  ps          List running models
  cp          Copy a model
  rm          Remove a model
  help        Help about any command

Flags:
  -h, --help      help for ollama
  -v, --version   Show version information
 
```

## 下载及终端运行模型

 在官网查找支持的- [Ollama - Models](https://ollama.com/library), 运行命令`ollama run model-name`进行下载,如下载llama3: 
 
 `ollama run llama3`
 
 ollama会在终端下载并运行`llama3`, 运行后就可以在终端进行对话了。在对话时,可以使用`/`开头调用一些帮助指令：
 
	Available Commands:
	/set            Set session variables
	/show           Show model information
	/load <model>   Load a session or model
	/save <model>   Save your current session
	/clear          Clear session context
	/bye            Exit
	/?, /help       Help for a command
	/? shortcuts    Help for keyboard shortcuts
	Use """ to begin a multi-line message.
	
如果需要使用多行的话，使用`"""`开头，使用`"""`表示多行输入结束。

使用`Ctrl + d` 或者输入 `/bye`退出终端会话。

 其它常用指令：
 
* `ollama -v`		: 查看当前版本
* `ollama run model-name` : 运行模型，如果没有下载会先进行下载动作`ollama pull`
* `ollama pull model-name`	: 下载或更新模型
* `ollama list`	: 查看已下载安装的语言模型
* `ollama show model-name`	: 查看对应模型的信息
* `ollama rm model-name`	: 删除模型

更新所有的模型：

```
#!/bin/bash
ollama list | tail -n +2 | awk '{print $1}' | while read -r model; do
  ollama pull $model
done
```

## allama API 服务

除了使用终端对话，也可以使用api调用服务。

```
$ollama show --help
Show information for a model

Usage:
  ollama show MODEL [flags]

Flags:
  -h, --help         help for show
      --license      Show license of a model
      --modelfile    Show Modelfile of a model
      --parameters   Show parameters of a model
      --system       Show system message of a model
      --template     Show template of a model

Environment Variables:
      OLLAMA_HOST                IP Address for the ollama server (default 127.0.0.1:11434)
```

可以看到`OLLAMA_HOST`默认的为`127.0.0.1:11434`

* 使用流式生成

```
curl http://localhost:11434/api/generate -d '{
  "model": "llama3",
   "prompt":"Tell me something about OLLAMA, the llvm language model runner.",
}'
```

* 使用非流式生成
```
curl http://localhost:11434/api/generate -d '{
  "model": "llama3",
  "prompt":"Tell me something about OLLAMA, the llvm language model runner.",
  "stream": false
}'
```

* 使用对话的形式

```
curl http://localhost:11434/api/chat -d '{
  "model": "llama3",
  "messages": [
    {
      "role": "user",
      "content": "why is the sky blue?"
    }
  ]
}'
```

[OLLAMA_HOST - api](https://github.com/ollama/ollama/blob/main/docs/api.md#generate-a-chat-completion)

## WebUI

因为有api，所以有一些开源的WebUI可以使用，如：[Open WebUI (Formerly Ollama WebUI)](https://github.com/open-webui/open-webui)

#### Open WebUI

* If Ollama is on your computer, use this command:
	
	`docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main`
	
* If Ollama is on a Different Server, use this command:

	To connect to Ollama on another server, change the OLLAMA_BASE_URL to the server's URL:

	`docker run -d -p 3000:8080 -e OLLAMA_BASE_URL=https://example.com -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main`
	
	To run Open WebUI with Nvidia GPU support, use this command:
	
	`docker run -d -p 3000:8080 --gpus all --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:cuda`
	

## FQA

[Ollama - FAQ](https://github.com/ollama/ollama/blob/main/docs/faq.md)











