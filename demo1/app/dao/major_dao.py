# -*- coding: utf-8 -*-
"""
专业数据访问层
"""
import pandas as pd
from app.models import db
from app.config import (
    TABLE_SCHOOL_MAJOR,
    TABLE_UNION_MAJOR_SCORE_ARTS,
    TABLE_UNION_MAJOR_SCORE_SCIENCES,
    TYPE_ARTS,
    TYPE_SCIENCES
)


class MajorDAO:
    @staticmethod
    def search_majors(school_id, subject_type, name, limit=100):
        """
        根据学校ID、科目类型、专业名称模糊查询专业
        关联合并分数表，只返回有历史数据的专业
        """
        score_table = TABLE_UNION_MAJOR_SCORE_SCIENCES if subject_type == TYPE_SCIENCES else TABLE_UNION_MAJOR_SCORE_ARTS

        sql = f"""
            SELECT a.id, b.major_name as name, a.remark 
            FROM {TABLE_SCHOOL_MAJOR} AS a 
            INNER JOIN {score_table} AS b 
            ON a.school_id = b.school_id AND a.id = b.major_id 
            WHERE a.school_id = :school_id 
            AND (a.name LIKE :name1 OR a.remark LIKE :name2) 
            AND (b.invisible IS NULL OR b.invisible != 1)
            ORDER BY b.major_name
            LIMIT :limit
        """
        result = db.session.execute(
            db.text(sql),
            {
                'school_id': school_id,
                'name1': f'{name}%',
                'name2': f'%{name}%',
                'limit': limit
            }
        )
        majors = []
        for row in result.fetchall():
            major_name = row[1] or ''
            remark = row[2] or ''
            # 如果专业名不含括号，加上备注
            if '（' not in major_name and remark:
                display_name = major_name + remark
            else:
                display_name = major_name
            majors.append({
                'id': row[0],
                'name': major_name,
                'display_name': display_name,
                'remark': remark
            })
        return majors

    @staticmethod
    def get_major_by_id(major_id):
        """根据ID获取专业"""
        sql = f"SELECT id, school_id, name, remark, code FROM {TABLE_SCHOOL_MAJOR} WHERE id = :id"
        result = db.session.execute(db.text(sql), {'id': major_id})
        row = result.fetchone()
        if row:
            return {
                'id': row[0],
                'school_id': row[1],
                'name': row[2],
                'remark': row[3] or '',
                'code': row[4] or ''
            }
        return None

    @staticmethod
    def get_school_majors_df(school_id):
        """获取学校所有专业DataFrame"""
        sql = f"SELECT * FROM {TABLE_SCHOOL_MAJOR} WHERE school_id = :school_id"
        return pd.read_sql_query(sql, db.engine, params={'school_id': school_id})
