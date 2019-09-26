docker build -t nuodb:latest .<br>
docker run -d -p 48004:48004 -p 48005:48005 -p 48006:48006 -p 8888:8888 -p 9001:9001 nuodb:latest<br>
service nuoagent start<br>
service nuorestsvc start<br>
bin/nuodbmgr --broker localhost --password bird<br>
https://github.com/yrobla/docker-nuodb/blob/master/Dockerfile<br>
