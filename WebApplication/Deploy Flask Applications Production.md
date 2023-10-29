# 部署Flask - Deploy Flask Applications Production


[How to Deploy Flask with Gunicorn and Nginx (on Ubuntu)](https://www.youtube.com/watch?v=KWIIPKbdxD0)


开发运行`flask run`:

```
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
```


## Nginx

- 缓存及分配request
- 负载均衡，多服务器的负载均衡，同一机器的多服务
- 安全, 反向代理
- SSL,处理对外ssl加密，多服务器统一的https加密出口
- 对responses数据的压缩
- Nginx可代替Python处理静态文件的请求，可提高性能

## 使用gunicorn

- Gunicorn 'Green Unicorn' is a Python WSGI HTTP Server for UNIX
- gunicorn是Python语言的WSGI HTTP 服务器，即Web Servergatway Intergate
- 与gunicorn类似的库还有uSWGI

### WSGI - Python Web Server Gateway Interface

WSGI指定了web服务器和Python web应用或web框架之间的标准接口，以提高web应用在一系列web服务器间的移植性。

- WSGI是一套接口标准协议/规范；
- 通信（作用）区间是Web服务器和Python Web应用程序之间；
- 目的是制定标准，以保证不同Web服务器可以和不同的Python程序之间相互通信

[WSGI 官文 - PEP 333 – Python Web Server Gateway Interface v1.0](https://peps.python.org/pep-0333/)

[Gunicorn官网](https://gunicorn.org)

[Gunicorn的配置](https://docs.gunicorn.org/en/stable/settings.html)

安装 gunicorn: 
`pip install gunicorn`

使用gunicorn运行flask项目: 

`gunicorn -b your-local-ip:8000 app:app`

or

`gunicorn -b 0.0.0.0:8000 app:app`

注意将使用的端口开放访问此处是`8000`号端口

`app:app`中，第一个app为flask项目实例所在的包（就是启动文件app.py），第二个app为生成的flask项目实例（就是你app.py里定义的flask实例）。
> `app = Flask(__name__)`


[gunicorn.org](https://gunicorn.org/)

[Flask - 生产部署](https://dormousehole.readthedocs.io/en/latest/deploying/index.html)

[Step-by-step visual guide on deploying a Flask application on AWS EC2](https://medium.com/techfront/step-by-step-visual-guide-on-deploying-a-flask-application-on-aws-ec2-8e3e8b82c4f7)

[部署Flask](https://spacewander.github.io/explore-flask-zh/13-deployment.html)

[AWS - Deploying a Flask application to Elastic Beanstalk](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-flask.html)

[Flask之旅](https://spacewander.github.io/explore-flask-zh/)