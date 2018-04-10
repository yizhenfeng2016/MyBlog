#检查端口是否被占用
echo "check uwsgi"
lsof -t -i tcp:9090
echo "check nginx"
lsof -t -i tcp:80
echo "check memcached"
ps -ef|grep memca
#启动memcached
echo "start memcached"
/usr/local/bin/memcached -u root -d  -p 11211 -c 256 -P /tmp/memcached.pid
sleep 2
#启动nginx和uwsgi
echo "start uwsgi and nginx"
uwsgi --ini /etc/uwsgi9090.ini &/usr/local/nginx-1.5.6/sbin/nginx