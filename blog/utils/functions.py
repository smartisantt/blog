from functools import wraps

from flask import session,redirect,url_for

from back.models import User, Article, ArticleType


def is_login(func):
    @wraps(func)
    def check(*arg, **kwargs):
        user_id = session.get('user_id')
        if user_id:
            return func(*arg, **kwargs)
        else:
            return redirect(url_for('back.login'))
    return check


def get_username(session):
    return User.query.filter(session['user_id'] == User.id).first().username


def category(articles):
    atypes = ArticleType.query.all()
    # 统计每个分类有多少篇文章
    results = {}
    for atype in atypes:
        num = Article.query.filter(atype.id == Article.type).count()
        if num == 0:
            continue
        results[atype.t_name] = num
    return results




