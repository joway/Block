---
title: Hexo折腾记——终极加速:全线接入CDN
comments: true
categories: Hexo
tags:
	- hexo
	- 前端
	- blog
	- 七牛
	- CDN
	- 加速
---


前段时间一不小心看到了七牛支持HTTPS证书导入，就想去试试把博客全线接入CDN(啊，说好的好好读书不折腾博客了呢 ? 😂)，不过七牛这货也是坑，光是证书录入就花了快一个星期，完了以后我改个源站又是好几天，最后改个缓存策略又要等。严重怀疑七牛纯粹是手动来搞这些东西。。。同样的东西，又拍云就分分钟生效完成。

<!--more-->

上一篇文章里我讲了因为载入的资源太多，我用插件把js,css全部内联了，但是如果接入了CDN后，首先由于缓存的原因，我不能够把html给缓存太长时间，否则我更新一篇文章在客户端生效得等好长时间，这样的话，如果我全部内联，相当于大部分资源都有去缓存，虽然CDN仍旧能够以其速度优势来弥补单个文件过大的缺陷，但显然这种做法还是不够高效。

由于我并不是特别清楚全部内联减少请求次数，与减小单个文件体积两种做法之间具体的性能差异，所以我两种方式都部署了一遍，最后从"手感"上判断后一种方法似乎响应更加迅速。之所以说"手感"，是因为有好多次我都发现明明数据很好看，但是实际浏览器访问的时候还是感觉很慢，加载也不流畅。而接入七牛CDN后，虽然数据上不怎么好看，有时候甚至会有10秒以上的加载时间，但是的确响应上流畅多了，目前我还不是特别清楚这种差异是由于什么。

