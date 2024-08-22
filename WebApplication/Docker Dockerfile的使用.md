# Dockerfile的使用



#### `EXPOSE 端口`

* `EXPOSE`用于声明容器在运行时监听的网络端口。它并不会实际地开放端口或进行网络配置，而只是作为文档和约定，告知用户和其他开发者这个容器期望使用哪些端口。
* 实际需要`docker run -p <host_port>:<container_port>`中指定对应的端口映射关系。
* 如果使用`docker run -P`自动端口映射,则会使用`EXPOSE`中的端口,而不是随机的端口。
 


docker run -P 时，会自动随机映射 EXPOSE 的端口。



[Dockerfile overview](https://docs.docker.com/build/concepts/dockerfile/)

[Dockerfile reference](https://docs.docker.com/reference/dockerfile/#copy)