from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from models.models import db, Task

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/tasks', methods=['GET'])
@login_required
def get_tasks():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return jsonify({
        'status': 'success',
        'count': len(tasks),
        'tasks': [task.to_dict() for task in tasks]
    })

@api.route('/tasks/<int:task_id>', methods=['GET'])
@login_required
def get_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    if not task:
        return jsonify({'error': 'Задача не найдена'}), 404
    return jsonify(task.to_dict())

@api.route('/tasks', methods=['POST'])
@login_required
def create_task():
    data = request.get_json()

    if not data or not data.get('title'):
        return jsonify({'error': 'Необходимо указать название задачи'}), 400

    task = Task(
        title=data['title'],
        description=data.get('description', ''),
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

@api.route('/tasks/<int:task_id>', methods=['PUT'])
@login_required
def update_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    if not task:
        return jsonify({'error': 'Задача не найдена'}), 404

    data = request.get_json()

    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
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

@api.route('/tasks/<int:task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    if not task:
        return jsonify({'error': 'Задача не найдена'}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({
        'status': 'success',
        'message': 'Задача удалена'
    }), 200

@api.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'TaskFlow API',
        'version': '1.0'
    })