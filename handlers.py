#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
#author dengguo
from aiohttp import web
from coroweb import get, post
from apis  import APIValueError, APIResourceNotFoundError,APIError
import re, time, json, logging, hashlib, base64, asyncio
import config
from orm import Model
from models import MemberInfo, Member, Comment, Chooseclass, User
from models import  next_id
# class Comment(object):
#     def __init__(self,*args,**kwargs):
#         self.user_id = kwargs.get('user_id')
#         self.user_name = kwargs.get('user_name')
#         self.created_time = kwargs.get('created_at')
#         self.content = kwargs.get('content',None)
#
# class MemberInfo(object):
#     def __init__(self, *args, **kwargs):
#         self.user = kwargs.get('user')
#         self.age = kwargs.get('age')
#         self.athnic = kwargs.get('athnic')
#         self.admission_time = kwargs.get('admission_time')
#         self.native_place = kwargs.get('native_place')
#         self.address = kwargs.get('address')
#         self.idcard = kwargs.get('idcard')
#         self.email = kwargs.get('email')
#         self.phonenumber = kwargs.get('phonenumber')
#
#
# class Chooselesson(object):
#     def __init__(self, *args, **kwargs):
#         self.lesson_name = kwargs.get('class_name')
#         self.teacher_name = kwargs.get('teacher_name')
#         self.lesson_time = kwargs.get('lesson_time')
#         self.lesson_type = kwargs.get('lesson_type')
#         self.lesson_id = kwargs.get('lesson_id')
#
# class SysInfo(object):
#     def __init__(self, *args, **kwargs):
#         self.content = kwargs.get('content')
#         self.publish_time = kwargs.get('publish_time')
#
# class Updatepasswd(object):
#     def __init__(self, *args, **kwargs):
#         self.new_passwd = kwargs.get('new_passwd')



# def check_admin(request):
#     if request.__user__ is None or not request.__user__.admin:
#         raise APIPermissionError()

@get('/')
def index():
    return {
        '__template__': 'login.html'
    }

@get('/top.html')
def top():
    return {
        '__template__':'top.html'
    }

@get('/update_pswd.html')
def update_pswd():
    return {
        '__template__':'update_pswd.html'
    }

@get('/liuyanban.html')
def liuyanban():
    return {
        '__template__':'liuyanban.html'
    }

@get('/error.html')
def error():
    return {
        '__template__':'error.html'
    }

@get('/choose_class.html')
def choose_class():
    return {
        '__template__':'choose_class.html'
    }

@get('/tools.html')
def tools():
    return {
        '__template__':'tools.html'
    }

@get('/form.html')
def form():
    return {
        '__template__':'form.html'
    }

@get('/success.html')
def success():
    return {
        '__template__':'success.html'
    }

@get('/left.html')
def left():
    return {
        '__template__':'left.html'
    }

@get('/member_index.html')
def member_index():
    return {
        '__template__':'member_index.html'
    }

@get('/member_main.html')
def member_main():
    return {
        '__template__':'member_main.html'
    }

@get('/check_schedule.html')
def search_schedule():
    return {
        '__template__': 'check_schedule'
    }

@get('/check_score.html')
def search_score():
    return {
        '__template__': 'check_score'
    }

@get('/check_memberinfo.html')
async def search_score():
    users = await MemberInfo.findAll()
    print(users)
    return {
        '__template__': 'check_memberinfo.html',
        'users':users
    }
def user2cookie(user, passwd):

    # build cookie string by: id-expires-sha1
    expires = str(int(time.time()))
    s = '%s-%s-%s-%s' % (user, passwd, expires, _COOKIE_KEY)
    L = [user, expires, hashlib.sha1(s.encode('utf-8')).hexdigest()]
    print(L)
    return '-'.join(L)

