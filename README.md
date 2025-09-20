Portfolio App – Flask + PostgreSQL

Project created as part of my final exam (UCD, September 2025).
The app showcases my portfolio, with CRUD features for projects.

Features: <br>
Home (Home)<br>
Project List (Projects)<br>
Adding Projects (Create)<br>
Editing Projects (Update)<br>
Deleting Projects (Delete)<br>
Skills List (Read)<br>
About Me (About)<br>
Contact Form (Contact) – messages saved in the database <br>
Flash messages informing about success, errors, and updates <br>
Hemburger Menu for responsive navigate <br>


Technologies: <br>
Python 3 <br>
JavaScript <br>
Flask <br>
SQLAlchemy <br>
PostgreSQL <br>
HTML, CSS <br>
GitHub <br>

Local startup instructions: <br>
Clone the repository: <br>
bash <br>
git clone https://github.com/sebastian-elbacho/DBAssignment20.09.25 <br>
cd DBAssignment20.09.25 <br>


Deployment on Render <br>

This app is live and hosted on Render.com <br>

Live demo here => https://dbassignment20-09-25.onrender.com <br>


DEPLOYMENT STEPS: <br>
Create an account on Render.com<br>
Create a Web Service from this GitHub repo<br>
Add a postgrSQL Database (in Render also) <br>
Set environment variables: <br>
   DATABASE_URL => use internal Render DB URL <br>
   SECRET_KEY => any string <br>
Set Start Command in Render <br>




Create a virtual environment: <br>
python3 -m venv venv <br>
source venv/bin/activate   # Mac/Linux <br>
venv\Scripts\activate      # Windows <br>

Install dependencies: <br>
bash <br>
pip install -r requirements.txt <br>

Run the application: <br>
bash <br>
python3 app.py <br>

Open in browser: <br>
http://127.0.0.1:5000 <br>


Created by Sebastian Kajda, Assignement for UCD - September 2025









