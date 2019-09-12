# GoChessParse

### Description：
围棋拍照识别

### Features：

1. 输出棋子位置矩阵
2. 自动检测 <9> <13> <19> 路棋盘类型
3. 逆透视变换视角修正
4. HTTP Detect API 
5. docker-compose 快速部署

### Quick Install：

```shell
cd GoChessParse
docker-compose up
```

### Usage：

```shell
python GoChessParse.py
```

- `run` :   启动HTTP-API服务端
- `test` : 单元测试
- `input_image`，`--image_path `输入图片
- `--help` : 输出帮助信息

###  Note：

- HTTP API后端flask，默认端口5000，生产环境使用Nginx端口转发
- upload文件夹保存用户上传图片，默认挂载到/var/upload

### Picture：

- 输入图


![nwxiSs.jpg](https://s2.ax1x.com/2019/09/12/nwxiSs.jpg)
	
	
- 输出矩阵

  [[0 0 0 0 0 2 1 0 1 0 1 0 2 2 2 2 0 2 0]  
 [0 0 0 0 2 2 1 0 1 0 1 2 1 1 2 0 0 0 0]  
 [0 0 0 0 2 1 1 1 2 1 1 2 1 1 2 0 0 2 2]  
 [2 2 0 2 2 1 2 2 2 2 2 1 1 0 0 2 0 2 1]  
 [2 1 2 2 0 2 0 0 0 0 0 2 1 1 0 2 2 1 1]  
 [1 1 1 1 2 0 0 0 0 0 2 0 2 1 2 2 1 1 2]  
 [0 0 0 0 1 2 2 0 0 0 0 2 0 2 2 1 1 1 0]  
 [0 0 0 1 0 1 2 0 0 0 0 0 0 0 0 2 1 1 1]  
 [0 0 0 1 1 2 2 0 0 0 0 0 0 0 0 2 1 0 0]  
 [0 0 0 0 1 2 2 0 0 2 0 0 0 0 0 2 1 1 1]  
 [0 0 0 1 1 2 0 0 0 0 0 0 0 0 0 2 1 2 2]  
 [0 0 0 1 2 0 0 0 0 0 0 0 0 0 2 0 2 2 0]  
 [0 0 0 1 2 2 0 0 0 0 0 2 0 0 2 0 2 2 0]  
 [0 0 0 1 1 2 0 0 0 0 0 0 0 2 0 2 2 0 0]  
 [0 0 0 0 1 2 2 2 2 0 0 0 0 0 2 2 1 2 2]   
 [0 0 0 1 0 1 1 1 1 2 2 2 2 1 1 1 1 1 2]  
 [0 0 1 0 0 0 1 0 0 1 1 1 1 1 0 0 1 0 1]  
 [0 0 0 0 0 0 0 1 1 0 0 0 0 0 0 0 0 0 0]  
 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]]    

- 处理过程


[![nwg3pd.gif](https://s2.ax1x.com/2019/09/11/nwg3pd.gif)](https://imgchr.com/i/nwg3pd)
