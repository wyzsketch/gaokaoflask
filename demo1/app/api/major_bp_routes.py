# -*- coding: utf-8 -*-
"""
专业API接口
"""
from flask import request, jsonify
from app.api import major_bp
from app.service.major_service import MajorService
from app.config import TYPE_SCIENCES


def success_response(data=None, msg='success'):
    return jsonify({'code': 0, 'msg': msg, 'data': data})


def error_response(msg='error', code=-1):
    return jsonify({'code': code, 'msg': msg, 'data': None})


@major_bp.route('/search')
def search_majors():
    """
    搜索专业
    参数:
        school_id - 学校ID
        type - 科目类型(0文科, 1理科)
        name - 专业名称关键词
    """
    school_id = request.args.get('school_id')
    subject_type = request.args.get('type', str(TYPE_SCIENCES))
    name = request.args.get('name', '').strip()
    limit = int(request.args.get('limit', 100))

    if not school_id:
        return error_response('学校ID不能为空')

    try:
        majors = MajorService.search_majors(
            int(school_id),
            int(subject_type),
            name,
            limit
        )
        return success_response(majors)
    except Exception as e:
        return error_response(f'搜索专业失败: {str(e)}')


@major_bp.route('/detail')
def major_detail():
    """获取专业详情"""
    major_id = request.args.get('id')
    if not major_id:
        return error_response('专业ID不能为空')

    try:
        major = MajorService.get_major_detail(int(major_id))
        return success_response(major)
    except Exception as e:
        return error_response(f'获取专业详情失败: {str(e)}')
