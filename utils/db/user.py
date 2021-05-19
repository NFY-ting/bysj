# -*- coding: utf-8 -*- 
# @Time : 2021/3/14 19:23 
# @Author : NFY_ting
# @File : user.py
# @contact: nfy_ting@qq.com

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,UserMixin
app = Flask(__name__)
# 创建数据库对象
db = SQLAlchemy(app)
# 注意点:
# ①定义数据库表名： tablename = '表名’
# ②定义字段： 字段名 = db.Column(类型,完整性约束条件)


class Student(db.Model, UserMixin):
    # 定义表名
    __tablename__ = 'students'
    # 定义字段
    stu_id = db.Column(db.Integer, primary_key=True)
    stu_name = db.Column(db.String(50), nullable=False)
    pwd = db.Column(db.String(100))
    sex = db.Column(db.Enum('male', 'female'), server_default='male', nullable=False)
    email = db.Column(db.String(50))
    class_id = db.Column(db.Integer, db.ForeignKey('classes.class_id'))
    # repr()方法显示一个可读字符串,实例返回的内容

    # def verify_password(self, password):
    #     return check_password_hash(self.password_hash, password)


class Teacher(db.Model):
    # 定义表名
    __tablename__ = 'teachers'
    # 定义字段
    tec_id = db.Column(db.Integer, nullable=False, primary_key=True)
    tec_name = db.Column(db.String(50), nullable=False)
    pwd = db.Column(db.String(100))
    sex = db.Column(db.Enum('male', 'female'), server_default='male', nullable=False)
    email = db.Column(db.String(50))


class Class(db.Model):
    # 定义表名
    __tablename__ = 'classes'
    # 定义字段
    class_id = db.Column(db.Integer, nullable=False, primary_key=True)
    class_name = db.Column(db.String(50), nullable=False)
    class_code = db.Column(db.String(15), nullable=False)
    tec_id = db.Column(db.Integer,  db.ForeignKey('teachers.tec_id'), nullable=False)
    total = db.Column(db.Integer)


class Lab(db.Model):
    # 定义表名
    __tablename__ = 'labs'
    # 定义字段
    lab_id = db.Column(db.Integer,autoincrement=True, primary_key=True)
    lab_name = db.Column(db.String(30), nullable=False)
    lab_info = db.Column(db.String(200))
    lab_aim = db.Column(db.String(100))
    lab_url = db.Column(db.String(200), nullable=False)
    lab_img = db.Column(db.String(100), nullable=False)
    flag = db.Column(db.String(50))


class Grade(db.Model):
    # 定义表名
    __tablename__ = 'grades'
    # 定义字段
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    stu_id = db.Column(db.Integer, db.ForeignKey('students.stu_id'), nullable=False,)
    class_id = db.Column(db.String(8),  db.ForeignKey('classes.class_id'), nullable=False)
    lab_id = db.Column(db.Integer,  db.ForeignKey('labs.lab_id'), nullable=False)
    tec_id = db.Column(db.Integer, db.ForeignKey('teachers.tec_id'))
    grade = db.Column(db.Enum('0', '1'), server_default='0')

class Classgrade(db.Model):
    # 定义表名
    __tablename__ = 'classgrade'
    # 定义字段
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    class_id = db.Column(db.String(8), db.ForeignKey('classes.class_id'), nullable=False)
    tec_id = db.Column(db.Integer, db.ForeignKey('teachers.tec_id'), nullable=False)
    lab_id = db.Column(db.Integer, db.ForeignKey('labs.lab_id'), nullable=False)
    num = db.Column(db.Integer, server_default='0')
    rate = db.Column(db.Float, server_default = '0.00')
