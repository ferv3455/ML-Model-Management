branch data: 计划使用mongodb
https://www.runoob.com/docker/docker-install-mongodb.html

https://www.runoob.com/mongodb/mongodb-tutorial.html

https://www.runoob.com/python3/python-mongodb.html

控制台运行mongodb:
docker run -itd --name mongo -p 27017:27017 mongo --auth

添加用户和设置密码:
docker exec -it mongo mongo admin
创建一个名为 admin，密码为 2333333 的用户。
>  db.createUser({ user:'admin',pwd:'2333333',roles:[ { role:'userAdminAnyDatabase', db: 'admin'},"readWriteAnyDatabase"]});
尝试使用上面创建的用户信息进行连接。
> db.auth('admin', '2333333')
在data.py中也需要用相应的语句进行身份验证

或者直接在docker中运行mongodb,则不需要用户名、密码
