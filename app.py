# import the necessary modules from Flask
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# create an instance of the Flask application
app = Flask(__name__)

# Configuration for PostgreSQL
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/portfolio_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:TWOJE_HASLO@localhost:5432/portfolio_db'

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Models
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

# Routes
@app.route('/')
def home():
    return render_template('home.html')

# Route to the projects section - now using database
@app.route('/projects')
def projects():
    projects = Project.query.all()
    return render_template('projects.html', projects=projects)

# route to the skills section - now using database
@app.route('/skills')
def skills():
    skills = Skill.query.all()
    return render_template('skills.html', skills=skills)

# route to the about section
@app.route('/about')
def about():
    return render_template('about.html')

# route to the contact form (GET – shows the form, POST – receives data).
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message_text = request.form['message']
        
        # Save to database instead of just printing
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
    
    # For the GET method we return an empty form
    return render_template('contact.html', submitted=False)

# Function to create tables and add sample data
def init_db():
    """Initialize database with sample data"""
    db.create_all()
    
    # Check if data already exists
    if Project.query.first() is None:
        # Add sample projects
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
        
        # Add sample skills
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

# We only run the application if the file is run directly
if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)

# Portfolio Flask App created by Sebastian Kajda (UCD Assignment - August 2025)