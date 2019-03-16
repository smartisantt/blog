import os
from datetime import timedelta

import redis
from flask import Flask
from flask_script import Manager
from flask_session import Session

from back.models import db
from back.views import back_blue
from utils.functions import get_username, category
from web.views import web_blue

app = Flask(__name__)
app.register_blueprint(blueprint=back_blue, url_prefix='/back')
app.register_blueprint(blueprint=web_blue, url_prefix='/web')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@39.105.49.244:3306/blog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.Redis(host='39.105.49.244', port='6379', password='123456')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60)
app.secret_key = os.urandom(24)

Session(app)
db.init_app(app)
manage = Manager(app)


# 注册自定义过滤器，实现通过session保存的id取到用户名，最终呈现在界面上
env = app.jinja_env
env.filters['get_username'] = get_username
env.filters['category'] = category



if __name__ == '__main__':
    manage.run()