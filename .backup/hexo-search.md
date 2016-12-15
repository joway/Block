---
title: Hexo折腾记——静态站点搜索
comments: true
categories: Hexo
toc: true
tags:
	- hexo
	- 前端
	- blog
	- github
---


## 前言

对于静态博客一直有两大心病，其中一个是缺乏靠谱的评论插件, 的确有许多好的评论插件，但要么是要收费要么是大陆访问非常慢， 剩下的国内的也就多说了，然而这家伙不稳定不说，还不支持https，而且目前似乎也无人在维护了。另一块心病就是站内搜索。搜索技术虽然很复杂很麻烦，但说时候对于一个小博客网站而言，其实仅仅只是需要一个全站数据的json文件 ，一个靠谱算法，完全不需要任何后端技术就能够实现一个基本能用的搜索了。网上找了一圈，发现都没有人在做这个。只好自己动手了。

<!--more-->

把生成search.json的部分做成了一个插件: [hexo-tokenize-search](https://github.com/joway/hexo-tokenize-search) 

[Demo](https://joway.wang/search/)

## 准备

首先一个小的搜索引擎所需要的技术大概是以下几点:

- 数据抓取
- 数据净化(去除标点, 英文大小写, 以及同义词转换等等)
- 分词(中英文分词)
- 匹配排序

## 实践

### 数据抓取

对于自己的网站，事实上根本无所谓抓取，尤其是对于诸如Hexo之类的静态站点，可以查阅相关文档，自己编写插件使其在编译静态文件阶段就把文章数据导入到json中，当然，也可以自己写一个python/js 的脚本，把 markdown 源文件给解析出来生成单个json文件。

我这里找到了 hexo-search 插件，但是这个插件只能把数据给拿出来，并不具备数据处理功能，后来我自己在它的基础上，魔改出一个了一个 [hexo-tokenize-search](https://github.com/joway/hexo-tokenize-search) 版本。

### 数据净化与分词

在 我的 hexo-tokenize-search 插件中， 我添加了最基本的数据处理功能:

- 利用正则表达式把html tags全部清除
- 利用 Segment 分词模块，对title和content两个field的数据进行分词处理。 Segment 功能很强大，在分词中，还支持进行同义词转换，去掉诸如"因为、所以"这类无意义的关联词，去除标点符号等等

最后我把数据处理成为如下形式:

``` json
[
{
"title": "xxxxxx",
"url": "xxxxxx" ,
"content": "xxxxxx" ,
"title_tokenize": "xx xx xx xx",
"content_tokenize": "xx xx xx xx"
},
{
...
}
]
```


### 匹配排序

经国上面这几步，基本上完成了数据那块，接下来就是最让我头痛的关键字匹配排序了。

由于我一切都是前端进行，所以不可能去加载什么字典，也无法进行复杂的计算，我的需求其实很简单，针对某个查询，对每个文本评估得出一个分数，再拿这个分数排序展现结果。但是这个评估算法我一直无法寻找到好的，许多现成的算法都是只能对英文有效，中文的匹配需要进行特殊处理。而这个东西又是一个非常麻烦的事情。

最后，我实在无奈了，就写了一个弱智版本的加权算法，其实都不能称之为算法，因为它就是不停遍历遍历遍历比较是否相等......

而且，如果只是比较两个字符是否相等的话，事实上也没必要进行分词了，所以这个算法让我非常蛋疼。。以后有空再来把这个评估算法写出来把。

我当前版本的思路是: 分别对内容和标题进行匹配，计算出匹配的字符个数，总分数 计算公式为:

> 总分数 = 内容匹配次数 + 标题匹配次数 * 100

这样就可以优先把标题匹配的给取出来了。

这种做法很傻逼，但是暂时没有能力想到评估的方法，因为分词的长度也是不定的，不依赖后端实在是想不出又快又好的算法。


## 后记

其实我后来想到, 写个脚本把hexo的文章数据post到elasticsearch服务器，然后前端直接能够进行各种花式搜索了。这种实践的成本无非是开一个es的容器，并配置好中文分词的插件。

在折腾这个之前，我是想做一个开箱急用的插件，不过现在看来，还是开个es后端比较方便，但是话也说回来，为了一个博客搜索功能开个容器也太奢侈了。况且es本身就很占内存。如果能够有人做个API大家公用，或许我们前端只要三行代码就能实现一个搜索引擎了。:) 


## 源码

现看js教程现写js代码 ... 对js这种语言真的完全不能把控 ， 如果你要使用，calcScore 函数这段代码效率低，并且没有利用分词的优势，最好能够写个更好的替换掉。

``` html 搜索框
<form action="/search" method="get" style="text-align: center">
    <input type="text" class="st-default-search-input search" id="search"
        placeholder=" Search..." name="query" style="height: 40px">
</form>
<div id='result'></div>
<script src='/js/search.js'></script>
```

``` js
function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}

function calcScore(key, tokenize) {
    var score = 0;
    for (var x = 0; x < tokenize.length; ++x) {
        if (tokenize[x] == null) {
            break;
        }
        for (var i = 0; i < key.length; ++i) {
            for (var t = 0; t < tokenize[x].length; ++t) {
                if (tokenize[x][t] == key[i]) {
                    score++;
                }
            }

        }
    }
    return score;
}

function addCountToJson(key, json) {
    for (var i = 0; i < json.length; ++i) {
        // 题目匹配权重100 , 内容匹配权重1 , 匹配算法: 单字匹配 (待优化)
        json[i]['score'] = calcScore(key, json[i].content_tokenize) + calcScore(key, json[i].title_tokenize) * 100;
    }
}


// 按 json 元素 score 值进行排序
function quickSort(json) {
    if (json.length <= 1) {
        return json;
    }
    var pivotIndex = Math.floor(json.length / 2);
    var pivot = json.splice(pivotIndex, 1)[0]; // 基准
    var left = [];
    var right = [];
    for (var i = 0; i < json.length; i++) {
        if (json[i].score < pivot.score) {
            left.push(json[i]);
        } else {
            right.push(json[i]);
        }
    }
    return quickSort(left).concat(pivot, quickSort(right));
}

window.onload = function () {

    var query = getParameterByName('query');
    if (query == null) {
        query = '';
    }

    $(".st-default-search-input").val(query);
    $.get("../search.json", function (result) {
        addCountToJson(query, result);
        result = quickSort(result);
        for (var i = result.length - 1; i >= 0; --i) {
            $("#result").append('<a href="' + result[i].url + '"' + ' target="_blank"' + '><li>' + result[i].title + ' 评分: ' + result[i].score + '</li></a>');
        }
    });
};

```
