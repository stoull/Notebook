# Open ssl 检查证书


`openssl s_client -servername ces.growatt.com -connect ces.growatt.com:7006 | openssl x509 -noout -dates`

```
depth=2 C = US, O = DigiCert Inc, OU = www.digicert.com, CN = DigiCert Global Root CA
verify return:1
depth=1 C = CN, O = "TrustAsia Technologies, Inc.", OU = Domain Validated SSL, CN = TrustAsia TLS RSA CA
verify return:1
depth=0 CN = ces.growatt.com
verify error:num=10:certificate has expired
notAfter=Mar  1 23:59:59 2023 GMT
verify return:1
depth=0 CN = ces.growatt.com
notAfter=Mar  1 23:59:59 2023 GMT
verify return:1
notBefore=Mar  2 00:00:00 2022 GMT
notAfter=Mar  1 23:59:59 2023 GMT
```

```
openssl s_client -connect sqimg.qq.com:443
```

```
openssl s_client -connect sqimg.qq.com:443 -servername sqimg.qq.com

```


#### 查看证书信息
`openssl x509 -noout -text -in ca.crt`