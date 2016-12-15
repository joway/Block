---
title: Hexo折腾记——性能优化篇
comments: true
categories: Hexo
toc: true
tags:
	- hexo
	- 前端
	- blog
	- github
---



折腾Hexo的本来目的就是为了学习把性能优化到极致，由于水平有限，这里牵涉到的所谓的性能优化仅仅只是一些表面工夫，并不牵涉非常细节的前端性能。

另外，由于我朝特殊的网络环境，我使用的谷歌分析，以及Disqus 均会导致出现因时因地因运营商而异的发抽状况，故而所有速度测试均在排除这些干扰下进行的。

<!--more-->


### 静态文件压缩

静态文件包括: html,css,js,images . 我才用了gulp来跑自动压缩任务 。具体方法如下:

1. npm 安装如下工具, 方法皆为 : npm install xxx --save

``` json
    "gulp": "^3.9.1",
    "gulp-htmlclean": "^2.7.6",
    "gulp-htmlmin": "^1.3.0",
    "gulp-imagemin": "^2.4.0",
    "gulp-minify-css": "^1.2.4",
    "gulp-uglify": "^1.5.3",
```

2. 建立 gulpfile.js 文件

``` js
	var gulp = require('gulp');
	var minifycss = require('gulp-minify-css');
	var uglify = require('gulp-uglify');
	var htmlmin = require('gulp-htmlmin');
	var htmlclean = require('gulp-htmlclean');

	// 获取 gulp-imagemin 模块
	var imagemin = require('gulp-imagemin')

	// 压缩 public 目录 css
	gulp.task('minify-css', function() {
	    return gulp.src('./public/**/*.css')
	        .pipe(minifycss())
	        .pipe(gulp.dest('./public'));
	});
	// 压缩 public 目录 html
	gulp.task('minify-html', function() {
	  return gulp.src('./public/**/*.html')
	    .pipe(htmlclean())
	    .pipe(htmlmin({
	         removeComments: true,
	         minifyJS: true,
	         minifyCSS: true,
	         minifyURLs: true,
	    }))
	    .pipe(gulp.dest('./public'))
	});
	// 压缩 public/js 目录 js
	gulp.task('minify-js', function() {
	    return gulp.src('./public/**/*.js')
	        .pipe(uglify())
	        .pipe(gulp.dest('./public'));
	});


	// 压缩图片任务
	// 在命令行输入 gulp images 启动此任务
	gulp.task('images', function () {
	    // 1. 找到图片
	    gulp.src('./photos/*.*')
	    // 2. 压缩图片
	        .pipe(imagemin({
	            progressive: true
	        }))
	    // 3. 另存图片
	        .pipe(gulp.dest('dist/images'))
	});



	// 执行 gulp 命令时执行的任务
	gulp.task('default', [
	    'minify-html','minify-css','minify-js','images'
	]);

```

注意， 修改上面的各个目录为你的真实目录， ** 代表0或多个子目录

3.  执行 gulp ，即可自动压缩所有静态文件


### CDN 接入

上面的静态文件压缩幅度有限，要先提升下载速率还需要CDN的支持 。 理论上最佳方案是把所有静态文件都放在CDN上，但是由于hexo各处都在调用内部的js/css，如果需要改动，工程量会比较大，后期维护也不是很方便。不知道以后Hexo会不会原生提供一个配置静态资源地址的选项。

所以我这里只将图片放在了七牛CDN上，hexo 有一个七牛的插件 : hexo-qiniu-sync 。 但是不知道为什么， 我在我电脑上跑不来这个，我看网上也有人说这个插件有许多bug，于是我就自己写了个脚本(本来想写插件，但是并没有研究过hexo的插件该如何写，所以暂时放弃了，后期有时间尝试下吧)。

我的需求很简单，我有一个相册的页面，里面可能会放许多图片，我只想要一个脚本，能过一键上传所有图片然后把url全部写进我的相册界面里。具体实现思路参见 [Hexo 折腾记(基本配置篇)]() 。

