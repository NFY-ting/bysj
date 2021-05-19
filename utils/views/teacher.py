# -*- coding: utf-8 -*- 
# @Time : 2021/4/7 15:27 
# @Author : NFY_ting
# @File : teacher.py
# @contact: nfy_ting@qq.com
from flask import Blueprint, redirect, url_for, render_template, request, abort, session, jsonify
from utils.db.user import Student, Teacher, Lab, Grade, Class, Classgrade
import xlrd
from werkzeug.security import generate_password_hash
from flask_login import LoginManager,login_user,logout_user,login_required

teacher = Blueprint("teacher", __name__)
from run import db


@teacher.route('/tec')
# @login_required
def tecIndex():
    return render_template('tecIndex.html')


@teacher.route('/tec/login/')
# @login_required
def tec_login():
    return render_template('page/tec_login.html')

@teacher.route('/tec_info', methods=['GET', 'POST'])
# @login_required
def tec_info():
    if request.method == 'GET':
        return render_template('page/tec_info.html')
    else:
        if session.get("tec_id"):               # 获取session
            tec_id = session.get("tec_id")
            class_name = []
            # 查找教师，一个老师同时教授多个班
            tec = Teacher.query.filter(Teacher.tec_id == tec_id).first()          # 返回结果为教师信息
            if tec is None:
                return jsonify({'status': False, 'code': 2, 'info': '个人信息加载失败，请重试'})
            else:
                 cla = Class.query.filter(Class.tec_id == tec_id).all()         #查询教师所有授课
                 if cla is None:
                     return jsonify({'status': False, 'code': 1, 'info': '班級信息加载失败，请重试'})
                 else:
                     for item in cla:  # 遍历该教师所授课程
                         class_name.append(item.class_name)  # 找到该班级,存入班级名
                 return jsonify({'status': True, 'tec_id': tec_id, 'tec_name': tec.tec_name, 'sex': tec.sex,
                                        'email': tec.email, 'class_name': class_name})
        else:                                   # 非法访问
            abort(401)
            return jsonify({'status': False, 'code': 2, 'info': 'Unauthorized，未授权访问'})


@teacher.route('/fix_tecemail', methods=['POST'])
def fix_tecemail():
    tec_id = session.get("tec_id")
    if tec_id:
        mail = request.form['mail']
        # 查找学生
        tec = Teacher.query.get(tec_id)
        tec.email = mail
        db.session.commit()
        # db.session.close()
        return jsonify({'status': True, 'code': 0, 'info': '修改成功'})
    else:
        abort(401)
        return jsonify({'status': False, 'code': 2, 'info': 'Unauthorized，未授权访问'})


@teacher.route('/addClass',methods=['GET', 'POST'])
def addClass():
    if request.method == 'GET':
        return render_template('page/addClass.html')
    else:
        file = request.files.get('file')       # 获取前端发送内容
        if file is None:
            return jsonify({'status': False, 'code': 1, 'msg': '请先选择要上传的学生名单'})
        re = file.read()  # 文件内容
        data = xlrd.open_workbook(file_contents=re)
        table = data.sheets()[0]
        # names = data.sheet_names()  # 返回所有工作表的名字
        # status = data.sheet_loaded(names[0])  # 检查sheet1是否导入完毕
        nrows = table.nrows  # 获取该sheet中的有效行数
        ncols = table.ncols  # 获取该sheet中的有效列数
        # col = table.col_values(0)  # 第1列数据
        # ro = table.row_values(0)  # 第1行数据
        for rowIndex in range(1, nrows):                       # 遍历表格 从第二行开始
            item = []
            for colIndex in range(ncols):
                val = table.row_values(rowIndex)[colIndex]
                if val == '男':
                    val = 'male'
                elif val == '女':
                    val = 'female'
                item.append(val)        # 遍历每行每列
            pwd = generate_password_hash("student01")
            item.append(pwd)
            cla = Class.query.filter(Class.class_id == item[3]).first()        # 存入班级id
            item[3] = cla.class_id
            stu = Student(stu_id=item[0], stu_name=item[1], pwd=item[5], sex=item[2], email=item[4],
                              class_id=item[3])
            db.session.add(stu)
            db.session.commit()
            # db.session.close()
        return jsonify({'status': True, 'code': 0, 'info': '导入成功'})


