# -*- coding: utf-8 -*-
"""
全局配置文件
"""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ========== 数据库配置 ==========
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = int(os.environ.get('DB_PORT', 3306))
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'root')
DB_NAME = os.environ.get('DB_NAME', 'gaokao')

SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False

# ========== 表名配置 ==========
TABLE_SCHOOLS = "t_schools"
TABLE_SCHOOL_MAJOR = "t_school_majors"
TABLE_MAJOR_SCORE_ARTS = "t_entry_score_history_arts"
TABLE_MAJOR_SCORE_SCIENCES = "t_entry_score_history_sciences"
TABLE_UNION_MAJOR_SCORE_ARTS = "t_entry_union_score_history_arts"
TABLE_UNION_MAJOR_SCORE_SCIENCES = "t_entry_union_score_history_sciences"
TABLE_PREDICT_ARTS = "t_entry_predict_arts_2026"
TABLE_PREDICT_SCIENCES = "t_entry_predict_sciences_2026"

# ========== 常量配置 ==========
TYPE_ARTS = 0      # 文科
TYPE_SCIENCES = 1  # 理科

RAW_DATA_FOLDER = os.path.join(BASE_DIR, "raw3")
SCORE_EXCEL_FILE = os.path.join(BASE_DIR, "data", "一分一段表.xlsx")
CSV_SCHOOL_FILE = os.path.join(BASE_DIR, "data", "学校名称.csv")
CSV_EXPORT_FOLDER = os.path.join(BASE_DIR, "data", "export")
CSV_IMPORT_FOLDER = os.path.join(BASE_DIR, "data", "import")

DEFAULT_PROVINCE = ""
DEFAULT_YEAR = 2025
PREDICT_YEAR = 2026

DEFAULT_SCHOOLS = [532]

# ========== Flask配置 ==========
SECRET_KEY = os.environ.get('SECRET_KEY', 'gaokao-predict-secret-key-2026')
DEBUG = True
HOST = '0.0.0.0'
PORT = 5000
