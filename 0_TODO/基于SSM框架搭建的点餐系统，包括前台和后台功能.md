# 基于SSM框架搭建的点餐系统，包括前台和后台功能

[基于SSM框架搭建的点餐系统，包括前台和后台功能。](https://github.com/CodingLink/meal_ordering_system)


### About Apache Maven

[Welcome to Apache Maven](https://maven.apache.org/)

[Installing Apache Maven](https://maven.apache.org/install.html)

### Install JDK


安装JDK 1.8: `brew install openjdk@8`

安装最新版本: `brew install openjdk`, 即这个时间的21的版本

[Amazon Linux 2 安装JDK](https://docs.aws.amazon.com/zh_tw/corretto/latest/corretto-8-ug/amazon-linux-install.html)

[How to Install Java on Mac](https://phoenixnap.com/kb/install-java-macos)

[How to Install JDK on Mac OS X](https://learn.saylor.org/mod/book/view.php?id=26799&chapterid=2446)

[Java Downloads](https://www.oracle.com/java/technologies/downloads/)

[Java SE( Standard Edition)](https://www.oracle.com/java/technologies/java-se-glance.html)

[Java SE 18 Archive Downloads](https://www.oracle.com/java/technologies/javase/jdk18-archive-downloads.html)


### MySql安装

下载RPM文件：
`sudo wget https://dev.mysql.com/get/mysql80-community-release-el9-1.noarch.rpm `

查看下载的文件：`ls -lrt`

安装：
`sudo dnf install mysql80-community-release-el9-1.noarch.rpm -y`
`sudo dnf install mysql-community-server -y`

### 安装tomcat

#### Amazon Linux 安装tomcat
[Step by Step guide to install Apache Tomcat on Amazon Linux](https://medium.com/@raguyazhin/step-by-step-guide-to-install-apache-tomcat-on-amazon-linux-120748a151a9)

确认java jdk已安装：`java -version`
如未安装，需安装：`sudo yum install java-1.8*`

```
sudo su -
cd /
cd /opt/
```
下载：
`wget https://dlcdn.apache.org/tomcat/tomcat-9/v9.0.80/bin/apache-tomcat-9.0.80.tar.gz`
解包：
`tar -xvf apache-tomcat-9.0.80.tar.gz`

重命名方便使用：
`mv apache-tomcat-9.0.71 tomcat9`



### 安装docker

`sudo yum install docker`

查看docker：

`docker info`

docker服务管理

```
sudo service docker start
sudo systemctl enable docker.service

sudo systemctl start docker.service #<-- start the service
sudo systemctl stop docker.service #<-- stop the service
sudo systemctl restart docker.service #<-- restart the service
sudo systemctl status docker.service #<-- get the service status
```