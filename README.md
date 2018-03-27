# V-rep based ARIE Visualization
ARIE visualization package based on v-rep simulation environment



## 配置方法

1. 安装V-REP（目前在3.4.0版本上可正常运行）；
2. 安装Python 3.5（可通过Anaconda安装依赖的包）；
3. 从https://gitee.com/raysworld/V-rep-based-ARIE-Visualization下载源代码；
4. ​







## V-rep based ARIE Visualization

说明：

该仿真主要基于V-Rep的碰撞检测和remote API，利用Matlab或者Python作为脚本语言编写仿真逻辑，通过TCP协议与V-Rep仿真环境通信，从而实现三维环境约束域的可视化。



主要分两部分配置：服务器端（V-Rep）和脚本端（Matlab/Python）



### 服务器端（V-Rep）配置

所需文件放置在/vrep_files文件夹下：

```RemoteApi_ARIE_Assembly.ttt```

后缀名为.ttt的是V-Rep的场景文件，里面包含了一些V-Rep的remote API没有提供的函数（通过自定义函数功能实现）。具体请参见remoteApiCommandServer上绑定的Customization script。



```remoteApiConnections.txt```

该文件是V-Rep安装后存在与其安装目录内的文件，里面定义了所有V-Rep在启动时将自动开启的remote API service。由于我们可以利用命令行实现程序多开，而并不需要一个程序开启多个端口，因此可以利用```//```将该文件内的所有内容都注释掉。



