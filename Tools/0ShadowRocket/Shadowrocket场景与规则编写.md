# Shadowrocket：场景使用与纯文本规则编写

本文说明 Shadowrocket 中「配置 / 场景 / 纯文本规则」的关系，以及如何在公司 Wi‑Fi 等受限网络下，让微信、邮箱等流量走代理。

---

## 1. 核心概念

### 1.1 配置文件（`.conf`）

一份 `.conf` 通常包含：

- `[General]`：DNS、旁路、IPv6 等通用参数
- `[Rule]`：分流规则（域名 / IP / GEOIP / FINAL）
- 可选：`[Host]`、`[URL Rewrite]`、`[Proxy Group]` 等

节点（服务器）与规则配置是分开的：节点在首页选，规则在「配置」页选。

### 1.2 黄点 vs 勾选（非常重要）

在「配置 → 本地文件」列表中：

| 标记 | 含义 |
|------|------|
| 前面的**黄色小圆点** | **默认配置**：VPN 扩展实际加载并编译的那份 |
| 右侧**勾选** | 当前界面关联/选中，**不等于**已加载进 VPN |

只打勾、不点「使用配置」，VPN 仍可能继续跑旧的 `default.conf`，日志里就会一直出现：

```text
DOMAIN-SUFFIX,qq.com,DIRECT
DOMAIN-SUFFIX,icloud.com,DIRECT
GEOIP,CN,DIRECT
```

正确做法：点击目标配置 → **使用配置**（必要时再点 **编译配置**），确认该文件**同时有黄点 + 勾选**。

### 1.3 全局路由模式

首页「全局路由」：

| 模式 | 行为 |
|------|------|
| **配置** | 按当前默认配置（黄点）里的 `[Rule]` 分流 |
| **代理** | 几乎全部流量走当前节点（适合临时排查） |
| **直连** | 几乎全部流量不走代理 |
| **场景** | 按 Wi‑Fi / 蜂窝自动切换「路由模式 + 配置文件 + 节点」 |

### 1.4 `default.conf` 会不会一直叠加？

**不会。**

- 同一时刻只生效**一份**默认配置（黄点）
- 不是 `default.conf` 再叠一层你的 conf
- 若日志命中 `qq.com,DIRECT`，说明当时黄点仍是带这条规则的默认/旧配置

---

## 2. 纯文本规则编写

### 2.1 基本格式

```ini
类型,匹配内容,策略
```

常见策略：

- `PROXY`：走首页当前节点（或策略组）
- `DIRECT`：直连
- `REJECT`：拒绝

规则**自上而下**匹配，**命中即停**。更具体的规则写在更宽泛的规则前面。

### 2.2 常用规则类型

| 类型 | 作用 | 示例 |
|------|------|------|
| `DOMAIN` | 精确域名 | `DOMAIN,dns.weixin.qq.com,PROXY` |
| `DOMAIN-SUFFIX` | 后缀匹配 | `DOMAIN-SUFFIX,weixin.qq.com,PROXY` |
| `DOMAIN-KEYWORD` | 关键词 | `DOMAIN-KEYWORD,google,PROXY` |
| `IP-CIDR` | IPv4/IPv6 网段 | `IP-CIDR,101.226.142.0/24,PROXY` |
| `IP-ASN` | ASN | `IP-ASN,132203,PROXY` |
| `GEOIP` | 国家/地区 IP | `GEOIP,CN,DIRECT` |
| `FINAL` | 兜底（必须最后） | `FINAL,PROXY` |

说明：

- `DOMAIN-SUFFIX,weixin.qq.com` 能匹配 `long.weixin.qq.com`，但**匹配不了** `dns.weixin.qq.com.cn`（需另写 `DOMAIN-SUFFIX,weixin.qq.com.cn`）
- `DOMAIN-SUFFIX,qq.com` 很宽，会覆盖微信子域；若写成 `DIRECT`，会把微信「抢走」
- 微信长连/短连经常**先解析域名，再按纯 IP 连接**；只有域名规则不够，需要 `IP-CIDR` / `IP-ASN`

### 2.3 `[General]` 常用项

```ini
[General]
bypass-system = true
skip-proxy = 192.168.0.0/16, 10.0.0.0/8, 172.16.0.0/12, localhost, *.local
dns-server = system
ipv6 = false
```

- `ipv6 = false`：减少双栈绕开规则的情况
- 改完规则后务必再点一次 **使用配置 / 编译配置**，并断开重连 VPN

### 2.4 推荐规则顺序

```text
1. 精确 DOMAIN / 关键业务 DOMAIN-SUFFIX（微信、邮箱等）→ PROXY
2. IP-CIDR / IP-ASN（业务相关 IP）→ PROXY
3. 其它国内站点 DOMAIN-SUFFIX → DIRECT（可选）
4. GEOIP,CN,...
5. FINAL,...
```

