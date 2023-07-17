# SQL分页操作

当查询的数据量很大的时候，不管查询效率或者考虑用户端的显示，都应该考虑分页查询。

# All in All
* 分页查询的实现是使用限定`LIMIT`数据量(即页大小)及偏移`OFFSET`（即页数）从结果集中截取一段数据，利用一段一段的数据实现分页效果。

* 随着偏移量`OFFSET`的增加,需要查询的数据量也增加，数据量大的话会导致查询时间变长, 偏移大于10万以后，查询时间就会急剧增加。

* 总页数是先查询记录总数，然后使用公式(除以页大小）而得到。

* 数据量大使用COUNT(*) 会影响查询速度，数据量大需要考虑使用缓存或其他优化技术。

* `OFFSET`超过了数据库的最大数量并不会报错，而是得到一个空的结果集。


### 分页

一般使用`LIMIT`加`OFFSET`实现，如：

`Select id FROM orders ORDER BY date ASC LIMIT 50 OFFSET 0;`

取的是0到49的数据，即第一页的数据。

`Select id FROM orders ORDER BY date ASC LIMIT 50 OFFSET 50;`

取的是50到99的数据，即第二页的数据, 以此类推...., 方法上也可以写成：

`SELECT * FROM table LIMIT [offset,] rows | rows OFFSET offset`

如：

`select * from orders_history where type=8 limit 1000,10;`

该条语句将会从表 orders_history 中查询第1000条数据之后的10条数据，也就是第1001条到第1010条数据。
数据表中的记录默认使用主键（一般为id）排序，上面的结果相当于：

```
select * from orders_history where type=8 order by id limit 10000,10;
```

* limit后的第一个参数是偏移量offset
* limit后的第二个参数是大小限制limit
* limit后如果只有一个参数则表示的是大小限制limit
* 初始记录行的偏移量是0(而不是 1)

### 总页数
使用下面得到总记录数：

`SELECT COUNT(*) FROM table_name;`

然后使用总数除以页大小得到总页数。

### 优化

在使用上面方法分页查询时，因为使用`limit`加`offset`,并不跳过offset行，而是取offset+N行，然后返回放弃前offset行，返回N行，那当offset特别大的时候，效率就非常的低下，要么控制返回的总页数，要么对超过特定阈值的页数进行SQL改写。

#### 基于主键ID实现查询优化分页查询优化

使用此方法的前提是主键需是自增长的，即满足直接跳过`offset`前的条件，如：

`select id,name from movie where id>100000 limit 10;`

这里就可以直接跳过前100000个数据，直接取100000到100009的数据。

更多示例：

`select * from big_table where id > (select id from big_table where data_type in (1,2) limit 1000000,1) limit 10;`

`select * from big_table a inner join (select id from big_table where data_type in (1,2) limit 1000000,10) b on a.id = b.id; ##耗时：0.69s`

```
select * from orders_history where type=8 order by id limit 10000,10;
```

### 关于count的优化

* 建立缓存
* 对大表的分页的操作
* 避免总数的查询, 即显示用户关心的几页数据，用`上一页`,`下一页`表表示
* 估算总结果数, 用户可以接受不精确的总数


#### Sources
 
[mysql千万级分页查询SQL优化](https://www.cnblogs.com/lingyejun/p/16181378.html)
 
[MySQL分页查询方法及优化](https://www.w3cschool.cn/mysql/mysql-xilz2oy6.html)
 
[分页查询](https://www.liaoxuefeng.com/wiki/1177760294764384/1217864791925600)

[mysql 分页 总数](https://juejin.cn/s/mysql%20分页%20总数)

[大意了，1次亿级数据分页优化搞了半夜！](https://www.51cto.com/article/650144.html)