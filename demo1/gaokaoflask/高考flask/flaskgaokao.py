from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import (JWTManager, create_access_token,
                                jwt_required, get_jwt_identity)
from flask_sqlalchemy import SQLAlchemy
import re
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

def admin_required():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            username = get_jwt_identity()
            login_user = User.query.filter_by(username=username).first()
            if not login_user:
                return jsonify(code=401, msg="用户不存在，请重新登录")
            if login_user.role != "admin":
                return jsonify(code=403, msg="权限不足，仅管理员可访问")
            return func(*args, **kwargs)
        return wrapper
    return decorator

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///auth.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "wyz-flask-auth-2026-random-long-key-123789"

db = SQLAlchemy(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    nickname = db.Column(db.String(30), default="默认用户")
    role = db.Column(db.String(16), default="user")

USERNAME_PATTERN = re.compile(r'^[\u4e00-\u9fa5a-zA-Z0-9_]{3,20}$')
PASSWORD_PATTERN = re.compile(r'^[a-zA-Z0-9!@#$%^&*()_+-=]{6,24}$')


@app.route("/api/register", methods=["POST"])
def register():
    try:
        json_data = request.get_json()
        if json_data is None:
            return jsonify(code=400, msg="请求必须携带JSON参数")

        username = json_data.get("username", "")
        password = json_data.get("password", "")

        if not USERNAME_PATTERN.match(username):
            return jsonify(code=400, msg="用户名3~20位，仅支持中英文、数字、下划线")
        if not PASSWORD_PATTERN.match(password):
            return jsonify(code=400, msg="密码6~24位，仅支持字母、数字及!@#$%^&*()_+-=")

        exist_user = User.query.filter_by(username=username).first()
        if exist_user:
            return jsonify(code=400, msg="用户名已注册")

        hash_pwd = generate_password_hash(password)
        new_user = User(username=username, password_hash=hash_pwd)
        db.session.add(new_user)
        db.session.commit()

        return jsonify(code=200, msg="注册成功", data={"username": username})
    except Exception:
        return jsonify(code=500, msg="服务器内部异常")


@app.route("/api/login", methods=["POST"])
def login():
    try:
        json_data = request.get_json()
        if json_data is None:
            return jsonify(code=400, msg="请求必须携带JSON参数")

        username = json_data.get("username", "")
        password = json_data.get("password", "")

        if not USERNAME_PATTERN.match(username):
            return jsonify(code=400, msg="用户名3~20位，仅支持中英文、数字、下划线")
        if not PASSWORD_PATTERN.match(password):
            return jsonify(code=400, msg="密码6~24位，仅支持字母、数字及!@#$%^&*()_+-=")

        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password_hash, password):
            return jsonify(code=401, msg="账号或密码错误")

        access_token = create_access_token(
            identity=username,
            expires_delta=timedelta(minutes=10)
        )
        return jsonify(code=200, msg="登录成功", data={"token": access_token})
    except Exception:
        return jsonify(code=500, msg="服务器内部异常")


@app.route("/api/userinfo", methods=["GET"])
@jwt_required()
def userinfo():
    try:
        current_user = get_jwt_identity()
        user = User.query.filter_by(username=current_user).first()
        if not user:
            return jsonify(code=404, msg="用户不存在")
        data = {
            "id": user.id,
            "username": user.username,
            "nickname": user.nickname,
            "role": user.role
            }
        return jsonify(code=200, msg="获取个人信息成功", data=data)
    except Exception:
        return jsonify(code=500, msg="服务器内部异常")


@app.route("/api/user/edit_nickname", methods=["PUT"])
@jwt_required()
def edit_nickname():
    try:
        json_data = request.get_json()
        if json_data is None:
            return jsonify(code=400, msg="请求必须携带JSON参数")
        new_nickname = json_data.get("nickname", "")
        if len(new_nickname) > 30 or len(new_nickname) == 0:
            return jsonify(code=400, msg="昵称不能为空且最长30字符")
        login_username = get_jwt_identity()
        user = User.query.filter_by(username=login_username).first()
        user.nickname = new_nickname
        db.session.commit()
        return jsonify(code=200, msg="昵称修改成功")
    except Exception:
        return jsonify(code=500, msg="服务器内部异常")


