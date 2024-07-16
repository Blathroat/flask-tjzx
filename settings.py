from hashlib import md5
from flask import Flask
from flask_bootstrap import Bootstrap4
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
bootstrap = Bootstrap4(app)
app.config['WTF_I18N_ENABLED'] = False  # 禁用默认语言
app.config['SECRET_KEY'] = "HU7YUSsBgjec3GdcS621"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


def md5_hash(s):
    obj = md5()
    obj.update(str.encode(s, "utf-8"))
    return obj.hexdigest()
