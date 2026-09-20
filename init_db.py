# init_db.py —— 首次运行：建表 + 初始化账号
import sys
sys.path.insert(0, ".")

from app import create_app
from extensions.db import db
from app.models import User, Department
from werkzeug.security import generate_password_hash

app = create_app("dev")

with app.app_context():
    db.create_all()  # 如果用 schema.sql 建过表，这步会跳过已存在表，安全

    if not Department.query.filter_by(name="计算机系").first():
        db.session.add(Department(name="计算机系"))
    if not Department.query.filter_by(name="软件工程系").first():
        db.session.add(Department(name="软件工程系"))
    db.session.commit()

    dept = Department.query.filter_by(name="计算机系").first()

    # 张三
    zs = User.query.filter_by(username="zhangsan").first()
    if not zs:
        zs = User(username="zhangsan", nickname="三哥", student_no="20210901", dept_id=dept.id)
        zs.password = "123456"
        db.session.add(zs)

    # 李四（用来演示越权）
    ls = User.query.filter_by(username="lisi").first()
    if not ls:
        ls = User(username="lisi", nickname="四妹", student_no="20210902", dept_id=dept.id)
        ls.password = "123456"
        db.session.add(ls)

    db.session.commit()
    print("✅ 初始化完成：")
    print("   zhangsan / 123456")
    print("   lisi     / 123456")