@teacher.route('/addTask',methods=['GET', 'POST'])
def addTask():
    tec_id = session.get("tec_id")
    if tec_id is None:
        return render_template('page/addTask.html')
    if request.method == 'GET':
        claList = Class.query.filter(Class.tec_id == tec_id).all()
        return render_template('page/addTask.html',claList = claList)
    else:
        data = request.get_json()
        class_id = data['class_id']
        cla_list = Classgrade.query.filter(Classgrade.tec_id == tec_id,Classgrade.class_id == class_id).all()
        if cla_list is None:
            return render_template('page/addTask.html',labList = '')
        labId_list = []
        data = []
        for cla in cla_list:
            labId_list.append(cla.lab_id)
        labList = Lab.query.filter(Lab.lab_id.notin_(labId_list)).all()
        for item in labList:
            dataItem = {
                "lab_id": item.lab_id,
                "lab_name": item.lab_name,
            }
            data.append(dataItem)
        return jsonify({'status': True, 'code': 0, 'data': data})


@teacher.route('/postTask',methods=['POST'])
def postTask():
    tec_id = session.get("tec_id")
    if tec_id is None:
        return jsonify({'status': False,'code': 1,'info': '请先登录！'})
    data = request.get_json()
    class_id = data['class_id']
    lab_id = data['lab_id']
    task = Classgrade(class_id=class_id, lab_id=lab_id, tec_id=tec_id)
    db.session.add(task)
    db.session.commit()
    stu_list = Student.query.filter(Student.class_id == class_id).all()             # 同时初始化该班级学生实验成绩
    for stu in stu_list:
        grade = Grade(class_id=class_id, lab_id=lab_id, tec_id=tec_id, stu_id=stu.stu_id, grade='0')
        db.session.add(grade)
        db.session.commit()
    return jsonify({'status': True, 'code': 0, 'info': '任务添加成功'})


@teacher.route('/delTask',methods=['POST'])
def delTask():
    from utils.db.user import db as thisdb
    tec_id = session.get("tec_id")
    if tec_id is None:
        return jsonify({'status': False,'code': 1,'info': '请先登录！'})
    data = request.get_json()
    class_id = data['class_id']
    lab_id = data['lab_id']
    delItem = Classgrade.query.filter(Classgrade.tec_id == tec_id,Classgrade.class_id == class_id, Classgrade.lab_id == lab_id).first()
    thisdb.session.delete(delItem)  # 删除任务
    thisdb.session.commit()
    Grade.query.filter(Grade.tec_id == tec_id,Grade.class_id == class_id, Grade.lab_id == lab_id).delete(synchronize_session=False)
    thisdb.session.commit()# 删除学生实验成绩
    return jsonify({'status': True, 'code': 0, 'info': '删除成功'})


@teacher.route('/forTask', methods=['GET'])
# @login_required
def forTask():
    tec_id = session.get("tec_id")
    page = int(request.args['page'])
    limit = int(request.args['limit'])
    data = []
    itemNum = (page-1) * limit
    try:                                            # 查询所有教师名单
        task_list = Classgrade.query.filter(Classgrade.tec_id == tec_id).order_by(Classgrade.class_id).offset(itemNum).limit(limit).all()# offset(x)表示跳过前几页数据，limit(x)再取几条记录
        if task_list is None:
          return jsonify({'status': True, 'code': 1, 'info': '暂无实验任务'})
    except Exception as e:
        print(e)
    count = len(task_list)
    for item in task_list:
        class_name = Class.query.filter(Class.class_id == item.class_id).first()
        lab_name = Lab.query.filter(Lab.lab_id == item.lab_id).first()
        dataItem = {
            "class_id": item.class_id,
            "class_name": class_name.class_name,
            "lab_id": item.lab_id,
            "lab_name": lab_name.lab_name,
            "num": item.num,
            "rate": item.rate
        }
        data.append(dataItem)
    return jsonify({'count': count, 'code': 0, 'msg': '查询成功', 'data': data})


