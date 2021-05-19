# -*- coding: utf-8 -*- 
# @Time : 2021/3/14 19:22 
# @Author : NFY_ting
# @File : run.py 
# @contact: nfy_ting@qq.com'
from flask import Flask, redirect, url_for, render_template, request, abort, session, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from utils.db.user import Student, Class, Teacher
from werkzeug.security import generate_password_hash, check_password_hash
# 实例化flask登录插件
# login_manager = LoginManager()
app = Flask(__name__)
# 初始化登录插件
# login_manager.init_app(app)
# 告诉login插件认证失败是跳转的页面,将登陆页面的视图函数的endpoint告诉login插件
# login_manager.login_view = '/'
# 跳转后提示信息的定义
# login_manager.login_message = '请先登录或注册'

app.config.from_object('config.Config')
db = SQLAlchemy(app)


# 这个函数是独立的模块函数，不是User模型的方法
# 加上装饰器是让login_manager这个插件加载这个函数，在其他视图函数中可以调用这个函数
# @login_manager.user_loader
# def get_user(uid):
    # 通过用户的id 来查询用户的模型，uid是主键查询可以不用filer_by可用get
    # return Student.query.get(int(uid))

@app.route('/')
def index():
    return render_template('page/stu_login.html')


@app.route('/register')
def register():
    return render_template('page/register.html')


@app.route('/register_request', methods=['GET', 'POST'])
def register_request():
    stu_id = request.form.get('stu_id')
    stu_name = request.form.get('stu_name')
    pwd = request.form.get('repwd')
    sex = request.form.get('sex')
    email = request.form.get('email')
    class_code = request.form.get('class_code')
    strclass = Class.query.filter(Class.class_code == class_code).first()
    if strclass:          # 找到该生班级
        pwd = generate_password_hash(pwd)               # 动态加密密码
        stu = Student(stu_id=stu_id, stu_name=stu_name, pwd=pwd, sex=sex, email=email, class_id=strclass.class_id)
        db.session.add(stu)
        db.session.commit()
        return jsonify({'status': True, 'code': 0, 'info': '注册成功'})
    else:
        return jsonify({'status': False, 'code': 1, 'info': '班级邀请码错误'})


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        # form = LoginForm()
        # 找到改学号学生
        stu_id = request.form['stu_id']
        pwd = request.form['pwd']
        # 查找学生
        stu = Student.query.filter(Student.stu_id == stu_id).first()
        # if student and student.verify_password(pwd):
        if check_password_hash(str(stu.pwd), str(pwd)):
            session["stu_id"] = stu_id                                          # 设置session
            session["stu_name"] = stu.stu_name
            session["class_id"] = stu.class_id
            resp = make_response("success")
            resp.set_cookie("stu_id", stu_id, "stu_name", stu.stu_name)   # 设置cookie4h
            return redirect(url_for('student.stuIndex'))
    else:
        abort(401)                                            # 未验证身份
    return redirect(url_for('/'))


@app.route('/tecLogin', methods=['POST'])
def tec_login():
    if request.method == 'POST':
        # 找到教师
        tec_id = request.form['tec_id']
        pwd = request.form['pwd']
        # 查找教师
        tec = Teacher.query.filter(Teacher.tec_id == tec_id).first()
        if tec is None:         #用户不存在
            abort(404)
            return redirect(url_for('tec_login'))
        else:
            if tec.pwd == pwd:
                session["tec_id"] = tec_id                                          # 设置session
                session["tec_name"] = tec.tec_name
                resp = make_response("success")
                resp.set_cookie("tec_id", tec_id, "tec_name", tec.tec_name)   # 设置cookie4h
                if tec_id == '123456':           #admin
                    return redirect(url_for('manger.admin'))
                else:
                    return redirect(url_for('teacher.tecIndex'))
            else:           # 密码错误
                abort(401)
    return redirect(url_for('teacher.tec_login'))


@app.route('/uploads/<string:filename>', methods=['GET'])
def display_img(filename):
    if request.method == 'GET':
        if filename is None:
            pass
        else:
            image_data = open('./uploads/' + filename, "rb").read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/jpg'
            return response
    else:
        pass


from utils.views.student import student
from utils.views.teacher import teacher
from utils.views.admin import manger
# 注册蓝图
app.register_blueprint(student)
app.register_blueprint(teacher)
app.register_blueprint(manger)


if __name__ == '__main__':
    app.run(debug=True)
