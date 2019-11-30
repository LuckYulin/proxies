from flask import Blueprint, Response
from redis import Redis
from config import REDIS_URL


REDIS_db = Redis(*REDIS_URL)
bp_index = Blueprint('bp_index', __name__)   # 创建蓝图bp_index
bp_get = Blueprint('bp_get', __name__)       # 创建蓝图bp_get


def _get():
    """get a new porxy"""
    return REDIS_db.rpop('proxy')


@bp_index.route('/')
def index():
    return Response('你好, 欢迎使用代理...')


@bp_get.route('/')
def get():
    return Response(_get())


