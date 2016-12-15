---
title: Hexo折腾记——通过压缩与内联提升访问速度
comments: true
categories: Hexo
toc: true
tags:
	- hexo
	- 博客
	- 优化
	- 加速
	- 性能
	- 压缩
	- 内联
	- 静态文件
---


经常混V站的朋友对某个号称"国内最快的博客"一定不陌生，https://imququ.com/ 这个博客从前端到服务端都使用了非常极致的优化，从而做到了正常网络下所有页面加载速度都能在1s以内，甚至会在200ms左右。出于学习的目的，也对自己的博客弄了一通。

<!-- more -->
首先我看了他博客的加载情况:

![](https://dn-joway.qbox.me/1463459787511_%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202016-05-17%2012.36.22.png)

基本上就没有用css/js的文件，全部内联到了html中。然后再对它的html进行了压缩。

![](https://dn-joway.qbox.me/1463459962503_%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202016-05-17%2012.38.43.png)

这里其实还是有很多地方可以进一步压缩到极致。

另外，对于一些小图片，也可以才用硬编码进html里面，从而不需要为了一张几k的图片，再去服务端访问。

这是他看得见的部分，另外，他在服务端所做的优化远远超过了前端部分，比如他页面里是没有任何调用谷歌统计的部分的，这点我咨询了博主本人，他说他是在服务端去生成每个用户标识然后异步发送到google-analysics.com，此外，https 的加速和优化，以及各类黑科技更是层出不穷，详细可研究该博主的博客。

我的博客为了实现高可用(其实是因为阿里云青岛学生机高不可用被逼的)，在一台阿里云，一台腾讯云各开了一个docker容器，另外，由于本身静态博客就是为了省事，如果还得去两台机器上折腾一堆东西，那就太复杂了。所以我终点把优化搞在前端部分。

我的gulpfile.js如下:

``` js
var gulp = require('gulp');
var minifycss = require('gulp-minify-css');
var uglify = require('gulp-uglify');
var minifyHTML = require("gulp-minify-html");
var htmlclean = require('gulp-htmlclean');
var gutil = require('gulp-util');
var minifyInline = require('gulp-minify-inline');
var inline = require('gulp-inline')
var inlineimage = require('gulp-inline-image');


// 获取 gulp-imagemin 模块
var imagemin = require('gulp-imagemin');

var dir = './public'


// 压缩 public 目录 html
gulp.task('minify-html',function() {
  var opts = {
         removeComments: true,
         minifyJS: true,
         minifyCSS: true,
         minifyURLs: true,
  };
  gulp.src('./public/**/*.html')
    .pipe(inline({
        base: './public/',
        disabledTypes: ['svg', 'img'], // Only inline css files
    }))
    .pipe(minifyInline())
    .pipe(minifyHTML(opts))
    .pipe(gulp.dest(dir));
});

// 压缩 public 目录 css
gulp.task('minify-css', function() {
    gulp.src('./public/**/*.css')
        .pipe(inlineimage())
        .pipe(minifycss())
        .pipe(gulp.dest(dir));
});

// 压缩 public/js 目录 js
gulp.task('minify-js', function() {
    gulp.src('./public/**/*.js')
        .pipe(uglify().on('error', function(e){
            console.log(e);
        }))
        .pipe(gulp.dest(dir));
});


// 压缩图片任务
// 在命令行输入 gulp images 启动此任务
gulp.task('images-photos', function () {
    // 1. 找到图片
    gulp.src('./photos/*.*')
    // 2. 压缩图片
        .pipe(imagemin({
            progressive: true
        }))
    // 3. 另存图片
        .pipe(gulp.dest('dist/images'))
});


// 压缩图片任务
// 在命令行输入 gulp images 启动此任务
gulp.task('images-public', function () {
    // 1. 找到图片
    gulp.src('./public/**/*.*')
    // 2. 压缩图片
        .pipe(imagemin({
            progressive: true
        }))
    // 3. 另存图片
        .pipe(gulp.dest(dir))
});


// 执行 gulp 命令时执行的任务
gulp.task('default', [
    'minify-css','minify-js','minify-html',
    'images-photos','images-public']
    );

```

过程无非就是 压缩css,js,再把他们内联到html中，顺带把图片也压缩了(虽然我大图都是自己手动压缩好的，否则我拍出来的相片都是20M起步的)

但是在折腾过程中，我也发现了一个弊端，由于之前我搞得太花里胡哨了，导致我的css,js 奇多，肯定无法都inline到一个html中，所以我这里只是将大小比较小的静态资源inline进去，而jquery之类的东西使用第三方cdn，这样我的构建工具本来也就只能inline本地的静态资源，刚好可以把两者区分开来。





