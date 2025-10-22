from django.db import models

"""
    models.py中定义数据表，通过以下命令创建表
    python manage.py makemigrations
    python manage.py migrate
    删除表只需将代码中的相应部位注释，再执行上述命令即可实现
    增加属性直接在类里增加定义即可
"""


# Create your models here.
# 在MySQL中创建对应的一个表
class UserInfo(models.Model):
    # 创建字段
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=64)


class FileInfo(models.Model):
    file_name = models.TextField(max_length=255, verbose_name="文件名")
    file_size = models.CharField(max_length=32, verbose_name="文件大小", null=True, blank=True)
    upload_time = models.DateTimeField()
    upload_user = models.TextField(max_length=128, verbose_name="上传用户", null=True, blank=True)

