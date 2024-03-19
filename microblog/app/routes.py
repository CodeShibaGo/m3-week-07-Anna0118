from app import app,db
from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.security import check_password_hash, generate_password_hash
from app.models import User

@app.route('/')
def home():
    # return redirect(url_for('login'))
    return "Hello"

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
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        print(user)
        if user and check_password_hash(user.password_hash, password):
            flash('Login successful')
            return "Login successful"
        flash('Invalid username or password')
    return render_template('login.html',  title='Sign In')

# 測試db是否連線成功
@app.route('/test_db')
def test_db():
    try:
        user_count = User.query.count()
        return f"資料庫連線成功，用戶數量為：{user_count}"
    except Exception as e:
        return f"資料庫連線失敗，錯問訊息：{e}"
