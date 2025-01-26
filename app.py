from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	description = db.Column(db.String(200), nullable=True)
	status = db.Column(db.String(10), default='Pending')
	dueDate = db.Column(db.DateTime, nullable=True)

# Create the database
with app.app_context():
    db.create_all()

@app.route('/')
def home():
	tasks = Task.query.all()
	return render_template('index.html', tasks=tasks)
if __name__ == '__main__':
	app.run(debug=True)

@app.route('/add-task', methods=['POST'])
def add_task():
	name = request.form['name']
	description = request.form['description']
	duedate = request.form['duedate']
	print(f"Due Date Received: {duedate}")  # Debug: Print received due_date


	duedate = datetime.strptime(duedate, '%Y-%m-%dT%H:%M') if duedate else None
	print(duedate)
	new_task = Task(name=name, description=description, dueDate=duedate)
	db.session.add(new_task)
	db.session.commit()
	return redirect(url_for('home'))

@app.route('/delete-task/<int:task_id>', methods=['GET'])
def delete_task(task_id):
	task = Task.query.get_or_404(task_id)
	db.session.delete(task)
	db.session.commit()
	return redirect(url_for('home'))
