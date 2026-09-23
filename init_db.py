# init_db.py —— 首次运行：建表 + 初始化账号
import sys
sys.path.insert(0, ".")

from app import create_app
from extensions.db import db
from app.models import User, Department, UserExtension

app = create_app("dev")

with app.app_context():
    db.create_all()  # 如果用 schema.sql 建过表，这步会跳过已存在表，安全

    if not Department.query.filter_by(name="计算机系").first():
        db.session.add(Department(name="计算机系"))
    if not Department.query.filter_by(name="软件工程系").first():
        db.session.add(Department(name="软件工程系"))
    db.session.commit()

    dept = Department.query.filter_by(name="计算机系").first()

    def make_user(username: str, nickname: str, student_no: str) -> User:
        """幂等创建：已存在就跳过。学号在扩展表上，与用户一起提交。"""
        user = User.query.filter_by(username=username).first()
        if user:
            return user
        user = User(username=username, nickname=nickname, department_id=dept.id)
        user.password = "123456"  # setter 内自动哈希
        user.extension = UserExtension(student_no=student_no)
        db.session.add(user)
        return user

    # 张三
    make_user("zhangsan", "三哥", "20210901")
    # 李四（用来演示越权）
    make_user("lisi", "四妹", "20210902")

    db.session.commit()
    print("✅ 初始化完成：")
    print("   zhangsan / 123456")
    print("   lisi     / 123456")
