# penework document(不断完善中...)

Tags: penework


```
                                           _
 ____   ____ ____   ____ _ _ _  ___   ____| |  _
|  _ \ / _  )  _ \ / _  ) | | |/ _ \ / ___) | / )
| | | ( (/ /| | | ( (/ /| | | | |_| | |   | |< (
| ||_/ \____)_| |_|\____)\____|\___/|_|   |_| \_)
|_|                                               
```
penework是一个开源的渗透测试框架，主要是受到猪猪侠乌云峰会上的ppt的启发，才准备着手开发自己的渗透测试框架，并且主要根据[pocsuite](https://github.com/knownsec/Pocsuite)和[sqlmap](https://github.com/sqlmapproject/sqlmap)开发，其中还借鉴了很多优秀的开源工具的思路和相关代码，完全不用于商业用途，只是自己对所学知识的利用，并通过开发来锻炼自己的能力。


# 依赖
环境
1. python 2.7
2. redis 
3. mongodb

python库
1. redis
2. pymongo
3. requests
4. pudb(debug)
5. rq(分布式框架消息队列)
6. bs4
7. lxml

	ubuntu 14.04
	```
	sudo apt-get install libxml2-dev libxslt-dev python-dev
	pip install lxml
	```



# 爬虫部分

```
lib/utils/crawler/crawler.py 单机爬虫
lib/utils/crawler/crawlerDist.py 分布式爬虫
lib/utils/crawler/master.py 分布式爬虫的master
```

## 分布式爬虫

主要利用[rq](https://github.com/nvie/rq)做工作队列，master负责投入job进入Queue，slave(worker)从工作队列中拿出job，进行处理

爬虫主要的搜索方法使用宽度优先搜索，主要代码如下
```python
countDepth = 0
countUrls = 0
while countDepth <= int(conf.CRAWL_DEPTH):
    while True:
        url = self.redisCon.lpop('visit')
        if url:
            countUrls += 1
            print 'countDepth:', countDepth, 'countUrls:', countUrls
            self.jobQueue.enqueue_call(crawl, args=(url, countDepth, countUrls))
        else:
            self.redisCon.delete('visitSet')
            break
    while True:
        # wait 30 seconds, if timeout, jobqueue is empty(except failed job)
        keyUrl = self.redisCon.blpop('tmpVisit', timeout=30)
        if keyUrl:
            url = keyUrl[1]
            hashData = hashUrl(url)
            if not self.redisCon.sismember('visited', hashData) \
                    not sefl.redisCon.sismember('visitSet', hashData):
                self.redisCon.lpush('visit', url)
                self.redisCon.sadd('visitSet', hashData)
        else:
            break

    countDepth += 1
```

### url去重
我所做的只是简单的url去重，因为数据量也比较小，也没有用bloom
去重的方法：
根据url的netloc、path、还有查询的keys进行hash，举个例子

```
http://www.example.com/test/test.php?a=2&b=3
http://www.example.com/test/test.php?b=4&a=4
http://www.exmaple.com/test/test.php?a=4&b=4
```
上面的所有url都算作一个url
相对应的hash函数`lib/utils/hashUrl`
```python
def hashUrl(url):

    urlParse = urlparse.urlparse(url)
    urlSchemePath = urlparse.urljoin(urlParse.scheme, urlParse.netloc + urlParse.path)
    urlQueryKeys = (urlparse.parse_qs(urlParse.query)).keys()
    # combine urlSchemaPath and urlQueryKeys as urlHashData
    urlQueryKeys.append(urlSchemePath)
    urlQueryKeys.sort()
    hashData = hash(str(urlQueryKeys))
    return hashData
```


### 重要数据结构

visited(set)
> 存储的是url的hash值，为了简单过滤已经访问过的url，利用set数据类型进行存储。url具体的hash方法可查看lib/utilts/hashUrl中的hashUrl函数

visitSet(set)
> 这个结构一开始根本没有想到使用，在分布式处理的过程中，发现url去重的效果特别的差，查了很久之后，终于发现了问题，因为我采用的是宽度优先搜索的方式进行数据的爬取，每次都是一层一层的爬，随着层数的增加，每层上的url结点会变的越来越多，难免的就会出现重复的url，用visited去重肯定是不行的(以前就是用visited去重)，因为细想一下就可以知道，假如某一层出现了一个url，比如`http://www.test.com/test/testsql.php`，这个url在这层中出现了很多次，并且都没有访问过，这些url会首先存在tmpVisit中，之后进行visited去重后，放在即将访问的visit中，这样visit中就存在了重复的url。这种重复有一种方法可以去除，就是在访问之前再次利用visited判断一下是否重复，这样就确定访问的url肯定是以前没有访问到的。这种方法在单线程，单主机的条件下，可以完美的解决我们的困难，但是在分布式和多线程中，肯定是不行的，多线程暂时我们不讨论，现在只讨论一下分布式中出现的问题，从我们crawlDist.py中的代码可以看到，我们可以在访问之前进行判断，假如判断非visited，之后我们需要进行`很多其他的操作`，之后才能将url的hash值存入visited中，假如我们在进`很多其他的操作`的过程中，别的slave(worker)，获取了visit中那个重复的url，也用visited进行判断，同样也是非visited，同样进行接下来的很多操作，包括进行requests的请求。这样同一个url就进行了多次请求，并且我们为同一个url进行了多次的job提交，这样会浪费大量的时间(如果重复率比较高的话)

> 所以我就想了这个结构，这个结构存储的就是与visit对应的url的hash，这样可以保证每层的url也是不会重复的，这样也就不用在爬取前进行visited判断了


tmpVisit(list)
> 存储每层需要访问的url

visit(list)
> 存储即将访问的url


### 数据存储(mongodb)


# TODO
- [ ] autosqlmapi
- [ ] struts2 scan
- [ ] dirbrute
- [ ] many poc and exp to add 