接入七牛CDN的过程非常简单，首先，写个脚本每次在构建的时候上传public目录至七牛，然后在七牛那边，配置一个https的证书，由于我只是个博客，并没有太大的安全需求，搞个https纯粹为了防劫持和装逼，所以我很开心地就把私钥上传上去了(😂）. 建议在上传前就做好源站配置和缓存策略，否则，每次更改都需要很长时间等待。

关于上传脚本，可以用我写的python 上传脚本，也可以用gulp的一个插件: [gulp-qiniu](https://github.com/hfcorriez/gulp-qiniu)

注意，七牛自身不支持目录，而是以文件前缀的形式来指定文件路经，所以在上传的时候要把路径指定好。

PS: 七牛HTTPS弄好后，需要把CDN配到七牛上去，然而我用的cloudxns无法让mx记录和cname记录在@下共存。查阅了cloudxns的解释后，才发现之前我一直在dnspod上两个一起设置，是有可能导致我的域名邮箱丢件的。cloudxns为这种情况提供了一种解决方案: 用 www.joway.wang 域名cname 到 七牛上，然后joway.wang 用 link 记录到www.joway.wang 上。这样就解决了问题，虽然我没看懂link记录是个什么鬼。。


上传目录的Python 脚本如下: 

``` python
import os
import sys
from easy_qiniu import SevenCow

prefix_dir = sys.path[0]+'/public'

#可获取文件夹内全部文件名(包括子文件夹)
def get_all_files(DirectoryPath):
    filenamesList = []
    for dirpath, dirnames, filenames in os.walk(DirectoryPath):
        """
        dirpath：当前遍历文件夹全名
        dirnames：当前文件夹内子文件夹名
        filenames：当前文件夹下文件名列表(不包括子文件夹里的文件)
        """
        for filename in filenames:
            filenamesList.append(dirpath + '/' + filename)#全名
    return filenamesList


#生成网站根目录形式的文件名
def get_root_filename(fullname):
    dir_path = sys.path[0]
    return fullname[len(prefix_dir) + 1:len(fullname)].replace('\\','/')

#生成{目标文件名:源文件名,...}形式的字典
def get_filenames_dict(filenamesList=[]):
    filenames_dict = {}
    for filename in filenamesList:
        filenames_dict[get_root_filename(filename)] = filename
    return filenames_dict

#上传，根据返回值判断是否成功
def upload_into_qiniu(access_key,secret_key,bucket_name,director_path=sys.path[0]):
    try:
        sc = SevenCow(access_key,secret_key)
        sc.delete_files(bucket_name,sc.list_file_names(bucket_name)[0])
        print('Delete Successful')
        sc.upload_files(bucket_name,get_filenames_dict(get_all_files(director_path)))
    except:
        return False
    else:
        return True

access_key = ''
secret_key = ''
bucket_name = 'hexo-blog'
if(upload_into_qiniu(access_key,secret_key,bucket_name, director_path=prefix_dir)):
    print('Bak Successful')
else:
    print('Bak Error')
```



easy_qiniu.py:

``` python 
from qiniu import  Auth
from qiniu import put_file
from qiniu import BucketManager
from qiniu import build_batch_stat
from qiniu import build_batch_copy
from qiniu import build_batch_move
from qiniu import build_batch_delete
from qiniu import etag

import requests
import mimetypes


#class SevenCowException(Exception):
#    def __init__(self,status_code,content):
#        self.url = url
#        self.status_code = status_code
#        self.content = content
#        Exception.__init__(self, content)

class SevenCow(object):
    def __init__(self, access_key,secret_key):
        self.__access_key = access_key
        self.__secret_key = secret_key
        #使用access_key,secret_key登陆七牛，得到Auth类型返回值，以它作为后续操作凭证
        self.__auth = Auth(access_key, secret_key)

        

    # 上传本地文件(断点续上传、分块并行上传)
    def upload_files(self,bucket_name='',filedict={},
                     mime_type='',params={'x:a': 'a'}):
        """Args:
        bucket_name:'bucket_name'
        filedict: {'key':'localfile',...}
        mime_type: mime_type
        params: eg {'x:var': 'var'} 
        """

        """
        params用法:
        params={'x:price':'price','x:location':'location'}
        """
        # 上传本地文件(断点续上传、分块并行上传)
        rets = []
        infos = []
        for key in filedict.keys():
            #上传策略仅指定空间名和上传后的文件名，其他参数为默认值
            token = self.__auth.upload_token(bucket_name, key)
            progress_handler = lambda progress, total: progress
            if(mime_type == ''):
                ret,info = put_file(token, key, filedict[key], params ,mime_type=mimetypes.guess_type(key)[0], progress_handler=progress_handler)
            else:
                ret,info = put_file(token, key, filedict[key], params ,mime_type=mime_type, progress_handler=progress_handler)
            #assert ret['key'] == key
            rets.append(ret)
            infos.append(info)
        return rets,infos


    def download_files(self,url='',filedict={}):
        """Args:
        url: 'url'
        filedict: {'key':'localfile',...}
        """
        if(url[0:4].upper() != 'HTTP'):
            url = 'http://' + url
        status_codes = []
        for fkey in filedict.keys():
            with open(filedict[fkey], "wb") as file:
                r = requests.get(url + '/' + fkey,timeout=5)
                status_codes.append(r.status_code)
                file.write(r.content)
        return status_codes


    # 获取文件信息
    def get_file_info(self,bucket_name,keys=[]):
        """Args:
        bucket_name:'bucket_name'
        keys:  ['fileName1','fileName2']
        """
        bucket = BucketManager(self.__auth)
        ops = build_batch_stat(bucket_name, keys)
        ret, info = bucket.batch(ops)
        return ret,info


    # 复制文件
    def copy_files(self,source_bucket,target_bucket,pathdict={}):
        """Args:
        source_bucket： 'source_bucket'
        target_bucket:  'target_bucket'
        pathdict: {'source_file_name':'target_file_name',...}
        """
        bucket = BucketManager(self.__auth)
        ops = build_batch_copy(source_bucket, pathdict, target_bucket)
        ret, info = bucket.batch(ops)
        return ret,info


    # 移动文件
    def move_files(self,source_bucket,target_bucket,pathdict={}):
        """Args:
        source_bucket： 'source_bucket'
        target_bucket:  'target_bucket'
        pathdict: {'source_file_name':'target_file_name',...}
        """
        bucket = BucketManager(self.__auth)
        ops = build_batch_move(source_bucket, pathdict, target_bucket)
        ret, info = bucket.batch(ops)
        return ret,info


    # 删除文件
    def delete_files(self,source_bucket,pathlist=[]):
        """Args:
        source_bucket： 'source_bucket'
        pathlist: ['source_file_name',...]
        """
        bucket = BucketManager(self.__auth)
        ops = build_batch_delete(source_bucket, pathlist)
        ret, info = bucket.batch(ops)
        return ret,info

    # 列出所有文件
    def list_file_names(self,bucket_name, prefix=None, marker=None, limit=None, delimiter=None):
        """
        Args:
            bucket:     空间名
            prefix:     列举前缀
            marker:     列举标识符(首次为None)
            limit:      单次列举个数限制(默认列举全部)
            delimiter:  指定目录分隔符
            
        Returns:
            pathlist: ['file_name',...]
        """
        file_name_list = []
        bucket = BucketManager(self.__auth)
        marker = None
        eof = False
        while eof is False:
            ret, eof, info = bucket.list(bucket_name, prefix=prefix, marker=marker, limit=limit)
            marker = ret.get('marker', None)
            for item in ret['items']:
                file_name_list.append(item['key'])
        return file_name_list,eof

    # 抓取资源
    def fetch_files_from_net_to_qiniu(self,bucket_name,pathdict={}):
        """Args:
        bucket_name： 'bucket_name'
        pathdict: {'source_file_name':'target_file_name',...}
        """
        bucket = BucketManager(self.__auth)
        rets=[]
        infos=[]
        for p in pathdict.keys():
            ret, info = bucket.fetch(pathdict[p], bucket_name,p)
            rets.append(ret)
            infos.append(info)
        return rets,infos

    # 更新镜像资源
    def update_image_source(self,bucket_name,pathlist=[]):
        """Args:
        bucket_name： 'bucket_name'
        pathlist: ['file_name',...]
        !需要提前对仓库设置镜像源!
        """

        bucket = BucketManager(self.__auth)
        rets=[]
        infos=[]
        for p in pathlist:
            ret, info = bucket.prefetch(bucket_name, p)
            rets.append(ret)
            infos.append(info)
        return rets,infos
```