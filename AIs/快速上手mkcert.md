# 快速上手mkcert

[GitHub 上的项目地址 - mkcert: ](https://github.com/FiloSottile/mkcert/)

### 1. 安装 mkcert

**macOS：**
```bash
brew install mkcert
```

**Windows：**

```bash
choco install mkcert
# 或直接下载 exe：https://github.com/FiloSottile/mkcert/releases
```

**Linux (Ubuntu/Debian)：**

```bash
sudo apt install libnss3-tools
# 然后去 GitHub releases 下载二进制文件
```

### 2. 安装本地 CA 到系统信任库
```bash
mkcert -install
```
这一步会创建并信任一个本地根证书，只需做一次。

### 3. 生成证书
```bash
# 为 localhost 和 127.0.0.1 生成证书
mkcert -key-file key.pem -cert-file cert.pem localhost 127.0.0.1 ::1

# 如果你用自定义域名（如 myapp.test）
mkcert -key-file myapp-key.pem -cert-file myapp-cert.pem myapp.test
```

执行后会生成两个文件：
- `cert.pem` - 证书
- `key.pem` - 私钥

### 4. 在代码中使用

**Node.js (Express)：**

```javascript
const https = require('https');
const fs = require('fs');
const express = require('express');

const app = express();

const options = {
  key: fs.readFileSync('key.pem'),
  cert: fs.readFileSync('cert.pem')
};

https.createServer(options, app).listen(3000, () => {
  console.log('https://localhost:3000');
});
```

**Python (Flask)：**

```python
from flask import Flask
import ssl

app = Flask(__name__)

if __name__ == '__main__':
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('cert.pem', 'key.pem')
    app.run(host='0.0.0.0', port=3000, ssl_context=context)
```

**Python (FastAPI/uvicorn)：**

```bash
uvicorn main:app --host 0.0.0.0 --port 3000 --ssl-keyfile=key.pem --ssl-certfile=cert.pem
```

**.NET Core：**

```bash
# 最省心，自带工具
dotnet dev-certs https --trust
# 运行项目时会自动使用开发证书
dotnet run
```

**Go：**

```go
package main

import (
    "log"
    "net/http"
)

func main() {
    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        w.Write([]byte("Hello HTTPS"))
    })
    
    log.Fatal(http.ListenAndServeTLS(":3000", "cert.pem", "key.pem", nil))
}
```

### 5. 测试
打开浏览器访问 `https://localhost:3000`，应该可以看到绿色锁标志，不会出现安全警告。

---

## 三、临时调试（不推荐，但快）

如果只是临时调试，可以在浏览器中忽略证书警告：

- **Chrome**：在警告页面输入 `thisisunsafe`（焦点在页面上直接输入，没有输入框）
- **Edge**：同上
- **Firefox**：点击"高级" → "接受风险并继续"
- **Safari**：点击"显示详细信息" → "访问此网站"

或者启动浏览器时禁用安全检查：

```bash
# macOS Chrome
open -a Google\ Chrome --args --ignore-certificate-errors --unsafely-treat-insecure-origin-as-secure=https://localhost:3000

# Windows Chrome
chrome.exe --ignore-certificate-errors --unsafely-treat-insecure-origin-as-secure=https://localhost:3000
```

**⚠️ 警告**：这些方法只用于临时测试，用完立刻关掉浏览器。

---

## 四、常见问题

### 1. 端口被占用

```bash
# 查看 3000 端口占用
lsof -i :3000  # macOS/Linux
netstat -ano | findstr :3000  # Windows
```

### 2. 证书不生效
- 确认证书域名和你访问的 URL 完全匹配（`localhost` ≠ `127.0.0.1`）
- 重启浏览器（证书缓存问题）
- macOS：在钥匙串中删除旧证书，重新 `mkcert -install`

### 3. API 请求失败（前端调用）
前端代码需要配置 `fetch` 或 `axios` 忽略证书验证（仅限开发环境）：

**Node.js 后端调用另一个 HTTPS 服务：**

```javascript
// 设置环境变量
process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';
// ⚠️ 仅用于开发，不要提交到代码库
```

或者更精细的控制：

```javascript
const https = require('https');
const agent = new https.Agent({
  rejectUnauthorized: false
});
axios.get('https://localhost:3001/api', { httpsAgent: agent });
```

---

## 五、推荐工作流总结

1. **日常开发**：用 `mkcert`，一步到位
2. **团队协作**：把 `mkcert -install` 和证书生成命令写进 README
3. **CI/CD 测试**：用 `openssl` 动态生成（因为 CI 环境不需要信任证书）
4. **与后端联调**：前后端都用同一套 `mkcert` 生成的证书

这样就完全可以愉快地调试 HTTPS 了，不会再有证书警告。