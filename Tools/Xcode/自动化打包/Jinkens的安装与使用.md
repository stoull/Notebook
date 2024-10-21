# Jenkins For MacOS 


Jenkins LTS vs Jenkins Weekly


## Install

Jenkins can be installed using the Homebrew package manager. Homebrew formula: jenkins-lts This is a package supported by a third party which may be not as frequently updated as packages supported by the Jenkins project directly.

Sample commands:

* Install the latest LTS version: `brew install jenkins-lts`
* Start the Jenkins service: brew `services start jenkins-lts`
* Restart the Jenkins service: `brew services restart jenkins-lts`
* Update the Jenkins version: `brew upgrade jenkins-lts`

After starting the Jenkins service, browse to http://localhost:8080 and follow the instructions to complete the installation. Also see the external materials for installation guidelines. For example, this blogpost describes the installation process.


-- [macOS Installers for Jenkins LTS](https://www.jenkins.io/download/lts/macos/)

`brew install jenkins-lts`

安装完成之后：

```
==> Caveats
==> jenkins-lts
Note: When using launchctl the port will be 8080.

To start jenkins-lts now and restart at login:
  brew services start jenkins-lts
Or, if you don't want/need a background service you can just run:
  /usr/local/opt/openjdk/bin/java -Dmail.smtp.starttls.enable\=true -jar /usr/local/opt/jenkins-lts/libexec/jenkins.war --httpListenAddress\=127.0.0.1 --httpPort\=8080

```