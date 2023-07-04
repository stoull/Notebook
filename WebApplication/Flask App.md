# Flask App

[Flask](https://flask.palletsprojects.com/en/2.0.x/)

[Templates](https://flask.palletsprojects.com/en/2.0.x/templating/)

[Large Applications as Packages](https://flask.palletsprojects.com/en/2.1.x/patterns/packages/)

## 安装 Flask
### 安装虚拟环境

```
$ mkdir myproject
$ cd myproject
$ python3 -m venv venv
```

激活虚拟环境
```
$ source path_to/venv/bin/activate	# bash/zsh
$ source path_to/venv/bin/activate.fish	# fish
$ source path_to/venv/bin/activate.csh	# csh/tcsh
```

### 安装Flask
```
$ pip install Flask
```

## 最小web(WSGI)程序

代码如下：

```
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
```
将上面的代存储名为`hello.py `，运行web程序:

```
$ export FLASK_APP=hello
$ flask run
 * Running on http://127.0.0.1:5000/
```
如果存储的名字为`app.py` 或者 `wsgi.py`, 则不需要运行`export FLASK_APP=hello`, 详情见[Command Line Interface](https://flask.palletsprojects.com/en/2.0.x/cli/)

**让服务在网络可见：**
`$ flask run --host=0.0.0.0`

`$ flask run --host=0.0.0.0 --port 5001`

这让系统监听所有公共ip，注意安全！

其它url path访问，或处理json接口等，详见[Quickstart](https://flask.palletsprojects.com/en/2.0.x/quickstart/#a-minimal-application)

**进入开发模式**

```
$ export FLASK_ENV=development
$ flask run
```

## Flask-Login
Flask-Login 提供了用户session管理功能
### 安装

```
$ pip install flask-login
```

### 使用Flask-Login




# 如何分离功能模块，不让app.py文件那么大？

[Templates](https://flask.palletsprojects.com/en/2.0.x/templating/)