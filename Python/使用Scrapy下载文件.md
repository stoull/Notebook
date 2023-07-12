# 使用Scrapy下载文件


## 安装Scrapy并创建工程

#### 安装python虚拟环境：
`python -m venv /path/to/new/virtual/environment`
或者：
`virtualenv venv`

#### 激活虚拟环境
`source /path/to/new/virtual/environment/bin/activate`

### 安装Scrapy
`pip install scrapy` 会将安装Scrapy package 

### 创建scrapy工程

`scrapy startproject FileDownload` : scrapy 会创建一个名为`FileDownload`工程文件夹，并生成对应的初始项目文件，可进入对应的文件夹查看。

命令输出如下：

```
$ scrapy startproject FileDownload
New Scrapy project 'FileDownload', using template directory '/Users/kevin/Documents/hut_space/python_projects/venv/lib/python3.9/site-packages/scrapy/templates/project', created in:
    /Users/kevin/Documents/hut_space/python_projects/projects/FileDownload

You can start your first spider with:
    cd FileDownload
    scrapy genspider example example.com
```

### scrapy模板

```
  $scrapy genspider -l
Available templates:
  basic
  crawl
  csvfeed
```

* `basic`：提供基础构架，继承于Spider类, 爬取方式需自定, 可见此例中的`SfulakezaSpider`类
* `crawl`：提供更灵活的提取方式，继承于CrawlSpider类, 适用于爬取，可见此例中的`SfulakezaslidesSpider`类
* `csvfeed`：提供提取CSV格式文件的方式，继承于CSVFeedSpider类，适用于解析csv文件
* `xmlfeed`: 用于提取XML文件，继承于XMLFeedSpider类，适用于解析xml文件

### 创建scrapy Spider

进入工程目录:     `cd FileDownload`

使用`crawl`模板创建一个spider:

```
scrapy genspider -t crawl sfulakezaSlides http://comet.lehman.cuny.edu/sfulakeza/su21/ttp/slides/
```

- `genspider`: 创建命令
- `-t`: 使用的模板，这里使用的是`crawl `
- `sfulakezaSlides`: 名称
- `http://comet.lehman.cuny.edu/sfulakeza/su21/ttp/slides/`: 可带协议头或不带，为初始url

此命令会在工程的`spiders`目录下创建一个对应名称的`name.py`文件，类`SfulakezaslidesSpider`中有四个变量：

```
    name = "sfulakezaSlides"
    allowed_domains = ["comet.lehman.cuny.edu"]
    start_urls = ["http://comet.lehman.cuny.edu/sfulakeza/su21/ttp/slides/"]

    rules = (Rule(LinkExtractor(allow=r"Items/"), callback="parse_item", follow=True),)
```

其中最重要的是`rules`,定义在爬行过程哪些url需要抓取，定义好我们所需要的爬取规划，可节省爬取次数及流量。爬取规划的定义有：

* allow
* deny
* restrict_xpaths
* restrict_css

