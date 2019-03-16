from datetime import datetime
from math import ceil

from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash,check_password_hash

from back.models import User, Article, ArticleType, db
from utils.functions import is_login

back_blue = Blueprint('back', __name__)

ITEMS_PER_PAGE = 10

@back_blue.route('/index/')
@is_login
def index():
    return render_template('back/index.html')





@back_blue.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('back/register.html')
    if request.method == 'POST':
        # 获取数据
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        if not all([username, password, password2]):
            error = '请提交完整的信息！'
            return render_template('back/register.html', error=error)
        user = User.query.filter(User.username == username).first()
        if user:
            error = '改账号已注册，请更换账号！'
            return render_template('back/register.html', error=error)
        if password != password2:
            error = '两次密码不一致！'
            return render_template('back/register.html', error=error)

        # 成功注册
        user = User()
        user.username = username
        print(username)
        user.password = generate_password_hash(password)
        user.save()
        return redirect(url_for('back.login'))


@back_blue.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('back/login.html')

    if request.method == 'POST':
        # 获取数据
        username = request.form.get('username')
        password = request.form.get('password')
        if not all([username, password]):
            error = '请填写完整信息！'
            return render_template('back/login.html', error=error)
        user = User.query.filter(User.username == username).first()
        if not user:
            error = '改用户未注册！'
            return render_template('back/login.html', error=error)
        if not check_password_hash(user.password, password):
            error = '密码错误，请修改密码！'
            return render_template('back/login.html', error=error)
        # 登录成功,保存标识符，跳转首页
        # session['user'] = user
        session['user_id'] = user.id
        session.permanent = True
        user.current_login_time = datetime.now()
        user.save()

        return redirect(url_for('back.index'))


@back_blue.route('/logout/', methods=['GET'])
@is_login
def logout():
    user = User.query.filter(User.id == session['user_id']).first()
    user.last_login_time = user.current_login_time
    user.current_login_time = None
    user.save()
    del session['user_id']
    return redirect(url_for('back.login'))


@back_blue.route('/a_type/', methods=['GET', 'POST'])
@is_login
def a_type():
    if request.method == 'GET':
        types = ArticleType.query.all()
        return render_template('back/category_list.html', types=types)


@back_blue.route('/add_type/', methods=['GET', 'POST'])
@is_login
def add_type():
    if request.method == 'GET':
        return render_template('back/category_add.html')
    if request.method == 'POST':
        atype = request.form.get('atype')
        if atype:
            # 保存分类
            art_type = ArticleType()
            art_type.t_name = atype
            art_type.save()
            return redirect(url_for('back.a_type'))
        else:
            error = '请填写分类信息！'
            return render_template('back/category_add.html', error=error)


@back_blue.route('/del_type/<int:id>/', methods=['GET'])
@is_login
def del_type(id):
    # 删除分类
    atype = ArticleType.query.get(id)
    db.session.delete(atype)
    db.session.commit()
    return redirect(url_for('back.a_type'))


@back_blue.route('/article_list/', methods=['GET'])
@is_login
def article_list():
    articles = Article.query.all()
    art_total = len(articles)
    pages = ceil(art_total / ITEMS_PER_PAGE)
    return render_template('back/article_list.html', articles=articles, pages=pages)



@ back_blue.route('/article_page/<int:page>',methods=['GET'])
@ is_login
def article_page(page):
    articles = Article.query.all()
    art_total = len(articles)
    pages = ceil(art_total / ITEMS_PER_PAGE)
    articles = articles[(page - 1) * ITEMS_PER_PAGE:page * ITEMS_PER_PAGE]
    return render_template('back/article_list.html', articles=articles, pages=pages, page=page)



@back_blue.route('/article_add/', methods=['GET', 'POST'])
@is_login
def article_add():
    if request.method == 'GET':
        types = ArticleType.query.all()
        return render_template('back/article_add.html', types=types)
    if request.method == 'POST':
        # 获取数据
        title = request.form.get('name')
        desc = request.form.get('desc')
        category = request.form.get('category')
        content = request.form.get('my-editormd-html-code')
        content2 = request.form.get('my-editormd-markdown-doc')
        print(content)
        print(content2)

        if not all([title, desc, category, content]):
            error = '请填写完整信息！'
            return render_template('back/article_add.html', error=error)
        # 保存到数据库
        art = Article()
        art.title = title
        art.desc = desc
        art.type = category
        art.content = content
        art.save()
        return redirect(url_for('back.article_page', page=1))


@back_blue.route('/user_info/', methods=['GET', 'POST'])
@is_login
def user_info():
    if request.method == 'GET':
        user = User.query.filter(session['user_id'] == User.id).first()
        username = user.username
        create_time = user.create_time
        last_login_time = user.last_login_time
        current_login_time = user.current_login_time
        return render_template('back/user_info.html',
                               username=username,
                               create_time=create_time,
                               last_login_time=last_login_time,
                               current_login_time=current_login_time)
    if request.method == 'POST':
        return logout()



@back_blue.route('/del_art/<int:id>/', methods=['GET'])
@is_login
def del_art(id):
    # 删除分类
    art = Article.query.get(id)
    db.session.delete(art)
    db.session.commit()
    return redirect(url_for('back.article_page', page=1))


@back_blue.route('/art_modify/<int:id>/', methods=['GET', 'POST'])
@is_login
def art_modify(id):
    art = Article.query.get(id)
    types = ArticleType.query.all()
    if request.method == 'GET':
        return render_template('back/article_modify.html', art=art, types=types)
        # 修改文章前显示原文本信息
    if request.method == 'POST':
        # 修改文章后重新获取数据，保存到数据库
        title = request.form.get('name')
        desc = request.form.get('desc')
        category = request.form.get('category')
        content = request.form.get('content')

        art.title = title
        art.desc = desc
        art.type = category
        art.content = content
        art.save()
        return redirect(url_for('back.article_page', page=1))