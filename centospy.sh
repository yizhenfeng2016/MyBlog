#!/bin/bash
# a script to install python 2.7 on CentOS 6.x system.
# CentOS 6.x has python 2.6 by default, while some software (e.g. django1.7)
# need python 2.7.
 
# install some necessary tools & libs
echo "install some necessary tools & libs"
yum install -y update # 更新内置程序
yum groupinstall -y development # 安装所需的development tools
yum install -y zlib-dev openssl-devel sqlite-devel bzip2-devel # 安装附加包
yum install xz-libs # 安装XZ解压库(可选)
sleep 5
 
echo "download and install python"
cd /usr/home/
wget http://www.python.org/ftp/python/2.7.6/Python-2.7.6.tar.xz # 下载源码包
sleep 10
#解压源码包,分为两步
xz -d Python-2.7.6.tar.xz
tar -xvf Python-2.7.6.tar
#编译与安装,先进入源码目录
cd Python-2.7.6
./configure --prefix=/usr/local
make && make install
sleep 5
 
echo "change python version"
mv /usr/bin/python /usr/bin/python2.6.6
ln -s /usr/local/bin/python2.7 /usr/bin/python
sleep 5

# install setuptools
echo "-------------------------"
echo "install setuptools"
cd /usr/home/
wget https://pypi.python.org/packages/source/s/setuptools/setuptools-0.6c11.tar.gz
sleep 10
tar zxf setuptools-0.6c11.tar.gz
cd setuptools-0.6c11/
python setup.py build
python setup.py install
sleep 5
 
# install pip for the new python
echo "-------------------------"
echo "install pip for the new python"
cd /usr/home/
wget https://pypi.python.org/packages/source/p/pip/pip-1.3.1.tar.gz --no-check-certificate
sleep 10    
tar -xzvf pip-1.3.1.tar.gz
cd pip-1.3.1
python setup.py install

echo "Finished. Well done!"
echo "If 'python -V' still shows the old version, you may need to re-login."
echo "And/or set /usr/local/bin in the front of your PATH environment variable."
echo "-------------------------"