# MySQL数据迁移


## mysqldump 的使用

### 一、mysqldump的安装

* Debian/Ubuntu系统安装

	```
	# 更新软件包列表
	sudo apt update
	
	# 安装MySQL客户端（包含mysqldump）
	sudo apt install mysql-client
	```

* Red Hat/CentOS系统安装

	```
	# 使用yum安装（较旧版本）
	sudo yum install mysql
	
	# 或使用dnf安装（较新版本）
	sudo dnf install mysql
	```

* 安装完成后，通过版本查询命令验证是否成功：

	```
	# 显示mysqldump版本信息
	mysqldump --version
	```

### 二、mysqldump相关指令

```
- 导出数据库
mysqldump -u username -p database_name > backup. sql

- 导入到目标数据库
mysql -u username -p target_database < backup.sql

- 导出所有数据库
mysqldump -u username -p --all-databases > all_databases.sql

- 只导出表结构（不含数据）
mysqldump -u username -p --no-data database_name > structure.sql
```

 mysqldump 导出的是数据库的数据内容，不包括：


* ❌ MySQL 用户账号
* ❌ 用户密码
* ❌ 权限信息

这些信息存储在 MySQL 系统数据库 mysql 中（特别是 mysql.user 表）。

如果需要迁移用户和权限：

- 单独导出用户和权限

`mysqldump -u root -p mysql user db tables_priv columns_priv > users_privileges.sql`

- 或者导出所有系统库

`mysqldump -u root -p --all-databases > all_including_users.sql`

### 使用mysqldump备份数据库

```
1. 备份目标数据库的现有数据
mysqldump -u root -p target_database > target_backup_$(date +%Y%m%d).sql

2. 再导入新数据
mysql -u root -p target_database < source_backup.sql
```

### 导出数据


#### 只导出表数据（不含结构）


 导出单个表的数据（不含 CREATE TABLE 语句）:
`mysqldump -u root -p --no-create-info database_name table_name > table_data_only.sql`

如果有多个表:
`mysqldump -u root -p --no-create-info database_name table1 table2 table3 > tables_data. sql`

导出为 CSV 格式（更灵活）:
`mysqldump -u root -p --no-create-info --tab=/tmp --fields-terminated-by=',' database_name table_name`

### 导入数据

直接导入（表已存在）
mysql -u root -p database_name < table_data_only.sql

临时禁用约束以加快导入

```
mysql -u root -p database_name << EOF
SET FOREIGN_KEY_CHECKS=0;
SET UNIQUE_CHECKS=0;
SET AUTOCOMMIT=0;
SOURCE table_data_only.sql;
COMMIT;
SET FOREIGN_KEY_CHECKS=1;
SET UNIQUE_CHECKS=1;
EOF
```