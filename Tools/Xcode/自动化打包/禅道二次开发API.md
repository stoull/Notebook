# 禅道二次开发API


[创建版本](https://www.zentao.net/book/api/setting-369.html)

创建禅道版本：

```
POST: http://20.6.1.140:8088/zentao/api.php/v1/projects/676/builds
{
    "execution": 677,
    "product": 676,
    "name": "iOS 2.6.0 (Build 2.6.0.7)-test",
    "builder": "chencc",
    "date": "2024-03-24",
    "scmPath": "git@20.6.1.65:chenchangchun/mygro.git",
    "filePath": "https://fir.xcxwo.com/2w63",
    "desc": "此版本用于自动化构建版本测试"
}
```
```
{
    "id": 756,
    "project": 676,
    "product": 676,
    "branch": "0",
    "execution": 677,
    "builds": "",
    "name": "iOS 2.6.0 (Build 2.6.0.7)-test",
    "scmPath": "git@20.6.1.65:chenchangchun/mygro.git",
    "filePath": "https://fir.xcxwo.com/2w63",
    "date": "2024-03-24",
    "stories": "",
    "bugs": "",
    "builder": "chencc",
    "desc": "此版本用于自动化构建版本测试",
    "createdBy": "chencc",
    "createdDate": "2024-03-24 12:09:32",
    "deleted": "0",
    "executionName": "mygro V2.6.0",
    "productName": null,
    "productType": null,
    "allBugs": "",
    "allStories": "",
    "files": []
}
```