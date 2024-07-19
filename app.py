from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('user_list'))
        flash('Login failed. Check your username and/or password.')
    return render_template('login.html')

@app.route('/user_list')
def user_list():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    users = User.query.all()
    return render_template('user_list.html', users=users)

def create_db():
    with app.app_context():
        db.create_all()
        # Tambahkan pengguna default jika tidak ada
        if User.query.count() == 0:
            hashed_password = generate_password_hash('password123', method='pbkdf2:sha256')
            user = User(username='testuser', password=hashed_password)
            db.session.add(user)
            db.session.commit()

if __name__ == '__main__':
    create_db()
    app.run(debug=True)
