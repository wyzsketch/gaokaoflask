# -*- coding: utf-8 -*-
"""
页面路由
"""
from flask import render_template
from app.api import page_bp


@page_bp.route('/')
def index():
    """首页"""
    return render_template('index.html')


@page_bp.route('/predict')
def predict():
    """预测页面"""
    return render_template('predict.html')
