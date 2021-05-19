# -*- coding: utf-8 -*- 
# @Time : 2021/4/7 15:27 
# @Author : NFY_ting
# @File : admin.py analysis
# @contact: nfy_ting@qq.com

from flask import Blueprint, redirect, url_for, render_template, request, abort, session, jsonify
from utils.db.user import Student, Teacher, Lab, Class, Classgrade, Grade
import xlrd
from werkzeug.security import generate_password_hash
import os
from werkzeug.utils import secure_filename
from flask_login import LoginManager,login_user,logout_user,login_required

manger = Blueprint("manger", __name__)
from run import db


@manger.route('/admin')
# @login_required
def admin():
  return render_template('admin.html')


@manger.route('/analysis')
# @login_required
def analysis():
	tec = Teacher.query.count()       # 统计教师
	stu = Student.query.count()       # 统计学生
	cla = Class.query.count()       # 统计班级
	lab = Lab.query.count()       # 统计实验
	return render_template('page/ad_analysis.html', tecLen=tec, stuLen=stu, claLen=cla, labLen=lab,)


@manger.route('/analysis_lab',methods=['GET'])
# @login_required
def analysis_lab():
	labs = Lab.query.all()       # 统计实验
	legend = []
	data = []
	for lab in labs:
		# item = '实验'+lab.lab_id+":"+
		legend.append(lab.lab_name)
		all_grade = Grade.query.filter(Grade.lab_id == lab.lab_id).count()
		perfect = Grade.query.filter(Grade.lab_id == lab.lab_id, Grade.grade == '1').count()
		if all_grade != 0:
			fill = round(perfect / all_grade, 2)
		else:
			fill = 0.0
		data.append(fill)
	return jsonify({'status': True, 'code': 0, 'msg': '查询成功','data': data,'legend':legend})


@manger.route('/allLab',methods=['GET'])
def allLab():
	if request.method == 'GET':
		lab_list = Lab.query.all()
		return render_template('page/allLab.html',lab_list = lab_list)


@manger.route('/addTeacher', methods=['GET', 'POST'])
def addTeacher():
    if request.method == 'GET':
        return render_template('page/ad_teacher.html')
    else:
        file = request.files.get('file')         # 获取前端发送内容
        if file is None:
            return jsonify({'status': False, 'code': 1, 'msg': '请先选择要上传的教师名单'})
        re = file.read()  # 文件内容
        data = xlrd.open_workbook(file_contents=re)
        table = data.sheets()[0]
        nrows = table.nrows  # 获取该sheet中的有效行数
        ncols = table.ncols  # 获取该sheet中的有效列数
        for rowIndex in range(1, nrows):                       # 遍历表格 从第二行开始
            item = []
            for colIndex in range(ncols):
                val = table.row_values(rowIndex)[colIndex]
                if val == '男':
                    val = 'male'
                elif val == '女':
                    val = 'female'
                item.append(val)        # 遍历每行每列
            pwd = generate_password_hash("1101teacher")
            item.append(pwd)
            # cla = Class.query.filter(Class.class_id == item[3]).first()
            tec = Teacher(tec_id=item[0], tec_name=item[1], pwd=item[4], sex=item[2], email=item[3])
            db.session.add(tec)
            db.session.commit()
            # cla.tec_id = item[0]  # 存入授课情况
            # db.session.commit()
            # db.session.close()
        return jsonify({'status': True, 'code': 0, 'info': '导入成功'})


@manger.route('/forTeacher', methods=['GET'])
# @login_required
def forTeacher():
	page = int(request.args['page'])
	limit = int(request.args['limit'])
	data = []
	itemNum = (page-1) * limit
	try:                                            # 查询所有教师名单
		tec_list = Teacher.query.filter(Teacher.tec_id != '123456').order_by(Teacher.tec_id).offset(itemNum).limit(limit).all()# offset(x)表示跳过前几页数据，limit(x)再取几条记录
		if tec_list is None:
			return jsonify({'status': True, 'code': 1, 'info': '暂无教师'})
	except Exception as e:
		print(e)
	count = len(tec_list)
	for item in tec_list:
		dataItem = {
		"tec_id": item.tec_id,
		"tec_name": item.tec_name,
		"sex": item.sex,
		"email": item.email,
		}
		data.append(dataItem)
	return jsonify({'count': count, 'code': 0, 'msg': '查询成功', 'data': data})


@manger.route('/addLab', methods=['GET','POST'])
# @login_required
def addLab():
	if request.method == 'GET':
		return render_template('page/addLab.html')
	else:           # 添加实验
		data = request.get_json()
		print(data)
		lab_name = data['lab_name']  # 获取前端发送内容
		lab_url = data['lab_url']
		lab_info = data['lab_info']
		lab_aim = data['lab_aim']
		lab_img = data['lab_img']
		flag = data['flag']
		print(lab_name)
		try:
			lab = Lab(lab_name = lab_name,lab_url = lab_url,lab_info = lab_info,lab_aim = lab_aim,lab_img = lab_img, flag = flag)
			db.session.add(lab)
			db.session.commit()
			# db.session.close()
			return jsonify({'status': True,'code': 0,'msg': '添加成功'})
		except Exception as e:
			print(e)
			return jsonify({'status': False, 'code': 1, 'msg': '添加失败，SQL error'})


# 设置允许的文件格式
ALLOWED_EXTENSIONS = set(['png','jpg','JPG','PNG','bmp','jpeg'])

# 检查文件类型
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@manger.route('/uploadImg', methods=['POST'])
# @login_required
def uploadImg():
	if request.method == 'GET':
		return render_template('page/addLab.html')
	else:
		f = request.files['file']
		if not (f and allowed_file(f.filename)):
			return jsonify({'status': False, 'code': 1, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp、jpeg"})
		basepath = os.path.dirname(__file__)                                              # 当前文件所在路径
		upload_path = os.path.join(basepath, '../../uploads',secure_filename(f.filename))  # 将上传文件存入uploads路径下
		f.save(upload_path)
		upload_path = os.path.relpath(upload_path, 'securityPlatform\..')                # 存取文件相对路径
		upload_path = upload_path.replace('\\', '/')
		# 从start后面第一个文件夹或者文件开始计算相对路径：path一般是绝对路径，而start是path的一部分。
		return upload_path


@manger.route('/classScore',methods=['POST'])
# @login_required
def classScore():
	data = request.get_json()
	tec_id = data['tec_id']
	cla = Classgrade.query.filter(Classgrade.tec_id == tec_id).all()         #查询教师所有授课
	# return cla
	class_name = []
	if cla is None:
		return jsonify({'status': False, 'code': 1, 'info': '班級信息加载失败，请重试'})
	else:
		for item in cla:  # 遍历该教师所授课程
			dataItem = {
				"class_id": item.class_id,
				"lab_id": item.lab_id,
				"num": item.num,
				"rate": item.rate
			}
			class_name.append(dataItem)
		return jsonify({'status': True, 'tec_id': tec_id, 'class_name': class_name})

