from flask import render_template, flash, session, redirect
from markupsafe import Markup
from time import time

from forms import *
from userdb import *
from settings import app, md5_hash


@app.errorhandler(404)
def error404(error):
    return render_template('404page.html'), 404


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        username = Markup(login_form.username.data)
        password = Markup(login_form.password.data)
        if user_verification(username, password):
            session['username'] = username
            return redirect('/')
        else:
            flash('用户名或密码错误')
    return render_template('login.html', loginform=login_form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        username = Markup(register_form.username.data)
        password = Markup(register_form.password.data)
        email = Markup(register_form.email.data)
        if is_user_available(username, email):
            add_datas = User(username, md5_hash(password), email, 'admin', 'normal')
            db.session.add(add_datas)
            db.session.commit()
            session['username'] = username
            return redirect('/')
        else:
            flash('用户名或邮箱已被占用')
    return render_template('register.html', registerform=register_form)


@app.route('/posts_board/<page>', methods=['GET', 'POST'])
def posts_board(page):
    post_form = PostForm()
    if page:
        posts = get_post_pages(page).items
        if get_post_pages(page).has_next:
            next_page = int(page) + 1
        else:
            next_page = 0
        if post_form.validate_on_submit():
            post = Markup(post_form.post.data)
            print(post, time(), get_user(session.get('username')).id)
            add_datas = Posts(post, time(), get_user(session.get('username')).id)
            db.session.add(add_datas)
            db.session.commit()
            return redirect('/posts_board/' + page)
    return render_template('posts_board.html', posts=posts, post_form=post_form, next_page=next_page)


if __name__ == '__main__':
    app.run()
