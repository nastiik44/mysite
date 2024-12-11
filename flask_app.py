from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import re

app = Flask(__name__)
app.secret_key = ''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emails.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Модель данных
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    confirmed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Главная страница с формой
@app.route('/')
def index():
    return render_template('index.html')

# Обработка формы
@app.route('/submit', methods=['POST'])
def submit_email():
    email = request.form.get('textInput', '').strip().lower()

    # Выражение для проверки email
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$' 

    # Проверка: email не пустой и соответствует формату
    if not email or not re.match(email_regex, email):
        return redirect(url_for('error_page'))

    # Проверка: существует ли уже email в базе данных
    if User.query.filter_by(email=email).first():
        return redirect(url_for('already_sub_page'))

    # Добавление email в базу данных
    new_user = User(email=email)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('success_page'))

# Страница успешной подписки
@app.route('/success')
def success_page():
    return render_template('sucess.html')

# Страница ошибки
@app.route('/error')
def error_page():
    return render_template('error.html')

# Страница ошибки
@app.route('/already_sub')
def already_sub_page():
    return render_template('already_sub.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Создание таблиц
    app.run(debug=True)