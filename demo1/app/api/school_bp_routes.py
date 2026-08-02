# -*- coding: utf-8 -*-
"""
学校API接口
"""
from flask import request, jsonify
from app.api import school_bp
from app.service.school_service import SchoolService


def success_response(data=None, msg='success'):
    """统一成功响应"""
    return jsonify({'code': 0, 'msg': msg, 'data': data})


def error_response(msg='error', code=-1):
    """统一错误响应"""
    return jsonify({'code': code, 'msg': msg, 'data': None})


@school_bp.route('/search')
def search_schools():
    """
    搜索学校
    参数: name - 学校名称关键词
    """
    name = request.args.get('name', '').strip()
    limit = int(request.args.get('limit', 50))

    try:
        schools = SchoolService.search_schools(name, limit)
        return success_response(schools)
    except Exception as e:
        return error_response(f'搜索学校失败: {str(e)}')


@school_bp.route('/list')
def list_schools():
    """获取所有学校列表"""
    try:
        schools = SchoolService.get_all_schools()
        return success_response(schools)
    except Exception as e:
        return error_response(f'获取学校列表失败: {str(e)}')


@school_bp.route('/detail')
def school_detail():
    """获取学校详情"""
    school_id = request.args.get('id')
    if not school_id:
        return error_response('学校ID不能为空')

    try:
        school = SchoolService.get_school_detail(int(school_id))
        return success_response(school)
    except Exception as e:
        return error_response(f'获取学校详情失败: {str(e)}')
