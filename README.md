# 金山学院待办事项系统

基于 Flask + SQLAlchemy 2.0 + JWT 的待办事项 RESTful API，用于课程设计与实习项目展示。

## 技术栈

- Python 3.10
- Flask 3.1.2
- Flask-SQLAlchemy 3.1
- Flask-JWT-Extended 4.6
- SQLAlchemy 2.0
- PyMySQL
- MySQL 8
- python-dotenv

## 项目结构

jinshan-todo/
  wsgi.py
  config.py
  requirements.txt
  schema.sql
  init_db.py
  .env.example
  .gitignore
  README.md
  extensions/
    db.py
  app/
    __init__.py
    models/
      __init__.py
      user.py
      department.py
      permission.py
      user_extension.py
      todo.py
    routes/
      auth.py
      todo.py
    utils/
      response.py
      logger.py

## 快速开始

### 1. 克隆项目

git clone your-repo-url
cd jinshan-todo

### 2. 创建虚拟环境并安装依赖

conda create -n flask-env python=3.10
conda activate flask-env
pip install -r requirements.txt

### 3. 配置环境变量

复制 .env.example 为 .env，填写你的 MySQL 配置：

FLASK_ENV=dev
DB_USER=root
DB_PASSWORD=你的MySQL密码
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=jinshan
JWT_SECRET_KEY=你自己设一个随机字符串
JWT_ACCESS_TOKEN_EXPIRES=43200

### 4. 建库建表

mysql -u root -p < schema.sql
python init_db.py

默认测试账号：

zhangsan / 123456 - 计算机系学生
lisi / 123456 - 计算机系学生

### 5. 启动服务

python wsgi.py

服务运行于 http://127.0.0.1:5000

## 接口文档

所有写接口需在 Header 中携带 Authorization: Bearer token

统一响应格式：
{"code": 0, "msg": "ok", "data": {}}

POST   /api/auth/login        登录             请求体: {"username","password"}       返回: {"token","nickname"}
GET    /api/auth/me           当前用户信息      返回: {nickname,department,student_no}
POST   /api/todo              新建待办          请求体: {"title"}                   返回: {"id","title"}
GET    /api/todo              待办列表          返回: {total, items}
GET    /api/todo/<id>         待办详情          返回: {id,title,done,owner}
PATCH  /api/todo/<id>         修改待办          请求体: {"title?","done?"}          返回: {id,title,done}
DELETE /api/todo/<id>         删除待办          返回: null

业务错误码：

0    - 成功
4104 - 无权操作（越权）
4404 - 资源不存在
4201 - 参数非法
4401 - 未登录或 token 失效
4500 - 服务器内部错误

## 核心设计决策

1. 工厂函数 + 配置分离：create_app(profile) 根据环境名加载对应配置类
2. 数据库单例抽离：db 对象定义在 extensions/db.py 中，避免循环导入
3. 蓝图按域拆分：bp_auth 和 bp_todo 各自独立，路由模块化
4. JWT 鉴权：token 仅存储 user_id，JWT_SECRET_KEY 签名防篡改，有效期 12 小时
5. 越权拦截：业务层校验 todo.user_id == current_user_id，越权返回 4104
6. 统一响应与错误处理：所有接口返回 {code, msg, data}，全局错误处理器统一转 JSON

## 测试示例

curl -X POST http://127.0.0.1:5000/api/auth/login -H "Content-Type: application/json" -d "{\"username\":\"zhangsan\",\"password\":\"123456\"}"

curl http://127.0.0.1:5000/api/todo -H "Authorization: Bearer token"

## 许可证

MIT
