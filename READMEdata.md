branch data: 计划使用mongodb
https://www.runoob.com/docker/docker-install-mongodb.html

https://www.runoob.com/mongodb/mongodb-tutorial.html

https://www.runoob.com/python3/python-mongodb.html

运行mongodb:
docker run -itd --name mongo -p 27017:27017 mongo --auth

添加用户和设置密码:
docker exec -it mongo mongo admin
创建一个名为 admin，密码为 2333333 的用户。
>  db.createUser({ user:'admin',pwd:'2333333',roles:[ { role:'userAdminAnyDatabase', db: 'admin'},"readWriteAnyDatabase"]});
尝试使用上面创建的用户信息进行连接。
> db.auth('admin', '2333333')

