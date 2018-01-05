#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
#author dengguo
'''
Models for user, member, comment.
'''


import time, uuid
#uuid https://www.cnblogs.com/dkblog/archive/2011/10/10/2205200.html

from orm import Model, StringField, BooleanField, FloatField, TextField

def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)



class User(Model):
    __table__ = 'Users'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    user = StringField(ddl='varchar(50)')
    passwd = StringField(ddl='varchar(50)')
    # admin = BooleanField()
    # name = StringField(ddl='varchar(50)')
    # image = StringField(ddl='varchar(500)')
    # created_time = FloatField(default=time.time)

class MemberInfo(Model):
    __table__ = 'memberInfo'
    id = StringField(primary_key=True, default=next_id, ddl='varchar(200)')
    name = StringField(ddl='varchar(200)')
    age = StringField(ddl='varchar(200)')
    athnic = StringField(ddl='varchar(200)')
    admission_time = StringField(ddl='varchar(200)')
    native_place = StringField(ddl='varchar(200)')
    address = StringField(ddl='varchar(200)')
    email = StringField(ddl='varchar(200)')
    phonenumber = StringField(ddl='varchar(200)')
    idcard = StringField(ddl='varchar(200)')



class Blog(Model):
    __table__ = 'blogs'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    user_id = StringField(ddl='varchar(50)')
    user_name = StringField(ddl='varchar(50)')
    user_image = StringField(ddl='varchar(500)')
    name = StringField(ddl='varchar(50)')
    summary = StringField(ddl='varchar(200)')
    content = TextField()
    created_at = FloatField(default=time.time)



class Comment(Model):
    __table__ = 'comments'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    study_id = StringField(ddl='varchar(50)')
    user_name = StringField(ddl='varchar(50)')
    content = TextField()
    created_time = FloatField(default=time.time)

class Member(Model):
    __table__ =  'members'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    study_id = StringField(ddl='varchar(50)')
    passwd = StringField(ddl='varchar(50)')



class Newpswd(Model):
    __table__ = 'newpswd'

    id = StringField(primary_key=True, default=next_id, ddl='carchar(50)')
    new_pswd = StringField(ddl='varchar(50)')


class Chooseclass(Model):
    __table__ = 'chooseclasses'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)' )
    class_name = StringField(ddl='varchar(50)')
    teacher_name = StringField(ddl='varchar(50)')
    class_time = 'monday'            #固定值


class SysInfo(Model):
    __table__ = 'sysinfos'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')

    title = StringField(ddl='varchar(50)')
    content = TextField()
    create_time = FloatField(default=time.ctime())