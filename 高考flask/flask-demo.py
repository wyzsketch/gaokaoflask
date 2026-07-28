from flask import Flask, request, jsonify
#导入cors，允许访问后端
from flask_cors import CORS
#把登录认证功能挂载到我们当前这个 Flask 服务上。
from flask_jwt_extended import (JWTManager, create_access_token,
                                jwt_required, get_jwt_identity)
#建立简单数据库
from flask_sqlalchemy import SQLAlchemy
import re
#时间变量引入，用于限制token
from datetime import timedelta
#哈希引入
from werkzeug.security import generate_password_hash, check_password_hash
#自定义管理员权限装饰器
from functools import wraps
# 管理员权限校验装饰器
def admin_required():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 获取当前登录用户名
            username = get_jwt_identity()
            # 查询数据库拿到用户完整信息
            login_user = User.query.filter_by(username=username).first()
            if not login_user:
                return jsonify(code=401, msg="用户不存在，请重新登录")
            if login_user.role != "admin":
                return jsonify(code=403, msg="权限不足，仅管理员可访问")
            return func(*args, **kwargs)
        return wrapper
    return decorator
# 创建Flask应用实例
app = Flask(__name__)
# 开启跨域，允许前端网页访问后端接口
CORS(app)

# ----------------------数据库配置----------------------
# 使用SQLite文件数据库，自动在项目目录生成 auth.db 文件
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///auth.db"
# 关闭不必要的信号监听，消除警告
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# JWT加密密钥，用于签名登录令牌，生产环境建议使用更复杂随机字符串
app.config["JWT_SECRET_KEY"] = "wyz-flask-auth-2026-random-long-key-123789"

# 创建数据库操作对象
db = SQLAlchemy(app)
# 创建JWT管理对象
#做全局初始化，给整套 JWT 功能提供环境；
jwt = JWTManager(app)

# ----------------------数据库模型（数据表结构）----------------------
# User模型 对应数据库user数据表
class User(db.Model):
    # 主键id，     自增数据类型 → 整数     主键，每条数据唯一编号（类似身份证号）     新增用户时不用手动填写 id，第一条 id=1，第二条自动 = 2，依次递增
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 用户名字段，最大30字符，         唯一不允许重复，        不能为空
    username = db.Column(db.String(30), unique=True, nullable=False)
    # 密码哈希存储字段，不保存明文密码，长度256
    #固定格式：
    #字段变量 = db.Column(数据类型, 参数1, 参数2...)
    password_hash = db.Column(db.String(256), nullable=False)
    # 新增：昵称
    nickname = db.Column(db.String(30), default="默认用户")
    # 新增角色：user普通用户 / admin管理员
    role = db.Column(db.String(16), default="user")

# ----------------------正则校验规则（接口参数过滤，防御简易注入攻击）----------------------
# 用户名规则：3~20位，支持中文、大小写字母、数字、下划线
USERNAME_PATTERN = re.compile(r'^[\u4e00-\u9fa5a-zA-Z0-9_]{3,20}$')
# 密码规则：6~24位，大小写字母、数字、指定安全特殊符号
PASSWORD_PATTERN = re.compile(r'^[a-zA-Z0-9!@#$%^&*()_+-=]{6,24}$')


# ----------------------注册接口 POST /api/register ----------------------
@app.route("/api/register", methods=["POST"])
def register():
    try:
        # 读取前端传递的JSON请求体
        json_data = request.get_json()
        # 判断请求是否携带合法JSON数据，为空直接拦截
        if json_data is None:
            return jsonify(code=400, msg="请求必须携带JSON参数")

        # 提取用户名、密码；设置默认空字符串，避免None造成正则报错
        username = json_data.get("username", "")
        password = json_data.get("password", "")

        # 正则校验用户名格式
        if not USERNAME_PATTERN.match(username):
            return jsonify(code=400, msg="用户名3~20位，仅支持中英文、数字、下划线")
        # 正则校验密码格式
        if not PASSWORD_PATTERN.match(password):
            return jsonify(code=400, msg="密码6~24位，仅支持字母、数字及!@#$%^&*()_+-=")

        # 根据用户名查询数据库，判断账号是否已经注册
        #这套语法属于Flask - SQLAlchemy（ORM），作用：去数据库查询用户名匹配的用户
        exist_user = User.query.filter_by(username=username).first()
        if exist_user:
            return jsonify(code=400, msg="用户名已注册")

        # 将明文密码单向哈希加密
        hash_pwd = generate_password_hash(password)
        # 创建用户对象
        new_user = User(username=username, password_hash=hash_pwd)
        # 添加到数据库会话
        db.session.add(new_user)
        # 提交事务，真正写入数据库auth.db
        db.session.commit()

        # 注册成功返回信息
        return jsonify(code=200, msg="注册成功", data={"username": username})
    except Exception:
        # 捕获全部异常，统一返回服务器错误，避免把代码错误暴露给前端
        return jsonify(code=500, msg="服务器内部异常")


