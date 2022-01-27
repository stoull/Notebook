# scrapy learning


[官方 Scrapy Tutorial](https://docs.scrapy.org/en/latest/intro/tutorial.html)

[News and notifications](https://www.immigration.govt.nz/about-us/media-centre/news-notifications)

response.xpath("//a[@class='listing_link outer-link']/span[@class='sr-only']/text()").extract()

## 安装scrapy

`pip install Scrapy`

或使用虚拟环境:
>`python3 -m venv /path/to/new/virtual/environment`
>`source /path/to/new/virtual/environment/bin/activate`
>`pip install Scrapy`


## 开始一个Scrapy项目


### 生成一个Scrapy项目
Using this command `scrapy startproject your_project_name` under the directory, which your like, to create a new project

### 新建一个spider
会生一些自动生成的文件，先不管这些文件。在自动生成的`spiders`目录下新建一个`My-spider.py`文件，并使用如下代码：

```
import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'quotes-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')
```
### 运行spider
在项目的根目录运行 `scrapy crawl quotes`, 既可以对网页`http://quotes.toscrape.com/page/1/`进行抓取

这样会在根目录生成`quotes-1.html`,`quotes-2.html`两个文件。

## 调试及分析工具 scrapy shell

Using command `scrapy shell` to Interactive scraping console.
Always using `scrapy --help` to check command.

Try this to understand how to use scrapy shell:

>

```

scrapy shell

fetch("https://movie.douban.com/subject/1291843/")

response.xpath("//a[@class='listing_link outer-link']/span[@class='sr-only']/text()").extract()
```

有时候遇到`robots.txt`会出现403的错误，这个时候要给请求加上可通过的`USER_AGENT`

> `scrapy shell -s USER_AGENT='custom user agent' 'http://www.example.com'`

如：

> `scrapy shell -s USER_AGENT='Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko' 'https://movie.douban.com'`

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




参考资料：

[Scrapy Offical Tutorial](https://docs.scrapy.org/en/latest/intro/tutorial.html)

[Making Web Crawlers Using Scrapy for Python](https://www.datacamp.com/community/tutorials/making-web-crawlers-scrapy-python)