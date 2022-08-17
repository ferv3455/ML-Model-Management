## 软件学院2022年暑期小学期大作业

### 环境需求

1. Ubuntu 20.04 (操作系统)

2. NodeJS v16.16.0 (前端框架)

   ```
   安装前端相关依赖包方法：
   cd client
   npm install
   ```

3. Python 3.8.10 (后端框架)

   ```
   安装后端相关依赖包方法：
   cd server
   pip install -r requirements.txt
   ```

3. Java openJDK version 11.0.16 (PMML解析)

4. Docker version 20.10.17 (后端数据库服务器)

   ```
   Docker 获取Redis最新版镜像
   docker pull redis:latest
   
   Docker 在端口16379运行Redis
   docker run -itd --name redis-test -p 16379:6379 redis
   
   Docker 获取MongoDB最新版镜像
   docker pull mongo:latest
   
   Docker 在端口27017运行MongoDB
   docker run -itd --name mongo -p 27017:27017 mongo
   ```

   

   

### 运行方式

前端:
```
cd client
npm run serve
```
后端:
```
cd server
python3 app.py
```
前后端运行后，浏览器访问http://localhost:8080 即可

