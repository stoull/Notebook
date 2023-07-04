# SQLite 数据库

平生建的第一张表：

```
CREATE TABLE System(
   ...> id INT NOT NULL AUTO_INCREMENT,
   ...> date DATETIME NOT NULL,
   ...> core_frequency LONG,
   ...> cpu_temp FLOAT,
   ...> gpu_temp FLOAT,
   ...> cpu_rate FLOAT,
   ...> memory_rate FLOAT,
   ...> fan_rate FLOAT,
   ...> count INTEGER,
   ...> sys_run_time VARCHAR(25),
   ...> note TEXT,
   ...> isRead BOOLEAN,
   ...> PRIMARY KEY (id)
   ...> );
```

### 查看创建的表的column名称

列出表中的column名称
`PRAGMA table_info(your_tablename);`

列出数据库中的所有表名

`. tables `

列出your_tablename表中的column名称

`.schema your_tablename`

也可以使用 `.headers ON` 查出的结果中会包括column名称

### 从DATETIME中过滤 date 信息进行查询

```
select * from test 
where date between '2021-10-22' and '2021-10-22 23:59:59'
```

```
select * from test 
where datediff(day, date, '2021-10-22') = 0
```