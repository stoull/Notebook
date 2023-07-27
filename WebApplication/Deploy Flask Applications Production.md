# 部署Flask - Deploy Flask Applications Production




## 使用gunicorn

安装 gunicorn: 
`pip install gunicorn`

使用gunicorn运行flask项目: 

`gunicorn -b your-local-ip:8000 app:app `

or 

`gunicorn -b 0.0.0.0:8000 app:app`

注意将使用的端口开放访问此处是`8000`号端口

`app:app`中，第一个app为flask项目实例所在的包（就是启动文件app.py），第二个app为生成的flask项目实例（就是你app.py里定义的flask实例）。
> `app = Flask(__name__)`


[Flask - 生产部署](https://dormousehole.readthedocs.io/en/latest/deploying/index.html)

[Step-by-step visual guide on deploying a Flask application on AWS EC2](https://medium.com/techfront/step-by-step-visual-guide-on-deploying-a-flask-application-on-aws-ec2-8e3e8b82c4f7)

[部署Flask](https://spacewander.github.io/explore-flask-zh/13-deployment.html)

[AWS - Deploying a Flask application to Elastic Beanstalk](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-flask.html)

[Flask之旅](https://spacewander.github.io/explore-flask-zh/)