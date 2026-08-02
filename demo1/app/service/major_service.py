# -*- coding: utf-8 -*-
"""
专业业务服务层
"""
from app.dao.major_dao import MajorDAO
from app.config import TYPE_SCIENCES


class MajorService:
    @staticmethod
    def search_majors(school_id, subject_type, keyword, limit=100):
        """搜索专业"""
        if not school_id:
            return []
        keyword = keyword.strip() if keyword else ''
        return MajorDAO.search_majors(school_id, subject_type, keyword, limit)

    @staticmethod
    def get_major_detail(major_id):
        """获取专业详情"""
        return MajorDAO.get_major_by_id(major_id)
