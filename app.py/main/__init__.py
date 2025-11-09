from flask import Blueprint
main = Blueprint('main', __name__)
from . import routes  # 导入该蓝图的路由


