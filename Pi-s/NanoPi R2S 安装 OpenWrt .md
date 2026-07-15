# NanoPi R2S 安装 OpenWrt 

NanoPi R2S 安装 OpenWrt 很简单：**把镜像写入 microSD 卡，插卡上电即可从 TF 卡启动**。R2S 没有板载 eMMC，系统通常就跑在 SD 卡上。

---

## 安装前准备

### 硬件

| 项目 | 要求 |
|------|------|
| 设备 | **NanoPi R2S**（Rockchip RK3328，1GB RAM，双千兆网口） |
| 存储 | microSD 卡 ≥ 8GB（建议 16GB+，Class 10 / A1） |
| 电源 | 5V/2A USB Type-C |
| 读卡器 | 用于写卡 |

> **注意区分 R2S 和 R2C**：网口芯片不同，镜像不能混用。请确认板子上写的是 **R2S**。

### 选哪个镜像

| 镜像 | 适合谁 | 下载 |
|------|--------|------|
| **官方 OpenWrt**（推荐） | 想要纯净系统、自己配置 | [OpenWrt 固件选择器](https://firmware-selector.openwrt.org/?target=rockchip/armv8&id=friendlyarm_nanopi-r2s) |
| **FriendlyWrt** | 新手、想少折腾，自带一些优化 | [FriendlyELEC 下载页](http://download.friendlyelec.com/NanoPiR2S) → `01_Official images/01_SD card images` |

官方 OpenWrt 24.10.2 直接下载链接：

```
https://downloads.openwrt.org/releases/24.10.2/targets/rockchip/armv8/openwrt-24.10.2-rockchip-armv8-friendlyarm_nanopi-r2s-squashfs-sysupgrade.img.gz
```

```
https://downloads.openwrt.org/releases/25.12.5/targets/rockchip/armv8/openwrt-25.12.5-rockchip-armv8-friendlyarm_nanopi-r2s-squashfs-sysupgrade.img.gz
```


FriendlyWrt 文件名类似：

```
rk3328-sd-friendlywrt-24.10-YYYYMMDD.img.gz
```

---

## 安装步骤（SD 卡刷机）

### 第 1 步：下载并解压镜像

`.img.gz` 需要先解压成 `.img`：

**macOS / Linux：**

```bash
gunzip openwrt-*-friendlyarm_nanopi-r2s-squashfs-sysupgrade.img.gz
```

**Windows：** 用 7-Zip 解压。

### 第 2 步：写入 SD 卡

**方法一：Balena Etcher（推荐，macOS / Windows / Linux 都行）**

1. 打开 [Balena Etcher](https://etcher.balena.io/)
2. 选择解压后的 `.img` 文件
3. 选择 SD 卡（别选错盘）
4. 点击 Flash

**方法二：macOS 命令行**

```bash
# 查看 SD 卡设备名（例如 /dev/disk4）
diskutil list

# 卸载 SD 卡（把 disk4 换成你的设备）
diskutil unmountDisk /dev/disk4

# 写入镜像（把 rdisk4 换成你的设备，rdisk 更快）
sudo dd if=openwrt-24.10.2-rockchip-armv8-friendlyarm_nanopi-r2s-squashfs-sysupgrade.img of=/dev/rdisk4 bs=4m status=progress

# 弹出
diskutil eject /dev/disk4
```

**方法三：Linux**

```bash
# 确认 SD 卡设备，例如 /dev/sdb
lsblk

sudo dd if=openwrt-*.img of=/dev/sdb bs=4M status=progress conv=fsync
```

### 第 3 步：插卡上电

1. SD 卡插入 R2S 的 TF 卡槽
2. 用 Type-C 接 5V/2A 电源
3. 等 1～2 分钟完成首次启动

---

## 首次登录与网络接线

### 网口说明（OpenWrt 默认）

| 接口 | 物理口 | 默认配置 |
|------|--------|----------|
| **eth0** | WAN 口 | DHCP 自动获取 IP |
| **eth1** | LAN 口 | 静态 `192.168.1.1` |

接线方式：

```
光猫/上级路由 ──► WAN 口 (eth0)
                    NanoPi R2S
你的电脑 ────────► LAN 口 (eth1)
```

若不确定哪个是 WAN/LAN，看外壳或 PCB 丝印；也可以两个口都试一下，能访问 `192.168.1.1` 的那个就是 LAN。

### 登录管理界面

电脑网卡设为 **自动获取 IP**（DHCP），浏览器访问：

```
http://192.168.1.1
```

| 系统 | 默认账号 | 默认密码 |
|------|----------|----------|
| 官方 OpenWrt | `root` | **无密码**（首次登录会要求设置） |
| FriendlyWrt | `root` | `password`（部分版本为空） |

FriendlyWrt **首次启动**会做分区扩展和初始化，需等 **2～3 分钟**，终端提示变成 `root@FriendlyWrt` 后再配置。

SSH 登录：

```bash
ssh root@192.168.1.1
```

---

## 基础网络配置

登录 LuCI 后，按你的上网方式配置 WAN：

### 光猫拨号（PPPoE）

**Network → Interfaces → WAN → Edit**

- Protocol：`PPPoE`
- Username / Password：填宽带账号密码

### 上级路由 DHCP（最常见）

默认就是 DHCP，WAN 接上级路由即可，一般不用改。

### 修改 LAN IP（避免和现有路由冲突）

**Network → Interfaces → LAN → Edit**

- 例如改成 `192.168.2.1`，保存并应用。

---

## 系统升级

以后升级 OpenWrt，在 LuCI 里：

**System → Backup / Flash Firmware → Flash new firmware image**

上传对应版本的 `*-sysupgrade.img.gz`（**不用解压**），等待重启即可。

---

## 常见问题

| 问题 | 原因 / 处理 |
|------|-------------|
| 启动后 LAN 灯不亮 | 检查 SD 卡是否插好、镜像是否写成功 |
| 访问不了 192.168.1.1 | 确认电脑接的是 LAN 口；关闭电脑 VPN |
| 首次启动很慢 | FriendlyWrt 在扩展分区，等 2～3 分钟 |
| WAN 无 IP | 检查 WAN 接线；上级路由是否开启 DHCP |
| 买成 R2C | R2C 要用 `friendlyarm_nanopi-r2c` 镜像，不能刷 R2S 的 |
| SD 卡损坏 | 换高质量卡重刷；长期运行建议买高 endurance 卡 |

### 恢复出厂 / Failsafe

- LuCI：**System → Backup / Flash Firmware → Perform reset**
- 或 SSH：`firstboot -y && reboot`

---

## 推荐安装路径

```
第一次玩 OpenWrt？
  → FriendlyWrt（少踩坑，Web 界面友好）

想要干净、可控的系统？
  → 官方 OpenWrt 24.10.x

装完要做 VPN 网关？
  → 继续参考你项目里的 NanoPi上配置VPN网关.md
```

---

## 快速命令清单

```bash
# 1. 下载官方镜像（macOS）
curl -LO https://downloads.openwrt.org/releases/24.10.2/targets/rockchip/armv8/openwrt-24.10.2-rockchip-armv8-friendlyarm_nanopi-r2s-squashfs-sysupgrade.img.gz

or  25.12.5 的版本

curl -LO https://downloads.openwrt.org/releases/25.12.5/targets/rockchip/armv8/openwrt-25.12.5-rockchip-armv8-friendlyarm_nanopi-r2s-squashfs-sysupgrade.img.gz

# 2. 解压
gunzip openwrt-*.img.gz

# 3. 写卡（替换 disk4 为你的 SD 卡）
diskutil unmountDisk /dev/disk4
sudo dd if=openwrt-*.img of=/dev/rdisk4 bs=4m status=progress
diskutil eject /dev/disk4

# 4. 插卡上电 → 浏览器打开 http://192.168.1.1
```

如果你希望，我可以把这份内容也整理成 `NanoPi R2S 安装OpenWrt.md`，和你现有的 VPN 网关文档放在一起。