一键上传所有文件至七牛的Node 脚本在Github上: [https://github.com/joway/qiniu_upload_node](https://github.com/joway/qiniu_upload_node)


### InstantClick 黑科技

说到性能优化，有一个黑科技虽然不是特别优雅，但是提升的速度却是立杆见影且惊人的，那就是 InstantClick 。

InstantClick 的思路非常巧妙，它利用鼠标点击链接前的短暂时间(统计说是平均400ms)进行预加载，从而在感观上实现了迅速打开页面的效果。当你在打开页面的时候，其实页面已经加载到本地了，也就会很快能个完成渲染。

InstantClick 并不能滥用，许多js无法与它兼容，比如 谷歌分析，百度统计，另外还有fancybox 。故而它有两种启用方式:

1. 白名单方式:

初始化:

``` html
	<script src="instantclick.min.js"data-no-instant></script>
	<script data-no-instant>InstantClick.init(true);</script>
```

针对具体每个链接启动:

``` html
	<a href="/blog/" data-instant>Blog</a>
```

2. 黑名单方式:

初始化，以及解决部分js无法加载的问题:

``` html
<script src="/js/instantclick.min.js" data-no-instant></script>
<script data-no-instant>
InstantClick.on('change', function(isInitialLoad) {
	if (isInitialLoad === false) {
	if (typeof MathJax !== 'undefined') // support MathJax
		MathJax.Hub.Queue(["Typeset",MathJax.Hub]);
	if (typeof prettyPrint !== 'undefined') // support google code prettify
		prettyPrint();
	if (typeof _hmt !== 'undefined')  // support 百度统计
		_hmt.push(['_trackPageview', location.pathname + location.search]);
	if (typeof ga !== 'undefined')  // support google analytics
		ga('send', 'pageview', location.pathname + location.search);
	}
});
InstantClick.init();
<script>
```

这时候对于所有链接都开启 预加载模式，但是可以针对部分链接假如黑名单:

``` html
	<a href="/blog/" data-no-instant>Blog</a>
```

这里我遇到的一个坑是，我的相册使用了fancybox，而对于InstantClick死活无法解决fancybox的问题(网上也没解决方案)，虽然我可以通过指定data-no-instant来达到不预加载的目的，但是hexo对于每个同级链接都是一样对待的，我如何让它单单对于相册不进行预加载呢?

我能够想到的方法就是对导航栏的每一个url指定一个以其中文名(暂时不映射成英文)命名的id值，然后待页面渲染完了以后，对id值为'相册'的元素添加 data-no-instant 属性:

``` html
	$("#相册").attr("data-no-instant",'');
```

有些时候这种加黑名单的方法也没用，那么就用最后一招，强制刷新（自己调试出来的，略土。。） :

``` js
	document.getElementById('相册').onclick = function(e){
	 	location.href = document.getElementById('相册').href;
	}
```


### Nginx 优化配置


Gzip压缩:

```
http {
    gzip               on;
    gzip_vary          on;

    gzip_comp_level    6;
    gzip_buffers       16 8k;

    gzip_min_length    1000;
    gzip_proxied       any;
    gzip_disable       "msie6";

    gzip_http_version  1.0;

    gzip_types         text/plain text/css application/json application/x-javascript text/xml application/xml application/xml+rss text/javascript application/javascript;
    ... ...
}
```


### 搜索引擎优化(SEO)

添加百度主动推送代码，让搜索引擎最快发现文章 .

方法: 在 <博客根目录>/themes/yilia/layout/_partial/article.ejs 的尾部评论位置, 添加:

``` html
<% if (!index){ %>
<script>
(function(){
    var bp = document.createElement('script');
    bp.src = '//push.zhanzhang.baidu.com/push.js';
    var s = document.getElementsByTagName("script")[0];
    s.parentNode.insertBefore(bp, s);
})();
</script>     
<% } %>
```

之后，每次用户访问界面，都会去调用推送代码

---


相关文章:


[Hexo折腾记——基本配置篇](https://joway.wang/posts/Hexo/2016-03-18-hexo-base.html)

[Hexo折腾记——自动部署篇](https://joway.wang/posts/Hexo/2016-03-19-Hexo-deploy.html)
