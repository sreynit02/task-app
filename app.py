from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from models import db, Task, User  # Ensure db is imported before using it
from auth import auth as auth_blueprint
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(auth_blueprint)

    @app.route('/')
    def home():
        tasks = Task.query.all()
        return render_template('index.html', tasks=tasks)

    @app.route('/profile')
    @login_required
    def profile():
        return render_template('profile.html', name=current_user.name)

    @app.route('/add-task', methods=['POST'])
    def add_task():
        name = request.form['name']
        description = request.form['description']
        duedate = request.form['duedate']
        print(f"Due Date Received: {duedate}")  # Debugging

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

    @app.route('/login')
    def login():
        return render_template('login.html')

    @app.route("/login", methods=["POST"])
    def login_post():
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if not user or user.password != password:
            flash("Please check your login details and try again.")
            return redirect(url_for("login"))

        login_user(user)
        return redirect(url_for("home"))

    @app.route('/signup')
    def signup():
        return render_template('signup.html')

    @app.route("/signup", methods=["POST"])
    def signup_post():
        email = request.form.get("email")
        password = request.form.get("password")
        name = request.form.get("name")

        user = User.query.filter_by(email=email).first()

        if user:
            flash("Email address already exists")
            return redirect(url_for("signup"))

        new_user = User(email=email, password=password, name=name)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('home'))

    return app

app = create_app()

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
