from flask_sqlalchemy import SQLAlchemy

# 单例：在 extensions 层创建，避免 models / routes 互相导入造成循环导入
db = SQLAlchemy()
