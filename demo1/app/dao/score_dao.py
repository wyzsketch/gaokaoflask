# # -*- coding: utf-8 -*-
# """
# 分数历史数据访问层
# """
# import pandas as pd
# from app.models import db
# from app.config import (
#     TABLE_UNION_MAJOR_SCORE_ARTS,
#     TABLE_UNION_MAJOR_SCORE_SCIENCES,
#     TABLE_MAJOR_SCORE_ARTS,
#     TABLE_MAJOR_SCORE_SCIENCES,
#     TYPE_ARTS,
#     TYPE_SCIENCES
# )
#
#
# class ScoreDAO:
#     @staticmethod
#     def get_major_scores_df(school_id, major_id, subject_type):
#         """
#         获取专业历年分数和位次
#         返回DataFrame，index为年份，列为score和section
#         """
#         score_table = TABLE_UNION_MAJOR_SCORE_SCIENCES if subject_type == TYPE_SCIENCES else TABLE_UNION_MAJOR_SCORE_ARTS
#
#         sql = f"SELECT * FROM {score_table} WHERE school_id = :school_id AND major_id = :major_id"
#         df = pd.read_sql_query(sql, db.engine, params={'school_id': school_id, 'major_id': major_id})
#
#         if df.empty:
#             return pd.DataFrame({'score': [], 'section': []})
#
#         data = {'score': [], 'section': []}
#         result_df = pd.DataFrame(data)
#         columns = df.columns
#
#         # 从后往前遍历列，跳过前3列(id, school_id, major_id)和最后一列(invisible)
#         # 列格式: 年份_score, 年份_section 交替
#         for i in range(3, len(columns) - 1, 2):
#             if i + 1 >= len(columns):
#                 break
#             score_col = columns[i]
#             section_col = columns[i + 1]
#
#             # 确保是score和section配对
#             if 'score' not in score_col.lower() and 'sec' not in section_col.lower():
#                 continue
#
#             min_score = df.iloc[0, i]
#             min_section = df.iloc[0, i + 1]
#
#             if pd.isna(min_score) or pd.isna(min_section):
#                 continue
#             if min_score <= 0 or min_section <= 0:
#                 continue
#
#             # 提取年份
#             year = score_col.split('_')[0]
#             try:
#                 year_int = int(year)
#             except (ValueError, IndexError):
#                 continue
#
#             new_row = pd.DataFrame(
#                 {'score': [int(min_score)], 'section': [int(min_section)]},
#                 index=[year_int]
#             )
#             result_df = pd.concat([result_df, new_row], axis=0)
#
#         # 按年份排序
#         result_df = result_df.sort_index()
#         return result_df
#
#     @staticmethod
#     def get_all_major_scores(school_id, subject_type):
#         """获取学校所有专业的分数历史"""
#         score_table = TABLE_MAJOR_SCORE_SCIENCES if subject_type == TYPE_SCIENCES else TABLE_MAJOR_SCORE_ARTS
#
#         sql = f"""
#             SELECT * FROM {score_table}
#             WHERE school_id = :school_id AND (deleted IS NULL OR deleted = 0)
#         """
#         df = pd.read_sql_query(sql, db.engine, params={'school_id': school_id})
#         if 'deleted' in df.columns:
#             df = df.drop(columns=['deleted'])
#         return df


# -*- coding: utf-8 -*-
"""
分数历史数据访问层
"""
import pandas as pd
from app.models import db
from app.config import (
    TABLE_UNION_MAJOR_SCORE_ARTS,
    TABLE_UNION_MAJOR_SCORE_SCIENCES,
    TABLE_MAJOR_SCORE_ARTS,
    TABLE_MAJOR_SCORE_SCIENCES,
    TYPE_ARTS,
    TYPE_SCIENCES
)


class ScoreDAO:
    @staticmethod
    def get_major_scores_df(school_id, major_id, subject_type):
        """
        获取专业历年分数和位次
        返回DataFrame，index为年份，列为score和section
        """
        score_table = TABLE_UNION_MAJOR_SCORE_SCIENCES if subject_type == TYPE_SCIENCES else TABLE_UNION_MAJOR_SCORE_ARTS

        # pymysql标准%s占位符
        sql = f"SELECT * FROM {score_table} WHERE school_id = %s AND major_id = %s"
        params = (school_id, major_id)
        # 使用原生pymysql连接执行查询
        with db.engine.raw_connection() as conn:
            df = pd.read_sql_query(sql, conn, params=params)

        if df.empty:
            return pd.DataFrame({'score': [], 'section': []})

        data = {'score': [], 'section': []}
        result_df = pd.DataFrame(data)
        columns = df.columns

        # 从后往前遍历列，跳过前3列(id, school_id, major_id)和最后一列(invisible)
        # 列格式: 年份_score, 年份_section 交替
        for i in range(3, len(columns) - 1, 2):
            if i + 1 >= len(columns):
                break
            score_col = columns[i]
            section_col = columns[i + 1]

            # 确保是score和section配对
            if 'score' not in score_col.lower() and 'sec' not in section_col.lower():
                continue

            min_score = df.iloc[0, i]
            min_section = df.iloc[0, i + 1]

            if pd.isna(min_score) or pd.isna(min_section):
                continue
            if min_score <= 0 or min_section <= 0:
                continue

            # 提取年份
            year = score_col.split('_')[0]
            try:
                year_int = int(year)
            except (ValueError, IndexError):
                continue

            new_row = pd.DataFrame(
                {'score': [int(min_score)], 'section': [int(min_section)]},
                index=[year_int]
            )
            result_df = pd.concat([result_df, new_row], axis=0)

        # 按年份排序
        result_df = result_df.sort_index()
        return result_df

    @staticmethod
    def get_all_major_scores(school_id, subject_type):
        """获取学校所有专业的分数历史"""
        score_table = TABLE_MAJOR_SCORE_SCIENCES if subject_type == TYPE_SCIENCES else TABLE_MAJOR_SCORE_ARTS

        sql = f"""
            SELECT * FROM {score_table} 
            WHERE school_id = %s AND (deleted IS NULL OR deleted = 0)
        """
        params = (school_id,)
        with db.engine.raw_connection() as conn:
            df = pd.read_sql_query(sql, conn, params=params)
        if 'deleted' in df.columns:
            df = df.drop(columns=['deleted'])
        return df