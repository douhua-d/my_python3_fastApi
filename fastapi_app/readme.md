<!-- 启动 FastAPI 服务 -->
<!-- main:app 表示 main.py 文件里的 app 对象 -->
<!-- --reload 表示代码变动时自动重启（开发时用） -->
uvicorn main:app --reload



<!--  访问和测试
打开浏览器访问 http://127.0.0.1:8000/
你会看到：{"message": "Hello, FastAPI!"}
访问自动生成的接口文档：
http://127.0.0.1:8000/docs -->


<!--   brew install mysql
  brew services start mysql -->

  <!-- mysql -u root -p
# 输入密码后进入 MySQL 命令行

CREATE DATABASE testdb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE testdb;

# 创建用户表
CREATE TABLE user (
  id INT PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(50) NOT NULL,
  email VARCHAR(100) NOT NULL
);

# 插入测试数据
INSERT INTO user (username, email) VALUES ('alice', 'alice@example.com'), ('bob', 'bob@example.com'); -->


<!-- # 启动 MySQL 服务
brew services start mysql

# 停止 MySQL 服务
brew services stop mysql

# 重启 MySQL 服务
brew services restart mysql

# 查看所有服务状态
brew services list -->


<!--  登录 MySQL 并创建数据库
 mysql -u root -p
# 输入密码后进入 MySQL 命令行

CREATE DATABASE testdb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE testdb;

# 创建用户表
CREATE TABLE user (
  id INT PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(50) NOT NULL,
  email VARCHAR(100) NOT NULL
);

# 插入测试数据
INSERT INTO user (username, email) VALUES ('alice', 'alice@example.com'), ('bob', 'bob@example.com');-->


<!-- 启动后端服务
Apply to main.py
Run
uvicorn main:app --reload
访问 http://127.0.0.1:8001/users 获取用户列表
访问 http://127.0.0.1:8001/users/1 获取某个用户信息 -->


<!-- uvicorn main:app --reload --port 8001 -->