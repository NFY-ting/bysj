# -*- coding: utf-8 -*- 
# @Time : 2021/4/7 15:26 
# @Author : NFY_ting
# @File : student.py
# @contact: nfy_ting@qq.com task
from flask import Blueprint, redirect, url_for, render_template, request, abort, session, jsonify
from utils.db.user import Student, Teacher, Lab, Grade, Class, Classgrade
student = Blueprint("student", __name__)
from utils.db.user import db
import time


@student.route('/stu', methods=['GET'])
# @login_required
def stuIndex():
    return render_template('stuIndex.html')


@student.route('/task', methods=['GET'])
# @login_required
def task():
    stu_id = session.get("stu_id")
    lab_id = []
    stu = Student.query.filter(Student.stu_id == stu_id).first()
    tasks = Classgrade.query.filter(Class.class_id == stu.class_id).all()
    for item in tasks:
        lab_id.append(item.lab_id)
    lab_list = Lab.query.filter(Lab.lab_id.in_(lab_id)).order_by(Lab.lab_id.desc()).all()
    return render_template('page/stu_task.html', lab_list = lab_list)


@student.route('/lab', methods=['GET', 'POST'])
# @login_required
def lab():
    if request.method == 'GET':
        stu_id = session.get("stu_id")
        lab_id = []
        stu = Student.query.filter(Student.stu_id == stu_id).first()
        tasks = Classgrade.query.filter(Class.class_id == stu.class_id).all()
        # isActive = Grade.query.filter(Grade.stu_id == stu_id,Grade.grade == '100').all()
        for item in tasks:
            lab_id.append(item.lab_id)
        lab_list = Lab.query.filter(Lab.lab_id.in_(lab_id)).all()
        return render_template('page/stu_lab.html', lab_list = lab_list)
    else:
        return jsonify({'status': True, 'code': 0, 'info': '初始化成功'})

@student.route('/info', methods=['GET', 'POST'])
# @login_required
def info():
    if request.method == 'GET':
        return render_template('page/stu_info.html')
    else:
        if session.get("stu_id"):               # 获取session
            stu_id = session.get("stu_id")
            # 查找学生
            stu = Student.query.filter(Student.stu_id == stu_id).first()
            if stu:
                class_id = stu.class_id
                cla = Class.query.filter(Class.class_id == stu.class_id).first()
                if cla:                         # 找到该生班级
                    return jsonify({'status': True, 'stu_id': stu_id, 'stu_name': stu.stu_name, 'sex': stu.sex,
                                    'email': stu.email, 'class_name': cla.class_name})
                else:
                    return jsonify({'status': False, 'code': 1, 'info': '班級加载失败，请重试'})
            else:
                return jsonify({'status': False, 'code': 1, 'info': '查找失败，请重试'})
        else:                                   # 非法访问
            abort(401)
            return jsonify({'status': False, 'code': 2, 'info': 'Unauthorized，未授权访问'})


@student.route('/fix_email', methods=['POST'])
def fix_email():
    stu_id = session.get("stu_id")
    if stu_id:
        mail = request.form['mail']
        # 查找学生
        stu = Student.query.filter(Student.stu_id == stu_id).first()
        stu.email = mail
        db.session.commit()
        db.session.close()
        return jsonify({'status': True, 'code': 0, 'info': '修改成功'})
    else:
        abort(401)
        return jsonify({'status': False, 'code': 2, 'info': 'Unauthorized，未授权访问'})


