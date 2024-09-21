from flask import Flask, render_template, redirect, url_for, flash, session, request
from flask_login import login_user, logout_user, current_user, login_required
from urllib.parse import urlparse as url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, UpdateProfileForm, ChangePasswordForm, RegistrationCodeForm, RegisterSchool
from app.models import User, School, Task, Story, Topic
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import uuid
import random, string
from datetime import datetime


@app.route('/')
def home():
    if current_user.is_authenticated:
        email = current_user.Email if current_user.Email else "No email found"
        first_name = current_user.FirstName if current_user.FirstName else "No first name found"
        flash(f"Sie sind bereits eingeloggt als {first_name} mit der E-Mail-Adresse {email}!") 
        return render_template('home.html') 
    else:
        #Not logged in. Shows the landing page
        return render_template('index.html')
    
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))  
    # Login Form
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data  
        password = form.password.data
        remember = form.remember.data
        # Password check
        user = User.query.filter_by(Email=email).first()  
        if user is None or not check_password_hash(user.Password, password):
            flash("Login fehlgeschlagen, bitte überprüfen Sie Ihre Anmeldedaten")
            return redirect(url_for('login'))
        # Login OK
        login_user(user, remember=remember)
        flash(f"Login erfolgreich! Willkommen, {user.FirstName}! Ihre E-Mail-Adresse ist {user.Email}.") 
        # Page navigation
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')  
        return redirect(next_page)
    # Login (via get)
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(Email=form.email.data).first()  
        if user:
            flash('Email already exists.', 'error')
            return redirect(url_for('register'))
        school = School.query.filter_by(registration_code=form.registration_code.data).first()
        if not school:
            flash('Invalid registration code.', 'error')
            return redirect(url_for('register'))
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(
            email=form.email.data, 
            password=hashed_password, 
            first_name=form.first_name.data, 
            last_name=form.last_name.data, 
            username=form.username.data, 
            language=form.language.data,
            is_admin=form.is_admin.data,
            school_id=school.idSchool  
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/geschichten')
@login_required
def geschichten():
    stories = Story.query.all()
    return render_template('geschichten.html', geschichten=geschichten)

@app.route('/geschichte/<int:story_id>')
def show_story_tasks(story_id):
    story = Story.query.get(story_id)
    tasks = Task.query.filter_by(story_id=story.idStory).all()
    return render_template('geschichte.html', story=story, tasks=tasks)

'''
@app.route('/create-test-data-and-task')
def create_test_data_and_task():
    # TestStories
    geschichte1 = TopicsGeschichten(Name='Testgeschichte 1', Description='Dies ist die Beschreibung für Testgeschichte 1', Enabled=True, CreatedAt=datetime.utcnow())
    geschichte2 = TopicsGeschichten(Name='Testgeschichte 2', Description='Dies ist die Beschreibung für Testgeschichte 2', Enabled=True, CreatedAt=datetime.utcnow())


    db.session.add(geschichte1)
    db.session.add(geschichte2)
    db.session.commit() 

    # Test Tasks
    task = Tasks(Name='Testaufgabe 1', Description='Dies ist die Beschreibung für Testaufgabe', IdTopic=geschichte1.IdTopic, CreatedAt=datetime.utcnow(), Enabled=True)
    task2 = Tasks(Name='Testaufgabe 2', Description='Dies ist die Beschreibung für Testaufgabe', IdTopic=geschichte2.IdTopic, CreatedAt=datetime.utcnow(), Enabled=True)

    db.session.add(task)
    db.session.add(task2)

    db.session.commit()

    return "Testdaten und Testaufgabe erfolgreich erstellt!"
'''

@app.route('/profil', methods=['GET'])
@login_required
def profil():
    return render_template('profile.html', title='Account')

@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.old_password.data):
            current_user.Password = generate_password_hash(form.new_password.data)
            db.session.commit()
            flash('Passwort wurde geändert', 'success')
            return redirect(url_for('profil'))
        else:
            flash('Incorrect old password.', 'error')
    return render_template('change_password.html', title='Passwort ändern', form=form)

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if not current_user.IsAdmin:
        return "You are not an administrator."
    
    form = RegisterSchool()
    # Generate an unique code
    def generate_code(length=8):
        letters_and_digits = string.ascii_letters + string.digits
        result_str = ''.join(random.choice(letters_and_digits) for i in range(length))
        return result_str

    if 'generate_code' in request.form:
        code = generate_code()
        flash(f"Generated code: {code}", 'info')
    elif form.validate_on_submit():
        code = generate_code()

        # Create a new School object
        school = School(
            name=form.school_name.data,
            teacher_name=form.teacher_name.data,
            teacher_email=form.teacher_email.data,
            address=form.address.data,
            num_students=form.num_students.data,
            registration_code=code,
            CreatedAt=datetime.utcnow(),
            UpdatedAt=datetime.utcnow()
        )
        
        db.session.add(school)
        db.session.commit()
        
        flash(f"Registration code for {form.school_name.data} created: {code}", 'success')
        
    return render_template('admin.html', title='Admin', form=form)


 #Test Generation of Stories and Tasks   
@app.route('/generate_stories_and_tasks')
def generate_stories_and_tasks():
    # Create Topics
    topic1 = Topic(name='Topic 1', type='Type 1', usage=0, difficulty='Easy', description='Description 1')
    topic2 = Topic(name='Topic 2', type='Type 2', usage=0, difficulty='Medium', description='Description 2')

    db.session.add(topic1)
    db.session.add(topic2)
    db.session.commit()

    # Create Tasks
    task1 = Task(name='Task 1', description='Description 1', value=10, task_type='Type 1', connection_info='Connection 1', download_info='Download 1', solution='Solution 1', possible_answers='Answers 1', hints='Hints 1', status='Status 1', avd='AVD 1', comment='Comment 1', story_id=1)
    task2 = Task(name='Task 2', description='Description 2', value=20, task_type='Type 2', connection_info='Connection 2', download_info='Download 2', solution='Solution 2', possible_answers='Answers 2', hints='Hints 2', status='Status 2', avd='AVD 2', comment='Comment 2', story_id=2)

    db.session.add(task1)
    db.session.add(task2)
    db.session.commit()

    # Associate Tasks with Topics
    topic1.tasks.append(task1)
    topic2.tasks.append(task2)

    db.session.commit()

    return "Stories and tasks generated successfully!"