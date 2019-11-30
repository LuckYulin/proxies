import flask
from .app_proxies import bp_get, bp_index
from flask import Flask

app = Flask('WEB')  # 创建APP应用
app.register_blueprint(bp_index)                  # 注册蓝图bp_index
app.register_blueprint(bp_get, url_prefix='/get') # 注册蓝图bp_get


