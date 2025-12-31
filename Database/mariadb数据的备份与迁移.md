# mariadb数据的备份与迁移



### 场景一：导出及导入单个（多个）数据表的数据

导出：
`mariadb-dump -h 127.0.0.1 -u root -p --no-create-info your_database your_table > your_table_only_data.sql`

如果是多个表：
`mariadb-dump -h 127.0.0.1 -u root -p --no-create-info your_database your_table1 your_table2 your_table3 > your_table_only_data.sql`

导入数据：
`mariadb -h 127.0.0.1 -u root -p your_database < your_table_only_data.sql`


### 场景二：整个数据库的导出及导入




## 安装及常用使用指令见如下


## mariadb-dump 的使用

### mariadb-dump的安装

* Ubuntu/Debian 系统

	```
	# 更新软件包列表
	sudo apt update
	
	# 安装 MariaDB 客户端工具（包含 mariadb-dump）
	sudo apt install mariadb-client
	
	# 或者安装完整版（如果需要）
	sudo apt install mariadb-client-core-10.6
	```

* CentOS/RHEL/Rocky Linux 系统

	```
	# CentOS 8 / Rocky Linux / RHEL 8+
	sudo dnf install mariadb
	
	# CentOS 7 / RHEL 7
	sudo yum install mariadb
	```

	或者安装 MariaDB 官方仓库

	```
	# 添加 MariaDB 官方仓库
	sudo curl -LsS https://r.mariadb.com/downloads/mariadb_repo_setup | sudo bash
	
	# 安装客户端
	sudo dnf install MariaDB-client
	# 或
	sudo yum install MariaDB-client
	```

* 验证安装

`mariadb-dump --version`




我来为你详细介绍 `mariadb-dump`（也叫 `mysqldump`）的使用方法。

## MariaDB-Dump 基础介绍

`mariadb-dump` 是 MariaDB/MySQL 的逻辑备份工具，它通过 SQL 语句导出数据库结构和数据。

---

## 一、数据备份

### 1. 备份单个数据库
```bash
mariadb-dump -u username -p database_name > backup. sql
```

### 2. 备份多个数据库
```bash
mariadb-dump -u username -p --databases db1 db2 db3 > backup.sql
```

### 3. 备份所有数据库
```bash
mariadb-dump -u username -p --all-databases > all_backup.sql
```

### 4. 只备份数据库结构（不含数据）
```bash
mariadb-dump -u username -p --no-data database_name > structure. sql
```

### 5. 只备份数据（不含结构）
```bash
mariadb-dump -u username -p --no-create-info database_name > data.sql
```

### 6. 备份指定表
```bash
mariadb-dump -u username -p database_name table1 table2 > tables_backup.sql
```

### 7. 压缩备份（节省空间）
```bash
mariadb-dump -u username -p database_name | gzip > backup.sql.gz
```

---

## 二、数据恢复

### 1. 恢复整个数据库
```bash
mariadb -u username -p database_name < backup.sql
```

### 2. 恢复压缩备份
```bash
gunzip < backup.sql.gz | mariadb -u username -p database_name
```

### 3. 恢复所有数据库
```bash
mariadb -u username -p < all_backup.sql
```

### 4. 在 MariaDB 命令行内恢复
```sql
MariaDB [(none)]> USE database_name;
MariaDB [database_name]> SOURCE /path/to/backup.sql;
```

---

## 三、常用选项说明

| 选项 | 说明 |
|------|------|
| `-u, --user` | 指定用户名 |
| `-p, --password` | 提示输入密码 |
| `-h, --host` | 指定主机地址（默认 localhost） |
| `-P, --port` | 指定端口号（默认 3306） |
| `--single-transaction` | 对 InnoDB 表使用一致性读取（推荐） |
| `--lock-tables` | 锁定所有表（MyISAM 推荐） |
| `--quick` | 快速导出，不缓存查询结果 |
| `--add-drop-database` | 在 CREATE DATABASE 前添加 DROP DATABASE |
| `--add-drop-table` | 在 CREATE TABLE 前添加 DROP TABLE |
| `--complete-insert` | 使用完整的 INSERT 语句 |
| `--routines` | 备份存储过程和函数 |
| `--triggers` | 备份触发器（默认开启） |
| `--events` | 备份事件调度器 |

---

## 四、实用备份脚本示例

### 1. 完整备份脚本
```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backup/mariadb"
DB_USER="root"
DB_NAME="mydb"

mkdir -p $BACKUP_DIR

mariadb-dump -u $DB_USER -p \
    --single-transaction \
    --routines \
    --triggers \
    --events \
    $DB_NAME | gzip > $BACKUP_DIR/${DB_NAME}_${DATE}.sql.gz

# 保留最近7天的备份
find $BACKUP_DIR -name "*.sql.gz" -mtime +7 -delete

echo "Backup completed: ${DB_NAME}_${DATE}.sql. gz"
```

### 2. 远程备份
```bash
mariadb-dump -h remote_host -P 3306 -u username -p database_name > remote_backup.sql
```

---

## 五、数据导入导出（其他方式）

### 直接导入（如表已存在）
mysql -u root -p database_name < table_data_only.sql

### 1. 使用 SELECT INTO OUTFILE 导出
```sql
SELECT * FROM table_name 
INTO OUTFILE '/tmp/output.csv'
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n';
```

### 2. 使用 LOAD DATA INFILE 导入
```sql
LOAD DATA INFILE '/tmp/output.csv'
INTO TABLE table_name
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';
```

### 3. 使用 mariadb-import 命令
```bash
mariadb-import -u username -p database_name datafile.txt
```

---

## 六、最佳实践建议

1. **使用 `--single-transaction`**：对 InnoDB 表进行无锁一致性备份
2. **定期自动化备份**：使用 cron 定时任务
3. **异地存储**：将备份文件传输到其他服务器
4. **测试恢复**：定期验证备份文件可用性
5. **压缩备份**：节省磁盘空间
6. **记录日志**：备份过程记录到日志文件

### Cron 定时备份示例
```bash
# 每天凌晨2点执行备份
0 2 * * * /usr/local/bin/backup.sh >> /var/log/mariadb_backup.log 2>&1
```

---

## 七、常见问题

**Q: 备份大数据库时内存不足？**  
A: 使用 `--quick` 选项，避免缓存整个结果集

**Q: 备份时锁表影响业务？**  
A: 对 InnoDB 使用 `--single-transaction`，避免锁表

**Q:  如何备份存储过程和触发器？**  
A:  添加 `--routines` 和 `--triggers` 选项

需要针对特定场景的详细配置吗？