# ----------------------登录接口 POST /api/login ----------------------
@app.route("/api/login", methods=["POST"])
def login():
    try:
        # 获取前端JSON数据
        json_data = request.get_json()
        if json_data is None:
            return jsonify(code=400, msg="请求必须携带JSON参数")

        # 提取账号密码，默认空字符串
        #用("username", "")最好，可以避免冗余数据造成报错
        username = json_data.get("username", "")
        password = json_data.get("password", "")

        # 第一步：先校验参数格式（优先拦截非法字符，减少数据库查询压力）
        if not USERNAME_PATTERN.match(username):
            return jsonify(code=400, msg="用户名3~20位，仅支持中英文、数字、下划线")
        if not PASSWORD_PATTERN.match(password):
            return jsonify(code=400, msg="密码6~24位，仅支持字母、数字及!@#$%^&*()_+-=")

        # 根据用户名查询数据库用户信息
        user = User.query.filter_by(username=username).first()
        # 用户不存在 或者 密码哈希校验失败，统一提示，防止黑客枚举有效账号
        if not user or not check_password_hash(user.password_hash, password):
            return jsonify(code=401, msg="账号或密码错误")

        # 创建登录令牌，identity存入用户名，设置有效期10分钟
        #登录成功颁发令牌
        access_token = create_access_token(
            identity=username,
            expires_delta=timedelta(minutes=10)
        )
        # 返回token给前端保存
        return jsonify(code=200, msg="登录成功", data={"token": access_token})
    except Exception:
        return jsonify(code=500, msg="服务器内部异常")


# ----------------------获取用户信息接口 GET /api/userinfo ----------------------
@app.route("/api/userinfo", methods=["GET"])
# jwt_required 装饰器：必须携带合法有效的token才能访问接口
@jwt_required() #【鉴权装饰器，来自 JWT 扩展】#检查请求头有没有携带
                #1，token，校验 token 是否被篡改、有没有过期
                #2，校验通过 → 执行下方 userinfo() 函数
                #3，校验失败 → 直接返回 401 错误，不会执行函数
def userinfo():
       #用户中心基础接口
       #需要登录鉴权，读取当前登录账号完整资料
    try:
        # 从token中读取存入的身份信息（用户名）
        current_user = get_jwt_identity()
        # 根据用户名查询数据库完整用户信息
        user = User.query.filter_by(username=current_user).first()
        # 判断用户是否存在（防止数据库数据被手动删除，token还没过期的异常场景）
        if not user:
            return jsonify(code=404, msg="用户不存在")
        # 返回用户信息，不返回密码哈希！
        data = {
            "id": user.id,
            "username": user.username,
            "nickname": user.nickname,
            "role": user.role
            }
        return jsonify(code=200, msg="获取个人信息成功", data=data)
    except Exception:
        # 捕获所有未知异常，统一对外返回500，避免泄露代码报错信息
        return jsonify(code=500, msg="服务器内部异常")

# ----------------------用户中心：修改昵称 PUT /api/user/edit_nickname ----------------------
@app.route("/api/user/edit_nickname", methods=["PUT"])
@jwt_required() # 需要登录鉴权
def edit_nickname():
    #登录用户修改自己的昵称
    try:
        # 接收前端提交的JSON请求体
        json_data = request.get_json()
        # 判断请求是否携带合法JSON
        if json_data is None:
            return jsonify(code=400, msg="请求必须携带JSON参数")
        # 提取前端传入昵称，默认空字符串
        new_nickname = json_data.get("nickname", "")
        # 简单长度校验
        if len(new_nickname) > 30 or len(new_nickname) == 0:
            return jsonify(code=400, msg="昵称不能为空且最长30字符")
        # 获取当前登录用户名
        login_username = get_jwt_identity()
        # 查询登录用户数据
        user = User.query.filter_by(username=login_username).first()
        # 覆盖原有昵称
        user.nickname = new_nickname
        # 提交事务，写入数据库
        db.session.commit()
        return jsonify(code=200, msg="昵称修改成功")
    except Exception:
        return jsonify(code=500, msg="服务器内部异常")

