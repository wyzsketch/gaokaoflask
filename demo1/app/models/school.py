# -*- coding: utf-8 -*-
"""
学校表模型
"""
from app.models import db
from app.config import TABLE_SCHOOLS


class School(db.Model):
    __tablename__ = TABLE_SCHOOLS

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, comment='学校名称')
    code = db.Column(db.String(50), nullable=True, comment='学校代码')
    province = db.Column(db.String(50), nullable=True, comment='省份')
    level = db.Column(db.String(50), nullable=True, comment='办学层次')
    type = db.Column(db.String(50), nullable=True, comment='学校类型')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code or '',
            'province': self.province or '',
            'level': self.level or '',
            'type': self.type or ''
        }
