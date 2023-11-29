# smartmontools 查看SSD状态


smartmontools只支持本地磁盘的SMART状态显示，对于USB移动硬盘，不支持。

对于USB移动硬盘需要安装插件：

* [GitHub - OS-X-SAT-SMART-Driver](https://github.com/kasbert/OS-X-SAT-SMART-Driver)
* 或者已打包好的：[External USB / FireWire drive diagnostics support](https://binaryfruit.com/drivedx/usb-drive-support)


# 安装

* `brew install smartmontools` - Mac
* `yum -y install smartmontools` - CentOS
* `sudo apt install smartmontools` -  Ubuntu

查看： `smartctl --all /dev/disk0`

在查看磁盘信息前，需要要知道磁盘的IDENTIFIER, 即标签, 使用：`sudo diskutil list`

```
$sudo diskutil list
$Password:
/dev/disk0 (internal, physical):
   #:                       TYPE NAME                    SIZE       IDENTIFIER
   0:      GUID_partition_scheme                        *1.0 TB     disk0
   1:                        EFI EFI                     209.7 MB   disk0s1
   2:                 Apple_APFS Container disk1         1000.0 GB  disk0s2
```

或者使用`ls -l /dev | grep -E 'disk'`:
```
ls -l /dev | grep 'disk' 
brw-r-----  1 root   operator        0x1000000 Nov 29 09:00 disk0
brw-r-----  1 root   operator        0x1000001 Nov 29 09:00 disk0s1
brw-r-----  1 root   operator        0x1000002 Nov 29 09:00 disk0s2
br--r-----  1 root   wheel           0x100000d Nov 29 09:09 disk2
br--r-----  1 root   wheel           0x100000e Nov 29 09:09 disk2s1
br--r-----  1 root   wheel           0x100000f Nov 29 09:09 disk3
br--r-----  1 root   wheel           0x1000010 Nov 29 09:09 disk3s1
crw-r-----  1 root   operator        0x1000000 Nov 29 09:00 rdisk0
```
### `smartctl --info /dev/disk0s1 `
```
smartctl --info /dev/disk0s1
smartctl 7.4 2023-08-01 r5530 [Darwin 22.6.0 x86_64] (local build)
Copyright (C) 2002-23, Bruce Allen, Christian Franke, www.smartmontools.org

=== START OF INFORMATION SECTION ===
Model Family:     Samsung based SSDs
Device Model:     Samsung SSD 860 EVO 1TB
Serial Number:    S4CTNS0NC01135X
LU WWN Device Id: 5 002538 e30c161b9
Firmware Version: RVT04B6Q
User Capacity:    1,000,204,886,016 bytes [1.00 TB]
Sector Size:      512 bytes logical/physical
Rotation Rate:    Solid State Device
Form Factor:      2.5 inches
TRIM Command:     Available, deterministic, zeroed
Device is:        In smartctl database 7.3/5528
ATA Version is:   ACS-4 T13/BSR INCITS 529 revision 5
SATA Version is:  SATA 3.2, 6.0 Gb/s (current: 6.0 Gb/s)
Local Time is:    Wed Nov 29 13:02:20 2023 CST
SMART support is: Available - device has SMART capability.
SMART support is: Enabled
```
### `smartctl -s on -a /dev/disk0s1`

在这个命令中，"-s on"标志开启指定设备上的SMART功能。如果/dev/sda上已开启SMART支持，那就省略它。

### `smartctl --a /dev/disk0s2 `

查看对应分区`disk0s2`的磁盘所有信息：

```
 % smartctl -a disk0s2
smartctl 7.4 2023-08-01 r5530 [Darwin 22.6.0 x86_64] (local build)
Copyright (C) 2002-23, Bruce Allen, Christian Franke, www.smartmontools.org

=== START OF INFORMATION SECTION ===
Model Family:     Samsung based SSDs
Device Model:     Samsung SSD 860 EVO 1TB
Serial Number:    S4CTNS0NC01135X
LU WWN Device Id: 5 002538 e30c161b9
Firmware Version: RVT04B6Q
User Capacity:    1,000,204,886,016 bytes [1.00 TB]
Sector Size:      512 bytes logical/physical
Rotation Rate:    Solid State Device
Form Factor:      2.5 inches
TRIM Command:     Available, deterministic, zeroed
Device is:        In smartctl database 7.3/5528
ATA Version is:   ACS-4 T13/BSR INCITS 529 revision 5
SATA Version is:  SATA 3.2, 6.0 Gb/s (current: 6.0 Gb/s)
Local Time is:    Wed Nov 29 12:43:36 2023 CST
SMART support is: Available - device has SMART capability.
SMART support is: Enabled

=== START OF READ SMART DATA SECTION ===
SMART overall-health self-assessment test result: PASSED

General SMART Values:
Offline data collection status:  (0x00)	Offline data collection activity
					was never started.
					Auto Offline Data Collection: Disabled.
Self-test execution status:      (   0)	The previous self-test routine completed
					without error or no self-test has ever 
					been run.
Total time to complete Offline 
data collection: 		(    0) seconds.
Offline data collection
capabilities: 			 (0x53) SMART execute Offline immediate.
					Auto Offline data collection on/off support.
					Suspend Offline collection upon new
					command.
					No Offline surface scan supported.
					Self-test supported.
					No Conveyance Self-test supported.
					Selective Self-test supported.
SMART capabilities:            (0x0003)	Saves SMART data before entering
					power-saving mode.
					Supports SMART auto save timer.
Error logging capability:        (0x01)	Error logging supported.
					General Purpose Logging supported.
Short self-test routine 
recommended polling time: 	 (   2) minutes.
Extended self-test routine
recommended polling time: 	 (  85) minutes.
SCT capabilities: 	       (0x003d)	SCT Status supported.
					SCT Error Recovery Control supported.
					SCT Feature Control supported.
					SCT Data Table supported.

SMART Attributes Data Structure revision number: 1
Vendor Specific SMART Attributes with Thresholds:
ID# ATTRIBUTE_NAME          FLAG     VALUE WORST THRESH TYPE      UPDATED  WHEN_FAILED RAW_VALUE
  5 Reallocated_Sector_Ct   0x0033   100   100   010    Pre-fail  Always       -       0
  9 Power_On_Hours          0x0032   096   096   000    Old_age   Always       -       15338
 12 Power_Cycle_Count       0x0032   098   098   000    Old_age   Always       -       1174
177 Wear_Leveling_Count     0x0013   090   090   000    Pre-fail  Always       -       178
179 Used_Rsvd_Blk_Cnt_Tot   0x0013   100   100   010    Pre-fail  Always       -       0
181 Program_Fail_Cnt_Total  0x0032   100   100   010    Old_age   Always       -       0
182 Erase_Fail_Count_Total  0x0032   100   100   010    Old_age   Always       -       0
183 Runtime_Bad_Block       0x0013   100   100   010    Pre-fail  Always       -       0
187 Uncorrectable_Error_Cnt 0x0032   100   100   000    Old_age   Always       -       0
190 Airflow_Temperature_Cel 0x0032   067   044   000    Old_age   Always       -       33
195 ECC_Error_Rate          0x001a   200   200   000    Old_age   Always       -       0
199 CRC_Error_Count         0x003e   100   100   000    Old_age   Always       -       0
235 POR_Recovery_Count      0x0012   099   099   000    Old_age   Always       -       46
241 Total_LBAs_Written      0x0032   099   099   000    Old_age   Always       -       73357941176

SMART Error Log Version: 1
No Errors Logged

SMART Self-test log structure revision number 1
No self-tests have been logged.  [To run self-tests, use: smartctl -t]

SMART Selective self-test log data structure revision number 1
 SPAN  MIN_LBA  MAX_LBA  CURRENT_TEST_STATUS
    1        0        0  Not_testing
    2        0        0  Not_testing
    3        0        0  Not_testing
    4        0        0  Not_testing
    5        0        0  Not_testing
  256        0    65535  Read_scanning was never started
Selective self-test flags (0x0):
  After scanning selected spans, do NOT read-scan remainder of disk.
If Selective self-test is pending on power-up, resume after 0 minute delay.

The above only provides legacy SMART information - try 'smartctl -x' for more
```


[smartmontools-Github](https://github.com/smartmontools/smartmontools)

[使用 smartmontools 查看硬盘的健康状态](https://linux.cn/article-4461-1.html)
