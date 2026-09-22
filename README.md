# 金山学院待办事项系统

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1-000000?logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8-4479A1?logo=mysql&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg)

基于 Flask + SQLAlchemy 2.0 + JWT 的待办事项系统，提供 RESTful API 和一个开箱即用的前端单页，用于课程设计与实习项目展示。

> 开源地址：https://github.com/bilicat2333/jinshan-todo

## 功能特性

- 用户注册 / 登录（JWT 鉴权，token 有效期 12 小时）
- 待办的增删改查，勾选完成 / 取消完成
- 用户 - 院系关联，接口返回当前用户院系信息
- 内置原生 JS 前端单页（零构建、零依赖），浏览器打开即可使用
- 水平越权拦截：所有待办操作校验资源归属，越权返回 4104
- 统一响应格式与业务错误码，全局异常处理；JWT 鉴权失败也统一收敛为 `code=4401`
- 密码哈希存储（werkzeug pbkdf2），密码字段"只写不可读"

## 技术栈

- Python 3.10 / Flask 3.1.2
- Flask-SQLAlchemy 3.1（SQLAlchemy 2.0 类型化 ORM）
- Flask-JWT-Extended 4.6
- PyMySQL / MySQL 8
- python-dotenv
- 前端：原生 HTML / CSS / JavaScript（fetch）

## 项目结构

```
jinshan-todo/
  wsgi.py              # 启动入口
  config.py            # dev / prod 配置类（读 .env）
  requirements.txt
  schema.sql           # 建库建表脚本（与模型定义保持一致）
  init_db.py           # 初始化测试数据
  .env.example
  static/
    index.html         # 前端单页（登录 / 注册 / 待办管理）
  extensions/
    db.py              # db 单例，避免循环导入
    jwt.py             # JWTManager 初始化 + 鉴权失败统一响应回调
  app/
    __init__.py        # 应用工厂 create_app + 全局错误处理 + 根路由托管前端
    models/
      user.py          # 用户（密码哈希只写保护）
      department.py    # 院系
      permission.py    # 权限（预留）
      user_extension.py# 用户扩展（预留）
      todo.py          # 待办
    routes/
      auth.py          # 注册 / 登录 / 当前用户
      todo.py          # 待办 CRUD + 越权校验
    utils/
      response.py      # 统一响应 ok / fail
      logger.py        # 滚动日志
```

## 快速开始

### 1. 克隆项目

```
git clone https://github.com/bilicat2333/jinshan-todo.git
cd jinshan-todo
```

### 2. 创建虚拟环境并安装依赖

```
conda create -n flask-env python=3.10
conda activate flask-env
pip install -r requirements.txt
```

### 3. 配置环境变量

复制 `.env.example` 为 `.env`，填写你的 MySQL 配置：

```
FLASK_ENV=dev
DB_USER=root
DB_PASSWORD=你的MySQL密码
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=jinshan
JWT_SECRET_KEY=你自己设一个随机字符串
JWT_ACCESS_TOKEN_EXPIRES=43200
```

### 4. 建库建表

```
mysql -u root -p < schema.sql
python init_db.py
```

默认测试账号：

- zhangsan / 123456 —— 计算机系学生
- lisi / 123456 —— 计算机系学生

### 5. 启动服务

```
python wsgi.py
```

服务运行于 http://127.0.0.1:5000

- **前端页面**：浏览器直接打开 http://127.0.0.1:5000/ ，注册或用测试账号登录即可管理待办
- **纯接口调试**：用 curl / Postman 调 `/api` 下的接口

## 接口文档

写接口需在 Header 中携带 `Authorization: Bearer <token>`。

统一响应格式：`{"code": 0, "msg": "ok", "data": {}}`（失败时 `data` 为 `null`）

| 方法 | 路径 | 说明 | 请求体 | 返回 |
| --- | --- | --- | --- | --- |
| POST | /api/auth/register | 注册（成功直接返回 token） | `{"username","password","nickname?"}` | `{"token","user"}` |
| POST | /api/auth/login | 登录 | `{"username","password"}` | `{"token","user"}` |
| GET | /api/auth/me | 当前用户信息 | - | `{nickname,department,...}` |
| POST | /api/todo | 新建待办 | `{"title","content?"}` | `{id,title,content,done,created_at}` |
| GET | /api/todo | 待办列表 | - | `{total, items}` |
| GET | /api/todo/\<id\> | 待办详情 | - | `{id,title,done,owner,dept}` |
| PATCH | /api/todo/\<id\> | 修改待办（标题/内容/完成状态） | `{"title?","content?","done?"}` | `{id,title,done}` |
| DELETE | /api/todo/\<id\> | 删除待办 | - | `null` |

业务错误码：

| 错误码 | 含义 | HTTP |
| --- | --- | --- |
| 0 | 成功 | 200 / 201 |
| 4001 | 参数缺失（账号密码为空） | 400 |
| 4002 | 账号或密码错误 | 401 |
| 4004 | 用户不存在 | 404 |
| 4005 | 用户名已被占用 | 409 |
| 4104 | 无权操作（越权） | 403 |
| 4201 | 参数非法 | 400 |
| 4401 | 未登录 / token 过期 / token 无效 | 401 |
| 4404 | 资源不存在 | 404 |
| 4405 | 请求方法不允许 | 405 |
| 4500 | 服务器内部错误 | 500 |

## 核心设计决策

1. **应用工厂 + 配置分离**：`create_app(profile)` 根据环境名加载对应配置类，生产环境强制校验 `JWT_SECRET_KEY`，杜绝密钥硬编码
2. **数据库单例抽离**：db 对象定义在 `extensions/db.py` 中，依赖单向流动，避免循环导入
3. **蓝图按域拆分**：`bp_auth` 和 `bp_todo` 各自独立，路由模块化
4. **JWT 鉴权**：token 仅存 `str(user.id)`，签名防篡改，有效期 12 小时
5. **越权拦截**：业务层校验 `todo.user_id == current_user_id`，越权返回 4104，资源归属在数据访问层一起过滤
6. **密码安全**：werkzeug 哈希 + Python property 实现密码字段只写不可读
7. **防 N+1 查询**：关联查询使用 `joinedload`（详情）与 `lazy="selectin"`（列表）预加载
8. **统一响应与错误处理**：所有接口返回 `{code, msg, data}`；全局错误处理器覆盖 404 / 405 / 401 / 500，500 时自动回滚事务。JWT 的鉴权失败（缺 token / 过期 / 签名错误 / 已撤销）由 `extensions/jwt.py` 里的 loader 回调统一收敛为 `code=4401`，不会绕过统一格式

## 前端页面说明

前端为单文件实现（`static/index.html`），不依赖任何构建工具：

- 登录 / 注册视图切换，注册成功自动登录
- token 存于 localStorage，请求封装自动携带 `Authorization: Bearer`
- 统一拦截 `code=4401`（未登录 / token 过期 / token 无效）自动清除登录态并回到登录页
- 所有业务错误码转为页面 toast 提示
- 支持回车快速添加待办、勾选完成、删除

## 测试示例

```
curl -X POST http://127.0.0.1:5000/api/auth/login -H "Content-Type: application/json" -d "{\"username\":\"zhangsan\",\"password\":\"123456\"}"

curl http://127.0.0.1:5000/api/todo -H "Authorization: Bearer <token>"
```

## 许可证

[MIT](./LICENSE)
