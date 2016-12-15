---
title: Java IO 性能优化一个小实例
comments: true
toc: true
tags:
  - Java
  - 性能
  - IO
categories: Java
---


### 现实需求: 

1. 把一个对象序列化，并保存至文件
2. 从文件中读出字节码并反序列化为对象

<!-- more -->
### 原代码:

``` java
        FileInputStream fileIn = new FileInputStream(filename);
        ObjectInputStream in = new ObjectInputStream(fileIn);
        Object object = in.readObject();
```

读取 24M 图片平均花费了 4000 ms 左右


### 优化:

``` java
        FileInputStream fileIn = new FileInputStream(filename);
        ObjectInputStream in = new ObjectInputStream(
                new BufferedInputStream(fileIn));
        Object object = in.readObject();
```

读取 24M 图片平均花费了 300 ms 左右


### 知其然，知其所以然:

原本文件是一个个字节地读的， 使用了BufferedInputStream后，它会首先把一段文件读入缓存内。

stackoverflow 里有人说 : [This will reduce I/O by a factor of 8.](http://stackoverflow.com/questions/23506651/why-is-inputstream-readobject-taking-so-much-of-time-reading-the-serialized-obje)

