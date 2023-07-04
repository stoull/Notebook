# Linux系统上遇到的问题

### 在Mac使用ssh连接后，不能输入及显示中文，但Mac本地终端是正常的

**解决方案**
将文件`/etc/ssh/ssh_config`文件最后的`SendEnv LANG LC_*`注释掉

### linux系统bash乱码问题

[linux乱码问题:LANG变量的秘诀](https://www.cnblogs.com/huangpeng/archive/2009/02/20/1394882.html)


[LANG variable on UNIX or Linux systems](https://www.ibm.com/docs/en/sva/7.0.0?topic=SSPREK_7.0.0/com.ibm.isam.doc_70/gsk_capicmd_user19.htm)