# # -*- coding: utf-8 -*-
# """
# 预测记录数据访问层
# """
# import pandas as pd
# from datetime import datetime
# from app.models import db
# from app.config import (
#     TABLE_PREDICT_ARTS,
#     TABLE_PREDICT_SCIENCES,
#     TYPE_ARTS,
#     TYPE_SCIENCES
# )
#
#
# class PredictDAO:
#     @staticmethod
#     def get_predict_record(school_id, major_id, subject_type):
#         """查询预测记录"""
#         table = TABLE_PREDICT_SCIENCES if subject_type == TYPE_SCIENCES else TABLE_PREDICT_ARTS
#
#         sql = f"SELECT * FROM {table} WHERE school_id = :school_id AND major_id = :major_id"
#         df = pd.read_sql_query(sql, db.engine, params={'school_id': school_id, 'major_id': major_id})
#
#         if df.empty:
#             return None
#
#         row = df.iloc[0]
#         return {
#             'id': row.get('id'),
#             'school_id': row.get('school_id'),
#             'major_id': row.get('major_id'),
#             'major_name': row.get('major_name', ''),
#             'score_mide': int(row.get('score_mide', 0) or 0),
#             'rank_mide': int(row.get('rank_mide', 0) or 0),
#             'score_up': int(row.get('score_up', 0) or 0),
#             'rank_up': int(row.get('rank_up', 0) or 0),
#             'score_down': int(row.get('score_down', 0) or 0),
#             'rank_down': int(row.get('rank_down', 0) or 0),
#             'score_jh': int(row.get('score_jh', 0) or 0),
#             'adj_mide': int(row.get('adj_mide', 0) or 0),
#             'adj_up': int(row.get('adj_up', 0) or 0),
#             'adj_down': int(row.get('adj_down', 0) or 0)
#         }
#
#     @staticmethod
#     def save_predict_record(school_id, major_id, subject_type, data):
#         """
#         保存预测记录，存在则更新，不存在则插入
#         data: dict，包含major_name, score_mide, rank_mide, score_up, rank_up,
#               score_down, rank_down, score_jh, adj_mide, adj_up, adj_down
#         """
#         table = TABLE_PREDICT_SCIENCES if subject_type == TYPE_SCIENCES else TABLE_PREDICT_ARTS
#
#         # 检查是否存在
#         check_sql = f"SELECT id FROM {table} WHERE school_id = :school_id AND major_id = :major_id"
#         result = db.session.execute(
#             db.text(check_sql),
#             {'school_id': school_id, 'major_id': major_id}
#         )
#         existing = result.fetchone()
#
#         now = datetime.now()
#
#         if existing:
#             # 更新
#             update_fields = []
#             params = {'school_id': school_id, 'major_id': major_id}
#             for key, value in data.items():
#                 update_fields.append(f"`{key}` = :{key}")
#                 params[key] = value
#             update_fields.append("updated_at = :updated_at")
#             params['updated_at'] = now
#
#             update_sql = f"UPDATE {table} SET {', '.join(update_fields)} WHERE school_id = :school_id AND major_id = :major_id"
#             db.session.execute(db.text(update_sql), params)
#         else:
#             # 插入
#             fields = ['school_id', 'major_id']
#             placeholders = [':school_id', ':major_id']
#             params = {'school_id': school_id, 'major_id': major_id}
#             for key, value in data.items():
#                 fields.append(f"`{key}`")
#                 placeholders.append(f':{key}')
#                 params[key] = value
#             fields.extend(['created_at', 'updated_at'])
#             placeholders.extend([':created_at', ':updated_at'])
#             params['created_at'] = now
#             params['updated_at'] = now
#
#             insert_sql = f"INSERT INTO {table} ({', '.join(fields)}) VALUES ({', '.join(placeholders)})"
#             db.session.execute(db.text(insert_sql), params)
#
#         db.session.commit()
#         return True
#
#     @staticmethod
#     def get_school_predict_list(school_id, subject_type, limit=100):
#         """获取学校所有预测记录"""
#         table = TABLE_PREDICT_SCIENCES if subject_type == TYPE_SCIENCES else TABLE_PREDICT_ARTS
#
#         sql = f"""
#             SELECT * FROM {table}
#             WHERE school_id = :school_id
#             ORDER BY rank_mide ASC
#             LIMIT :limit
#         """
#         df = pd.read_sql_query(sql, db.engine, params={'school_id': school_id, 'limit': limit})
#         return df


