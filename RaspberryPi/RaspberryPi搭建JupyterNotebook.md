# Jupyter Notebook on Raspberry Pi


apt-get update
apt-get install python3-matplotlib
apt-get install python3-scipy
pip3 install --upgrade pip
reboot
sudo pip3 install jupyter

sudo apt update
sudo apt upgrade
sudo pip3 install jupyter --upgrade
#### now repeated installation .. much faster and error free
sudo pip3 install jupyter
sudo apt-get clean


## 让Jupyter notebook 在本地的电脑可以访问

### 方法一： 配置文件 `jupyter_notebook_config.py`

* 检查配置文件是否存在
	>在目录：`~/.jupyter/jupyter_notebook_config.py` 下。
	
* 生成对应的配置文件（如果没有配置文件才生成）
	>可用命令`jupyter notebook --generate-config`生成。
	>可用命令`jupyter notebook --help`查看对应的配置项

* 增加下面两项配置
	>`c.NotebookApp.allow_origin = '*'`# allow all origins
	>`c.NotebookApp.ip = '0.0.0.0'` # listen on all IPs
* 如果对应`8888`端口关闭(可选)
	>使用`sudo ufw allow 8888` # enable your tcp:8888 port, which is ur default jupyter port
* 设置访问密码(可选)
	>`jupyter notebook password`
* 运行 jupyter notebook
	>`jupyter notebook`

### 方法二 临时配置

`jupyter notebook --ip 0.0.0.0 --port 8888`

或者下面的，`xx.xx.xx.xx`为对应的运行jupyter的机器ip

`jupyter notebook --ip xx.xx.xx.xx --port 8888` 




[Documentation on the Jupyter Notebook config file](https://jupyter-notebook.readthedocs.io/en/latest/config.html)


[Jupyter Notebook on Raspberry Pi](https://www.instructables.com/Jupyter-Notebook-on-Raspberry-Pi/#discuss)