from flask import Blueprint
auth = Blueprint('auth', __name__)
from . import routes  # 导入该蓝图的路由