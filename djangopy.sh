#!/bin/bash
# a script to install python 2.7 on CentOS 6.x system.
# CentOS 6.x has python 2.6 by default, while some software (e.g. django1.7)
# need python 2.7.

echo "start"
echo "install nginx"
sleep 2
cd /usr/home/
wget http://nginx.org/download/nginx-1.5.6.tar.gz
tar zxf nginx-1.5.6.tar.gz
cd nginx-1.5.6
./configure --prefix=/usr/local/nginx-1.5.6
make && make install

echo "install uwsgi"
sleep 2
pip install uwsgi
uwsgi --version

echo "install django==1.8.17"
sleep 2
pip install django==1.8.17

echo "install django-suit==0.2.25"
sleep 2
pip install django-suit==0.2.25

echo "install django-ckeditor==5.4.0"
sleep 2
pip install django-ckeditor==5.4.0

echo "install Pillow"
sleep 2
#安装依懒库
yum install libjpeg-turbo-devel
sleep 1
pip install Pillow

echo "install requests==2.18.4"
sleep 2
pip install requests==2.18.4

echo "install M2Crypto==0.27.0"
sleep 2
#先安装PCRE
yum search pcre
yum install pcre-devel.x86_64 #（根据搜索结果自己选）
sleep 1
#安装swing
cd /usr/home/
sleep 2
wget -O swig-3.0.7.tar.gz http://prdownloads.sourceforge.net/swig/swig-3.0.7.tar.gz
tar zxf swig-3.0.7.tar.gz
cd swig-3.0.7
./configure --prefix=/usr
make && make install
#安装typing
pip install typing
#安装M2Crypto-0.27
echo "make M2Crypto"
sleep 2
tar -xzvf frida-android-M2Crypto-0.27.0.tar.gz
cd frida-android-M2Crypto-0.27.0
python setup.py install

#安装libevent
echo "install libevent"
cd /usr/home/
sleep 2
wget https://github.com/libevent/libevent/releases/download/release-2.1.8-stable/libevent-2.1.8-stable.tar.gz
tar zxvf libevent-2.1.8-stable.tar.gz
cd libevent-2.1.8-stable
./configure --prefix=/usr
make && make install

#安装memcached
echo "install memcached"
cd /usr/home/
sleep 2
wget http://www.memcached.org/files/memcached-1.4.24.tar.gz
tar zxvf memcached-1.4.24.tar.gz
cd memcached-1.4.24
./configure --with-libevent=/usr
make && make install

#安装python-memcached
echo "install python-memcached==1.59"
sleep 2
pip install python-memcached==1.59
echo "end"

