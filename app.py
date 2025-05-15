from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модель задачи
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'completed': self.completed
        }

# Инициализация базы данных
@app.before_first_request
def create_tables():
    db.create_all()

# Главная страница
@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

# Получить все задачи
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.serialize() for task in tasks]), 200

# Создать новую задачу
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.form
    new_task = Task(title=data['title'])
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('index'))

# Обновить задачу
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get_or_404(id)
    data = request.get_json()
    task.completed = data.get('completed', task.completed)
    task.title = data.get('title', task.title)
    db.session.commit()
    return jsonify(task.serialize()), 200

# Удалить задачу
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
