-- schema.sql
-- 金山学院 Flask 待办项目 建库建表脚本
--
-- 用法：mysql -u root -p < schema.sql
--
-- 说明：本文件按数据库中的实际结构核对后重写，字段以 app/models/ 下的模型定义为
--       唯一事实来源（模型改了，这里要同步改）。表间删除的级联由 SQLAlchemy 的
--       relationship(cascade="all, delete-orphan") 在 ORM 层完成，库层未加 ON DELETE CASCADE。
--
-- 测试账号由 init_db.py 生成（用户名、密码写在脚本里，密码经 werkzeug 哈希后入库）：
--       python init_db.py

CREATE DATABASE IF NOT EXISTS jinshan
    DEFAULT CHARACTER SET utf8mb4
    COLLATE utf8mb4_general_ci;

USE jinshan;

-- 院系表
CREATE TABLE IF NOT EXISTS department (
    id      INT          NOT NULL AUTO_INCREMENT,
    name    VARCHAR(50)  NOT NULL,
    remark  VARCHAR(200) DEFAULT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 权限表（预留，暂无接口使用）
CREATE TABLE IF NOT EXISTS permission (
    id     INT         NOT NULL AUTO_INCREMENT,
    code   VARCHAR(50) NOT NULL,
    label  VARCHAR(50) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY code (code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 院系-权限 关联表（多对多中间表，两个外键组成复合主键）
CREATE TABLE IF NOT EXISTS department_permission (
    department_id  INT NOT NULL,
    permission_id  INT NOT NULL,
    PRIMARY KEY (department_id, permission_id),
    KEY permission_id (permission_id),
    CONSTRAINT department_permission_ibfk_1 FOREIGN KEY (department_id) REFERENCES department (id),
    CONSTRAINT department_permission_ibfk_2 FOREIGN KEY (permission_id) REFERENCES permission (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='部门-权限多对多中间表';

-- 用户表
-- 注意：password 列存的是 werkzeug 哈希值，不是明文；
--       模型里对应属性叫 _password_hash，且读明文会直接抛异常（只写不可读）。
CREATE TABLE IF NOT EXISTS user (
    id             INT          NOT NULL AUTO_INCREMENT,
    username       VARCHAR(50)  NOT NULL,
    password       VARCHAR(255) NOT NULL,
    nickname       VARCHAR(50)  DEFAULT NULL,
    department_id  INT          DEFAULT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY username (username),
    KEY department_id (department_id),
    CONSTRAINT user_ibfk_1 FOREIGN KEY (department_id) REFERENCES department (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 用户扩展表（一对一，user_id 上的唯一索引是"一对一"的关键）
CREATE TABLE IF NOT EXISTS user_extension (
    id          INT         NOT NULL AUTO_INCREMENT,
    user_id     INT         NOT NULL,
    student_no  VARCHAR(30) DEFAULT NULL,
    phone       VARCHAR(20) DEFAULT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY user_id (user_id),
    CONSTRAINT user_extension_ibfk_1 FOREIGN KEY (user_id) REFERENCES user (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 待办表
CREATE TABLE IF NOT EXISTS todo (
    id          INT          NOT NULL AUTO_INCREMENT,
    title       VARCHAR(100) NOT NULL,
    content     TEXT,
    done        TINYINT(1)   NOT NULL,
    user_id     INT          NOT NULL,
    created_at  DATETIME     NOT NULL,
    PRIMARY KEY (id),
    KEY user_id (user_id),
    CONSTRAINT todo_ibfk_1 FOREIGN KEY (user_id) REFERENCES user (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 初始院系数据
INSERT INTO department (id, name) VALUES (1, '计算机系')
    ON DUPLICATE KEY UPDATE name = name;
INSERT INTO department (id, name) VALUES (2, '软件工程系')
    ON DUPLICATE KEY UPDATE name = name;
