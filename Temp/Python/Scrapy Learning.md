# scrapy learning




[News and notifications](https://www.immigration.govt.nz/about-us/media-centre/news-notifications)

response.xpath("//a[@class='listing_link outer-link']/span[@class='sr-only']/text()").extract()



## scrapy shell
Using command `scrapy shell` to Interactive scraping console.
Always using `scrapy --help` to check command.

Try this to understand how to use scrapy shell:

>

```

scrapy shell

fetch ("https://www.immigration.govt.nz/about-us/media-centre/news-notifications")

response.xpath("//a[@class='listing_link outer-link']/span[@class='sr-only']/text()").extract()
```
在浏览器里查看抓取的内容

`view(response)`

在终端打印抓取的内容的文本

`print(response.text)`


Using CSS Selectors for Extraction
`response.css(".product::text").extract_first()`

使用树径(XPath)提取所需文本
``
### 示例
如保抓取[W3CScholl SQL Tryit Editor 中的Database](https://www.w3schools.com/sql/trysql.asp?filename=trysql_select_all)

#### **遇到的问题**
1. [SQL Tryit Editor](https://www.w3schools.com/sql/trysql.asp?filename=trysql_select_all) 这个页面中有一个button. 只有点击button数据才会显示出来，这里怎么做？！！！



## Start a project

生成一个Scrapy项目
Using this command `scrapy startproject your_project_name` under the directory, which your like, to create a new project



参考资料：

[Scrapy Offical Tutorial](https://docs.scrapy.org/en/latest/intro/tutorial.html)

[Making Web Crawlers Using Scrapy for Python](https://www.datacamp.com/community/tutorials/making-web-crawlers-scrapy-python)