# -*- coding: utf-8 -*-
"""
预测记录数据访问层
"""
import pandas as pd
from datetime import datetime
from app.models import db
from app.config import (
    TABLE_PREDICT_ARTS,
    TABLE_PREDICT_SCIENCES,
    TYPE_ARTS,
    TYPE_SCIENCES
)


class PredictDAO:
    @staticmethod
    def get_predict_record(school_id, major_id, subject_type):
        """查询预测记录"""
        table = TABLE_PREDICT_SCIENCES if subject_type == TYPE_SCIENCES else TABLE_PREDICT_ARTS

        sql = f"SELECT * FROM {table} WHERE school_id = %s AND major_id = %s"
        params = (school_id, major_id)
        with db.engine.raw_connection() as conn:
            df = pd.read_sql_query(sql, conn, params=params)

        if df.empty:
            return None

        row = df.iloc[0]
        return {
            'id': row.get('id'),
            'school_id': row.get('school_id'),
            'major_id': row.get('major_id'),
            'major_name': row.get('major_name', ''),
            'score_mide': int(row.get('score_mide', 0) or 0),
            'rank_mide': int(row.get('rank_mide', 0) or 0),
            'score_up': int(row.get('score_up', 0) or 0),
            'rank_up': int(row.get('rank_up', 0) or 0),
            'score_down': int(row.get('score_down', 0) or 0),
            'rank_down': int(row.get('rank_down', 0) or 0),
            'score_jh': int(row.get('score_jh', 0) or 0),
            'adj_mide': int(row.get('adj_mide', 0) or 0),
            'adj_up': int(row.get('adj_up', 0) or 0),
            'adj_down': int(row.get('adj_down', 0) or 0)
        }

    @staticmethod
    def save_predict_record(school_id, major_id, subject_type, data):
        """
        保存预测记录，存在则更新，不存在则插入
        data: dict，包含major_name, score_mide, rank_mide, score_up, rank_up,
              score_down, rank_down, score_jh, adj_mide, adj_up, adj_down
        """
        table = TABLE_PREDICT_SCIENCES if subject_type == TYPE_SCIENCES else TABLE_PREDICT_ARTS

        # 检查是否存在，使用原生pymysql连接
        check_sql = f"SELECT id FROM {table} WHERE school_id = %s AND major_id = %s"
        check_params = (school_id, major_id)
        existing = None
        with db.engine.raw_connection() as conn:
            cur = conn.cursor()
            cur.execute(check_sql, check_params)
            existing = cur.fetchone()
            cur.close()

        now = datetime.now()

        with db.engine.raw_connection() as conn:
            cur = conn.cursor()
            if existing:
                # 更新逻辑
                update_fields = []
                update_params = []
                for key, value in data.items():
                    update_fields.append(f"`{key}` = %s")
                    update_params.append(value)
                update_fields.append("updated_at = %s")
                update_params.append(now)
                # where条件参数
                update_params.append(school_id)
                update_params.append(major_id)

                update_sql = f"UPDATE {table} SET {', '.join(update_fields)} WHERE school_id = %s AND major_id = %s"
                cur.execute(update_sql, update_params)
            else:
                # 插入逻辑
                fields = ['school_id', 'major_id']
                placeholders = ['%s', '%s']
                insert_params = [school_id, major_id]
                for key, value in data.items():
                    fields.append(f"`{key}`")
                    placeholders.append('%s')
                    insert_params.append(value)
                fields.extend(['created_at', 'updated_at'])
                placeholders.extend(['%s', '%s'])
                insert_params.append(now)
                insert_params.append(now)

                insert_sql = f"INSERT INTO {table} ({', '.join(fields)}) VALUES ({', '.join(placeholders)})"
                cur.execute(insert_sql, insert_params)
            conn.commit()
            cur.close()
        return True

    @staticmethod
    def get_school_predict_list(school_id, subject_type, limit=100):
        """获取学校所有预测记录"""
        table = TABLE_PREDICT_SCIENCES if subject_type == TYPE_SCIENCES else TABLE_PREDICT_ARTS

        sql = f"""
            SELECT * FROM {table} 
            WHERE school_id = %s 
            ORDER BY rank_mide ASC 
            LIMIT %s
        """
        params = (school_id, limit)
        with db.engine.raw_connection() as conn:
            df = pd.read_sql_query(sql, conn, params=params)
        return df