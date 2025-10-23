# 简易文件管理系统

> 文件的上传仅为添加数据库数据，并未真实上传

## 一. 基本环境

1. Python

   后端使用django框架，使用pymysql连接数据库

2. MySQL

   使用MySQL作为数据库管理工具

## 二. 部署

### 1. 安装MySQL

### 2. 配置python环境

``pip install django,pymysql``

### 3. 新建数据库并修改配置文件

在MySQL中创建数据库存储项目数据

修改```\websec\websec\settings.py```以下字段：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  
        'NAME': '',  # 数据库名
        'USER': '',  # 用户名
        'PASSWORD': '',  # 密码
        'HOST': 'localhost',  # 数据库服务器地址
        'PORT': 3306,  # 端口号（MySQL默认3306）
    }

}
```

### 4. 创建数据表

使用Django内置ORM对数据库进行管理，在`websec\`目录下运行以下命令：

> 此处的`websec\`目录指的是最高级目录

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. 运行

配置成功，在`websec\`目录下运行以下命令：

> 此处的`websec\`目录指的是最高级目录

```python manage.py runserver```

访问127.0.0.1即可使用