def text2html(text):
    lines = map(lambda s: '<p>%s</p>' % s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'), filter(lambda s: s.strip() != '', text.split('\n')))
    return ''.join(lines)


# class User(object):
#     def __init__(self,*args,**kwargs):
#         self.user = kwargs.get('user')
#         self.passwd = kwargs.get('passwd')
#
# @post('/update_pswd')
# def update_pswd(* ,newpswd, oldpswd):
#     pass

@post('/entry_infomations')
async def entry_informatimes(*args, **kwargs ):
    name = kwargs.get('name')
    age = kwargs.get('age')
    athnic = kwargs.get('athnic')
    admission_time = kwargs.get('admission_time')
    native_place = kwargs.get('native_place')
    address = kwargs.get('address')
    idcard = kwargs.get('idcard')
    email = kwargs.get('email')
    phonenumber = kwargs.get('phonenumber')
    print(name, age, athnic)
    print('-------&&&&&&&&:', native_place)
    # return user, age, athnic, admission_time, native_place, address, idcard, email, phonenumber
    memberInfo = MemberInfo(id=next_id(),name=name , age=age, athnic=athnic,
                            admission_time=admission_time, native_place=native_place,
                            idcard=idcard, email=email, address=address, phonenumber=phonenumber
                            )
    print('++++++++++++++------+++++', memberInfo)
    await memberInfo.save()

    r = web.Response()
    r.content_type = 'application/json'
    r.body = json.dumps(memberInfo, ensure_ascii=False, default=lambda o: o.__dict__).encode('utf-8')
    return r

@post('/update_passwd')
def update_passwd(*args, **kwargs):
    oldpasswd = kwargs.get('oldpasswd')
    newpasswd = kwargs.get('newpasswd')
    print(oldpasswd, newpasswd)

    r = web.Response()
    r.content_type = 'application/json'
    r.body = json.dumps(newpasswd, ensure_ascii=False, default=lambda o: o.__dict__).encode('utf-8')
    return r

@post('/publish_comment')
def publist_comment(*args, **kwargs):
    comments = kwargs.get('comment')
    print('dadadadadadada&&&&&&&&', comments)


_RE_USER = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
_RE_SHA1 = re.compile(r'^[0-9a-f]{40}$')

COOKIE_NAME = 'mysession'
_COOKIE_KEY = config.configs.session.secret

print('dbhost',config.configs.db.host)

@post('/authenticate')       #验证帐号密码登录
def authenticate(*, user, passwd):
    # users = User(user=user, passwd=passwd)
    # users.save()
    print(0)
    print('+++++', user, passwd)
    if not user:
        raise APIValueError('user', 'Invalid user.')
    if not passwd:
        raise APIValueError('passwd', 'Invalid password.')
    users_info = {'admin': 'admin', '17082601':'123456' }
    print(1)
    if user:
        user_ps = users_info[user]
        print(2)
        uid = '1234567890ABCDEFG'
        sha1_passwd = '%s:%s' % (uid, passwd)
    # user = User(id=uid, user='user',
    #             passwd=hashlib.sha1(sha1_passwd.encode('utf-8')).hexdigest())
    # #users[0]
    # # check passwd:
        sha1 = hashlib.sha1()
        sha1.update(user.encode('utf-8'))
        sha1.update(b':')
        sha1.update(user_ps.encode('utf-8'))
        print(user_ps,sha1.hexdigest())
        if passwd != sha1.hexdigest():
            raise APIValueError('passwd', 'Invalid password.')

    # authenticate ok, set cookie:
        r = web.Response()
        r.set_cookie(COOKIE_NAME, user2cookie(user, passwd), httponly=True)
        passwd = '******'
        r.content_type = 'application/json'
        r.body = json.dumps(user, ensure_ascii=False,default=lambda o:o.__dict__).encode('utf-8')
        print('----+++++',r)
        print(type(r))
        return r


# 解密cookie:
@asyncio.coroutine
def cookie2user(cookie_str):
    if not cookie_str:
        return None
    try:
        L = cookie_str.split('-')
        if len(L) != 3:
            return None
        uid, expires, sha1 = L
        if int(expires) < time.time():
            return None
        #user = yield from User.find(uid)
        uid = '1234567890ABCDEFG'  # next_id()
        sha1_passwd = '%s:%s' % (uid, "123456")
        user = {'admin': 'happya11', '17082601': '123456'}
        if user is None:
            return None
        s = '%s-%s-%s-%s' % (uid, user, expires, _COOKIE_KEY)
        if sha1 != hashlib.sha1(s.encode('utf-8')).hexdigest():
           logging.info('invalid sha1')
           return None
        passwd = '******'
        return user
    except Exception as e:
        logging.exception(e)
        return None