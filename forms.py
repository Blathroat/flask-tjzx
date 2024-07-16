from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class MyBaseForm(FlaskForm):  # 设定默认语言为中文
    class Meta:
        locales = ['zh']


class LoginForm(MyBaseForm):
    username = StringField('用户名')
    password = PasswordField('密码')
    remember = BooleanField('记住我')
    submit = SubmitField('确定')


class RegisterForm(MyBaseForm):
    username = StringField('用户名', validators=[DataRequired(), Length(4, 24)])
    password = PasswordField('密码', validators=[DataRequired(), Length(8, 64)])
    re_password = PasswordField('重复密码', validators=[DataRequired(), EqualTo('password')])
    email = StringField('邮箱', validators=[DataRequired(), Email(message='邮箱格式错误')])
    submit = SubmitField('确定')


class PostForm(MyBaseForm):
    post = TextAreaField('来留个言吧', validators=[DataRequired()])
    submit = SubmitField('确定')
