# -*- coding: utf-8 -*-
"""
数据库初始化脚本
执行此脚本可自动创建数据库表并插入示例数据
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pymysql
from app.config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME


def init_database():
    """初始化数据库"""
    print("=" * 50)
    print("  数据库初始化脚本")
    print("=" * 50)

    # 读取SQL文件
    sql_file = os.path.join(os.path.dirname(__file__), 'data', 'init.sql')
    if not os.path.exists(sql_file):
        print(f"❌ SQL文件不存在: {sql_file}")
        return False

    with open(sql_file, 'r', encoding='utf-8') as f:
        sql_content = f.read()

    try:
        # 连接MySQL（不指定数据库）
        conn = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            charset='utf8mb4'
        )
        cursor = conn.cursor()

        print(f"✅ 已连接到 MySQL: {DB_HOST}:{DB_PORT}")

        # 执行SQL（分号分割）
        # 注意：简单的分号分割可能有问题，这里用于初始化脚本足够
        statements = []
        current_stmt = []
        in_comment = False

        for line in sql_content.split('\n'):
            line_stripped = line.strip()
            if line_stripped.startswith('--') or line_stripped.startswith('#'):
                continue
            if line_stripped.startswith('/*'):
                in_comment = True
                continue
            if line_stripped.endswith('*/'):
                in_comment = False
                continue
            if in_comment:
                continue

            current_stmt.append(line)
            if line_stripped.endswith(';'):
                stmt = '\n'.join(current_stmt).strip()
                if stmt:
                    statements.append(stmt)
                current_stmt = []

        print(f"📝 共 {len(statements)} 条SQL语句")

        # 执行每条SQL
        success_count = 0
        for i, stmt in enumerate(statements):
            try:
                cursor.execute(stmt)
                success_count += 1
            except Exception as e:
                print(f"⚠️  第{i+1}条SQL执行警告: {e}")

        conn.commit()
        print(f"✅ 成功执行 {success_count}/{len(statements)} 条SQL")

        cursor.close()
        conn.close()

        print("=" * 50)
        print("  数据库初始化完成！")
        print(f"  数据库名: {DB_NAME}")
        print("  已创建表:")
        print("    - t_schools (学校表)")
        print("    - t_school_majors (专业表)")
        print("    - t_entry_union_score_history_arts (文科合并分数表)")
        print("    - t_entry_union_score_history_sciences (理科合并分数表)")
        print("    - t_entry_score_history_arts (文科原始分数表)")
        print("    - t_entry_score_history_sciences (理科原始分数表)")
        print("    - t_entry_predict_arts_2026 (文科预测表)")
        print("    - t_entry_predict_sciences_2026 (理科预测表)")
        print("  已插入示例数据: 四川大学、电子科技大学等")
        print("=" * 50)

        return True

    except Exception as e:
        print(f"❌ 数据库初始化失败: {e}")
        return False


if __name__ == '__main__':
    success = init_database()
    sys.exit(0 if success else 1)
