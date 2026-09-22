# app/models/__init__.py
from extensions.db import db

from app.models import user, department, permission, user_extension, todo

# 只把「类」提到包层级，方便外面 from app.models import User, Department...
from app.models.user import User
from app.models.department import Department
from app.models.permission import Permission
from app.models.user_extension import UserExtension
from app.models.todo import Todo

# 关系已在各模型类内声明完成，这里不需要再补 relationship