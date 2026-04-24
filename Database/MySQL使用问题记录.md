# MySQL使用问题记录

#### 1. mysql如何复制一整个表，并命名为新的表名？

MySQL 复制整张表常用有 3 种，按你需求选：

- 只复制结构（字段、索引），不复制数据  
`CREATE TABLE new_table LIKE old_table;`

- 复制结构 + 数据（快速）  
`CREATE TABLE new_table AS SELECT * FROM old_table;`  
（注意：这种方式通常不会完整保留索引、主键、自增、触发器等）

- 推荐的“完整复制”流程（先结构后数据）  
```sql
CREATE TABLE new_table LIKE old_table;
INSERT INTO new_table SELECT * FROM old_table;
```

补充：

- 触发器不会随 `LIKE` 自动复制，需单独创建。
- 外键约束在不同版本/场景下行为可能不完全一致，建议 `SHOW CREATE TABLE old_table;` 对比确认。
- 如果只想改名，不是复制，用：`RENAME TABLE old_table TO new_table;`