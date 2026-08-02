# # -*- coding: utf-8 -*-
# """
# 学校数据访问层
# """
# import pandas as pd
# from app.models import db
# from app.models.school import School
# from app.config import TABLE_SCHOOLS
#
#
# class SchoolDAO:
#     @staticmethod
#     def get_all_schools():
#         """获取所有学校"""
#         result = db.session.execute(
#             db.text(f"SELECT id, name, code FROM {TABLE_SCHOOLS} ORDER BY name")
#         )
#         return [{'id': row[0], 'name': row[1], 'code': row[2] or ''} for row in result.fetchall()]
#
#     @staticmethod
#     def search_schools_by_name(name, limit=50):
#         """根据名称模糊查询学校"""
#         sql = f"""
#             SELECT id, name, code FROM {TABLE_SCHOOLS}
#             WHERE name LIKE :name
#             ORDER BY name
#             LIMIT :limit
#         """
#         result = db.session.execute(
#             db.text(sql),
#             {'name': f'%{name}%', 'limit': limit}
#         )
#         return [{'id': row[0], 'name': row[1], 'code': row[2] or ''} for row in result.fetchall()]
#
#     @staticmethod
#     def get_school_by_id(school_id):
#         """根据ID获取学校"""
#         sql = f"SELECT id, name, code FROM {TABLE_SCHOOLS} WHERE id = :id"
#         result = db.session.execute(db.text(sql), {'id': school_id})
#         row = result.fetchone()
#         if row:
#             return {'id': row[0], 'name': row[1], 'code': row[2] or ''}
#         return None
#
#     @staticmethod
#     def get_schools_df():
#         """获取所有学校DataFrame"""
#         sql = f"SELECT * FROM {TABLE_SCHOOLS}"
#         return pd.read_sql_query(sql, db.engine)


# -*- coding: utf-8 -*-
"""
学校数据访问层
"""
import pandas as pd
from app.models import db
from app.config import TABLE_SCHOOLS


class SchoolDAO:
    @staticmethod
    def get_all_schools():
        """获取所有学校"""
        sql = f"SELECT id, name, code FROM {TABLE_SCHOOLS} ORDER BY name"
        # 获取pymysql原生连接执行
        with db.engine.raw_connection() as conn:
            cur = conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            cur.close()
        return [{'id': row[0], 'name': row[1], 'code': row[2] or ''} for row in rows]

    @staticmethod
    def search_schools_by_name(name, limit=50):
        """根据名称模糊查询学校"""
        sql = f"""
            SELECT id, name, code FROM {TABLE_SCHOOLS} 
            WHERE name LIKE %s 
            ORDER BY name 
            LIMIT %s
        """
        params = (f'%{name}%', limit)
        with db.engine.raw_connection() as conn:
            cur = conn.cursor()
            cur.execute(sql, params)
            rows = cur.fetchall()
            cur.close()
        return [{'id': row[0], 'name': row[1], 'code': row[2] or ''} for row in rows]

    @staticmethod
    def get_school_by_id(school_id):
        """根据ID获取学校"""
        sql = f"SELECT id, name, code FROM {TABLE_SCHOOLS} WHERE id = %s"
        params = (school_id,)
        with db.engine.raw_connection() as conn:
            cur = conn.cursor()
            cur.execute(sql, params)
            row = cur.fetchone()
            cur.close()
        if row:
            return {'id': row[0], 'name': row[1], 'code': row[2] or ''}
        return None

    @staticmethod
    def get_schools_df():
        """获取所有学校DataFrame"""
        sql = f"SELECT * FROM {TABLE_SCHOOLS}"
        with db.engine.raw_connection() as conn:
            df = pd.read_sql_query(sql, conn)
        return df