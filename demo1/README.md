# 高考位次智能预测系统 - Flask Web版

基于 Flask + ECharts + scikit-learn 的高考院校专业录取位次智能预测系统。

## 项目特点

- **分层架构**：Model → DAO → Service → Controller → Template 五层架构
- **智能预测**：基于线性回归算法，结合手动修正参数
- **可视化**：ECharts动态图表展示历年位次趋势与预测区间
- **数据存档**：预测结果可保存到数据库，方便后续查看对比

## 项目结构

```
gaokao_predict_web/
├── app/                        # Flask核心应用
│   ├── __init__.py             # 应用工厂
│   ├── config.py               # 全局配置
│   ├── models/                 # Model层 - 数据库模型
│   │   ├── __init__.py
│   │   ├── school.py
│   │   ├── major.py
│   │   ├── score_history.py
│   │   └── predict_record.py
│   ├── dao/                    # DAO层 - 数据访问
│   │   ├── __init__.py
│   │   ├── school_dao.py
│   │   ├── major_dao.py
│   │   ├── score_dao.py
│   │   └── predict_dao.py
│   ├── service/                # Service层 - 业务逻辑
│   │   ├── __init__.py
│   │   ├── school_service.py
│   │   ├── major_service.py
│   │   └── predict_service.py  # 核心预测算法
│   ├── api/                    # Controller层 - API接口
│   │   ├── __init__.py         # 蓝图注册
│   │   ├── page_bp_routes.py   # 页面路由
│   │   ├── school_bp_routes.py # 学校API
│   │   ├── major_bp_routes.py  # 专业API
│   │   ├── chart_bp_routes.py  # 图表API
│   │   └── predict_bp_routes.py# 预测记录API
│   └── utils/                  # 工具层
│       ├── __init__.py
│       └── global_utils.py
├── templates/                  # 前端模板
│   ├── base.html
│   ├── index.html
│   └── predict.html
├── static/                     # 静态资源
│   ├── css/style.css
│   └── js/
│       ├── app.js              # 页面交互
│       └── chart.js            # ECharts图表
├── data/                       # 数据目录
│   └── 一分一段表.xlsx         # 一分一段表（需自行放入）
├── raw3/                       # 原始数据目录
├── run.py                      # 启动入口
└── requirements.txt            # 依赖清单
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置数据库

编辑 `app/config.py`，修改数据库连接信息：

```python
DB_HOST = 'localhost'
DB_PORT = 3306
DB_USER = 'root'
DB_PASSWORD = 'root'
DB_NAME = 'gaokao'
```

### 3. 准备数据

确保MySQL数据库中存在以下表（与原桌面版共用同一数据库）：
- `t_schools` - 学校表
- `t_school_majors` - 专业表
- `t_entry_union_score_history_arts` - 文科合并分数表
- `t_entry_union_score_history_sciences` - 理科合并分数表
- `t_entry_predict_arts_2026` - 文科预测表
- `t_entry_predict_sciences_2026` - 理科预测表

将 `一分一段表.xlsx` 放入 `data/` 目录。

### 4. 启动服务

```bash
python run.py
```

### 5. 访问系统

- 首页：http://localhost:5000
- 预测页面：http://localhost:5000/predict

## API接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/school/search` | GET | 搜索学校 |
| `/api/major/search` | GET | 搜索专业 |
| `/api/chart/get_data` | POST | 获取图表数据+预测结果 |
| `/api/predict/record` | GET | 获取预测记录 |
| `/api/predict/save` | POST | 保存预测记录 |

## 核心算法

1. **数据过滤**：过滤偏离平均值100%以上的异常值
2. **线性回归**：使用 scikit-learn LinearRegression 拟合年份-位次关系
3. **偏差计算**：计算历史数据与回归线的最大偏差，乘以1.1作为置信区间半径
4. **手动修正**：叠加用户输入的上/中/下修正参数
5. **分数换算**：通过一分一段表将位次换算为对应分数

## 技术栈

- **后端**：Python 3.9+ / Flask / SQLAlchemy / pandas / scikit-learn
- **前端**：Bootstrap 5 / ECharts 5 / jQuery
- **数据库**：MySQL
