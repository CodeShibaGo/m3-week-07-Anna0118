from app import app, db
from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.security import check_password_hash, generate_password_hash
from app.models import User, Post
from flask_login import login_user, logout_user, current_user, login_required
from urllib.parse import urlsplit
from datetime import datetime, timezone


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        #  不需要add，因為數據已存在，current_user會自動去追蹤
        db.session.commit()


# 首頁
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    print(current_user.is_authenticated)
    if request.method == 'POST':
        post = request.form.get('post')
        if len(post.strip()) == 0:
            flash('Post content cannot be empty.')
            return redirect(url_for('index'))
        posts = Post(body=post, author=current_user)
        db.session.add(posts)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    posts = current_user.following_posts().all()
    return render_template("index.html", title='Home Page', posts=posts)

# 註冊
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
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
    return render_template('register.html', title='Register')

# 登入
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

# 登出
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('register'))


# 測試db是否連線成功
@app.route('/test_db')
def test_db():
    try:
        user_count = User.query.count()
        return f"資料庫連線成功，用戶數量為：{user_count}"
    except Exception as e:
        return f"資料庫連線失敗，錯問訊息：{e}"


# 個人頁面
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(user_id=user.id).all()
    return render_template('user.html', user=user, posts=posts)


# 編輯個人檔案
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
        # 不可與資料庫內的username重複
        user = User.query.filter_by(username=username).first()
        if user is not None and user.username != current_user.username:
            flash('This username is already in use. Please use a different username.')
            return redirect(url_for('edit_profile'))
        current_user.username = username
        current_user.about_me = about_me
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    return render_template('edit_profile.html', title='Edit Profile',
                           username=current_user.username,
                           about_me=current_user.about_me)

# 追蹤
@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    if request.method == 'POST':
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(f'User {username} not found.')
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash(f'You are following {username}!')
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))

# 退追蹤
@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    if request.method == 'POST':
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(f'User {username} not found.')
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash(f'You are not following {username}.')
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))