---

## 3. 绕过公司网络限制：微信走代理示例

场景：公司 Wi‑Fi 限制微信；家里网络正常。希望连上公司 Wi‑Fi 后自动换一套「微信走代理」的配置。

### 3.1 准备两份配置

| 文件 | 用途 |
|------|------|
| `home.conf` | 日常分流（可保留国内直连） |
| `company_proxy.conf` | 公司 Wi‑Fi：微信 / 邮箱等强制 PROXY |

两份都要导入本地，并各自点过一次「使用配置」确认能单独生效。

### 3.2 公司配置示例：`company_proxy.conf`

```ini
# 公司 Wi‑Fi：微信 / 网易邮箱 / Google 邮箱走代理
[General]
bypass-system = true
skip-proxy = 192.168.0.0/16, 10.0.0.0/8, 172.16.0.0/12, localhost, *.local, captive.apple.com
dns-server = system
ipv6 = false

[Rule]
# ===== WeChat（必须写在 qq.com 直连规则之前；本文件不要写 qq.com,DIRECT）=====
DOMAIN,apd-pcdnwxlogin.teg.tencent-cloud.net,PROXY
DOMAIN,btrace.qq.com,PROXY
DOMAIN,dldir1.qq.com,PROXY
DOMAIN,weixin110.qq.com,PROXY
DOMAIN-SUFFIX,weixin.qq.com,PROXY
DOMAIN-SUFFIX,weixin.qq.com.cn,PROXY
DOMAIN-SUFFIX,wx.qq.com,PROXY
DOMAIN-SUFFIX,weixin.com,PROXY
DOMAIN-SUFFIX,wechat.com,PROXY
DOMAIN-SUFFIX,servicewechat.com,PROXY
DOMAIN-SUFFIX,weixinbridge.com,PROXY
DOMAIN-SUFFIX,tenpay.com,PROXY
DOMAIN-SUFFIX,wechatpay.com,PROXY
DOMAIN-SUFFIX,qlogo.cn,PROXY
DOMAIN-SUFFIX,qpic.cn,PROXY
DOMAIN-SUFFIX,wx.gtimg.com,PROXY
DOMAIN-SUFFIX,wxs.qq.com,PROXY
DOMAIN-SUFFIX,wxapp.tc.qq.com,PROXY

# 微信常落在运营商机房 IP（不一定是腾讯 ASN 132203）
# 以下网段来自实测日志，可按 Shadowrocket「连接日志」继续增补
IP-CIDR,101.226.142.0/24,PROXY
IP-CIDR,101.91.37.0/24,PROXY
IP-CIDR,117.89.177.0/24,PROXY
IP-CIDR,180.111.196.0/24,PROXY
IP-CIDR,175.6.84.0/24,PROXY
IP-CIDR,221.181.99.18/32,PROXY
IP-CIDR,112.65.193.165/32,PROXY
IP-ASN,132203,PROXY

# ===== NetEase Mail =====
DOMAIN-SUFFIX,163.com,PROXY
DOMAIN-SUFFIX,126.com,PROXY
DOMAIN-SUFFIX,yeah.net,PROXY
DOMAIN-SUFFIX,netease.com,PROXY

# ===== Google / Gmail =====
DOMAIN-SUFFIX,gmail.com,PROXY
DOMAIN-SUFFIX,google.com,PROXY
DOMAIN-SUFFIX,googleapis.com,PROXY
DOMAIN-SUFFIX,gstatic.com,PROXY
DOMAIN-SUFFIX,googleusercontent.com,PROXY
DOMAIN-KEYWORD,google,PROXY

# 其余国内 IP 直连；未匹配走代理
GEOIP,CN,DIRECT
FINAL,PROXY
```

要点：

1. **不要**在公司配置里写 `DOMAIN-SUFFIX,qq.com,DIRECT`
2. `IP-ASN,132203` 盖不住国内运营商托管的微信 IP，必须配合 `IP-CIDR`
3. 若日志仍出现 `GEOIP,CN,DIRECT` 的纯 IP，把该 IP 加成 `IP-CIDR,x.x.x.x/32,PROXY`，并放在 `GEOIP` 之前
4. 策略名 `PROXY` 须与 Shadowrocket 内置/策略组名称一致

### 3.3 最小验证配置（排查用）

排查「规则是否真正加载」时，可用极简配置（仓库内亦有 `wechat_minimal_test.conf`）：

