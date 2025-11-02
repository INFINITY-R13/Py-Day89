from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    complete = db.Column(db.Boolean, default=False)


with app.app_context():
    db.create_all()


@app.route('/')
@app.route('/filter/<filter_type>')
def index(filter_type='all'):
    if filter_type == 'active':
        todos = Todo.query.filter_by(complete=False).all()
    elif filter_type == 'completed':
        todos = Todo.query.filter_by(complete=True).all()
    else:
        todos = Todo.query.all()
    return render_template('index.html', todos=todos, filter_type=filter_type)


@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    filter_type = request.args.get('filter', 'all')
    if task:
        new_todo = Todo(task=task)
        db.session.add(new_todo)
        db.session.commit()
    return redirect(url_for('index', filter_type=filter_type))


@app.route('/complete/<int:id>')
def complete(id):
    filter_type = request.args.get('filter', 'all')
    todo = Todo.query.get_or_404(id)
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for('index', filter_type=filter_type))


@app.route('/delete/<int:id>')
def delete(id):
    filter_type = request.args.get('filter', 'all')
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index', filter_type=filter_type))


if __name__ == '__main__':
    app.run(debug=True)
