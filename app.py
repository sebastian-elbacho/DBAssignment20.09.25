# import the necessary modules from Flask
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# create an instance of the Flask application
app = Flask(__name__)

# Configuration for PostgreSQL
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:tyju@localhost:5432/portfolio_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# ------------------------
# MODELS
# ------------------------
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    technologies = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Project {self.title}>'

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))
    
    def __repr__(self):
        return f'<Skill {self.name}>'

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ContactMessage from {self.name}>'


# ------------------------
# ROUTES
# ------------------------
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/projects')
def projects():
    projects = Project.query.all()
    return render_template('projects.html', projects=projects)

@app.route('/skills')
def skills():
    skills = Skill.query.all()
    return render_template('skills.html', skills=skills)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message_text = request.form['message']
        
        new_message = ContactMessage(name=name, email=email, message=message_text)
        try:
            db.session.add(new_message)
            db.session.commit()
            print(f"Wiadomość zapisana w bazie od {name} ({email})")
            return render_template('contact.html', submitted=True, name=name)
        except Exception as e:
            db.session.rollback()
            print(f"Błąd przy zapisie: {e}")
            return render_template('contact.html', submitted=False, error=True)
    
    return render_template('contact.html', submitted=False)


# ------------------------
# CRUD dla Project
# ------------------------
@app.route('/projects/new', methods=['GET', 'POST'])
def new_project():
    """Create - dodawanie nowego projektu"""
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        technologies = request.form['technologies']

        new_project = Project(title=title, description=description, technologies=technologies)
        db.session.add(new_project)
        db.session.commit()
        flash(f"Projekt '{title}' został dodany ✅", "success")
        return redirect(url_for('projects'))

    return render_template('new_project.html')



@app.route('/projects/edit/<int:id>', methods=['GET', 'POST'])
def edit_project(id):
    """Update - edycja projektu"""
    project = Project.query.get_or_404(id)

    if request.method == 'POST':
        project.title = request.form['title']
        project.description = request.form['description']
        project.technologies = request.form['technologies']
        db.session.commit()

        flash(f"Projekt '{project.title}' updated", "info" )
        return redirect(url_for('projects'))

    return render_template('edit_project.html', project=project)

@app.route('/projects/delete/<int:id>', methods=['POST'])
def delete_project(id):
    """Delete - usuwanie projektu"""
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()

    flash(f"Project '{project.title}' removed", "error")
    return redirect(url_for('projects'))


# ------------------------
# INIT DB
# ------------------------
def init_db():
    """Initialize database with sample data"""
    db.create_all()
    
    if Project.query.first() is None:
        projects_data = [
            {
                'title': 'Portfolio web',
                'description': 'created using Flask, HTML, CSS and JS.',
                'technologies': 'Flask, HTML, CSS, JavaScript, PostgreSQL'
            },
            {
                'title': 'Game, "Guess the name"',
                'description': 'A simple Python game using loops and conditionals.',
                'technologies': 'Python'
            },
            {
                'title': 'To-Do App',
                'description': '(planned) task management application with database.',
                'technologies': 'Python, Flask, PostgreSQL'
            }
        ]
        
        for project_data in projects_data:
            project = Project(**project_data)
            db.session.add(project)
        
        skills_data = [
            {'name': 'HTML, CSS, Bootstrap', 'category': 'Frontend'},
            {'name': 'JavaScript (basics)', 'category': 'Frontend'},
            {'name': 'Python - Flask, Databases structure, Logic', 'category': 'Backend'},
            {'name': 'Git & GitHub', 'category': 'Tools'},
            {'name': 'Terminal support, VS Code', 'category': 'Tools'}
        ]
        
        for skill_data in skills_data:
            skill = Skill(**skill_data)
            db.session.add(skill)
        
        db.session.commit()
        print("Database initialized with sample data!")


# ------------------------
# RUN APP
# ------------------------
if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True, port=5001)


# Portfolio Flask and Database App created by Sebastian Kajda (UCD Assignment - September 2025)
