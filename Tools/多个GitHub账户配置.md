#多个GitHub账户配置

[Linux配置OpenSSH](../linux/Linux配置OpenSSH.md)


### `~/.ssh/config`文件配置：

```
Host github.com-john
    HostName github.com
    User git
    AddKeysToAgent yes
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes

Host github.com-kevin
    HostName github.com
    User git
    AddKeysToAgent yes
    IdentityFile ~/.ssh/id_ed25519_2
    IdentitiesOnly yes

Host github.com-hut
    HostName github.com
    User git
    AddKeysToAgent yes
    IdentityFile ~/.ssh/id_ed25519_3
    IdentitiesOnly yes

Host hut-value-site
  HostName ahut.site
  Port 31800
  User hut
  AddKeysToAgent yes
  UseKeychain yes
```

`IdentitiesOnly yes` : 限制只使用 Host 条目里列出的IdentifyFile key，不再尝试其它的key了

### 

### 测试

- `ssh-add ~/.ssh/`: mac上添加新的key，这里是所有的key

- `ssh -T git@github.com-hut`: 测试连接的用户

```
ssh -T git@github.com-kevin   
Hi hutbe! You've successfully authenticated, but GitHub does not provide shell access.
```

`ssh -T git@github.com-john`: 测试连接的用户，如下，说明ssh-key和想要的用户不一致，说明用错了

```
hut@hutdeMac-mini Vault % ssh -T git@github.com-john
Hi stoull! You've successfully authenticated, but GitHub does not provide shell access.
```

### Git remote url 配置

在remote url配置中，使用对应的Host别名：

- `git remoet -v`
- `git remoet set-url origin git@github.com-john:hutbe/Vault.git`

这样就可以确定使用正确的ssh-key了。

[SSH: Bad configuration option: usekeychain](https://www.unixtutorial.org/ssh-bad-configuration-option-usekeychain/)


[1.6 起步 - 初次运行 Git 前的配置](https://git-scm.com/book/zh/v2/起步-初次运行-Git-前的配置)

[OpenSSH updates in macOS 10.12.2](https://developer.apple.com/library/archive/technotes/tn2449/_index.html)

[Best way to use multiple SSH private keys on one client [closed]
](https://stackoverflow.com/questions/2419566/best-way-to-use-multiple-ssh-private-keys-on-one-client)


[Developing with multiple GitHub accounts on one MacBook](https://medium.com/@ibrahimlawal/developing-with-multiple-github-accounts-on-one-macbook-94ff6d4ab9ca)