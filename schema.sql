-- schema.sql
-- 金山学院 Flask 待办项目 建库建表脚本
-- 用法：mysql -u root -p < schema.sql

CREATE DATABASE IF NOT EXISTS jinshan
    DEFAULT CHARACTER SET utf8mb4
    COLLATE utf8mb4_general_ci;

USE jinshan;

-- 院系表
CREATE TABLE IF NOT EXISTS department (
    id          INT PRIMARY KEY AUTO_INCREMENT,
    name        VARCHAR(100) NOT NULL,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 用户表
CREATE TABLE IF NOT EXISTS user (
    id              INT PRIMARY KEY AUTO_INCREMENT,
    username        VARCHAR(80)  NOT NULL UNIQUE,
    _password_hash  VARCHAR(255) NOT NULL,
    nickname        VARCHAR(100),
    student_no      VARCHAR(50),
    dept_id         INT,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_user_dept FOREIGN KEY (dept_id) REFERENCES department(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 待办表
CREATE TABLE IF NOT EXISTS todo (
    id          INT PRIMARY KEY AUTO_INCREMENT,
    title       VARCHAR(200) NOT NULL,
    done        TINYINT(1)   DEFAULT 0 NOT NULL,
    user_id     INT          NOT NULL,
    created_at  DATETIME     DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_todo_user FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
    INDEX idx_user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 权限表（预留）
CREATE TABLE IF NOT EXISTS permission (
    id          INT PRIMARY KEY AUTO_INCREMENT,
    name        VARCHAR(100) NOT NULL,
    code        VARCHAR(50)  NOT NULL UNIQUE,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 用户扩展表（预留）
CREATE TABLE IF NOT EXISTS user_extension (
    id          INT PRIMARY KEY AUTO_INCREMENT,
    user_id     INT NOT NULL UNIQUE,
    phone       VARCHAR(20),
    avatar_url  VARCHAR(255),
    CONSTRAINT fk_ext_user FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 初始化数据
INSERT INTO department (id, name) VALUES (1, '计算机系') ON DUPLICATE KEY UPDATE name=name;
INSERT INTO department (id, name) VALUES (2, '软件工程系') ON DUPLICATE KEY UPDATE name=name;

-- 密码为 123456 的管理员（_password_hash 需由程序生成，此处留空由 init_db.py 补）
-- 见 init_db.py