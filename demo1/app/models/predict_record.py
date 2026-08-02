# -*- coding: utf-8 -*-
"""
预测记录模型
"""
from app.models import db
from app.config import TABLE_PREDICT_ARTS, TABLE_PREDICT_SCIENCES


class PredictArts(db.Model):
    """文科预测表"""
    __tablename__ = TABLE_PREDICT_ARTS

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    school_id = db.Column(db.Integer, nullable=False, index=True)
    major_id = db.Column(db.Integer, nullable=False, index=True)
    major_name = db.Column(db.String(255), nullable=True)
    score_mide = db.Column(db.Integer, default=0)
    rank_mide = db.Column(db.Integer, default=0)
    score_up = db.Column(db.Integer, default=0)
    rank_up = db.Column(db.Integer, default=0)
    score_down = db.Column(db.Integer, default=0)
    rank_down = db.Column(db.Integer, default=0)
    score_jh = db.Column(db.Integer, default=0)
    adj_mide = db.Column(db.Integer, default=0)
    adj_up = db.Column(db.Integer, default=0)
    adj_down = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'school_id': self.school_id,
            'major_id': self.major_id,
            'major_name': self.major_name or '',
            'score_mide': self.score_mide or 0,
            'rank_mide': self.rank_mide or 0,
            'score_up': self.score_up or 0,
            'rank_up': self.rank_up or 0,
            'score_down': self.score_down or 0,
            'rank_down': self.rank_down or 0,
            'score_jh': self.score_jh or 0,
            'adj_mide': self.adj_mide or 0,
            'adj_up': self.adj_up or 0,
            'adj_down': self.adj_down or 0
        }


class PredictSciences(db.Model):
    """理科预测表"""
    __tablename__ = TABLE_PREDICT_SCIENCES

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    school_id = db.Column(db.Integer, nullable=False, index=True)
    major_id = db.Column(db.Integer, nullable=False, index=True)
    major_name = db.Column(db.String(255), nullable=True)
    score_mide = db.Column(db.Integer, default=0)
    rank_mide = db.Column(db.Integer, default=0)
    score_up = db.Column(db.Integer, default=0)
    rank_up = db.Column(db.Integer, default=0)
    score_down = db.Column(db.Integer, default=0)
    rank_down = db.Column(db.Integer, default=0)
    score_jh = db.Column(db.Integer, default=0)
    adj_mide = db.Column(db.Integer, default=0)
    adj_up = db.Column(db.Integer, default=0)
    adj_down = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'school_id': self.school_id,
            'major_id': self.major_id,
            'major_name': self.major_name or '',
            'score_mide': self.score_mide or 0,
            'rank_mide': self.rank_mide or 0,
            'score_up': self.score_up or 0,
            'rank_up': self.rank_up or 0,
            'score_down': self.score_down or 0,
            'rank_down': self.rank_down or 0,
            'score_jh': self.score_jh or 0,
            'adj_mide': self.adj_mide or 0,
            'adj_up': self.adj_up or 0,
            'adj_down': self.adj_down or 0
        }
