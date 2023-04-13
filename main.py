from flask import Flask, flash, redirect, render_template, request
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo

from data import db_session
from data.users import User

app = Flask(__name__)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


class LoginForm(FlaskForm):
    username = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Enter')

class RegisterForm(FlaskForm):
    username = StringField('Login', validators=[DataRequired()])
    password_1 = PasswordField('Create Password', validators=[DataRequired()])
    password_2 = PasswordField('Repeat the Password', validators=[DataRequired(), EqualTo('password_1', message='Passwords must match')])
    submit = SubmitField('Enter')


@app.route('/')
def start():
    return redirect('/register')

@app.route('/login', methods=['GET', 'POST'])
def login():
    global username
    global password
    form = LoginForm()
    if form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']
        print(username, password)
        return redirect('/success')
    return render_template('login.html', title='Authorisation', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    global username
    global password
    form = RegisterForm()
    if form.validate_on_submit():
        username = request.form['username']
        password_1 = request.form['password_1']
        password_2 = request.form['password_2']
        db_session.global_init("db/blogs.db")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.name == username).all():
            return render_template('register.html', title='AAAA', form=form, message="Такой пользователь уже есть")
        # <--------db-------->
        user = User()
        user.name = username
        user.password = password_1
        db_sess.add(user)
        db_sess.commit()
        # <--------db-------->
        #print(username, password_1, password_2)
        return redirect('/success')
    #elif request.method == 'POST':
    #    flash('Please correct the errors below.')
    return render_template('register.html', title='Authorisation', form=form)


@app.route('/success')
def success():
    return render_template('success.html', username=username)


if __name__ == '__main__':
    app.run(port=5000, host='127.0.0.1')
