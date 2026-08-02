# -*- coding: utf-8 -*-
"""
API控制器层 - 蓝图注册
"""
from flask import Blueprint

# 页面蓝图
page_bp = Blueprint('page', __name__)

# API蓝图
school_bp = Blueprint('school', __name__, url_prefix='/api/school')
major_bp = Blueprint('major', __name__, url_prefix='/api/major')
chart_bp = Blueprint('chart', __name__, url_prefix='/api/chart')
predict_bp = Blueprint('predict', __name__, url_prefix='/api/predict')

# 导入路由模块（确保路由被注册）
from app.api import page_bp_routes
from app.api import school_bp_routes
from app.api import major_bp_routes
from app.api import chart_bp_routes
from app.api import predict_bp_routes


def register_blueprints(app):
    """注册所有蓝图到Flask应用"""
    app.register_blueprint(page_bp)
    app.register_blueprint(school_bp)
    app.register_blueprint(major_bp)
    app.register_blueprint(chart_bp)
    app.register_blueprint(predict_bp)
