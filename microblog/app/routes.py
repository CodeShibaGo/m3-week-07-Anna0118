from app import app
from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.security import check_password_hash, generate_password_hash

users = []


@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password)
        users.append({"username": username, "password": hashed_password})
        flash('Registration successful')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        for user in users:
            if user['username'] == username and check_password_hash(user['password'], password):
                flash('Login successful')
                return "Login successful"
        flash('Invalid username or password')
    return render_template('login.html')
