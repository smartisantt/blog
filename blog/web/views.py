
from flask import Blueprint, render_template

from back.models import Article, ArticleType

web_blue = Blueprint('web', __name__)

@web_blue.route('/index/')
def index():
    articles = Article.query.order_by(Article.create_time).all()
    # atypes = ArticleType.query.all()
    # # 统计每个分类有多少篇文章
    # results = {}
    # for atype in atypes:
    #     num = Article.query.filter(atype.id == Article.type).count()
    #     if num == 0:
    #         continue
    #     results[atype.t_name] = num
    return render_template('web/index.html', articles=articles)


@web_blue.route('/category/<category_name>')
def category(category_name):
    atype = ArticleType.query.filter(ArticleType.t_name == category_name).first()
    articles= Article.query.filter(Article.type == atype.id).all()
    return render_template('web/category.html', articles=articles)


@web_blue.route('/info/<int:id>/')
def info(id):
    article = Article.query.get(id)
    articles = Article.query.order_by(Article.create_time).all()
    index = articles.index(article)
    length = len(articles) - 1

    if index == 0:
        pre_art = {}
    else:
        pre_art = articles[index-1]

    if index == length :
        next_art = {}
    else:
        next_art = articles[index+1]
    return render_template('web/info.html', article=article, pre_art=pre_art, next_art=next_art)


@web_blue.route('/art_list/')
def art_list():
    # 首页按发布时间显示文章
    articles = Article.query.order_by(Article.create_time).all()
    return render_template('web/art_list.html', articles=articles)