@teacher.route('/forClass',methods=['GET'])
# @login_required
def forClass():
    data = []
    count = 0
    tec_id = session.get("tec_id")
    # 查询该教师授课班级
    class_list = Class.query.filter(Class.tec_id == tec_id).order_by(Class.class_id).all()
    if class_list is None:
        return jsonify({'status': True, 'code': 1, 'info': '暂无授课班级'})
    for item in class_list:
        dataItem = {
            "stu_id":item.class_id,"stu_name": item.class_name,"sex": '',"email": '',
            "classId": item.class_id,"parentId":-1

        }
        data.append(dataItem)
        # 查询各个班学生
        stu_list = Student.query.filter(Student.class_id == item.class_id).order_by(Student.stu_id).all()
        count += len(stu_list)
        for stuItem in stu_list:
            dataItem = {
                "stu_id": stuItem.stu_id,"stu_name": stuItem.stu_name,"sex": stuItem.sex,
                "email": stuItem.email,"classId": stuItem.class_id,"parentId": stuItem.class_id,
            }
            data.append(dataItem)
    return jsonify({'count': count, 'code': 0, 'msg': '查询成功', 'data': data})


@teacher.route('/stuScore',methods=['POST'])
# @login_required
def stuScore():
    data = request.get_json()
    stu_id = data['stu_id']
    class_id = data['class_id']
    if class_id == -1:              # 查看班级成绩
        class_score = []
        class_list = Classgrade.query.filter(Classgrade.class_id == stu_id).all()
        for item in class_list:
            data_item = {
                "lab_id": item.lab_id,
                "rate":item.rate,
                "num":item.num
            }
            class_score.append(data_item)
        return jsonify({'status': True,'code': 0,'msg': '查询成功','class_socre':class_score})
    else:                           # 查看学生成绩
        grade_list = Grade.query.filter(Grade.stu_id == stu_id).all()               # 查询学生实验成绩
        complete = []
        print("grade_list:",grade_list)
        not_complete = []
        for item in grade_list:
            data_item = {
                "lab_id": item.lab_id
            }
            if item.grade == '1':             # 已完成实验
                complete.append(data_item)
            elif item.grade == '0':                               # 未完成实验
                not_complete.append(data_item)
        return jsonify({'status': True, 'code': 1, 'msg': '查询成功', 'complete': complete, "not_complete": not_complete})


@teacher.route('/tecGrade')
# @login_required
def tecGrade():
    return render_template('page/tec_grade.html')

@teacher.route('/tec_grade', methods=['GET'])
# @login_required
def tec_grade():
    tec_id = session.get("tec_id")
    page = int(request.args['page'])
    limit = int(request.args['limit'])
    data = []
    itemNum = (page-1) * limit
    try:                                            # 查询所有教师名单
        grade_list = Grade.query.filter(Grade.tec_id == tec_id).order_by(Grade.class_id).offset(itemNum).limit(limit).all()# offset(x)表示跳过前几页数据，limit(x)再取几条记录
        if grade_list is None:
          return jsonify({'status': True, 'code': 1, 'info': '暂无实验任务'})
    except Exception as e:
        print(e)
    count = len(grade_list)
    for item in grade_list:
        stu = Student.query.filter(Student.stu_id == item.stu_id).first()
        cla = Class.query.filter(Class.tec_id == item.tec_id).first()
        lab = Lab.query.filter(Lab.lab_id == item.lab_id).first()
        dataItem = {
            "class_id": item.class_id,
            "class_name": cla .class_name,
            "stu_id": item.stu_id,
            "stu_name": stu.stu_name,
            "lab_id": item.lab_id,
            "lab_name": lab.lab_name,
            "yes_no": item.grade,
        }
        data.append(dataItem)
    return jsonify({'count': count, 'code': 0, 'msg': '查询成功', 'data': data})
