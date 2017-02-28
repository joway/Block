# 深入探究 Docker 内核

## Docker 总架构图


![](http://cdn1.infoqstatic.com/statics_s2_20161220-0322/resource/articles/docker-source-code-analysis-part1/zh/resources/001.jpg)

## 概述

二进制 docker 文件的作用包含了  client 和 daemon 两部分, 在docker命令执行时，通过传入的参数来判别Docker Daemon与Docker Client。

## Docker Client

Docker Client可以通过以下三种方式和Docker Daemon建立通信：tcp://host:port，unix://path_to_socket和fd://socketfd。

Docker Client发送容器管理请求后，由Docker Daemon接受并处理请求，当Docker Client接收到返回的请求相应并简单处理后，Docker Client一次完整的生命周期就结束了。当需要继续发送容器管理请求时，用户必须再次通过docker可执行文件创建Docker Client。

## Docker Daemon

Docker Daemon是Docker架构中一个常驻在后台的系统进程，功能是：接受并处理Docker Client发送的请求。该守护进程在后台启动了一个Server，Server负责接受Docker Client发送的请求；接受请求后，Server通过路由与分发调度，找到相应的Handler来执行请求。

Docker Daemon的架构，大致可以分为以下三部分：Docker Server、Engine和Job。

![](http://cdn1.infoqstatic.com/statics_s2_20161220-0322/resource/articles/docker-source-code-analysis-part1/zh/resources/002.jpg)

### Server

Docker Server在Docker架构中是专门服务于Docker Client的server。该server的功能是：接受并调度分发Docker Client发送的请求。Docker Server的架构如图:

![](http://cdn1.infoqstatic.com/statics_s2_20161220-0322/resource/articles/docker-source-code-analysis-part1/zh/resources/003.jpg)

原则上，Docker Server的运行是众多job中的一个 。


### Engine

Engine是Docker架构中的运行引擎，同时也Docker运行的核心模块。它扮演Docker container存储仓库的角色，并且通过执行job的方式来操纵管理这些容器。

### Job

一个Job可以认为是Docker架构中Engine内部最基本的工作执行单元。

## Docker Registry
Docker Registry是一个存储容器镜像的仓库。而容器镜像是在容器被创建时，被加载用来初始化容器的文件架构与目录。

## Graph

Graph在Docker架构中扮演已下载容器镜像的保管者，以及已下载容器镜像之间关系的记录者。一方面，Graph存储着本地具有版本信息的文件系统镜像，另一方面也通过GraphDB记录着所有文件系统镜像彼此之间的关系。

![](http://cdn1.infoqstatic.com/statics_s2_20161220-0322/resource/articles/docker-source-code-analysis-part1/zh/resources/004.jpg)

## Driver

在Docker Driver的实现中，可以分为以下三类驱动：graphdriver、networkdriver和execdriver。

### graphdriver

graphdriver 主要用于完成容器镜像的管理，包括存储与获取。即当用户需要下载指定的容器镜像时，graphdriver 将容器镜像存储在本地的指定目录；同时当用户需要使用指定的容器镜像来创建容器的rootfs时，graphdriver从本地镜像存储目录中获取指定的容器镜像。

在graphdriver的初始化过程之前，有4种文件系统或类文件系统在其内部注册，它们分别是aufs、btrfs、vfs和devmapper。而Docker在初始化之时，通过获取系统环境变量”DOCKER_DRIVER”来提取所使用driver的指定类型。而之后所有的graph操作，都使用该driver来执行。

#### PS: docker1.9 以后 新增 Overlay 方式的文件系统, 推荐使用 Overlay

![](http://cdn1.infoqstatic.com/statics_s2_20161220-0322/resource/articles/docker-source-code-analysis-part1/zh/resources/005.jpg)

### networkdriver

networkdriver的用途是完成Docker容器网络环境的配置，其中包括Docker启动时为Docker环境创建网桥；Docker容器创建时为其创建专属虚拟网卡设备；以及为Docker容器分配IP、端口并与宿主机做端口映射，设置容器防火墙策略等。networkdriver的架构如图：

![](http://cdn1.infoqstatic.com/statics_s2_20161220-0322/resource/articles/docker-source-code-analysis-part1/zh/resources/006.jpg)

### execdriver

execdriver作为Docker容器的执行驱动，负责创建容器运行命名空间，负责容器资源使用的统计与限制，负责容器内部进程的真正运行等。在execdriver的实现过程中，原先可以使用LXC驱动调用LXC的接口，来操纵容器的配置以及生命周期，而现在execdriver默认使用native驱动，不依赖于LXC。

![](http://cdn1.infoqstatic.com/statics_s2_20161220-0322/resource/articles/docker-source-code-analysis-part1/zh/resources/007.jpg)

## libcontainer (runc)

设计初衷是希望该库可以不依靠任何依赖，直接访问内核中与容器相关的API。

Docker可以直接调用libcontainer，而最终操纵容器的namespace、cgroups、apparmor、网络设备以及防火墙规则等。

![](http://cdn1.infoqstatic.com/statics_s2_20161220-0322/resource/articles/docker-source-code-analysis-part1/zh/resources/008.jpg)


## Docker container

Docker container（Docker容器）是Docker架构中服务交付的最终体现形式。

Docker按照用户的需求与指令，订制相应的Docker容器：

- 用户通过指定容器镜像，使得Docker容器可以自定义rootfs等文件系统；
- 用户通过指定计算资源的配额，使得Docker容器使用指定的计算资源；
- 用户通过配置网络及其安全策略，使得Docker容器拥有独立且安全的网络环境；
- 用户通过指定运行的命令，使得Docker容器执行指定的工作。

![](http://cdn1.infoqstatic.com/statics_s2_20161220-0322/resource/articles/docker-source-code-analysis-part1/zh/resources/009.jpg)

## 命令剖析

### docker pull

docker pull命令的作用为：从Docker Registry中下载指定的容器镜像，并存储在本地的Graph中

![](http://cdn1.infoqstatic.com/statics_s2_20161220-0322/resource/articles/docker-source-code-analysis-part1/zh/resources/010.jpg)


### docker run

第一，创建Docker容器所需的rootfs；第二，创建容器的网络等运行环境，并真正运行用户指令。因此，在整个执行流程中，Docker Client给Docker Server发送了两次HTTP请求，第二次请求的发起取决于第一次请求的返回状态。

![](http://cdn1.infoqstatic.com/statics_s2_20161220-0322/resource/articles/docker-source-code-analysis-part1/zh/resources/011.jpg)



