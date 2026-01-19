import os
import sys
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

ON_PYTHONANYWHERE = 'PYTHONANYWHERE_DOMAIN' in os.environ

app = Flask(__name__)

app.config['SECRET_KEY'] = 'emikpro-super-secret-key-2024-0123456789'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taskflow.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Пожалуйста, войдите в систему для доступа к этой странице'

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    tasks = db.relationship('Task', backref='author', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')
    priority = db.Column(db.String(20), default='medium')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<Task {self.title}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_tables():
    with app.app_context():
        try:
            db.create_all()

            if User.query.count() == 0:
                test_user = User(username='test', email='test@example.com')
                test_user.set_password('test123')
                db.session.add(test_user)
                db.session.commit()

                sample_tasks = [
                    ('Настроить Flask приложение', 'Установить Flask и настроить виртуальное окружение', 'high'),
                    ('Создать базу данных', 'Инициализировать SQLite базу данных с таблицами', 'high'),
                    ('Добавить аутентификацию', 'Реализовать регистрацию и вход пользователей', 'medium'),
                    ('Реализовать REST API', 'Создать API для работы с задачами', 'medium'),
                    ('Протестировать все функции', 'Проверить работу всех компонентов системы', 'low'),
                    ('Развернуть на PythonAnywhere', 'Загрузить приложение на хостинг', 'high')
                ]

                for title, description, priority in sample_tasks:
                    task = Task(
                        title=title,
                        description=description,
                        priority=priority,
                        user_id=test_user.id
                    )
                    db.session.add(task)

                db.session.commit()
                print("Cоздан тестовый пользователь: test / test123")
                print("Добавлены тестовые задачи")

            print(f"База данных создана: {app.config['SQLALCHEMY_DATABASE_URI']}")

        except Exception as e:
            print(f"Ошибка при создании таблиц: {e}")
            db.session.rollback()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not username or len(username) < 3:
            flash('Имя пользователя должно быть не менее 3 символов')
            return redirect(url_for('register'))

        if not email or '@' not in email:
            flash('Введите корректный email адрес')
            return redirect(url_for('register'))

        if not password or len(password) < 6:
            flash('Пароль должен быть не менее 6 символов')
            return redirect(url_for('register'))

        if User.query.filter_by(username=username).first():
            flash('Пользователь с таким именем уже существует')
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash('Пользователь с таким email уже зарегистрирован')
            return redirect(url_for('register'))

        try:
            user = User(username=username, email=email)
            user.set_password(password)

            db.session.add(user)
            db.session.commit()

            flash('Регистрация успешна! Теперь вы можете войти в систему.')
            return redirect(url_for('login'))

        except Exception as e:
            db.session.rollback()
            flash('Ошибка при регистрации. Попробуйте еще раз.')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Вход в систему"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user, remember=True)
            flash(f'Добро пожаловать, {username}!')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))

        flash('Неверное имя пользователя или пароль')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """Выход из системы"""
    logout_user()
    flash('Вы успешно вышли из системы')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Панель управления"""
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.created_at.desc()).all()

    task_count = len(tasks)
    completed_count = len([t for t in tasks if t.status == 'completed'])
    pending_count = task_count - completed_count

    return render_template('dashboard.html',
                         tasks=tasks,
                         task_count=task_count,
                         completed_count=completed_count,
                         pending_count=pending_count)

@app.route('/add_task', methods=['POST'])
@login_required
def add_task():
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    priority = request.form.get('priority', 'medium')

    if not title:
        flash('Введите название задачи')
        return redirect(url_for('dashboard'))

    try:
        task = Task(
            title=title,
            description=description,
            priority=priority,
            user_id=current_user.id
        )

        db.session.add(task)
        db.session.commit()

        flash('Задача успешно добавлена!')

    except Exception as e:
        db.session.rollback()
        flash('Ошибка при добавлении задачи')

    return redirect(url_for('dashboard'))

@app.route('/complete_task/<int:task_id>', methods=['POST'])
@login_required
def complete_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()

    if task:
        try:
            task.status = 'completed' if task.status != 'completed' else 'pending'
            db.session.commit()
            flash(f'Задача "{task.title}" обновлена')

        except Exception as e:
            db.session.rollback()
            flash('Ошибка при обновлении задачи')

    return redirect(url_for('dashboard'))

@app.route('/delete_task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()

    if task:
        try:
            db.session.delete(task)
            db.session.commit()
            flash(f'Задача "{task.title}" удалена')

        except Exception as e:
            db.session.rollback()
            flash('Ошибка при удалении задачи')

    return redirect(url_for('dashboard'))

@app.route('/api/tasks', methods=['GET'])
@login_required
def api_get_tasks():
    try:
        tasks = Task.query.filter_by(user_id=current_user.id).all()
        return jsonify({
            'status': 'success',
            'count': len(tasks),
            'tasks': [task.to_dict() for task in tasks]
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
@login_required
def api_get_task(task_id):
    try:
        task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
        if not task:
            return jsonify({'status': 'error', 'message': 'Задача не найдена'}), 404

        return jsonify({
            'status': 'success',
            'task': task.to_dict()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/tasks', methods=['POST'])
@login_required
def api_create_task():
    try:
        data = request.get_json()

        if not data or not data.get('title'):
            return jsonify({
                'status': 'error',
                'message': 'Необходимо указать название задачи'
            }), 400

        task = Task(
            title=data['title'].strip(),
            description=data.get('description', '').strip(),
            priority=data.get('priority', 'medium'),
            user_id=current_user.id
        )

        db.session.add(task)
        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': 'Задача создана',
            'task': task.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
@login_required
def api_update_task(task_id):
    try:
        task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
        if not task:
            return jsonify({'status': 'error', 'message': 'Задача не найдена'}), 404

        data = request.get_json()

        # Обновляем поля если они есть в запросе
        if 'title' in data:
            task.title = data['title'].strip()
        if 'description' in data:
            task.description = data['description'].strip()
        if 'status' in data:
            task.status = data['status']
        if 'priority' in data:
            task.priority = data['priority']

        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': 'Задача обновлена',
            'task': task.to_dict()
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
@login_required
def api_delete_task(task_id):
    """Удалить задачу (API)"""
    try:
        task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
        if not task:
            return jsonify({'status': 'error', 'message': 'Задача не найдена'}), 404

        db.session.delete(task)
        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': 'Задача удалена'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def api_health():
    return jsonify({
        'status': 'healthy',
        'service': 'TaskFlow API',
        'version': '1.0',
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/api/user/info', methods=['GET'])
@login_required
def api_user_info():
    return jsonify({
        'status': 'success',
        'user': {
            'id': current_user.id,
            'username': current_user.username,
            'email': current_user.email,
            'created_at': current_user.created_at.isoformat() if current_user.created_at else None
        }
    })

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

@app.cli.command('init-db')
def init_db_command():
    create_tables()
    print('База данных инициализирована.')

@app.cli.command('create-user')
def create_user_command():
    username = input('Имя пользователя: ')
    email = input('Email: ')
    password = input('Пароль: ')

    if User.query.filter_by(username=username).first():
        print('Пользователь уже существует.')
        return

    user = User(username=username, email=email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    print(f'Пользователь {username} создан.')

@app.cli.command('list-users')
def list_users_command():
    """Список всех пользователей"""
    users = User.query.all()
    for user in users:
        print(f'{user.id}: {user.username} ({user.email})')

if __name__ == '__main__':
    create_tables()

    if ON_PYTHONANYWHERE:
        print("=" * 60)
        print("TASKFLOW запущен на PythonAnywhere")
        print("=" * 60)
    else:
        print("=" * 60)
        print("🚀 TASKFLOW - Менеджер задач на Flask")
        print("=" * 60)
        print("\n📊 Информация о приложении:")
        print(f"   • Режим: {'Разработка' if app.debug else 'Продакшн'}")
        print(f"   • База данных: {app.config['SQLALCHEMY_DATABASE_URI']}")
        print("\n🌐 Доступные маршруты:")
        print("   • Главная: http://localhost:5000")
        print("   • Регистрация: http://localhost:5000/register")
        print("   • Вход: http://localhost:5000/login")
        print("   • Панель управления: http://localhost:5000/dashboard")
        print("   • API задачи: http://localhost:5000/api/tasks")
        print("   • API здоровье: http://localhost:5000/api/health")
        print("\n👤 Тестовый аккаунт:")
        print("   • Логин: test")
        print("   • Пароль: test123")
        print("\n" + "=" * 60)
        print("   Сервер запущен. Нажмите Ctrl+C для остановки.")
        print("=" * 60)

        app.run(
            debug=True,
            host='0.0.0.0',
            port=5000
        )