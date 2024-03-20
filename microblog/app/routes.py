from app import app,db
from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.security import check_password_hash, generate_password_hash
from app.models import User
from flask_login import login_user, logout_user, current_user, login_required
from urllib.parse import urlsplit

# @app.route('/')
# def home():
#     return redirect(url_for('login'))


@app.route('/')
def home():
    return 'Hello world'

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        password_hash = generate_password_hash(password)
        user = User(username=username, email=email,
                    password_hash=password_hash)
        db.session.add(user)
        db.session.commit()

        flash('Registration successful')
        return redirect(url_for('login'))
    return render_template('register.html',title='Register')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        print(user)
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            if not next_page or urlsplit(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))
    return render_template('login.html',  title='Log In')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# 測試db是否連線成功
@app.route('/test_db')
def test_db():
    try:
        user_count = User.query.count()
        return f"資料庫連線成功，用戶數量為：{user_count}"
    except Exception as e:
        return f"資料庫連線失敗，錯問訊息：{e}"


# 登入成功後，可以看到index頁面
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')

# 個人頁面
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        # print(current_user)
        # 從表單獲取資料
        username = request.form.get('username')
        about_me = request.form.get('about_me')
        if not username:
            flash('Username is required.')
            return redirect(url_for('edit_profile'))
        current_user.username = username
        current_user.about_me = about_me
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    return render_template('edit_profile.html', title='Edit Profile',
                           username=current_user.username,
                           about_me=current_user.about_me)