```ini
[General]
bypass-system = true
skip-proxy = 192.168.0.0/16, 10.0.0.0/8, 172.16.0.0/12, localhost, *.local
dns-server = system
ipv6 = false

[Rule]
DOMAIN-SUFFIX,weixin.qq.com,PROXY
DOMAIN-SUFFIX,weixin.qq.com.cn,PROXY
IP-CIDR,101.226.142.0/24,PROXY
FINAL,PROXY
```

若此文件已是黄点，日志里仍出现 `qq.com,DIRECT` / `GEOIP,CN,DIRECT`，说明 VPN 扩展未加载该文件（未「使用配置」或未重连）。

---

## 4. 场景（Scene）怎么配

目标：连上「公司 Wi‑Fi」自动使用 `company_proxy.conf`；其它网络用日常配置。

### 4.1 操作步骤

1. 导入 `home.conf`、`company_proxy.conf`
2. 分别点击 → **使用配置**，确认两份都能单独工作
3. 首页 → **全局路由** → **场景**
4. **添加场景**，例如：

| 项 | 填写示例 |
|----|----------|
| 名称 | 公司 Wi‑Fi |
| 网络 | Wi‑Fi，SSID = 公司热点名（须与系统显示完全一致） |
| 路由 | **配置** |
| 配置 | `company_proxy.conf` |
| 类型 | 节点或分组（选可用代理） |

5. （可选）再添加「家里 Wi‑Fi / 蜂窝」场景，指向 `home.conf`
6. 未命中任何场景时，回落到**黄点默认配置**——请把日常那份设为黄点

### 4.2 逻辑示意

```text
全局路由 = 场景
    │
    ├─ 匹配「公司 Wi‑Fi」 → company_proxy.conf + 指定节点
    ├─ 匹配「家里 Wi‑Fi」 → home.conf
    └─ 未匹配           → 黄点默认配置
```

是**整份配置切换**，不是 `default.conf` 与场景 conf 叠加。

### 4.3 验证清单

1. 连公司 Wi‑Fi，确认场景已切换（名称/配置正确）
2. 清空连接日志后打开微信
3. 期望看到类似：
   - `DOMAIN-SUFFIX,weixin.qq.com,PROXY`
   - `IP-CIDR,...,PROXY`
4. 不应再看到（在公司场景下）：
   - `DOMAIN-SUFFIX,qq.com,DIRECT`（若公司 conf 未写这条）
5. 切回家里网络，应回到日常分流

---

## 5. 微信走代理时的常见坑

| 现象 | 原因 | 处理 |
|------|------|------|
| 域名测试走 PROXY，微信仍连不上 | 长连按纯 IP 连接，域名规则未覆盖 | 补 `IP-CIDR`，放在 `GEOIP` 前 |
| 日志 `DOMAIN-SUFFIX,qq.com,DIRECT` | 宽规则或默认配置抢先 | 删/改 `qq.com,DIRECT`，或换掉黄点配置 |
| 日志 `GEOIP,CN,DIRECT`，改文件无效 | 黄点仍是旧配置，或未编译/未重连 | 「使用配置」+ 黄点 + 重连 VPN |
| `IP-ASN,132203` 不生效 | 国内微信 IP 常属运营商 ASN | 用日志里的 IP 写 `IP-CIDR` |
| 只打勾不生效 | 未成为默认编译配置 | 必须「使用配置」出现黄点 |
| 全局代理可用、规则模式不行 | 规则漏拦或被 DIRECT | 按日志逐条补 PROXY 规则 |

排查顺序建议：

1. 全局路由先切 **代理**：微信若恢复 → 节点正常，问题在规则  
2. 再切 **配置** + 最小微信 conf + 黄点  
3. 看新日志命中的规则名，按命中结果补规则  
4. 最后再接到场景上

---

## 6. 改规则后的标准操作

每次修改纯文本后：

1. 保存
2. 配置文件 → **使用配置** 或 **编译配置**
3. 确认黄点在目标文件上
4. 断开 VPN → 再连接
5. 清空日志 → 复现 → 核对命中规则

若使用远程订阅配置：**更新配置**可能覆盖本地修改，公司专用规则建议用**本地 conf**，不要只改可自动更新的远程文件。

---

## 7. 相关文件

本仓库中可参考：

- `wechat_minimal_test.conf`：最小微信代理验证配置
- `wechat_default_proxy.conf`：在完整分流里前置微信 PROXY 的示例（使用前务必「使用配置」并确认黄点）

---

## 8. 一句话总结

- **黄点**才是 VPN 真正加载的配置；勾选不够。  
- **场景**按 Wi‑Fi 切换整份 conf，不与 `default.conf` 叠加。  
- **微信**既要域名规则，也要 `IP-CIDR`；且不能被 `DOMAIN-SUFFIX,qq.com,DIRECT` / 过早的 `GEOIP,CN,DIRECT` 抢走。
