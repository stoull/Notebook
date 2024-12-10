# Z shell-zsh

Starting with macOS Catalina, your Mac uses zsh as the default login shell and interactive shell. 

* `zsh` (Z shell) is the default shell for all newly created user accounts, starting with macOS Catalina.
* `bash` is the default shell in macOS Mojave and earlier.

自2019年起，macOS的默认Shell已从Bash改为Zsh。

[Z shell - WiKi](https://zh.wikipedia.org/zh-cn/Z_shell)

[Use zsh as the default shell on your Mac](https://support.apple.com/en-us/102360)

[What should/shouldn't go in .zshenv, .zshrc, .zlogin, .zprofile, .zlogout?](https://unix.stackexchange.com/questions/71253/what-should-shouldnt-go-in-zshenv-zshrc-zlogin-zprofile-zlogout)


Here is a non-exhaustive list, in execution-order, of what each file tends to contain:

* `.zshenv` is always sourced. It often contains exported variables that should be available to other programs. For example, $PATH, $EDITOR, and $PAGER are often set in .zshenv. Also, you can set $ZDOTDIR in .zshenv to specify an alternative location for the rest of your zsh configuration.
* `.zprofile` is for login shells. It is basically the same as .zlogin except that it's sourced before .zshrc whereas .zlogin is sourced after .zshrc. According to the zsh documentation, ".zprofile is meant as an alternative to .zlogin for ksh fans; the two are not intended to be used together, although this could certainly be done if desired."
* `.zshrc` is for interactive shells. You set options for the interactive shell there with the setopt and unsetopt commands. You can also load shell modules, set your history options, change your prompt, set up zle and completion, et cetera. You also set any variables that are only used in the interactive shell (e.g. $LS_COLORS).
* `.zlogin` is for login shells. It is sourced on the start of a login shell but after .zshrc, if the shell is also interactive. This file is often used to start X using startx. Some systems start X on boot, so this file is not always very useful.
* `.zlogout` is sometimes used to clear and reset the terminal. It is called when exiting, not when opening.