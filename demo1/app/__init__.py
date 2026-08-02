# -*- coding: utf-8 -*-
"""
Flask应用工厂
"""
from flask import Flask
from app.models import db
from app.config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, SECRET_KEY


def create_app():
    """创建并配置Flask应用"""
    app = Flask(
        __name__,
        template_folder='../templates',
        static_folder='../static'
    )

    # 配置数据库
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['SECRET_KEY'] = SECRET_KEY

    # 初始化数据库
    db.init_app(app)

    # 注册蓝图
    from app.api import register_blueprints
    register_blueprints(app)

    return app
