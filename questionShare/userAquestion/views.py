from django.shortcuts import render
from userAquestion.models import *


# Create your views here.
def create_user_with_errorlog(username, password):
    try:
        User.objects.get(username=username)
        return False, None
    except User.DoesNotExist:
        errorlog = ErrorLog.objects.create()  # 这个地方具体怎么做好不确定
        user = User.objects.create_user(username=username, password=password, errorlog=errorlog)
        user.save()
        return True, user


def create_admin_with_errorlog(username, password):
    try:
        User.objects.get(username=username)
        return False, None
    except User.DoesNotExist:
        errorlog = ErrorLog.objects.create()  # 这个地方具体怎么做好不确定
        admin = Admin.objects.create_user(username=username, password=password, errorlog=errorlog)
        admin.save()
        return True, admin


# 创建用户组，用祖名和创建者唯一确定
def create_group(name, creator_username):
    try:
        creator = User.objects.get(username=creator_username)
        group = Group.objects.get(creator=creator, name=name)
        return False, None
    except (User.DoesNotExist, Group.DoesNotExist):
        # 获取创建者的实例
        creator = User.objects.get(username=creator_username)
        # 创建组实例
        group = Group(name=name, creator=creator)
        group.save()
        return True, group


# 添加用户的借口，错误信息或许需要详细给出是哪个，以便于错误信息输出
def group_adduser(name, creator_username, username):
    try:
        creator = User.objects.get(username=creator_username)
        group = Group.objects.get(creator=creator, name=name)
        user = User.objects.get(username)
        group.users.all(user)
        return True
    except(User.DoesNotExist, Group.DoesNotExist):
        return False


# 创建一个问题并返回该问题的对象
def create_question(content, correct_answer, question_type):
    # 检查数据库中是否已存在相同内容的问题
    if Question.objects.filter(content=content).exists():
        # 如果存在相同内容的问题，则不进行创建，并返回 None
        return None
    else:
        # 如果不存在相同内容的问题，则创建并保存问题对象，并返回创建的问题实例
        question = Question(content=content, correct_answer=correct_answer, question_type=question_type)
        question.save()
        return question


def create_questionset(name, creator_name, permission, group, group_creator_name):
    try:
        creator = User.objects.get(username=creator_name)
        QuestionSet.objects.get(name=name, creator=creator, permission=permission)
        return False, None
    except(User.DoesNotExist, QuestionSet.DoesNotExist):
        if not User.objects.filter(username=creator_name):
            return False, None
        creator = User.objects.get(username=creator_name)
        questionset = QuestionSet(name=name, creator=creator, permission=permission, group=group,
                                  group_creator_name=group_creator_name)
        questionset.save()
        return True, questionset

def get_questionset(name,creator_name,permission):
    try:
        creator = User.objects.get(username=creator_name)
        questionset = QuestionSet.objects.get(name=name, creator=creator, permission=permission)
        return True, questionset
    except(User.DoesNotExist,QuestionSet.DoesNotExist):
        return False, None

#用于获取用户或管理员
def get_user(name):
    user = User.objects.filter(username=name)
    return user

#用于获取组，如果信息不全可以得到的是一个列表：
def get_group(name,creator_name):
    if name==None:
        try:
            creator = User.objects.get(username=creator_name)
            group_list = Group.objects.filter(creator=creator)
            return group_list
        except(User.DoesNotExist):
            return None
    if creator_name==None:
        group_list = Group.objects.filter(name=name)
        return group_list
    try:
        creator = User.objects.get(username=creator_name)
        group_list = Group.objects.filter(name=name, creator=creator)
        return group_list
    except(User.DoesNotExist):
        return None