# -*- coding: utf-8 -*- 
# @Time : 2021/4/7 16:09 
# @Author : NFY_ting
# @File : config.py 
# @contact: nfy_ting@qq.com
from datetime import timedelta
import os


class Config(object):
	SECRET_KEY = os.urandom(24)                               # 设置密钥
	SQLALCHEMY_TRACK_MODIFICATIONS = False                     # debug sql
	SQLALCHEMY_ECHO = True                                    # 输出SQL标准语句
	PERMANENT_SESSION_LIFETIME = timedelta(hours=4)           # 设置session有效期为4h
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:xxxxxxx@xxx.xxx.xxx:3306/experiment'
	# SQLALCHEMY_POOL_RECYCLE = 10
	SQLALCHEMY_POOL_SIZE = 0                                  # 连接池中缓存的连接数，如果为0，表示缓冲池大小无限制。
	SQLALCHEMY_MAX_OVERFLOW = -1                              # max_overflow 表示超出pool_size的，允许建立的最大连接数量。如果为-1，表示无限制

