# -*- coding: utf-8 -*-
"""
高考位次智能预测系统 - 启动入口
"""
from app import create_app
from app.config import HOST, PORT, DEBUG

app = create_app()

if __name__ == '__main__':
    print("=" * 50)
    print("  高考位次智能预测系统 - Flask Web版")
    print("=" * 50)
    print(f"  访问地址: http://{HOST}:{PORT}")
    print(f"  预测页面: http://{HOST}:{PORT}/predict")
    print("=" * 50)
    app.run(host=HOST, port=PORT, debug=False)
