# openssl 的使用


查看证书：
`openssl s_client -showcerts -connect projectevcharger.com:8443`


查看证书：
`echo | openssl s_client -servername projectevcharger.com:8443`


openssl s_client -showcerts -connect testcharge.growatt.com:9091