# ubuntu 安装docker

```
# 这个方法安装的不是最新的docker
sudo apt-get install docker.io

# 使用中科大的源
vim /etc/docker/daemon.json

{
    "registry-mirrors": ["https://docker.mirrors.ustc.edu.cn"]

}

＃　todo安装最新版本的
```