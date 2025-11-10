#多个GitHub账户配置



`~/.ssh/config`文件：

```
Host github.com-stoull
    HostName github.com
    User git
    AddKeysToAgent yes
    IdentityFile ~/.ssh/id_ed25519

Host github.com-achangehut
    HostName github.com
    User git
    AddKeysToAgent yes
    IdentityFile ~/.ssh/id_ed25519_achangehut

Host github.com-hutbe
    HostName github.com
    User git
    AddKeysToAgent yes
    IdentityFile ~/.ssh/id_ed25519_hutbe

Host ahut.site
  HostName ahut.site
  Port 31800
  User hut
  AddKeysToAgent yes
  UseKeychain yes
```

`ssh-add ~/.ssh/id_ed25519_personal`: 加载key

`ssh -T git@github.com-hutbe`: 测试连接的用户

```
ssh -T git@github.com-hutbe   
Hi hutbe! You've successfully authenticated, but GitHub does not provide shell access.
```

`ssh -T git@github.com-achangehut`: 测试连接的用户，如下，说明ssh-key和想要的用户不一致，说明用错了

```
hut@hutdeMac-mini Vault % ssh -T git@github.com-achangehut
Hi stoull! You've successfully authenticated, but GitHub does not provide shell access.
```

[SSH: Bad configuration option: usekeychain](https://www.unixtutorial.org/ssh-bad-configuration-option-usekeychain/)


[1.6 起步 - 初次运行 Git 前的配置](https://git-scm.com/book/zh/v2/起步-初次运行-Git-前的配置)

[OpenSSH updates in macOS 10.12.2](https://developer.apple.com/library/archive/technotes/tn2449/_index.html)

[Best way to use multiple SSH private keys on one client [closed]
](https://stackoverflow.com/questions/2419566/best-way-to-use-multiple-ssh-private-keys-on-one-client)


[Developing with multiple GitHub accounts on one MacBook](https://medium.com/@ibrahimlawal/developing-with-multiple-github-accounts-on-one-macbook-94ff6d4ab9ca)