from django.db import models
from django.contrib.auth.models import AbstractUser

#访问权限
PRIVATE = 0
GROUP = 1
PUBLIC = 2

class Question(models.Model):
    content = models.TextField()#题目内容
    correct_answer = models.TextField()#正确答案
    question_type = models.IntegerField()#题目类型

class ErrorLog(models.Model):#错误日志的model,放在user和admin中
    Question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question')#问题
    wrong_answer = models.TextField()#错误的答案
    error_frequency = models.IntegerField()#错频
    question_count = models.IntegerField()#错题总数

class User(AbstractUser):#这个AbstractUser自己包含用户名和密码
    errorlog = models.ForeignKey(ErrorLog, on_delete=models.CASCADE, related_name='error_log')
    pass

class Admin(AbstractUser):#这个AbstractUser自己包含用户名和密码
    errorlog = models.ForeignKey(ErrorLog, on_delete=models.CASCADE, related_name='error_log')
    pass

class Group(models.Model):
    name = models.CharField(max_length=100)#组名
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator')#创建者
    users = models.ManyToManyField(User, related_name='groups')#用户成员

class QuestionSet(models.Model):
    name = models.CharField(max_length=100)#问题集合名称
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator')#创建者
    permission = models.IntegerField()#访问权限
    group = models.CharField(max_length=100, null=True)#如果访问权限是GROUP，则该字段用于存储组名称
    group_creator_name = models.CharField(max_length=100, null=True)#新增一个用户组的创建者的名字
    questions = models.ManyToManyField(Question)#所有问题
