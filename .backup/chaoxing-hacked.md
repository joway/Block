---
title: 超星慕课视频系统破解
comments: true
categories: Hacked
tags:
	- 超星
	- Hacked
	- js
---


本教程只适用于超星慕课上的课程，其它课程网站需要修改代码 。

<!-- more -->

如果未安装Chrome，请下载并安装好Chrome。

相关附件下载 :  [https://dn-joway.qbox.me/1460124976338_chaoxin-hacked-crx.zip](https://dn-joway.qbox.me/1460124976338_chaoxin-hacked-crx.zip)

原理使用了javascript劫持技术，若你明白如何在浏览器中手动运行代码可跳到第二种方法，直接Chrome的开发工具里插入js脚本代码。这段代码参考了网上另外一个人的实现，如果还想进一步Hack，可以修改代码，我没有时间去折腾这个了，就直接拿来用了。

在浏览器中输入 : [chrome://extensions/](chrome://extensions/) , 打开扩展程序页，将附件中的Tampermonkey_3.12_0.crx拖入页面，即可安装好插件。

安装好后， 在插件页选择选项按钮，进入如下配置页:

![](https://dn-joway.qbox.me/1460123362978_%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202016-04-08%2021.41.28.png)

在Zip栏点击选择文件，导入 chaoxing-hacked.zip 压缩包

![](https://dn-joway.qbox.me/1460123447255_%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202016-04-08%2021.41.40.png)

安装好后，在已安装脚本里:选中装好的脚本，

![](https://dn-joway.qbox.me/1460123510167_%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202016-04-08%2021.42.02.png)

选择启动

![](https://dn-joway.qbox.me/1460123537987_%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202016-04-08%2021.42.09.png)

然后就可以打开超星的视频页，当加载完成后，即可自动破解快进限制，之后就可以直接拖动到最后完成观看任务了~

---

如果不想安装插件，可以打开开发工具，手动输入 （ 会比较麻烦，且由于加载策略的不同，会有bug，推荐上面那种方法:

``` js
	var HtmlUtil = {
	    htmlEncodeByRegExp: function (str) {
	        var s = "";
	        if (str.length == 0) return "";
	        s = str.replace(/&/g,"&amp;");
	        s = s.replace(/</g,"&lt;");
	        s = s.replace(/>/g,"&gt;");
	        s = s.replace(/\'/g,"&#39;");
	        s = s.replace(/\"/g,"&quot;");
	        return s;
	    },
	    htmlDecodeByRegExp: function (str) {
	        var s = "";
	        if (str.length == 0) return "";
	        s = str.replace(/&amp;/g,"&");
	        s = s.replace(/&lt;/g,"<");
	        s = s.replace(/&gt;/g,">");
	        s = s.replace(/&#39;/g,"\'");
	        s = s.replace(/&quot;/g,"\"");
	        return s;
	    }
	};
	
	function getByClass(sClass){
	    var aResult = [];
	    var aEle = document.getElementsByTagName('*');
	    for (var i = 0; i < aEle.length; i++) {
	        var arr = aEle[i].className.split(/\s+/);
	        for(var j = 0; j < arr.length; j++){
	            if(arr[j] == sClass){
	                aResult.push(aEle[i]);
	            }
	        }
	    }
	    return aResult;
	}
	
	if (typeof mArg == "object") {
	    if (mArg.attachments[0].isPassed == true) {
	        alert('Warning: This job has been finished once.');
	    } else {
	        mArg.attachments[0].isPassed = true;
	        mArg.attachments[0].headOffset = 1478000;
	        mArg.attachments[0].playTime = 1478000;
	        mArg.attachments[0].job = false;
	        var aBox = getByClass("ans-attach-online");
	        if (aBox[0]) {
	            var htmlData = aBox[0].getAttribute("data");
	            var bBox = getByClass("ans-cc");
	            if (bBox[0]) {
	                bBox[0].innerHTML = '<p><iframe frameborder="0" scrolling="no" class="ans-module ans-attach-online ans-insertvideo-module" module="insertvideo" data="'
	                    + HtmlUtil.htmlEncodeByRegExp(htmlData)
	                    + '" type="online"></iframe><br/></p>';
	                uParse(".ans-cc", null, mArg);
	                alert('Hacked');
	            }
	        }
	    }
	}
```


