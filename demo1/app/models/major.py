# -*- coding: utf-8 -*-
"""
专业表模型
"""
from app.models import db
from app.config import TABLE_SCHOOL_MAJOR


class SchoolMajor(db.Model):
    __tablename__ = TABLE_SCHOOL_MAJOR

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    school_id = db.Column(db.Integer, nullable=False, index=True, comment='学校ID')
    name = db.Column(db.String(255), nullable=False, comment='专业名称')
    remark = db.Column(db.String(500), nullable=True, comment='专业备注')
    code = db.Column(db.String(50), nullable=True, comment='专业代码')

    def to_dict(self):
        return {
            'id': self.id,
            'school_id': self.school_id,
            'name': self.name,
            'remark': self.remark or '',
            'code': self.code or ''
        }
