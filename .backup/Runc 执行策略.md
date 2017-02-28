# Runc 使用总结

## 概述

runc 本质是一个 libcontainer + 调用以管理使用 Libcontainer 的命令行工具 。

内核版本最低要求为2.6，最好是3.8，这与内核对namespace的支持有关。

## 容器包组成

### config.json

基本配置文件，包括与宿主机独立的和应用相关的特定信息，如安全权限、环境变量和参数等。

### rootfs/

根文件系统目录，包含了容器执行所需的必要环境依赖，如/bin、/var、/lib、/dev、/usr等目录及相应文件。rootfs目录必须与包含配置信息的config.json文件同时存在容器目录最顶层。


## 运行时文件 

### /run/runc/<containerID>/state.json:

state.json文件中包含的具体信息需要有：

- 版本信息：存放OCI标准的具体版本号。
- 容器ID：通常是一个哈希值，也可以是一个易读的字符串。在state.json文件中加入容器ID是为了便于之前提到的运行时hooks只需载入state.json就可以定位到容器，然后检测state.json，发现文件不见了就认为容器关停，再执行相应预定义的脚本操作。
- PID：容器中运行的首个进程在宿主机上的进程号。
- 容器文件目录：存放容器rootfs及相应配置的目录。外部程序只需读取state.json就可以定位到宿主机上的容器文件目录。 标准的容器生命周期应该包含三个基本过程。
	- 容器创建：创建包括文件系统、namespaces、cgroups、用户权限在内的各项内容。
	- 容器进程的启动：运行容器进程，进程的可执行文件定义在的config.json中，args项。
	- 容器暂停：容器实际上作为进程可以被外部程序关停（kill），然后容器标准规范应该包含对容器暂停信号的捕获，并做相应资源回收的处理，避免孤儿进程的出现。


## 依赖技术

### Namespace

Linux Namespace是Linux提供的一种内核级别环境隔离的方法, 提供了对UTS、IPC、mount、PID、network、User等的隔离机制。

主要含三个系统调用:

- clone() – 实现线程的系统调用，用来创建一个新的进程，并可以通过设计上述参数达到隔离。
- unshare() – 使某进程脱离某个namespace
- setns() – 把某进程加入到某个namespace


### CGroup

Linux CGroup全称Linux Control Group， 是Linux内核的一个功能，用来限制，控制与分离一个进程组群的资源（如CPU、内存、磁盘输入输出等）。

主要提供了如下功能：

- Resource limitation: 限制资源使用，比如内存使用上限以及文件系统的缓存限制。
- Prioritization: 优先级控制，比如：CPU利用和磁盘IO吞吐。
- Accounting: 一些审计或一些统计，主要目的是为了计费。
- Control: 挂起进程，恢复执行进程。

## Libcontainer

### 作用

基于Go语言实现，通过管理namespaces、cgroups、capabilities以及文件系统来进行容器控制。容器是一个可管理的执行环境，与主机系统共享内核，可与系统中的其他容器进行隔离。

### 过程

Libcontainer创建容器进程时需要做初始化工作，我们把负责创建容器的进程称为父进程，容器进程称为子进程。父进程需要与容器的init进程通过通过管道进行同步通信。

	
## 参考文献

[DockOne技术分享（二十八）： OCI标准和runC原理解读](http://dockone.io/article/776)
[Docker背后的容器管理——Libcontainer深度解析
](http://www.infoq.com/cn/articles/docker-container-management-libcontainer-depth-analysis)
