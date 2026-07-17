# 官方 OpenWrt 扩展 SD 卡 overlay 空间

适用：官方 OpenWrt（如 25.12.x）刷在 TF/SD 卡上，**overlay 只有约 100MB、快满了**，但卡实际是 16G/32G 等大容量。

目标：把未使用的 TF 卡空间划进系统分区，让 `/`（可写层）接近整卡可用容量。

---

## 1. 为什么官方 OpenWrt 默认 overlay 很小？

官方镜像（`*-squashfs-sysupgrade.img.gz`）是为 **通用刷机** 设计的，不是按你的 TF 卡容量定制：

| 原因 | 说明 |
|------|------|
| **镜像体积固定** | 下载的 `.img` 里 root 分区只预留很小一块，方便下载、写入、适配各种容量的卡 |
| **只读 + 可写分离** | `/rom` = squashfs 只读固件；`/` = overlay 可写层。默认只给 overlay 预留约 **100MB 级** |
| **不假设卡有多大** | 同一镜像可能写到 4G / 16G / 64G 卡上；不会在刷机时自动「占满整张卡」 |
| **减少写放大风险** | 早期/默认策略偏保守，避免小卡刷大镜像失败 |

对比：

- **官方 OpenWrt**：常需 **手动扩容**（本文）
- **FriendlyWrt**：首次启动常会 **自动扩展** root，占满 TF 卡

所以：卡是 16G，但 `df` 里 `/` 只有约 98M，**不是卡坏了，是分区没用满。**

---

## 2. 先看懂 `df` 和分区（结合真实输出）

### 2.1 典型的「未扩容」`df -h`

```text
Filesystem                Size      Used Available Use% Mounted on
/dev/root                 3.8M      3.8M         0 100% /rom
tmpfs                   492.6M      1.9M    490.7M   0% /tmp
/dev/loop0               98.4M     89.9M      8.6M  91% /overlay
overlayfs:/overlay       98.4M     89.9M      8.6M  91% /
tmpfs                   512.0K         0    512.0K   0% /dev
```

| 挂载点 | 含义 | 要不要慌 |
|--------|------|----------|
| `/rom` 3.8M、100% | 只读固件（squashfs），固定大小 | **正常**，不要当成「卡只有 3.8M」 |
| `/` 与 `/overlay` ≈ 98M、91% | 真正可写空间，装软件、写配置都在这 | **要扩容**；只剩几 MB 时 `apk add` 易失败 |
| `/tmp` | 内存盘，重启清空 | 与 TF 卡容量无关 |

### 2.2 用 `/proc/partitions` 看真实布局（无需 lsblk）

官方精简固件可能没有 `lsblk` / `fdisk`，可用：

```bash
cat /proc/partitions
awk '{printf "%.2f GB\n", $1*512/1024/1024/1024}' /sys/block/mmcblk0/size
ls -l /dev/mmcblk*
```

**示例输出（16G 卡、未扩容）：**

```text
major minor  #blocks  name

   7        0     102848 loop0
 179        0   15360000 mmcblk0
 179        1      16384 mmcblk0p1
 179        2     106496 mmcblk0p2
```

```text
14.65 GB          ← 整卡约 14.65GB（标称 16G，正常）
```

```text
/dev/mmcblk0      ← 整张 TF 卡
/dev/mmcblk0p1    ← 引导分区（约 16MB）
/dev/mmcblk0p2    ← 系统分区（约 104MB）← 太小，后面要扩它
```

换算关系（`#blocks` 单位约为 **1KB**）：

| 设备 | #blocks | 约合 |
|------|---------|------|
| mmcblk0 | 15360000 | ≈ 14.65 GB（整卡） |
| mmcblk0p1 | 16384 | ≈ 16 MB（boot） |
| mmcblk0p2 | 106496 | ≈ 104 MB（root，未扩容） |
| loop0 | 102848 | ≈ 100 MB（overlay 文件系统） |

未使用空间 ≈ `15360000 - 16384 - 106496` ≈ **14.5 GB** 闲置在卡上。

### 2.3 结构示意

```text
TF 卡 mmcblk0（约 14.65 GB）
├── p1  boot          ~16 MB
├── p2  root          ~104 MB   ← 当前只用到这里
│     ├── squashfs → /rom（只读，几 MB）
│     └── f2fs     → /overlay → /（可写，~98 MB，易满）
└── （未分配）        ~14.5 GB  ← 扩容就是把 p2 扩到占满这里
```

---

## 3. 扩容前准备

### 3.1 确认是 SD 卡设备名

多数 R2S 为 `/dev/mmcblk0`。若是 `mmcblk1`，下文全部替换。

```bash
ls -l /dev/mmcblk*
```

### 3.2 备份配置（强烈建议）

```bash
sysupgrade -b /tmp/backup-OpenWrt.tar.gz
```

在电脑上拉走：

```bash
scp root@192.168.1.11:/tmp/backup-OpenWrt.tar.gz ~/Downloads/
```

（把 IP 换成你的 R2S 地址。）

### 3.3 腾出一点空间装工具

overlay 若已 90%+，先清临时文件再 `apk add`：

```bash
rm -rf /tmp/apk* /tmp/opkg-lists 2>/dev/null
df -h /
```

### 3.4 注意

- 扩容过程中 **尽量不要断电、不要强拔卡**
- 只 **扩大** 第 2 分区，**不要删除分区、不要 mkfs 格式化**
- OpenWrt **25.12+** 用 **`apk`**，不是 `opkg`

