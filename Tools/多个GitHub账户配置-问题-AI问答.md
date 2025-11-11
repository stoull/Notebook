# 多个GitHub账户配置-问题-AI问答

问：

在同一个电脑上配置了多个github的ssh-key. 比如现在有一个A账户的仓库git@github.com:john/project.git, 使用‘ssh -T git@github.com-john’，也是正常显示‘Hi john! You've successfully authenticated’。为什么执行push的时候，还会报：ERROR: Permission to john/project.git denied to Kevin. 它还是使用Kevin的ssh-key. ssh是怎么选择使用哪个人的ssh-key。在这里我又要怎么做才能保证，我这个仓库使用的是正确的人的ssh-key呢
 ~/.ssh/config文件中是这样定义的：
```
Host github.com-Kevin
    HostName github.com
    User git
    AddKeysToAgent yes
    IdentityFile ~/.ssh/id_ed25519

Host github.com-john
    HostName github.com
    User git
    AddKeysToAgent yes
    IdentityFile ~/.ssh/id_ed25519_2
```

答：


你遇到的情况核心原因是：Git 的远程 URL 用的是原生域名 github.com，而不是你在 ~/.ssh/config 里定义的别名 github.com-john；所以真正执行 git push 时，SSH 连接的 Host 是 github.com，这一行并不会触发你为 github.com-john 写的那段配置，只会使用默认加载到 ssh-agent 里的那些 key（其中包括 Kevin 的），GitHub 服务器根据收到的公钥判断身份，于是识别成 Kevin，导致提示 “Permission denied to Kevin”。

下面分步骤解释与解决。

一、为什么 ssh -T git@github.com-john 正常，而 git push 不正常  
1. 你执行的测试命令 ssh -T git@github.com-john，Host 是 github.com-john，OpenSSH 会匹配到对应的配置段：  
   Host github.com-john  
   ... IdentityFile ~/.ssh/id_ed25519_2  
   所以它用的是 john 的私钥。  
2. 你的仓库远程现在是：git@github.com:john/project.git。这里的 Host 是 github.com（不是 github.com-john），因此 ~/.ssh/config 中被匹配的是 Host github.com-Kevin 这一段吗？其实也不是——因为远程写的是 github.com，不是 github.com-Kevin。最终实际匹配到的可能是一个更通用的条目（如果没有专门的 “Host github.com” 配置，就会走默认行为，ssh-agent 里哪个 key先被尝试，就用哪个；GitHub 看到对应的公钥属于 Kevin）。  
3. 结论：远程 URL 必须使用你定义的别名 Host 才能强制选中对应 IdentityFile。

二、SSH 是怎么选 key 的  
- 如果你没有写 IdentitiesOnly yes，且启动了 ssh-agent，agent 里所有已加入的 key 都可能被逐个尝试。GitHub 会以第一个它认识的公钥来确定账号。  
- IdentityFile 只是“增加一个候选”，不加 IdentitiesOnly 时并不会阻止其他 key 被尝试。  
- 加上 IdentitiesOnly yes 才表示“只用我在此 Host 条目里列出的 key，不再枚举其它”。  

三、解决方案（推荐做法）  
方案 1：修改远程 URL 使用 Host 别名  
1. 在 ~/.ssh/config 中改为（加上 IdentitiesOnly）：  
```
Host github.com-Kevin
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes

Host github.com-john
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_2
    IdentitiesOnly yes
```
2. 到 john 的项目目录里，把 origin 改为使用别名：  
```
git remote set-url origin git@github.com-john:john/project.git
```
3. 测试：  
```
ssh -T git@github.com-john
git push
```
只要远程里 Host 是 github.com-john 就会强制用 id_ed25519_2。  

方案 2：使用 GIT_SSH_COMMAND 临时指定  
不想改远程，可临时：  
```
GIT_SSH_COMMAND='ssh -i ~/.ssh/id_ed25519_2 -o IdentitiesOnly=yes' git push
```
但这只是一次性，不适合长期维护多个仓库。  

方案 3：Git URL 重写（适合批量）  
在 ~/.gitconfig 加：  
```
[url "git@github.com-john:"]
    insteadOf = git@github.com:john/
```
这样即使你克隆用官方地址：  
```
git clone git@github.com:john/project.git
```
Git 会自动把它内部识别为 git@github.com-john:john/project.git，进而匹配别名 Host。  

方案 4：按目录自动切换（进阶）  
如果你把 john 的项目都放在某个路径，比如 ~/work/john/ 下，可以用 Git 的 includeIf：  
```
[includeIf "gitdir:~/work/john/"]
    path = ~/.gitconfig-john
```
然后在 ~/.gitconfig-john 里设置 user/email；SSH 依旧用 Host 别名控制 key。这样 Git commit 的用户名与推送的身份都对应。  

四、验证与排查  
1. 用 ssh -v git@github.com-john 看调试输出，确认只有正确的 key 被尝试。  
2. 如果看到尝试了多个 identity，说明缺 IdentitiesOnly yes。  
3. 确认公钥是否真的添加在 john 账户的 GitHub “SSH keys” 页面而不是 Kevin 的。  

五、常见误区  
- 误区：以为配置了 Host github.com-john，就能作用到所有 github.com 的连接。实际上 Host 必须精确匹配。  
- 误区：IdentityFile 写了就一定只用该 key。必须配合 IdentitiesOnly yes。  
- 误区：测试 ssh -T 成功就认为 push 一定成功。测试用的 Host 和远程用的 Host 必须一致。  

六、快速检查脚本（可选）  
你可以写一个简单脚本列出当前 origin：  
```
git remote -v
```
如果显示还是 github.com:john/... 就说明没用别名。  

七、总结操作最简步骤  
1. ~/.ssh/config 加 IdentitiesOnly yes。  
2. 修改远程：git remote set-url origin git@github.com-john:john/project.git  
3. 测试：ssh -T git@github.com-john  
4. 推送：git push  

这样就不会再出现 “denied to Kevin” 的问题。  

如果还有疑问（比如多个组织、多种协议 https/ssh 混用、CI 场景等），继续问我即可。