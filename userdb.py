from sqlalchemy import or_
from sqlalchemy.orm import Query

from settings import db, md5_hash


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    pwdhash = db.Column(db.String)
    email = db.Column(db.String)
    roler = db.Column(db.String)
    state = db.Column(db.String)
    comments = db.relationship('Posts', backref='user')

    def __init__(self, username, pwdhash, email, roler, state):
        self.username = username
        self.pwdhash = pwdhash
        self.email = email
        self.roler = roler
        self.state = state


class Posts(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    articles = db.Column(db.Text)
    timestamp = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, articles, timestamp, user_id):
        self.articles = articles
        self.timestamp = timestamp
        self.user_id = user_id


def get_post_pages(page, pagesize=10):
    query = Posts.query.order_by(Posts.timestamp.desc())
    posts = query.paginate(page=int(page), per_page=pagesize, error_out=False)
    return posts


def get_user(username):
    query: Query = User.query
    user = query.filter(User.username == username).one()
    return user


def user_verification(username, pwd):
    """
    用于登陆时验证用户信息
    """
    query: Query = User.query
    if query.filter(User.username == username, User.pwdhash == md5_hash(pwd)).one_or_none():
        return True
    else:
        return False


def is_user_available(username, email):
    """
    用于注册时检测有无重复的用户信息
    """
    query: Query = User.query
    if not (query.filter(or_(User.username == username, User.email == email)).limit(1).all()):  # 如果数据库中没有目标已注册用户名和邮箱
        return True
    else:
        return False
