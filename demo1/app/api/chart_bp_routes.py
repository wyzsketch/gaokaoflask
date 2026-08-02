# -*- coding: utf-8 -*-
"""
图表API接口 - 返回ECharts所需数据
"""
from flask import request, jsonify
from app.api import chart_bp
from app.service.predict_service import PredictService
from app.config import TYPE_SCIENCES


def success_response(data=None, msg='success'):
    return jsonify({'code': 0, 'msg': msg, 'data': data})


def error_response(msg='error', code=-1):
    return jsonify({'code': code, 'msg': msg, 'data': None})


@chart_bp.route('/get_data', methods=['POST'])
def get_chart_data():
    """
    获取图表数据
    POST参数:
        school_id - 学校ID
        major_id - 专业ID
        subject_type - 科目类型
        adj_mide - 中位修正
        adj_up - 上限修正
        adj_down - 下限修正
    """
    data = request.get_json() if request.is_json else request.form

    school_id = data.get('school_id')
    major_id = data.get('major_id')
    subject_type = int(data.get('subject_type', TYPE_SCIENCES))
    adj_mide = int(data.get('adj_mide', 0) or 0)
    adj_up = int(data.get('adj_up', 0) or 0)
    adj_down = int(data.get('adj_down', 0) or 0)

    if not school_id or not major_id:
        return error_response('学校ID和专业ID不能为空')

    try:
        result = PredictService.predict(
            int(school_id),
            int(major_id),
            subject_type,
            adj_mide,
            adj_up,
            adj_down
        )
        return success_response(result)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return error_response(f'获取图表数据失败: {str(e)}')


@chart_bp.route('/history', methods=['GET'])
def get_history():
    """
    获取专业历史分数（用于调试或单独展示）
    """
    school_id = request.args.get('school_id')
    major_id = request.args.get('major_id')
    subject_type = int(request.args.get('type', TYPE_SCIENCES))

    if not school_id or not major_id:
        return error_response('学校ID和专业ID不能为空')

    try:
        df = PredictService.get_major_history_scores(int(school_id), int(major_id), subject_type)
        history = []
        for idx, row in df.iterrows():
            history.append({
                'year': int(idx),
                'score': int(row['score']),
                'rank': int(row['section'])
            })
        return success_response(history)
    except Exception as e:
        return error_response(f'获取历史数据失败: {str(e)}')
