import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Project(db.Model):
    """Model representing a portfolio project."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    technologies = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Project {self.title}>'


class Skill(db.Model):
    """Model representing a skill."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))

    def __repr__(self):
        return f'<Skill {self.name}>'


class ContactMessage(db.Model):
    """Model for storing contact messages from users."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ContactMessage from {self.name}>'


def init_db():
    """Initializes the database and adds sample data if the database is empty."""
    db.create_all()
    print(">>> Tables created (if they did not exist).")

    if Project.query.first() is None:
        sample_projects = [
            Project(title='Portfolio web', description='created using Flask, HTML, CSS and JS.', technologies='Flask, HTML, CSS, JavaScript, PostgreSQL'),
            Project(title='Game, "Guess the name"', description='A simple Python game using loops and conditionals.', technologies='Python'),
            Project(title='To-Do App', description='(planned) task management application with database.', technologies='Python, Flask, PostgreSQL')
        ]

        sample_skills = [
            Skill(name='HTML, CSS, Bootstrap', category='Frontend'),
            Skill(name='JavaScript (basics)', category='Frontend'),
            Skill(name='Python - Flask, Databases structure, Logic', category='Backend'),
            Skill(name='Git & GitHub', category='Tools'),
            Skill(name='Terminal support, VS Code', category='Tools')
        ]

        db.session.bulk_save_objects(sample_projects + sample_skills)
        db.session.commit()
        print(">>> Sample data added.")


def create_app():
    """Creates the Flask app, configures the database, and registers routes."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')

    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("Missing DATABASE_URL")

    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        init_db()

    @app.route('/')
    def home():
        """Homepage route."""
        return render_template('home.html')

    @app.route('/about')
    def about():
        """About page route."""
        return render_template('about.html')

    @app.route('/projects')
    def projects():
        """Displays the list of projects."""
        all_projects = Project.query.order_by(Project.created_at.desc()).all()
        return render_template('projects.html', projects=all_projects)

    @app.route('/skills')
    def skills():
        """Displays the list of skills."""
        all_skills = Skill.query.order_by(Skill.name.asc()).all()
        return render_template('skills.html', skills=all_skills)

    @app.route('/contact', methods=['GET', 'POST'])
    def contact():
        """Handles the contact form – saves messages to the database."""
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            message_text = request.form['message']

            new_message = ContactMessage(name=name, email=email, message=message_text)
            try:
                db.session.add(new_message)
                db.session.commit()
                return render_template('contact.html', submitted=True, name=name)
            except Exception as e:
                db.session.rollback()
                print(f"Error while saving: {e}")
                return render_template('contact.html', submitted=False, error=True)

        return render_template('contact.html', submitted=False)

    @app.route('/projects/new', methods=['GET', 'POST'])
    def new_project():
        """Adds a new project to the database."""
        if request.method == 'POST':
            title = request.form['title']
            description = request.form['description']
            technologies = request.form['technologies']

            new_project = Project(title=title, description=description, technologies=technologies)
            db.session.add(new_project)
            db.session.commit()
            flash(f"Project '{title}' has been added!", "success")
            return redirect(url_for('projects'))

        return render_template('new_project.html')

    @app.route('/projects/edit/<int:id>', methods=['GET', 'POST'])
    def edit_project(id):
        """Edits an existing project by ID."""
        project = Project.query.get_or_404(id)

        if request.method == 'POST':
            project.title = request.form['title']
            project.description = request.form['description']
            project.technologies = request.form['technologies']
            db.session.commit()
            flash(f"Project '{project.title}' has been updated.", "info")
            return redirect(url_for('projects'))

        return render_template('edit_project.html', project=project)

    @app.route('/projects/delete/<int:id>', methods=['POST'])
    def delete_project(id):
        """Deletes a project from the database."""
        project = Project.query.get_or_404(id)
        db.session.delete(project)
        db.session.commit()
        flash(f"Project '{project.title}' has been deleted.", "danger")
        return redirect(url_for('projects'))

    return app


app = create_app()
