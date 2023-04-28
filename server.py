from deep_translator import GoogleTranslator
from flask import Flask, flash, make_response, redirect, render_template, request, session
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo

from data import db_session
from data.users import User

# FIXME:
# ~~ Translator can't translate digits

app = Flask(__name__)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password_1 = PasswordField('Create Password', validators=[DataRequired()])
    password_2 = PasswordField('Repeat the Password', validators=[DataRequired(), EqualTo('password_1', message='Passwords must match')])
    submit = SubmitField('Register')


@app.route('/')
def start():
    return redirect('/login')

#@app.route("/session_test")
#def session_test():
#    visits_count = session.get('visits_count', 0)
#    session['visits_count'] = visits_count + 1
#    return make_response(f"Вы пришли на эту страницу {visits_count + 1} раз")

@app.route('/login', methods=['GET', 'POST'])
def login():
    global username
    global password
    form = LoginForm()
    if form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']
        # <user--check>
        db_session.global_init("db/blogs.db")
        db_sess = db_session.create_session()
        #if db_sess.query(User).filter(User.name == username).all():
        #    print(f'User already exists: {username}')
        #    return render_template('login.html', title='Login Failed', form=form, message="Неверный пароль")
        user = db_sess.query(User).filter(User.name == username).first()
        if user and user.password == password:
            # login successful
            return redirect('/success')
        else:
            # login failed
            return render_template('login.html', title='Login Failed', form=form, message="Неверный логин или пароль")
        # </user--check>
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
            print(f'User already exists: {username}')
            return render_template('register.html', title='Registration failed', form=form, message="Такой пользователь уже есть")
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


#@app.route('/success')
#def success():
#    return render_template('success.html', username=username)

@app.route('/success', methods=['GET', 'POST'])
def translate():
    if request.method == 'POST':
        text = str(request.form['text'])
        #translated_text = text[::-1]
        if text.isdigit():
            return render_template('success.html', message="Нельзя переводить только числа")
        translated_text = GoogleTranslator(source='auto', target='ru').translate(str(text))
        return render_template('success.html', translated_text=translated_text, original_text=str(text))
    else:
        return render_template('success.html')

if __name__ == '__main__':
    app.run(port=5000, host='127.0.0.1')