# ----------------------用户中心：修改密码 PUT /api/user/update_pwd ----------------------
@app.route("/api/user/update_pwd", methods=["PUT"])
@jwt_required()
def update_password():
    #用户修改登录密码
    #逻辑：先校验旧密码正确 → 生成新哈希覆盖原有密码
    #修改密码后建议前端清除token，跳转登录页面
    try:
        json_data = request.get_json()
        if json_data is None:
            return jsonify(code=400, msg="请求必须携带JSON参数")
        # 获取前端传入新旧密码
        old_pwd = json_data.get("old_pwd", "")
        new_pwd = json_data.get("new_pwd", "")

        # 密码正则校验，复用全局规则
        if not PASSWORD_PATTERN.match(new_pwd):
            return jsonify(code=400, msg="密码6~24位，仅支持字母、数字及!@#$%^&*()_+-=")

        login_username = get_jwt_identity()
        user = User.query.filter_by(username=login_username).first()
        # 校验旧密码是否正确        # 使用哈希比对函数校验原始密码
        if not check_password_hash(user.password_hash, old_pwd):
            return jsonify(code=400, msg="原密码错误")

        # 设置新密码哈希 # 将新密码单向哈希，覆盖旧密码哈希
        user.password_hash = generate_password_hash(new_pwd)
        db.session.commit()
        # 修改密码后建议前端主动清除本地token，重新登录# 增加need_relogin标识，提示前端需要重新登录
        return jsonify(code=200, msg="密码修改成功，请重新登录",data={"need_relogin": True})
    except Exception:
        return jsonify(code=500, msg="服务器内部异常")


# ----------------------用户中心：获取业务导航入口 GET /api/user/menu ----------------------
@app.route("/api/user/menu", methods=["GET"])
@jwt_required()
def get_user_menu():
    """
    用户中心功能导航入口
    根据角色返回可访问模块，普通用户可见高考查询；管理员额外可见用户管理
    """
    try:
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()

        # 基础菜单：所有登录用户都可见
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
        # 管理员追加权限管理菜单
        if user.role == "admin":
            (menu_list.append({
                "menu_id": 99,
                "menu_name": "用户管理",
                "route": "/admin/user_list"
            }))

        return jsonify(code=200, msg="菜单加载成功", data=menu_list)
    except Exception:
        return jsonify(code=500, msg="服务器内部异常")

# ----------------------管理员接口：删除用户 DELETE /api/admin/del_user ----------------------
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
        # 禁止删除自己
        if user.username == current_name:
            return jsonify(code=400, msg="禁止删除当前登录账号")
        # 关键限制：不允许操作管理员角色
        if user.role == "admin":
            return jsonify(code=400, msg="无权查看/删除其他管理员账号")
        db.session.delete(user)
        db.session.commit()
        return jsonify(code=200, msg="删除成功")
    except Exception:
        return jsonify(code=500, msg="服务器内部异常")

# ----------------------权限管理：管理员专属接口 GET /api/admin/all_user ----------------------
@app.route("/api/admin/all_user", methods=["GET"])
@jwt_required()       # 第一层：必须登录
@admin_required()     # 第二层：必须是管理员
def get_all_user():
    try:
        # 只查询普通用户，自动过滤所有管理员admin，前端无法看到管理员
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
# ----------------------程序入口----------------------
if __name__ == '__main__':
    # 应用上下文，首次运行自动创建数据库数据表
    with app.app_context():
        # 创建数据表，仅新建不存在的表；已有表不会改动
        db.create_all()
        # 放在if __name__ == '__main__':内部 with app.app_context()里面
        # 仅首次运行生效，避免重复创建
        admin_test = User.query.filter_by(username="admin").first()
        if not admin_test:
            # 4名永久管理员
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
                    #临时存储
                    db.session.add(new_admin)
            #写入数据库
            db.session.commit()
            print("管理员初始化完成：wyz123、wll123、lgc123、professorHu123 |初始密码123456")

    # 启动web服务，debug=True开发模式，代码修改自动重启
    app.run(debug=True)