@student.route('/postFlag', methods=['POST'])
def postFlag():
    stu_id = session.get("stu_id")
    class_id = session.get("class_id")
    if stu_id:
        data = request.get_json()
        lab_id = data['lab_id']
        flag = data['flag']
        lab = Lab.query.filter(Lab.lab_id == lab_id).first()
        print(lab.flag == flag)
        if lab.flag == flag:
            stu = Grade.query.filter(Grade.stu_id==stu_id, Grade.lab_id==lab_id).first()
            cla_info = Class.query.filter(Class.class_id==class_id).first()
            stu.grade = '1'
            db.session.commit()
            all = Grade.query.filter(Grade.grade=='1', Grade.lab_id==lab_id).count()
            cla = Classgrade.query.filter(Classgrade.class_id==class_id, Classgrade.lab_id==lab_id).first()
            cla.num = all
            db.session.commit()
            cla.rate = all / cla_info.total
            db.session.commit()
            db.session.close()
            return jsonify({'status': True, 'code': 0, 'info': 'flag正确'})
        else:
            return jsonify({'status': False, 'code': 1, 'info': 'flag错误'})
    else:
        abort(401)
        return jsonify({'status': False, 'code': 2, 'info': 'Unauthorized，未授权访问'})


@student.route('/self_garde', methods=['GET'])
# @login_required
def self_garde():
    stu_id = session.get("stu_id")
    class_id = session.get("class_id")
    taskNum = Classgrade.query.filter(Classgrade.class_id == class_id).count()
    fillNum = Grade.query.filter(Grade.stu_id == stu_id,Grade.grade == '1').order_by(Grade.lab_id).count()
    return render_template('page/stu_grade.html', taskNum = taskNum, fillNum = fillNum)


@student.route('/forGrade', methods=['GET'])
# @login_required
def forGrade():
    stu_id = session.get("stu_id")
    class_id = session.get("class_id")
    data = []
    count = Classgrade.query.filter(Classgrade.class_id == class_id).count()+2
    zero = Grade.query.filter(Grade.stu_id == stu_id,Grade.grade == '0').order_by(Grade.lab_id).all()
    perfect = Grade.query.filter(Grade.stu_id == stu_id,Grade.grade == '1').order_by(Grade.lab_id).all()
    full = {
        "lab_id":'YES',
        "lab_name": '已完成实验',
        "lab_info": '',
        "lab_aim": '',
        "parentId":-1
    }
    not_full = {
        "lab_id":'NO',
        "lab_name": '未完成实验',
        "lab_info": '',
        "lab_aim": '',
        "parentId":-1
    }
    for item in perfect:
        lab = Lab.query.filter(Lab.lab_id == item.lab_id).first()
        dataItem = {
            "lab_id":lab.lab_id,
            "lab_name": lab.lab_name,
            "lab_info": lab.lab_info,
            "lab_aim": lab.lab_aim,
            "parentId":'YES'

        }
        data.append(dataItem)
    for item in zero:
        lab = Lab.query.filter(Lab.lab_id == item.lab_id).first()
        dataItem = {
            "lab_id":lab.lab_id,
            "lab_name": lab.lab_name,
            "lab_info": lab.lab_info,
            "lab_aim": lab.lab_aim,
            "parentId": 'NO'

        }
        data.append(dataItem)
    data.append(full)
    data.append(not_full)
    return jsonify({'count': count, 'code': 0, 'msg': '查询成功', 'data': data})


@student.route('/stu_class', methods=['GET'])
# @login_required
def stu_class():
    return render_template('page/stu_class.html')



@student.route('/class_grade', methods=['GET'])
# @login_required
def class_grade():
    # with session.no_autoflush:
    stu_id = session.get("stu_id")
    class_id = session.get("class_id")
    my_class = Class.query.filter(Class.class_id == class_id).first()
    class_num = my_class.total
    labs = Classgrade.query.filter(Classgrade.class_id == class_id).all()       # 统计实验
    xAxis = []
    data = []
    rate = []
    for lab in labs:
        self_grade = Grade.query.filter(Grade.stu_id == stu_id ,Grade.lab_id == lab.lab_id).first()
        lab_info = Lab.query.filter(Lab.lab_id == lab.lab_id).first()
        rate.append(lab.rate)
        xAxis.append(lab_info.lab_name)
        data.append(self_grade.grade)
    return jsonify({'status': True, 'code': 0, 'msg': '查询成功','data': data,'xAxis':xAxis,'rate':rate,'total':class_num})