---

## 4. 操作步骤（照着做）

### 第 1 步：安装工具

```bash
apk update
apk add parted losetup f2fs-tools resize2fs
```

确认命令存在：

```bash
which parted resize.f2fs losetup
```

可选：确认仓库里有 resize 相关包（示例）：

```bash
apk search resize
# 可见：resize2fs-...、fatresize-...、nilfs-resize-... 等
# overlay 为 f2fs 时，关键是 f2fs-tools 里的 resize.f2fs
```

### 第 2 步：确认 overlay / loop 信息

```bash
df -h /
cat /proc/mounts | grep -E 'overlay|loop|f2fs'
cat /sys/block/loop0/loop/backing_file 2>/dev/null
cat /sys/block/loop0/loop/offset 2>/dev/null
```

本指南针对：**`/overlay` 为 f2fs，挂在 `/dev/loop0`**（官方 squashfs 镜像常见情况）。

### 第 3 步：扩大分区 `mmcblk0p2` 到 100%

```bash
parted -s /dev/mmcblk0 resizepart 2 100%
```

检查分区是否变大：

```bash
cat /proc/partitions
```

**扩容前示例：**

```text
 179        2     106496 mmcblk0p2
```

**扩容后期望：** `mmcblk0p2` 的 `#blocks` 变为约 **1500 万** 量级（接近整卡减去 p1），而不再是 `106496`。

若提示设备忙 / 无法 resize：

```bash
parted /dev/mmcblk0 print
reboot
# 重启后再执行：
parted -s /dev/mmcblk0 resizepart 2 100%
cat /proc/partitions
```

### 第 4 步：扩大 f2fs 文件系统

```bash
# 让 loop 重新感知底层分区变大
losetup -c /dev/loop0

# 扩展 f2fs（你的可写层）
resize.f2fs /dev/loop0
```

若 `losetup -c` 或 `resize.f2fs` 报错，可 **先 reboot，再执行这两条**：

```bash
reboot
# SSH 重新登录后：
losetup -c /dev/loop0
resize.f2fs /dev/loop0
```

### 第 5 步：验证

```bash
df -h
cat /proc/partitions
```

**成功标志：**

| 检查项 | 期望 |
|--------|------|
| `/` 或 `/overlay` 的 Size | 从约 **98M** 变为 **十几 GB**（16G 卡） |
| Use% | 从约 91% 降到很低 |
| `mmcblk0p2` 的 #blocks | 远大于原来的 `106496` |

---

## 5. 一键命令清单（复制用）

确认设备是 `mmcblk0`、overlay 是 f2fs/loop0 后，可按序执行：

```bash
# --- 备份 ---
sysupgrade -b /tmp/backup-OpenWrt.tar.gz
# 再用电脑 scp 拷走

# --- 工具 ---
apk update
apk add parted losetup f2fs-tools resize2fs

# --- 扩分区 ---
parted -s /dev/mmcblk0 resizepart 2 100%
cat /proc/partitions

# --- 扩文件系统 ---
losetup -c /dev/loop0
resize.f2fs /dev/loop0

# --- 检查 ---
df -h
```

---

## 6. 常见问题

### Q1：`/rom` 一直是 3.8M、100%，扩容后还这样？

正常。`/rom` 永远是只读固件大小，**不会**变成 16G。看 **`/`（overlay）** 即可。

### Q2：没有 `lsblk` / `fdisk`？

正常。精简固件常不带。用：

```bash
cat /proc/partitions
awk '{printf "%.2f GB\n", $1*512/1024/1024/1024}' /sys/block/mmcblk0/size
```

需要时再：`apk add lsblk fdisk`。

### Q3：`apk add` 提示空间不足？

先：

```bash
rm -rf /tmp/*
df -h /
```

仍不够时，用电脑从备份恢复到另一张已扩容的卡，或临时删掉不急需的已装包（慎用）。

### Q4：`resize.f2fs` 失败？

1. 确认第 3 步后 `mmcblk0p2` 已经变大  
2. `reboot` 后再 `losetup -c` + `resize.f2fs`  
3. 确认是 f2fs：`mount | grep overlay`  
4. 若是 ext4（少见），改用：`resize2fs /dev/loop0`

### Q5：FriendlyWrt 也要这样做吗？

多数 FriendlyWrt **首次启动会自动扩满**，一般不必再做。本指南主要针对 **官方 OpenWrt**。

### Q6：扩容会影响 Tailscale / 旁路由配置吗？

一般不会丢配置（只扩分区和文件系统）。但仍建议先 `sysupgrade -b` 备份。

---

## 7. 扩容后建议

```bash
df -h /
apk update
# 再按需安装软件，例如：
# apk add luci-app-xxx
```

可写空间充足后，再装工具、跑服务更稳妥。

---

## 8. 相关文档

- `OpenWRT+Tailscale问题及要点记录.md` — 旁路由与 Tailscale 要点  
- `NanoPi上配置VPN网关.md` — VPN 网关配置  

---

> 环境示例：NanoPi R2S · OpenWrt 25.12.5 · 标称 16G TF（识别约 14.65GB）· squashfs + f2fs overlay  
> 扩容前：`mmcblk0p2` ≈ 104MB，`/` ≈ 98MB、Use% 91%  
> 包管理：使用 **apk**（非 opkg）
