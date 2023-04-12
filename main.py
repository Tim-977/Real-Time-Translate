from flask import Flask, render_template, redirect, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo

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
    return redirect('/login')

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
    return render_template('login.html', title='Авторизация', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    global username
    global password
    form = RegisterForm()
    if form.validate_on_submit():
        username = request.form['username']
        password_1 = request.form['password_1']
        password_2 = request.form['password_2']
        print(username, password_1, password_2)
        return redirect('/success')
    elif request.method == 'POST':
        flash('Please correct the errors below.')
    return render_template('register.html', title='Авторизация', form=form)


@app.route('/success')
def success():
    return render_template('success.html', username=username)


if __name__ == '__main__':
    app.run(port=5000, host='127.0.0.1')
