# Terminal Unicode字符转中文

## Unicode 转UTF-8
###使用 uni2ascii
* `brew search uni2ascii`
* `brew install uni2ascii`
* `echo '\u0144\u00f3' | ascii2uni -a U -q` 输出`ńó`
* `echo '\u6267\u884c\u51fa\u9519' | ascii2uni -a U -q` 输出`执行出错`

>  注意 Unicode 中的 `\u6267` \U 必须是小写 \u

[How to convert \uXXXX unicode to UTF-8 using console tools in *nix](https://stackoverflow.com/questions/8795702/how-to-convert-uxxxx-unicode-to-utf-8-using-console-tools-in-nix)




echo 文件名乱码 | iconv -t latin1 | iconv -f gbk


\U6267\U884c\U51fa\U9519



https://testcharge.growatt.com/ocpp/charge/info:{
    code = 0;
    data =     {
        Current = 0;
        Faulted = "";
        Voltage = "234.8";
        cKey = "G_SetAmount";
        cValue = 3;
        chargeEndTime = "2023-01-06T08:44:45";
        chargeId = D0BSB19011;
        connectorId = 1;
        cost = 0;
        ctime = 0;
        ctype = 0;
        current = 0;
        elockstate = locked;
        energy = 0;
        errorCode = NoError;
        idTag = D0BSB19011;
        info = "";
        meterStart = 0;
        online = 0;
        orderId = "D0BSB19011_89274";
        "order_status" = 0;
        rate = 0;
        status = Charging;
        symbol = "€";
        sysEndTime = 1672991086953;
        sysStartTime = 1672991086522;
        timestamp = "2023-01-06T08:44:44";
        transactionId = 89274;
        unit = euro;
        userId = test711;
        voltage = "234.8";
    };
}