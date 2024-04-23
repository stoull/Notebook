# Git多账号ssh-key配置

在同一台电脑上配置多个git账号的ssh key 访问，配置文件`~/.ssh/config`:

文件配置信息如下：

```
Host username1.github.com
    HostName github.com
    User username1
    AddKeysToAgent yes
    IdentityFile ~/.ssh/id_ed25519

Host username2.github.com
    HostName github.com
    User username12
    AddKeysToAgent yes
    IdentityFile ~/.ssh/id_ed25519_2

Host username3.github.com
    HostName github.com
    User username3
    AddKeysToAgent yes
    IdentityFile ~/.ssh/id_ed25519_3

Host 43.138.214.161
    HostName 43.138.214.161 
    User hut
    AddKeysToAgent yes
    IdentityFile ~/.ssh/id_ed25519
```