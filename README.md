# 用户注册系统

一个基于 Flask 和 MySQL 做的用户注册功能。

## 技术栈

后端：Python + Flask
数据库：MySQL
前端：HTML + CSS + JavaScript

## 功能

用户注册
密码加密存储
密码强度验证
用户名唯一性检查

## 如何运行

1. 安装 Python 3.6+
2. 安装 MySQL
3. 安装依赖：
   ```bash
   pip install flask pymysql
   ```
4. 创建数据库：
   ```sql
   CREATE DATABASE user_db;
   USE user_db;
   CREATE TABLE users (
       id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(50) UNIQUE,
       password VARCHAR(255)
   );
   ```
5. 修改 `config.py` 里的数据库密码
6. 运行：
   ```bash
   python app.py
   ```
7. 访问 http://127.0.0.1:5050

## 项目结构

```
├── app.py          # 主程序
├── db.py           # 数据库操作
├── config.py       # 配置文件
├── templates/
│   └── register1.html  # 前端页面
└── README.md       # 说明文档
```

## 作者

[Mei]