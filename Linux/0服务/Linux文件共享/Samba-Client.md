# Samba-Client

`sudo apt install samba-client`

`smbclient -L 20.50.1.20`
`smbclient -I 20.50.1.20 -V`


MacOS上查看当前连接的共享文件服务：

`smbutil statshares -a`

smbutil statshares详情：

```
usage : smbutil statshares [-m <mount_path> | -a] [-f <format>]
            [
             description :
             -a : attributes of all mounted shares
             -m <mount_path> : attributes of share mounted at mount_path
             -f <format> : print info in the provided format. Supported formats: JSON
             ]
```

`smbutil statshares -a`
```
hut@StoullMacMini ~ % smbutil statshares -a

==================================================================================================
SHARE                         ATTRIBUTE TYPE                VALUE
==================================================================================================
SharedDir                       
                              SERVER_NAME                   20.50.1.20
                              USER_ID                       501
                              SMB_NEGOTIATE                 SMBV_NEG_SMB1_ENABLED
                              SMB_NEGOTIATE                 SMBV_NEG_SMB2_ENABLED
                              SMB_NEGOTIATE                 SMBV_NEG_SMB3_ENABLED
                              SMB_VERSION                   SMB_3.1.1
                              SMB_ENCRYPT_ALGORITHMS        AES_128_CCM_ENABLED
                              SMB_ENCRYPT_ALGORITHMS        AES_128_GCM_ENABLED
                              SMB_ENCRYPT_ALGORITHMS        AES_256_CCM_ENABLED
                              SMB_ENCRYPT_ALGORITHMS        AES_256_GCM_ENABLED
                              SMB_CURR_ENCRYPT_ALGORITHM    OFF
                              SMB_SIGN_ALGORITHMS           AES_128_CMAC_ENABLED
                              SMB_SIGN_ALGORITHMS           AES_128_GMAC_ENABLED
                              SMB_CURR_SIGN_ALGORITHM       AES_128_CMAC
                              SMB_SHARE_TYPE                DISK
                              SIGNING_SUPPORTED             TRUE
                              EXTENDED_SECURITY_SUPPORTED   TRUE
                              LARGE_FILE_SUPPORTED          TRUE
                              FILE_IDS_SUPPORTED            TRUE
                              DFS_SUPPORTED                 TRUE
                              FILE_LEASING_SUPPORTED        TRUE
                              MULTI_CREDIT_SUPPORTED        TRUE
                              MULTI_CHANNEL_SUPPORTED       TRUE
                              DIR_LEASING_SUPPORTED         TRUE
                              SESSION_RECONNECT_TIME        0:0
                              SESSION_RECONNECT_COUNT       0
```