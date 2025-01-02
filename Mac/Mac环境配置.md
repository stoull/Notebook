# Mac环境配置


#### Brew
安装完成brew后，需要将brew加入环境中：

```
==> Next steps:
- Run these commands in your terminal to add Homebrew to your PATH:
    echo >> /Users/hut/.zprofile
    echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> /Users/hut/.zprofile
    eval "$(/opt/homebrew/bin/brew shellenv)"
- Run brew help to get started
- Further documentation:
    https://docs.brew.sh
```


#### Node

```
node@20 is keg-only, which means it was not symlinked into /opt/homebrew,
because this is an alternate version of another formula.

If you need to have node@20 first in your PATH, run:
  echo 'export PATH="/opt/homebrew/opt/node@20/bin:$PATH"' >> ~/.zshrc

For compilers to find node@20 you may need to set:
  export LDFLAGS="-L/opt/homebrew/opt/node@20/lib"
  export CPPFLAGS="-I/opt/homebrew/opt/node@20/include"
```