详情可见官方文档：[Link Extractors](https://docs.scrapy.org/en/latest/topics/link-extractors.html)

根据我们要爬取的文件的url:
```
http://comet.lehman.cuny.edu/sfulakeza/su21/ttp/slides/Day%201/
http://comet.lehman.cuny.edu/sfulakeza/su21/ttp/slides/Day%202/HOF,%20CB,%20Array%20Methods.pdf
http://comet.lehman.cuny.edu/sfulakeza/su21/ttp/slides/assignments/Day%201/
```

可以看到所需要的文件都在`sfulakeza/su21/ttp/slides/`后, 并且不需要爬父目录，所以可以将`rules`修改为：

```
    rules = (
        Rule(LinkExtractor(allow=(r"sfulakeza/su21/ttp/slides/"), deny=(r"/Parent Directory"),),
        callback="parse_item",
        follow=True),
    )
```

## 抓取并解析网页数据

此时在终端运行`scrapy crawl sfulakezaSlides`, spider应该会以`start_urls`中的位置开始抓取了(但还没有配置好，可先做个可运行性测试)

spider会从`start_urls`所指向的url开始抓取网页，并在`def parse_item(self, response):`方法中对网页中的数据进取提取操作。在这个示例中，我们所需要的数据都在`li`中的`a`标签的`href`属性中，只需解析每个页中的`href`并下载其中的文件即可。
 
将`SfulakezaslidesSpider.py`文件中的parse_item方法更改如下：

 ```
     def parse_item(self, response):
        hrefs = response.xpath('//ul/li').css('a::attr(href)').getall()
        for hrefPath in hrefs:
            if 'Parent%20Directory' not in hrefPath:    # 过滤父级文件夹
                new_file_path = response.urljoin(hrefPath)
                fileItem = FiledownloadItem()
                fileItem['file_urls'] = [new_file_path]
                fileItem['original_file_name'] = new_file_path.split('/')[-1]
                yield fileItem
 ```
 
  > 使用`basic`模板只会抓取`start_urls`中的url页面，更深入的页面需要设置后续Request，而使用`crawl`模板创建一个spider则会抓取`start_urls`下所有网面中的所有符合`rules`的url指向页面。
  
  
#### html数据提取

`response.xpath('//ul/li').css('a::attr(href)').getall()`， 提取所有`a`标签中的`href`:
 
> 更多关于Selector的知识：
> 
 [Selectors](https://docs.scrapy.org/en/latest/topics/selectors.html) and 
 [XML 的 XPath 语法](https://blog.walterlv.com/post/xml-xpath.html) and 
 [XPath type system](https://www.ibm.com/docs/en/i/7.1?topic=xpath-type-system) and 
 [Java XPath 示例 – XPath 教程](https://github.com/apachecn/howtodoinjava-zh/blob/master/docs/misc2/59.md)
 
 
#### html分析工具 `scrapy shell`

使用命令 `scrapy shell` 激活scrapy终端，常用`scrapy --help`获取更多的信息。
使用示例:

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

## 下载文件

### 创建需要下载的文件类

在获取到网页并解析到所需要的数据之后，要将要下载的文件及url通过`scrapy.Item`接入到spider中。文件类`Item`可包含文件的各种属性，如媒体文件有原始数据，缩略图，音频等。

在文件`items.py`文件中，创建或更改原有的类为`FiledownloadItem`,并继承`scrapy.Item`, 此类为需要下载的文件类，有属性`file_urls`, `files`, `original_file_name`,注意`file_urls`为`list`类型:

```
class FiledownloadItem(scrapy.Item):
    # define the fields for your item here like:
    file_urls = scrapy.Field()
    files = scrapy.Field
    original_file_name = scrapy.Field()
    pass
```

具体的FiledownloadItem生成，详见`SfulakezaslidesSpider.py`文件中 `def parse_item(self, response):`

### 下载动作配置及数据存储

在文件`setttings.py`中配置如下：

```
FILES_STORE = 'downloads'	# 下载文件的存储位置
FILES_EXPIRES = 999		# 下载文件时的超时时间

DOWNLOAD_DELAY = 5		# 下载每个文件的时间间隔（scrapy会在0～DOWNLOAD_DELAY之间随机的使用间隔，可看起来不像机器在定时请求）

ITEM_PIPELINES = {
   "FileDownload.pipelines.SliderPipeline": 300, # 下载的Pipeline
}

# 在请求增加HEADERS
DEFAULT_REQUEST_HEADERS = {
   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
   "Accept-Language": "en",
   'Referer': 'http://http://comet.lehman.cuny.edu',
   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
}
```

#### 自定义`Pipelien`

当在网页收集到数据之后，可以通过Pipelien定义数据的下载及存储行为，如哪些数据需要下载，哪些需要存在哪里，数据要怎么转换，怎么样防止重复下载等。

这个示例中有两个需求，一是保储网页上的文件目录结构（有些目录为空），二是保留文件名并移除空格。这些都是在自定义的Pipeline中实现。


在文件`pipelines.py` 创建类 `class SliderPipeline(FilesPipeline):` 继承`FilesPipeline `。重定方法`def file_path(self, request, response=None, info=None):`来重新指向文件的存储path及文件名。

```
    def file_path(self, request, response=None, info=None):
        # 方案一 直接配置下载目录及文件名称
        relative_url_path = request.url.split('sfulakeza/su21/ttp/slides/')[-1].replace("%20", "_") # 替换%20(空格)为下划线
        return relative_url_path
```
> 注意这里的path是在配置文件`FILES_STORE = 'downloads'	# 下载文件的存储位置` 下的

通过方法`get_media_requests`判断item需要下载文件或创建目录：

```
    # 对空目录对文件类型进行筛选下载
    def get_media_requests(self, item, info):
        for file_url in item['file_urls']:
            print(f"file_url in item {file_url}")
            relative_url_path = file_url.split('sfulakeza/su21/ttp/slides/')[-1].replace("%20", "_") # 替换%20(空格)为下划线
            if relative_url_path.endswith('/'):
                # 当前是目录，只创建目录，无文件下载
                settings = get_project_settings()
                storage = settings.get('FILES_STORE')
                dir_path = os.path.join(storage, relative_url_path)
                if not os.path.exists(dir_path):
                    print(f"创建目录: {dir_path}")
                    os.makedirs(dir_path)
            else:
                # 是文件
                file_extension = relative_url_path.split('.')[-1]
                # 对文件类型进行筛选下载
                print(f"下载文件 {relative_url_path}")
                if file_extension in ('pdf', 'ppt', 'docx', 'doc', 'md'):
                    yield scrapy.Request(file_url)
```

关于Pipeline更多可见： [Downloading and processing files and images](https://docs.scrapy.org/en/latest/topics/media-pipeline.html)

完整项目[Scrapy下载文件](https://github.com/stoull/FileDownload)














