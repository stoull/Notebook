# Linux多用户与系统安全



先理解Linux多用户，参见--Linux多用户理解与管理

如果机器运行了一个x服务，但这个服务发现有漏洞，黑客可以通过这个漏洞黑进这个机器。但黑进去的黑客现在只有运行这个服务的用户的权限。
如果你使用的是root用户运行的这个服务，那黑客就可以做任何事情。传各种数据文件，创建新用户，安装或删除各种软件。
如果使用一个单独的用户，这个用户只有防问x服务所需要的权限，黑客就不会像在root下那么容易，入侵整个系统了。

## 运行服务安全

#### 不要使用root运行公开服务

#### 使用不同的user隔离服务及资源，注意选择普通用户或服务用户

When you are creating an account to run a daemon, service, or other system software, rather than an account for interactive use.

- `useradd -s /sbin/nologin username` (Debian systems) 或 `useradd -s /bin/false username ` `-s`指定用户登录后使用的shell, 这里指定的为无nologin或false。
- `useradd -r username` : `-r` 为创建系统用户，无home目录无密码，不能登录，只有root可以登录。
- `useradd -m username`，将在/home目录下创建同名文件夹，然后利用（passwd + 用户名）为指定的用户名设置密码。

#### 服务用户使用Non Interactive Shell或移除Shell的访问


## 示例

### nginx服务

在配置文件`/etc/nginx/nginx.conf`中第一行为：

`user nginx;`

即表示nginx服务使用用户`nginx`运行。需要创建nginx用户并让它有资源目录根目录的权限。

这样运行nginx，只在master process运行在root环境下，因为只有 root processes 可以监听1024以下的端口，像80/443.

>The main purpose of the master process is to read and evaluate configuration files, as well as maintain the worker processes.
>
The worker processes do the actual processing of requests.
>
[NGINX Document - Master and Worker Processes](https://docs.nginx.com/nginx/admin-guide/basic-functionality/runtime-control/#master-and-worker-processes)

如果要让master process使用非root用户运行:

更改Nginx目录下下面文件的所属关系：

* error_log
* access_log
* pid
* client_body_temp_path
* fastcgi_temp_path
* proxy_temp_path
* scgi_temp_path
* uwsgi_temp_path

更改监听的端口号为1024上，如8080. 登录为对应的nginx用户，运行`nginx -c /path/to/nginx.conf`

[Running Nginx as non root user](https://stackoverflow.com/questions/42329261/running-nginx-as-non-root-user)













