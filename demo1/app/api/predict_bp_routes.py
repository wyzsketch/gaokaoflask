# -*- coding: utf-8 -*-
"""
预测记录API接口
"""
from flask import request, jsonify
from app.api import predict_bp
from app.service.predict_service import PredictService
from app.config import TYPE_SCIENCES


def success_response(data=None, msg='success'):
    return jsonify({'code': 0, 'msg': msg, 'data': data})


def error_response(msg='error', code=-1):
    return jsonify({'code': code, 'msg': msg, 'data': None})


@predict_bp.route('/record', methods=['GET'])
def get_predict_record():
    """
    获取已保存的预测记录
    参数:
        school_id - 学校ID
        major_id - 专业ID
        subject_type - 科目类型
    """
    school_id = request.args.get('school_id')
    major_id = request.args.get('major_id')
    subject_type = int(request.args.get('subject_type', TYPE_SCIENCES))

    if not school_id or not major_id:
        return error_response('学校ID和专业ID不能为空')

    try:
        record = PredictService.get_predict_record(int(school_id), int(major_id), subject_type)
        return success_response(record)
    except Exception as e:
        return error_response(f'获取预测记录失败: {str(e)}')


@predict_bp.route('/save', methods=['POST'])
def save_predict():
    """
    保存预测记录
    POST参数:
        school_id - 学校ID
        major_id - 专业ID
        subject_type - 科目类型
        major_name - 专业名称
        score_mide - 中位分数
        rank_mide - 中位位次
        score_up - 上限分数
        rank_up - 上限位次
        score_down - 下限分数
        rank_down - 下限位次
        score_jh - 第三方预测分数
        adj_mide - 中位修正
        adj_up - 上限修正
        adj_down - 下限修正
    """
    data = request.get_json() if request.is_json else request.form

    school_id = data.get('school_id')
    major_id = data.get('major_id')
    subject_type = int(data.get('subject_type', TYPE_SCIENCES))

    if not school_id or not major_id:
        return error_response('学校ID和专业ID不能为空')

    try:
        predict_data = {
            'major_name': data.get('major_name', ''),
            'score_mide': int(data.get('score_mide', 0) or 0),
            'rank_mide': int(data.get('rank_mide', 0) or 0),
            'score_up': int(data.get('score_up', 0) or 0),
            'rank_up': int(data.get('rank_up', 0) or 0),
            'score_down': int(data.get('score_down', 0) or 0),
            'rank_down': int(data.get('rank_down', 0) or 0),
            'score_jh': int(data.get('score_jh', 0) or 0),
            'adj_mide': int(data.get('adj_mide', 0) or 0),
            'adj_up': int(data.get('adj_up', 0) or 0),
            'adj_down': int(data.get('adj_down', 0) or 0),
        }

        PredictService.save_predict(
            int(school_id),
            int(major_id),
            subject_type,
            predict_data
        )
        return success_response(None, '保存成功')
    except Exception as e:
        import traceback
        traceback.print_exc()
        return error_response(f'保存预测失败: {str(e)}')


@predict_bp.route('/school_list', methods=['GET'])
def get_school_predict_list():
    """
    获取学校所有专业预测列表
    """
    school_id = request.args.get('school_id')
    subject_type = int(request.args.get('subject_type', TYPE_SCIENCES))

    if not school_id:
        return error_response('学校ID不能为空')

    try:
        df = PredictService.get_school_predict_list(int(school_id), subject_type)
        records = df.to_dict('records') if not df.empty else []
        return success_response(records)
    except Exception as e:
        return error_response(f'获取预测列表失败: {str(e)}')
