#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
#author dengguo
import pymysql


class DbOperator():
    def __init__(self,host,user,password):
        self.name = 'database operator'
        self.host = host
        self.user = user
        self.password = password

    def dbconnect(self,dbname):
        # 打开数据库连接
        db = pymysql.connect(self.host, self.user, self.password, dbname,charset="utf8")
        #print(pymysql.apilevel,pymysql.threadsafety,pymysql.paramstyle)
        return db

    def dbconnectvalidate(self,dbname):
        db = self.dbconnect(dbname)
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
        # 使用 execute()  方法执行 SQL 查询
        cursor.execute("SELECT VERSION()")
        # 使用 fetchone() 方法获取单条数据.
        data = cursor.fetchone()
        print("Database ", " : %s " % data)
        # 关闭数据库连接
        db.close()

    def dbcreatetable(self,dbname):
        # 打开数据库连接
        db = self.dbconnect(dbname)
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
        # 使用 execute() 方法执行 SQL，如果表存在则删除
        #cursor.execute("DROP TABLE IF EXISTS USER")

        # 使用预处理语句创建表
        sql = """CREATE TABLE IF NOT EXISTS Users(
        id VARCHAR(50) NOT NULL,
        email VARCHAR(50) NOT NULL,
        name VARCHAR(50) NOT NULL,
        passwd VARCHAR(50) NOT NULL,
        admin TINYINT(1),
        created_at FLOAT,
        image VARCHAR(50) NOT NULL,
        PRIMARY KEY (id)
        )ENGINE=InnoDB DEFAULT CHARSET=utf8;
        """
        sql = """CREATE TABLE IF NOT EXISTS blogs(
                id VARCHAR(50) NOT NULL,
                user_id VARCHAR(50) NOT NULL,
                user_name VARCHAR(50) NOT NULL,
                name VARCHAR(50) NOT NULL,
                summary VARCHAR(200) NOT NULL,
                content TEXT,
                created_at FLOAT,
                user_image VARCHAR(50) NOT NULL,
                PRIMARY KEY (id)
                )ENGINE=InnoDB DEFAULT CHARSET=utf8;
                """
        sql = """CREATE TABLE IF NOT EXISTS comments(
                    id VARCHAR(50) NOT NULL,
                    blog_id VARCHAR(50) NOT NULL,
                    user_id VARCHAR(50) NOT NULL,
                    user_name VARCHAR(50) NOT NULL,
                    user_image VARCHAR(50) NOT NULL,
                    content TEXT,
                    created_at FLOAT,
                    PRIMARY KEY (id)
                    )ENGINE=InnoDB DEFAULT CHARSET=utf8;
                    """
        cursor.execute(sql)
        # 关闭数据库连接
        db.close()

    def dbinsertdrecord(self,dbname,record):
        db = self.dbconnect(dbname)
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        # SQL 插入语句
        sql = "INSERT INTO USER(NAME, \
               PHOTO, AGE, SEX, TYPE) \
               VALUES ('%s', '%s', '%d', '%c', '%s' )" % \
              record

        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except Exception as e:
            # Rollback in case there is any error
            print(e)
            db.rollback()

        # 关闭数据库连接
        db.close()

    def dbqueryrecords(self,dbname):
        db = self.dbconnect(dbname)
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()

        # SQL 查询语句
        sql = "select * FROM EMPLOYEE \
               WHERE INCOME > '%d'" % (2000)
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            #print(cursor.rowcount)
            results = cursor.fetchall()
            for row in results:
                fname = row[0]
                lname = row[1]
                age = row[2]
                sex = row[3]
                income = row[4]
                # 打印结果
                print("fname=%s,lname=%s,age=%d,sex=%s,income=%d" % \
                (fname, lname, age, sex, income))
        except:
            print("Error: unable to fecth data")

        # 关闭数据库连接
        db.close()

    def dbupdaterecord(self,dbname):

        db = self.dbconnect(dbname)

        # 使用cursor()方法获取操作游标
        cursor = db.cursor()

        # SQL 更新语句
        sql = "UPDATE EMPLOYEE SET AGE = AGE + 1 WHERE SEX = '%c'" % ('M')

        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # 发生错误时回滚
            db.rollback()

        # 关闭数据库连接
        db.close()

    def dbdeleterecord(self,dbname):
        db = self.dbconnect(dbname)
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()

        # SQL 删除语句
        sql = "DELETE FROM EMPLOYEE WHERE AGE < '%d'" % (20)
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 提交修改
            db.commit()
        except Exception as  e:
            # 发生错误时回滚
            db.rollback()

        # 关闭连接
        db.close()



def test_initdbop():
    newdbop = DbOperator("140.143.189.20", "kcl", '123457*aZ')
    return newdbop


def test_db_op():
    newdbop = test_initdbop()
    newdbop.dbcreatetable('studyDB')
    #newdbop.dbinsertdrecord('studyDB',('我的名字', '你的姓', 20, 'F', 60000))
    #newdbop.dbqueryrecords('studyDB')
    #newdbop.dbupdaterecord('studyDB')
    #newdbop.dbdeleterecord('studyDB')

if __name__ == '__main__':
    test_db_op()