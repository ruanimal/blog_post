title: MySQL在django的应用与设置
date: 9, 10, 2015 4:32 PM
categories: 编程
tags: 

---

### MySQL安装
- 检查MySQL是否安装 sudo netstat -tap | grep mysql
- 如果没有 sudo apt-get install mysql-server mysql-client
- 设置mysql的root用户的密码 

### MySQL的python模块
- MySQL-Python
```
	$ wget https://pypi.python.org/packages/source/M/MySQL-python/MySQL-python-1.2.5.zip
	$ unzip MySQL-python-1.2.5.zip
	$ sudo python setup.py install
```

- 若提示“EnvironmentError: mysql_config not found”
	`$ sudo apt-get install libmysqld-dev`

<!--more-->

### django中的设置
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', #设置为mysql数据库
        'NAME': 'dmyz',  #mysql数据库名
        'USER': 'root',  #mysql用户名，留空则默认为当前linux用户名
        'PASSWORD': 'root',   #mysql密码(怀疑有安全性问题)
        'HOST': '',  #留空默认为localhost
        'PORT': '',  #留空默认为3306端口
    }
}
```
另一种方法是使用mysql配置文件，参看[](https://docs.djangoproject.com/en/1.9/ref/databases/#mysql-notes)

### MySQL 数据库操作
- 进入mysql命令行 `mysql -uroot -p[密码]`
- 新建数据库 `create database name`
- 使用数据库 `use name`
- (可选)导入sql备份文件 `mysql –uroot –p[密码] -Dtest< .sql`

### 运行
- #### django1.6环境加south
```
python manage.py syncdb  # 创建表
python manage.py migrate  # 数据迁移可选
python manage.py runserver 
```

- #### django1.8+
```
python manage.py makemigrations appname  # 建立迁移脚本 
python manage.py migrate  # 数据迁移可选
python manage.py runserver 
```



