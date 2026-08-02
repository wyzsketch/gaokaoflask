# -*- coding: utf-8 -*-
"""
分数历史模型
注意：由于分数表列是动态的（每年新增score和section列），
这里只定义基础字段，动态列查询使用原生SQL在DAO层处理
"""
from app.models import db
from app.config import (
    TABLE_UNION_MAJOR_SCORE_ARTS,
    TABLE_UNION_MAJOR_SCORE_SCIENCES,
    TABLE_MAJOR_SCORE_ARTS,
    TABLE_MAJOR_SCORE_SCIENCES
)


class UnionScoreHistoryArts(db.Model):
    """文科合并分数历史表"""
    __tablename__ = TABLE_UNION_MAJOR_SCORE_ARTS

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    school_id = db.Column(db.Integer, nullable=False, index=True)
    major_id = db.Column(db.Integer, nullable=False, index=True)
    major_name = db.Column(db.String(255), nullable=True)
    invisible = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            'id': self.id,
            'school_id': self.school_id,
            'major_id': self.major_id,
            'major_name': self.major_name or '',
            'invisible': self.invisible or 0
        }


class UnionScoreHistorySciences(db.Model):
    """理科合并分数历史表"""
    __tablename__ = TABLE_UNION_MAJOR_SCORE_SCIENCES

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    school_id = db.Column(db.Integer, nullable=False, index=True)
    major_id = db.Column(db.Integer, nullable=False, index=True)
    major_name = db.Column(db.String(255), nullable=True)
    invisible = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            'id': self.id,
            'school_id': self.school_id,
            'major_id': self.major_id,
            'major_name': self.major_name or '',
            'invisible': self.invisible or 0
        }


class ScoreHistoryArts(db.Model):
    """文科原始分数历史表"""
    __tablename__ = TABLE_MAJOR_SCORE_ARTS

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    school_id = db.Column(db.Integer, nullable=False, index=True)
    major_id = db.Column(db.Integer, nullable=False, index=True)
    major_name = db.Column(db.String(255), nullable=True)
    deleted = db.Column(db.Integer, default=0)


class ScoreHistorySciences(db.Model):
    """理科原始分数历史表"""
    __tablename__ = TABLE_MAJOR_SCORE_SCIENCES

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    school_id = db.Column(db.Integer, nullable=False, index=True)
    major_id = db.Column(db.Integer, nullable=False, index=True)
    major_name = db.Column(db.String(255), nullable=True)
    deleted = db.Column(db.Integer, default=0)
