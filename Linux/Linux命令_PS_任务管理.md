# Linux 命令：任务管理 `ps`

常用 `man ps`命令

`PID` : -  This is the unique process ID

`PPID` : -  This is the the Parent Process ID

`S/STAT`: the current status of the process

进程状态解释：

```
I       Marks a process that is idle (sleeping for longer than about 20 seconds).
R       Marks a runnable process.
S       Marks a process that is sleeping for less than about 20 seconds.
T       Marks a stopped process.
U       Marks a process in uninterruptible wait.
Z       Marks a dead process (a ``zombie'').

Additional characters after these, if any, indicate additional state information:

+       The process is in the foreground process group of its control terminal.
<       The process has raised CPU scheduling priority.
>       The process has specified a soft limit on memory requirements and is currently exceeding that limit;
       such a process is (necessarily) not swapped.
A       the process has asked for random page replacement (VA_ANOM, from vadvise(2), for example, lisp(1) in
       a garbage collect).
E       The process is trying to exit.
L       The process has pages locked in core (for example, for raw I/O).
N       The process has reduced CPU scheduling priority (see setpriority(2)).
S       The process has asked for FIFO page replacement (VA_SEQL, from vadvise(2), for example, a large
       image processing program using virtual memory to sequentially address voluminous data).
s       The process is a session leader.
V       The process is suspended during a vfork(2).
W       The process is swapped out.
X       The process is being traced or debugged.
```

`%cpu` : -  percentage CPU usage (alias pcpu)
`%mem` : -  percentage memory usage (alias pmem)

`TTY` : -  the name of the console that the user is logged into

`TIME` : -  the amount of CPU in minutes and seconds that the process has been running
`CMD` : -  the name of the command that launched the process

Examples:

`$ ps aux`  列出当前用户进程 

`$ ps -A`  列出所有进程

`$ ps -A --forest`  按树状结构列出所有进程

`$ ps -l`  列出所进程详细信息

### 缩小范围查找
`$ ps -C Xcode`  使用关健字键字进行过滤 **mac及rpi上待验证**

`$ ps -l -p 3536`  列出出特定PID的进程

`$ ps -hut`  列出出特定用户的进程

`$ ps --ppid 3536`  列出PID下的线程信息 **mac及rpi上待验证**

`$ ps -o user,pid,%cpu,%mem,stat,time` 根据字段查询进程信息

`ps aux | egrep '(cron|syslog)'` 查找与cron 与 syslog 这两个服务有关的 PID 号码

### 排序

`$ ps -A --sort=pcpu` 按cup使用率排序  或：

`$ ps -l | sort -nk 3 | head -3` 按cup使用率排序  

`$ ps -A --sort=pmem` 按内存使用率排序  或：

`$ ps -l | sort -nk 3 | head -3` 按内存使用率排序

**注意：**
> `--sort` is supported by ps from procps, other implementations may not have this option.如：
`$ ps --sort=-pcpu | head -n 6`