@app.route("/api/user/update_pwd", methods=["PUT"])
@jwt_required()
def update_password():
    try:
        json_data = request.get_json()
        if json_data is None:
            return jsonify(code=400, msg="请求必须携带JSON参数")
        old_pwd = json_data.get("old_pwd", "")
        new_pwd = json_data.get("new_pwd", "")

        if not PASSWORD_PATTERN.match(new_pwd):
            return jsonify(code=400, msg="密码6~24位，仅支持字母、数字及!@#$%^&*()_+-=")

        login_username = get_jwt_identity()
        user = User.query.filter_by(username=login_username).first()
        if not check_password_hash(user.password_hash, old_pwd):
            return jsonify(code=400, msg="原密码错误")

        user.password_hash = generate_password_hash(new_pwd)
        db.session.commit()
        return jsonify(code=200, msg="密码修改成功，请重新登录",data={"need_relogin": True})
    except Exception:
        return jsonify(code=500, msg="服务器内部异常")


@app.route("/api/user/menu", methods=["GET"])
@jwt_required()
def get_user_menu():
    try:
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()

        menu_list = [
            {
                "menu_id": 1,
                "menu_name": "个人资料",
                "route": "/user/profile"
            },
            {
                "menu_id": 2,
                "menu_name": "修改昵称",
                "route": "/user/edit_nickname"
            },
            {
                "menu_id": 3,
                "menu_name": "修改密码",
                "route": "/user/update_pwd"
            },
            {
                "menu_id": 4,
                "menu_name": "高考志愿查询系统",
                "route": "/gaokao/search"
            }
        ]
        if user.role == "admin":
            menu_list.append({
                "menu_id": 99,
                "menu_name": "用户管理",
                "route": "/admin/user_list"
            })

        return jsonify(code=200, msg="菜单加载成功", data=menu_list)
    except Exception:
        return jsonify(code=500, msg="服务器内部异常")


@app.route("/api/admin/del_user", methods=["DELETE"])
@jwt_required()
@admin_required()
def delete_user():
    try:
        json_data = request.get_json()
        del_id = json_data.get("id")
        user = User.query.get(del_id)
        if not user:
            return jsonify(code=400, msg="用户不存在")
        current_name = get_jwt_identity()
        if user.username == current_name:
            return jsonify(code=400, msg="禁止删除当前登录账号")
        if user.role == "admin":
            return jsonify(code=400, msg="无权查看/删除其他管理员账号")
        db.session.delete(user)
        db.session.commit()
        return jsonify(code=200, msg="删除成功")
    except Exception:
        return jsonify(code=500, msg="服务器内部异常")


@app.route("/api/admin/all_user", methods=["GET"])
@jwt_required()
@admin_required()
def get_all_user():
    try:
        user_list = User.query.filter(User.role == "user").all()
        res = []
        for u in user_list:
            res.append({
                "id": u.id,
                "username": u.username,
                "nickname": u.nickname,
                "role": u.role
            })
        return jsonify(code=200, msg="查询全部普通用户成功", data=res)
    except Exception:
        return jsonify(code=500, msg="服务器内部异常")


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        admin_test = User.query.filter_by(username="admin").first()
        if not admin_test:
            admin_list = [
                {"username": "wyz123", "nickname": "wyz管理员", "pwd": "123456"},
                {"username": "wll123", "nickname": "wll管理员", "pwd": "123456"},
                {"username": "lgc123", "nickname": "lgc管理员", "pwd": "123456"},
                {"username": "professorHu123", "nickname": "胡教授", "pwd": "123456"}
                         ]
            for info in admin_list:
                exist_admin = User.query.filter_by(username=info["username"]).first()
                if not exist_admin:
                    new_admin = User(
                        username=info["username"],
                        password_hash=generate_password_hash(info["pwd"]),
                        nickname=info["nickname"],
                        role="admin"
                    )
                    db.session.add(new_admin)
            db.session.commit()
            print("管理员初始化完成：wyz123、wll123、lgc123、professorHu123 |初始密码123456")

    app.run(debug=True)
