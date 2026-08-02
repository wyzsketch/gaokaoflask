from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import (JWTManager, create_access_token,
                                jwt_required, get_jwt_identity)
from flask_sqlalchemy import SQLAlchemy
import re
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)
# 数据库配置
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///auth.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "wyz-flask-auth-2026-random-long-key-123789"

db = SQLAlchemy(app)
jwt = JWTManager(app)

# 数据库模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

# 正则规则
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

        # 1.格式正则校验
        if not USERNAME_PATTERN.match(username):
            return jsonify(code=400, msg="用户名3~20位，仅支持中英文、数字、下划线")
        if not PASSWORD_PATTERN.match(password):
            return jsonify(code=400, msg="密码6~24位，仅支持字母、数字及!@#$%^&*()_+-=")

        # 2.查询账号是否存在
        exist_user = User.query.filter_by(username=username).first()
        if exist_user:
            return jsonify(code=400, msg="用户名已注册")

        # 3.哈希加密写入数据库
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

        # 【先格式校验，再查数据库】最优顺序
        if not USERNAME_PATTERN.match(username):
            return jsonify(code=400, msg="用户名3~20位，仅支持中英文、数字、下划线")
        if not PASSWORD_PATTERN.match(password):
            return jsonify(code=400, msg="密码6~24位，仅支持字母、数字及!@#$%^&*()_+-=")

        # 查询数据库用户
        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password_hash, password):
            return jsonify(code=401, msg="账号或密码错误")

        # 签发2分钟有效期token
        access_token = create_access_token(
            identity=username,
            expires_delta=timedelta(minutes=2)
        )
        return jsonify(code=200, msg="登录成功", data={"token": access_token})
    except Exception:
        return jsonify(code=500, msg="服务器内部异常")


@app.route("/api/userinfo", methods=["GET"])
@jwt_required()
def userinfo():
    current_user = get_jwt_identity()
    return jsonify(code=200, msg="获取个人信息成功", data={"username": current_user})


if __name__ == '__main__':
    # 必须加上：自动创建数据表
    with app.app_context():
        db.create_all()
    app.run(debug=True)