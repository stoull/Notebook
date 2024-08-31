# Linux常用工具

#### 复制大文件并显示进行和速度

```
rsync -ah --progress source destination
```
> `-a` 保持原有权限
> `-h` 人可读
> `-r` recurse directories

```
pv my_big_file > backup/my_big_file
```
> pv会丢失原有文件的权限及所属

[How to show the transfer progress and speed when copying files with cp?](https://askubuntu.com/questions/17275/how-to-show-the-transfer-progress-and-speed-when-copying-files-with-cp)

#### 使用命令行 打开某个网页

`x-www-browser http://hutpi.local/analyse`
`chromium-browser http://hutpi.local/analyse`
`xdg-open http://hutpi.local/analyse`

#### c


