# -*- coding: utf-8 -*-
"""
预测业务服务层 - 核心预测算法
基于线性回归的高考位次预测
"""
import os
import sys
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

from app.dao.score_dao import ScoreDAO
from app.dao.predict_dao import PredictDAO
from app.dao.school_dao import SchoolDAO
from app.config import (
    TYPE_ARTS,
    TYPE_SCIENCES,
    PREDICT_YEAR,
    SCORE_EXCEL_FILE
)


class PredictService:
    # 缓存一分一段表
    _arts_score_df = None
    _sciences_score_df = None

    @classmethod
    def _get_score_df(cls, subject_type):
        """获取一分一段表DataFrame（带缓存）"""
        if subject_type == TYPE_SCIENCES:
            if cls._sciences_score_df is None:
                if os.path.exists(SCORE_EXCEL_FILE):
                    cls._sciences_score_df = pd.read_excel(SCORE_EXCEL_FILE, sheet_name="理科", index_col=0)
                else:
                    cls._sciences_score_df = pd.DataFrame()
            return cls._sciences_score_df
        else:
            if cls._arts_score_df is None:
                if os.path.exists(SCORE_EXCEL_FILE):
                    cls._arts_score_df = pd.read_excel(SCORE_EXCEL_FILE, sheet_name="文科", index_col=0)
                else:
                    cls._arts_score_df = pd.DataFrame()
            return cls._arts_score_df

    @staticmethod
    def get_score_by_rank(subject_type, rank):
        """根据位次换算分数"""
        df = PredictService._get_score_df(subject_type)
        if df.empty:
            return 0
        last_score = 750
        for idx, row in df.iterrows():
            try:
                accumulate = int(row.get("accumulate", 0))
            except (ValueError, TypeError):
                continue
            if accumulate > rank:
                return last_score
            last_score = idx
        return last_score

    @staticmethod
    def get_major_history_scores(school_id, major_id, subject_type):
        """获取专业历年分数数据"""
        return ScoreDAO.get_major_scores_df(school_id, major_id, subject_type)

    @staticmethod
    def linear_regression_predict(years, sections):
        """
        线性回归预测
        返回: (model, predict_value)
        """
        model = LinearRegression()
        X = np.array(years).reshape(-1, 1)
        y = sections
        model.fit(X, y)
        predict_X = np.array([PREDICT_YEAR]).reshape(-1, 1)
        predict_val = model.predict(predict_X)[0]
        return model, int(predict_val)

    @staticmethod
    def calculate_predict(df_scores, adj_mide=0, adj_up=0, adj_down=0):
        """
        核心预测计算
        参数:
            df_scores: DataFrame，index为年份，列为score和section
            adj_mide: 中位修正
            adj_up: 上限修正（位次更小=更好，所以adj_up通常为负数）
            adj_down: 下限修正（位次更大=更差，所以adj_down通常为正数）
        返回:
            dict: 包含预测结果
        """
        result = {
            'years': [],
            'history_ranks': [],
            'history_scores': [],
            'predict_mid': None,
            'predict_up': None,
            'predict_down': None,
            'predict_score_mid': 0,
            'predict_score_up': 0,
            'predict_score_down': 0,
            'min_rank': 0,
            'max_rank': 0,
            'slope': 0,
            'intercept': 0
        }

        if df_scores.empty:
            return result

        # 提取历史数据
        years = []
        sections = []
        scores = []

        for idx, row in df_scores.iterrows():
            sec = int(row["section"])
            score = int(row["score"])
            years.append(int(idx))
            sections.append(sec)
            scores.append(score)

        result['years'] = years
        result['history_ranks'] = sections
        result['history_scores'] = scores

        if len(sections) < 2:
            # 只有1条数据，直接用该数据做预测
            predict0 = sections[-1]
            predict = predict0 + adj_mide
            d = predict0 / 5
            min_rank = predict0 - d // 2 + adj_up
            max_rank = predict0 + d // 2 + adj_down

            result['predict_mid'] = predict
            result['predict_up'] = int(min_rank)
            result['predict_down'] = int(max_rank)
            result['min_rank'] = int(min_rank)
            result['max_rank'] = int(max_rank)
            return result

        # 过滤异常值（偏离平均值100%以上的）
        average_sec = np.mean(sections)
        valid_years = []
        valid_sections = []

        min_rank = sys.maxsize
        max_rank = 0

        for i, sec in enumerate(sections):
            if average_sec > 0 and abs((sec - average_sec) / average_sec) > 1:
                continue
            valid_years.append(years[i])
            valid_sections.append(sec)
            if sec < min_rank:
                min_rank = sec
            if sec > max_rank:
                max_rank = sec

        if len(valid_sections) < 2:
            # 过滤后数据不足，使用全部数据
            valid_years = years
            valid_sections = sections
            min_rank = min(sections)
            max_rank = max(sections)

        # 线性回归
        model, predict_mid_raw = PredictService.linear_regression_predict(valid_years, valid_sections)
        predict_mid = predict_mid_raw + adj_mide

        slope = model.coef_[0]
        intercept = model.intercept_

        # 计算偏差d（历史数据与回归线的最大偏差 * 1.1）
        d = 0
        for i, year in enumerate(valid_years):
            predicted = slope * year + intercept
            actual = valid_sections[i]
            deviation = abs(actual - predicted)
            if deviation > d:
                d = deviation
        d = d * 1.1

        # 上下限
        b1 = intercept - d + adj_up  # 上限线截距（位次更小）
        b2 = intercept + d + adj_down  # 下限线截距（位次更大）

        predict_up = int(slope * PREDICT_YEAR + b1)
        predict_down = int(slope * PREDICT_YEAR + b2)

        # 更新min/max用于图表缩放
        if predict_mid > max_rank:
            max_rank = predict_mid
        elif predict_mid < min_rank:
            min_rank = predict_mid

        if min_rank > predict_up:
            min_rank += (predict_up - min_rank) // 4
        if max_rank < predict_down:
            max_rank += (predict_down - max_rank) // 4

        result['predict_mid'] = predict_mid
        result['predict_up'] = predict_up
        result['predict_down'] = predict_down
        result['min_rank'] = int(min_rank)
        result['max_rank'] = int(max_rank)
        result['slope'] = slope
        result['intercept'] = intercept

        return result

    @staticmethod
    def predict(school_id, major_id, subject_type, adj_mide=0, adj_up=0, adj_down=0):
        """
        完整预测流程
        返回预测结果和图表数据
        """
        # 1. 获取历史分数
        df_scores = PredictService.get_major_history_scores(school_id, major_id, subject_type)

        # 2. 计算预测
        predict_result = PredictService.calculate_predict(df_scores, adj_mide, adj_up, adj_down)

        # 3. 位次换算分数
        if predict_result['predict_mid'] is not None:
            predict_result['predict_score_mid'] = PredictService.get_score_by_rank(subject_type, predict_result['predict_mid'])
            predict_result['predict_score_up'] = PredictService.get_score_by_rank(subject_type, predict_result['predict_up'])
            predict_result['predict_score_down'] = PredictService.get_score_by_rank(subject_type, predict_result['predict_down'])

        # 4. 构建ECharts数据
        echarts_data = PredictService.build_echarts_data(predict_result)

        # 5. 构建预测文本
        subject_name = "理" if subject_type == TYPE_SCIENCES else "文"
        predict_text = (
            f"中:{predict_result['predict_score_mid']}分/{predict_result['predict_mid']}位 "
            f"上:{predict_result['predict_score_up']}分/{predict_result['predict_up']}位 "
            f"下:{predict_result['predict_score_down']}分/{predict_result['predict_down']}位"
        )

        return {
            'predict': predict_result,
            'echarts': echarts_data,
            'predict_text': predict_text,
            'subject_name': subject_name
        }

    @staticmethod
    def build_echarts_data(predict_result):
        """
        构建ECharts所需的数据格式
        """
        years = predict_result['years'].copy()
        history_ranks = predict_result['history_ranks'].copy()

        # 添加预测年份
        if PREDICT_YEAR not in years:
            years.append(PREDICT_YEAR)
            history_ranks.append(None)

        # 预测线数据（历史部分为None，预测年有值）
        predict_mid_data = [None] * (len(years) - 1) + [predict_result['predict_mid']]
        predict_up_data = [None] * (len(years) - 1) + [predict_result['predict_up']]
        predict_down_data = [None] * (len(years) - 1) + [predict_result['predict_down']]

        # 回归线数据（用于展示趋势线）
        if predict_result['slope'] != 0 and len(years) > 1:
            slope = predict_result['slope']
            intercept = predict_result['intercept']
            trend_line = []
            for year in years:
                trend_line.append(int(slope * year + intercept))
        else:
            trend_line = [None] * len(years)

        # 上下限区间填充数据
        up_band = []
        down_band = []
        if predict_result['slope'] != 0:
            slope = predict_result['slope']
            # 从最后一个历史年份到预测年的区间
            last_hist_year = years[-2] if len(years) >= 2 else years[0]
            for year in years:
                if year < last_hist_year:
                    up_band.append(None)
                    down_band.append(None)
                else:
                    # 简化：只在预测年显示区间
                    if year == PREDICT_YEAR:
                        up_band.append(predict_result['predict_up'])
                        down_band.append(predict_result['predict_down'])
                    else:
                        up_band.append(None)
                        down_band.append(None)
        else:
            up_band = [None] * len(years)
            down_band = [None] * len(years)

        return {
            'xAxis': [str(y) for y in years],
            'series': {
                'history': history_ranks,
                'trend': trend_line,
                'predict_mid': predict_mid_data,
                'predict_up': predict_up_data,
                'predict_down': predict_down_data,
                'up_band': up_band,
                'down_band': down_band
            },
            'min_rank': predict_result['min_rank'],
            'max_rank': predict_result['max_rank']
        }

    @staticmethod
    def get_predict_record(school_id, major_id, subject_type):
        """获取已保存的预测记录"""
        return PredictDAO.get_predict_record(school_id, major_id, subject_type)

    @staticmethod
    def save_predict(school_id, major_id, subject_type, predict_data):
        """
        保存预测记录
        predict_data: dict，包含major_name, score_mide, rank_mide, score_up, rank_up,
                      score_down, rank_down, score_jh, adj_mide, adj_up, adj_down
        """
        return PredictDAO.save_predict_record(school_id, major_id, subject_type, predict_data)

    @staticmethod
    def get_school_predict_list(school_id, subject_type):
        """获取学校所有专业预测列表"""
        return PredictDAO.get_school_predict_list(school_id, subject_type)
