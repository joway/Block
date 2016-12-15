---
title: Hexo折腾记——基本配置篇
comments: true
categories: Hexo
toc: true
tags:
	- hexo
	- 前端
	- blog
	- github
---





### 前言

人闲起来真是可怕，本来已经折腾过了jekyll和Ghost，静态和动态博客也都尝了遍鲜，然而还是按捺不住寂寞又折腾起来Hexo。话说我最早大概是两年前高考结束的时候知道的Hexo，那时在家里没事干想搭个博客玩，然后看见了jekyll和hexo，无奈那时候就一台windows，啥也不懂啥也不会，这两个博客工具楞是装不上去。而Jekyll的一个好处是可以不用在本地跑，Github 的Pages功能原生支持Jekyll，所以我只需要下载些别人的源文件，自己随便修改下，传到Github就能在线调试和运行了。

<!--more-->

这次尝试Hexo的另一个原因是，想重头学习下这些工具的原理和逻辑，另外再添加些可以将性能发挥到极致的黑科技(下文会有介绍)。

至于Hexo如何安装配置，网上有太多教程了，可以直接按照文档操作 。 这里只作为进阶，列举一些进阶配置以及踩过的坑。

PS ： 我用的Hexo 版本是3.2, 主题是 [yilia](https://github.com/litten/hexo-theme-yilia)

以下功能可能需要插件支持，我的package.json为:

``` json
{
  "name": "hexo-site",
  "version": "0.0.0",
  "private": true,
  "hexo": {
    "version": "3.2.0"
  },
  "dependencies": {
    "gulp": "^3.9.1",
    "gulp-htmlclean": "^2.7.6",
    "gulp-htmlmin": "^1.3.0",
    "gulp-imagemin": "^2.4.0",
    "gulp-minify-css": "^1.2.4",
    "gulp-uglify": "^1.5.3",
    "hexo": "^3.2.0",
    "hexo-deployer-git": "0.0.4",
    "hexo-generator-archive": "^0.1.4",
    "hexo-generator-category": "^0.1.3",
    "hexo-generator-feed": "^1.0.2",
    "hexo-generator-index": "^0.2.0",
    "hexo-generator-sitemap": "^1.1.2",
    "hexo-generator-tag": "^0.2.0",
    "hexo-migrator-rss": "^0.1.2",
    "hexo-renderer-ejs": "^0.2.0",
    "hexo-renderer-marked": "^0.2.10",
    "hexo-renderer-stylus": "^0.3.1",
    "hexo-server": "^0.2.0",
    "jgallery": "^1.5.4",
    "qiniu": "^6.1.9"
  }
}
```


### 文章永久链接

默认文章链结是以: http://xxx.com/2015/07/06/your-title/ 的格式的， 个人不是很喜欢这样的格式，而且末尾没有.html结尾有点动态页面的感觉，对搜索引擎是否友好也有疑问(如果你知道答案，请告诉我)，于是，我改成了 http://xxx.com/posts/programming/2016-03-18-hello-world.html 这样的格式，具体方法是在 根目录下的 _config.yml 文件里:

	permalink: posts/:category/:year-:month-:day-:title.html
	
### 开启目录支持

我本人并不是很喜欢以tag来分类文章的方式，但是hexo默认是以tag来分类的，于是我另外给它加了一个种类(Category)的选项，方法是在_config.yml 下:

	default_category: uncategorized
	category_map:
		编程: programming
		生活: life
		其他: other
		
其中, category_map 是为了让url中尽量少出现中文，做的映射。 

例如:
在文章开头，标柱目录为:

	---
	xxx: xxx
	categories: 编程
	---
	
则在url中， 会变成: 

	.../posts/programming/xxx.html

### 文章目录

默认不开启文章目录，若要开启:

	---
	xxx: xxx
	toc: true
	---
	
会自动根据标题权重进行目录生成。显示在最右边。 如需要更改格式， 可去 .../yilia/layout/_partial/archive.ejs 中修改


### 相册

一直很想要一个靠谱，方便，而且快捷的相册功能，以前用Jekyll的时候没弄懂如何动态生成界面，就直接用html写了一个相册界面，然后还用VC++写了一个windows下的把某个文件夹下所有图片名检索并自动生成相应的html相册页面的小工具，后来玩Ghost了， 天真地想把发布图片的功能集成到原生的管理面版上，然后最后还是失败了。

这次折腾hexo，我下定决心了一定要把相册功能给实现了!(然后我就浪费了一个下午 :( 

一开始贪图方便，使用 yilian 主题 自带的 基于instagram API的相册展示功能，本来还想着如果instagram被墙，试试看反代它的地址来实现功能，后来发现我申请的client_id 死活不能用我也是醉了，最后腾了半天还弄不好我也就放弃了。

于是想自己造轮子，思路很简单，把照片全部放在本地某个目录下，然后跑个Python或者Node脚本把所有文件上传到某个地方(github/七牛)，并把这些文件名全部保存为output.json 文件，之后相册页面通过get 这个json文件，来得到对应的所有照片url，生成界面。(这个流程参照了网上另一位仁兄的实现，然后我找不到链接了...下次找到了补充上来)

看了下七牛的Node SDK 文档，发现都不用写多少代码，直接能照着文档用，于是改了改，放在本地一键运行，成功!

一键上传七牛以及输出文件名json的代码如下:

``` js
	const fs = require("fs");
	const path = "../../photos";
	var qiniu = require("qiniu");
	
	
	//需要填写你的 Access Key 和 Secret Key
	qiniu.conf.ACCESS_KEY = 'xxx';
	qiniu.conf.SECRET_KEY = 'xxx';
	
	//要上传的空间
	bucket = 'hexo';
	
	
	//构建上传策略函数
	function uptoken(bucket, key) {
	  var putPolicy = new qiniu.rs.PutPolicy(bucket+":"+key);
	  return putPolicy.token();
	}
	
	
	
	//构造上传函数
	function uploadFile(uptoken, key, localFile) {
	    var extra = new qiniu.io.PutExtra();
	    qiniu.io.putFile(uptoken, key, localFile, extra, function(err, ret) {
	      if(!err) {
	        // 上传成功， 处理返回值
	        console.log('upload success : ',ret.hash, ret.key);
	      } else {
	        // 上传失败， 处理返回代码
	        console.log(err);
	      }
	  });
	}
	
	/**
	 * 读取文件后缀名称，并转化成小写
	 * @param file_name
	 * @returns
	 */
	function getFilenameSuffix(file_name) {
	  if(file_name=='.DS_Store'){
	    return '.DS_Store';
	  }
	    if (file_name == null || file_name.length == 0)
	        return null;
	    var result = /\.[^\.]+/.exec(file_name);
	    return result == null ? null : (result + "").toLowerCase();
	}
	
	
	fs.readdir(path, function (err, files) {
	    if (err) {
	        return;
	    }
	    var arr = [];
	    (function iterator(index) {
	        if (index == files.length) {
	            fs.writeFile("./output.json", JSON.stringify(arr, null, "\t"));
	            return;
	        }
	
	        fs.stat(path + "/" + files[index], function (err, stats) {
	            if (err) {
	                return;
	            }
	            if (stats.isFile()) {
	              var suffix = getFilenameSuffix(files[index]);
	              if(!(suffix=='.js'|| suffix == '.DS_Store')){
	                //要上传文件的本地路径
	                filePath = path+'/'+files[index];
	                console.log('抓取到文件: '+files[index]);
	                //上传到七牛后保存的文件名
	                key = files[index];
	                //生成上传 Token
	                token = uptoken(bucket, key);
	                // 异步执行
	                uploadFile(token, key, filePath);
	                arr.push(files[index]);
	            }
	
	                      }
	            iterator(index + 1);
	        })
	    }(0));
	});
```

### 一键部署

全局 _config.yml 中，设置:

	deploy:
	  type: git
	  repository: https://github.com/joway/hexo-blog.git
	  branch: master

执行

	hexo deploy

即可上传至git 仓库



---


相关文章:

[Hexo折腾记——性能优化篇](https://joway.wang/posts/Hexo/2016-03-19-Hexo-optimize.html)

[Hexo折腾记——自动部署篇](https://joway.wang/posts/Hexo/2016-03-19-Hexo-deploy.html)


