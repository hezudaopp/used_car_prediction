# 调用方法
自带http: 

	uwsgi --http :8000 --wsgi-file used_car_price_prediction/application.py

第三方web server: 

	uwsgi --socket 0.0.0.0:8000 --wsgi-file used_car_price_prediction/application.py --master --processes 4 --threads 2 --stats 127.0.0.1:9191

# pre-execution
1,升级python到2.7：

wget http://www.python.org/ftp/python/2.7.10/Python-2.7.10.tar.xz

unxz Python-2.7.10.tar.xz

tar -vxf Python-2.7.10.tar

./configure

make && make install

安装好Python2.7之后我们需要先把Python2.6备份起来，然后再对yum的配置进行修改，如果不进行这一步操作的话，执行yum命令将会提示你Python的版本不对。

执行以下命令，对Python2.6进行备份，然后为Python2.7创建软链接

mv /usr/bin/python /usr/bin/python2.6.6

ln -s /usr/local/bin/python2.7 /usr/bin/python



安装pip

下载最新版的pip，然后安装

wget https://bootstrap.pypa.io/get-pip.py

python get-pip.py

查找pip的位置

whereis pip

找到pip2.7的路径，为其创建软链作为系统默认的启动版本

ln -s /usr/local/bin/pip2.7 /usr/bin/pip

pip安装完毕，现在可以用它下载安装各种包了 :)



运行used_car_prediction所需安装的pip包：

DBUtils (1.1)

MySQL-python (1.2.5)

numpy (1.11.1)

pip (8.1.2)

scikit-learn (0.17.1)

scipy (0.17.1)

sklearn

pandas

uwsgi



如果需要替换因为pip模块库经常速度很慢，需要替换国内的镜像地址的话：

如果不存在的话，就创建目录和文件

1: 进入~/.pip目录

2: 打开vi pip.conf

3: 添加

[global]

index-url = http://pypi.douban.com/simple

trusted-host = pypi.douban.com

timeout = 6000