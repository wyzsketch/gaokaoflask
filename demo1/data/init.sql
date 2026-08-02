-- ============================================
-- 高考位次智能预测系统 - 数据库建表脚本
-- ============================================

-- 创建数据库
CREATE DATABASE IF NOT EXISTS gaokao DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE gaokao;

-- ============================================
-- 1. 学校表
-- ============================================
DROP TABLE IF EXISTS t_schools;
CREATE TABLE t_schools (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '学校ID',
    name VARCHAR(255) NOT NULL COMMENT '学校名称',
    code VARCHAR(50) DEFAULT NULL COMMENT '学校代码',
    province VARCHAR(50) DEFAULT NULL COMMENT '省份',
    level VARCHAR(50) DEFAULT NULL COMMENT '办学层次',
    type VARCHAR(50) DEFAULT NULL COMMENT '学校类型',
    INDEX idx_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='学校表';

-- ============================================
-- 2. 专业表
-- ============================================
DROP TABLE IF EXISTS t_school_majors;
CREATE TABLE t_school_majors (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '专业ID',
    school_id INT NOT NULL COMMENT '学校ID',
    name VARCHAR(255) NOT NULL COMMENT '专业名称',
    remark VARCHAR(500) DEFAULT NULL COMMENT '专业备注',
    code VARCHAR(50) DEFAULT NULL COMMENT '专业代码',
    INDEX idx_school_id (school_id),
    INDEX idx_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='专业表';

-- ============================================
-- 3. 文科合并分数历史表
-- ============================================
DROP TABLE IF EXISTS t_entry_union_score_history_arts;
CREATE TABLE t_entry_union_score_history_arts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    school_id INT NOT NULL COMMENT '学校ID',
    major_id INT NOT NULL COMMENT '专业ID',
    major_name VARCHAR(255) DEFAULT NULL COMMENT '专业名称',
    invisible TINYINT DEFAULT 0 COMMENT '是否隐藏',
    -- 历年分数和位次（根据实际年份添加列）
    `2020_score` INT DEFAULT NULL,
    `2020_section` INT DEFAULT NULL,
    `2021_score` INT DEFAULT NULL,
    `2021_section` INT DEFAULT NULL,
    `2022_score` INT DEFAULT NULL,
    `2022_section` INT DEFAULT NULL,
    `2023_score` INT DEFAULT NULL,
    `2023_section` INT DEFAULT NULL,
    `2024_score` INT DEFAULT NULL,
    `2024_section` INT DEFAULT NULL,
    `2025_score` INT DEFAULT NULL,
    `2025_section` INT DEFAULT NULL,
    INDEX idx_school_major (school_id, major_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='文科合并分数历史表';

-- ============================================
-- 4. 理科合并分数历史表
-- ============================================
DROP TABLE IF EXISTS t_entry_union_score_history_sciences;
CREATE TABLE t_entry_union_score_history_sciences (
    id INT PRIMARY KEY AUTO_INCREMENT,
    school_id INT NOT NULL COMMENT '学校ID',
    major_id INT NOT NULL COMMENT '专业ID',
    major_name VARCHAR(255) DEFAULT NULL COMMENT '专业名称',
    invisible TINYINT DEFAULT 0 COMMENT '是否隐藏',
    -- 历年分数和位次（根据实际年份添加列）
    `2020_score` INT DEFAULT NULL,
    `2020_section` INT DEFAULT NULL,
    `2021_score` INT DEFAULT NULL,
    `2021_section` INT DEFAULT NULL,
    `2022_score` INT DEFAULT NULL,
    `2022_section` INT DEFAULT NULL,
    `2023_score` INT DEFAULT NULL,
    `2023_section` INT DEFAULT NULL,
    `2024_score` INT DEFAULT NULL,
    `2024_section` INT DEFAULT NULL,
    `2025_score` INT DEFAULT NULL,
    `2025_section` INT DEFAULT NULL,
    INDEX idx_school_major (school_id, major_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='理科合并分数历史表';

-- ============================================
-- 5. 文科原始分数历史表
-- ============================================
DROP TABLE IF EXISTS t_entry_score_history_arts;
CREATE TABLE t_entry_score_history_arts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    school_id INT NOT NULL COMMENT '学校ID',
    major_id INT NOT NULL COMMENT '专业ID',
    major_name VARCHAR(255) DEFAULT NULL COMMENT '专业名称',
    deleted TINYINT DEFAULT 0 COMMENT '是否删除',
    `2020_score` INT DEFAULT NULL,
    `2020_section` INT DEFAULT NULL,
    `2021_score` INT DEFAULT NULL,
    `2021_section` INT DEFAULT NULL,
    `2022_score` INT DEFAULT NULL,
    `2022_section` INT DEFAULT NULL,
    `2023_score` INT DEFAULT NULL,
    `2023_section` INT DEFAULT NULL,
    `2024_score` INT DEFAULT NULL,
    `2024_section` INT DEFAULT NULL,
    `2025_score` INT DEFAULT NULL,
    `2025_section` INT DEFAULT NULL,
    INDEX idx_school_id (school_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='文科原始分数历史表';

-- ============================================
-- 6. 理科原始分数历史表
-- ============================================
DROP TABLE IF EXISTS t_entry_score_history_sciences;
CREATE TABLE t_entry_score_history_sciences (
    id INT PRIMARY KEY AUTO_INCREMENT,
    school_id INT NOT NULL COMMENT '学校ID',
    major_id INT NOT NULL COMMENT '专业ID',
    major_name VARCHAR(255) DEFAULT NULL COMMENT '专业名称',
    deleted TINYINT DEFAULT 0 COMMENT '是否删除',
    `2020_score` INT DEFAULT NULL,
    `2020_section` INT DEFAULT NULL,
    `2021_score` INT DEFAULT NULL,
    `2021_section` INT DEFAULT NULL,
    `2022_score` INT DEFAULT NULL,
    `2022_section` INT DEFAULT NULL,
    `2023_score` INT DEFAULT NULL,
    `2023_section` INT DEFAULT NULL,
    `2024_score` INT DEFAULT NULL,
    `2024_section` INT DEFAULT NULL,
    `2025_score` INT DEFAULT NULL,
    `2025_section` INT DEFAULT NULL,
    INDEX idx_school_id (school_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='理科原始分数历史表';

-- ============================================
-- 7. 文科预测表（2026）
-- ============================================
DROP TABLE IF EXISTS t_entry_predict_arts_2026;
CREATE TABLE t_entry_predict_arts_2026 (
    id INT PRIMARY KEY AUTO_INCREMENT,
    school_id INT NOT NULL COMMENT '学校ID',
    major_id INT NOT NULL COMMENT '专业ID',
    major_name VARCHAR(255) DEFAULT NULL COMMENT '专业名称',
    score_mide INT DEFAULT 0 COMMENT '中位分数',
    rank_mide INT DEFAULT 0 COMMENT '中位位次',
    score_up INT DEFAULT 0 COMMENT '上限分数',
    rank_up INT DEFAULT 0 COMMENT '上限位次',
    score_down INT DEFAULT 0 COMMENT '下限分数',
    rank_down INT DEFAULT 0 COMMENT '下限位次',
    score_jh INT DEFAULT 0 COMMENT '第三方预测分数',
    adj_mide INT DEFAULT 0 COMMENT '中位修正',
    adj_up INT DEFAULT 0 COMMENT '上限修正',
    adj_down INT DEFAULT 0 COMMENT '下限修正',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_school_major (school_id, major_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='文科预测表2026';

-- ============================================
-- 8. 理科预测表（2026）
-- ============================================
DROP TABLE IF EXISTS t_entry_predict_sciences_2026;
CREATE TABLE t_entry_predict_sciences_2026 (
    id INT PRIMARY KEY AUTO_INCREMENT,
    school_id INT NOT NULL COMMENT '学校ID',
    major_id INT NOT NULL COMMENT '专业ID',
    major_name VARCHAR(255) DEFAULT NULL COMMENT '专业名称',
    score_mide INT DEFAULT 0 COMMENT '中位分数',
    rank_mide INT DEFAULT 0 COMMENT '中位位次',
    score_up INT DEFAULT 0 COMMENT '上限分数',
    rank_up INT DEFAULT 0 COMMENT '上限位次',
    score_down INT DEFAULT 0 COMMENT '下限分数',
    rank_down INT DEFAULT 0 COMMENT '下限位次',
    score_jh INT DEFAULT 0 COMMENT '第三方预测分数',
    adj_mide INT DEFAULT 0 COMMENT '中位修正',
    adj_up INT DEFAULT 0 COMMENT '上限修正',
    adj_down INT DEFAULT 0 COMMENT '下限修正',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_school_major (school_id, major_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='理科预测表2026';

-- ============================================
-- 示例数据（用于测试）
-- ============================================

-- 插入示例学校
INSERT INTO t_schools (id, name, code, province) VALUES
(532, '四川大学', '10610', '四川'),
(561, '电子科技大学', '10614', '四川'),
(80, '西南交通大学', '10613', '四川');

-- 插入示例专业
INSERT INTO t_school_majors (id, school_id, name, remark, code) VALUES
(1, 532, '计算机科学与技术', '（国家基地班）', '080901'),
(2, 532, '软件工程', '', '080902'),
(3, 532, '临床医学', '（八年制）', '100201'),
(4, 561, '计算机科学与技术', '', '080901'),
(5, 561, '软件工程', '', '080902');

-- 插入示例理科分数数据（四川大学计算机）
INSERT INTO t_entry_union_score_history_sciences (school_id, major_id, major_name, invisible,
    `2020_score`, `2020_section`,
    `2021_score`, `2021_section`,
    `2022_score`, `2022_section`,
    `2023_score`, `2023_section`,
    `2024_score`, `2024_section`,
    `2025_score`, `2025_section`)
VALUES (532, 1, '计算机科学与技术（国家基地班）', 0,
    658, 28627,
    652, 26723,
    648, 25876,
    655, 31207,
    650, 30322,
    648, 30322);

-- 插入示例理科分数数据（四川大学软件工程）
INSERT INTO t_entry_union_score_history_sciences (school_id, major_id, major_name, invisible,
    `2020_score`, `2020_section`,
    `2021_score`, `2021_section`,
    `2022_score`, `2022_section`,
    `2023_score`, `2023_section`,
    `2024_score`, `2024_section`,
    `2025_score`, `2025_section`)
VALUES (532, 2, '软件工程', 0,
    645, 35000,
    640, 32000,
    638, 31000,
    642, 36000,
    638, 35500,
    635, 35000);

-- 插入示例理科分数数据（电子科大计算机）
INSERT INTO t_entry_union_score_history_sciences (school_id, major_id, major_name, invisible,
    `2020_score`, `2020_section`,
    `2021_score`, `2021_section`,
    `2022_score`, `2022_section`,
    `2023_score`, `2023_section`,
    `2024_score`, `2024_section`,
    `2025_score`, `2025_section`)
VALUES (561, 4, '计算机科学与技术', 0,
    665, 18000,
    660, 16500,
    658, 15000,
    662, 19000,
    658, 18500,
    655, 18000);

SELECT '数据库初始化完成！' AS result;
