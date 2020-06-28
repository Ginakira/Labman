from django.contrib.auth.models import AbstractUser
from django.db import models

from django.utils import timezone

# 用户
from iLab import settings


class User(AbstractUser):
    is_approved = models.BooleanField(default=False)  # 是否为已通过审核的正式成员


# 公告
class Notice(models.Model):
    title = models.CharField(max_length=255)  # 公告标题
    content = models.TextField()  # 公告内容
    publish_time = models.DateTimeField(default=timezone.now)  # 发布时间
    edit_time = models.DateTimeField(auto_now=True)  # 最后编辑时间
    priority = models.SmallIntegerField(default=1)  # 公告优先级 越大优先级越高 0为禁用
    publisher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 发布者


# 正式成员信息（档案）
class Archive(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 关联的用户（一对一）
    student_num = models.CharField(max_length=32, unique=True, null=True)  # 学号
    name = models.CharField(max_length=16, null=True)  # 真实姓名
    mobile_num = models.CharField(max_length=20, unique=True, null=True)  # 手机号
