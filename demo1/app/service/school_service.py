# -*- coding: utf-8 -*-
"""
学校业务服务层
"""
from app.dao.school_dao import SchoolDAO


class SchoolService:
    @staticmethod
    def search_schools(keyword, limit=50):
        """搜索学校"""
        if not keyword or len(keyword.strip()) < 1:
            return SchoolDAO.get_all_schools()[:limit]
        return SchoolDAO.search_schools_by_name(keyword.strip(), limit)

    @staticmethod
    def get_school_detail(school_id):
        """获取学校详情"""
        return SchoolDAO.get_school_by_id(school_id)

    @staticmethod
    def get_all_schools():
        """获取所有学校"""
        return SchoolDAO.get_all_schools()
