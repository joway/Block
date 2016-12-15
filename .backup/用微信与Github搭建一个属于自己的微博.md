---
title: 用微信与Github搭建一个属于自己的微博
comments: true
categories: Toy
toc: false
tags:
	- Toy
	- Github
	- 微信
	- 微博
---


最近给博客加了一个[闲扯](https://joway.wang/words/)的功能, 类似于一个个人的微博吧。 起初是因为看到了 Github 的 API ，然后觉得 Github 真的是把能开放的API都开放了，围绕这套API其实可以做相当多的东西，这里仅仅只是用了一个发布issues和获取issues的API，目的只是把Github作为了一个小型数据库，然后在前端直接调用API获取issues 就能渲染出issues信息了。

<!--more-->

但是这样的话，每次要发表信息就必须通过Github，这个显然有点麻烦，所以又写了一个微信公众号的服务端，通过发送到微信公众号的信息，通过服务器端写入Github。当然，我现在的话，是用微信的Openid限定了只有我发送内容才会被写进Issues里，事实上，稍微改下代码就能让别人也可以来参与发布内容。

服务端使用了Django，其实没必要用那么重的东西，web.py 就能够很好实现这个功能了。代码放在了服务端 : 

[wechat-post](https://github.com/joway/wechat-post)

在前端，主要就一个渲染json的工作, 下面这段代码是获取issues 的:

[https://gist.github.com/joway/5117654ab5a1f58a158ae887b6419a50](https://gist.github.com/joway/5117654ab5a1f58a158ae887b6419a50)

``` js

    function github_issues(github_account, repo, issues_id) {
        var url = 'https://api.github.com/repos/' + github_account + '/' + repo + '/issues/' + issues_id;
        var url_comments = url + '/comments';
        <!--$.get(url, function (result) {-->
        <!--$('#comments-title').html('<a target="_blank" href="' + 'https://github.com/joway/' + repo +-->
                            <!--'/issues/' + issues_id + '">' + result.title + '</a>');-->
        <!--});-->
        $.get(url_comments, function (result) {
            for (var i = 0; i < result.length; ++i) {
                var avatar = result[i].user.avatar_url;
                var username = result[i].user.login;
                var comment = result[i].body;
                var created_at = new Date(result[i].created_at).toLocaleString()	;
                # do something
            }
        });
    }
    
    window.onload = function() {
       github_issues('joway', 'Utopia', 3);
    };
    
```



现在终于可以愉快得发干净体面的"微博"了 :)
