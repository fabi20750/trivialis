from flask import render_template, redirect, url_for, flash, request, current_app
from flask_security import auth_required, current_user
from app import db
from app.admin import bp
from app.models import Story, Task, Answer, Hint, ReadQuestion, User, Role  # Ensure User and Role are imported
from sqlalchemy.orm import joinedload, subqueryload  # Import subqueryload

@bp.route('/', methods=['GET', 'POST'])
@auth_required()
def admin():
    if not current_user.has_role('Admin'):
        flash("You are not an administrator.", 'danger')
        return redirect(url_for('main.index'))

    stories = Story.query.all()  # Fetch all stories
    users = User.query.all()  # Fetch all users

    if request.method == 'POST':
        if 'toggle_story' in request.form:
            story_id = request.form.get('story_id')
            story = Story.query.get(story_id)
            if story:
                story.is_active = not story.is_active  # Toggle story active status
                db.session.commit()
                flash(f'Story "{story.name}" wurde {"aktiviert" if story.is_active else "deaktiviert"}.', 'success')
        elif 'edit_story' in request.form:
            story_id = request.form.get('story_id')
            return redirect(url_for('admin.edit_story', story_id=story_id))
        elif 'toggle_active' in request.form:
            user_id = request.form.get('user_id')
            user = User.query.get(user_id)
            if user:
                user.active = not user.active  # Toggle user active status
                db.session.commit()
                flash(f'User "{user.username}" wurde {"aktiviert" if user.active else "deaktiviert"}.', 'success')
        elif 'update_username' in request.form:
            user_id = request.form.get('user_id')
            new_username = request.form.get('new_username')
            user = User.query.get(user_id)
            if user:
                user.username = new_username  # Update username
                db.session.commit()
                flash(f'Username for user "{user.id}" has been updated to "{new_username}".', 'success')

    return render_template('admin/admin.html', stories=stories, users=users)  # Pass both stories and users to the template

@bp.route('/edit_story/<int:story_id>', methods=['GET', 'POST'])
@auth_required()
def edit_story(story_id):
    story = Story.query.get_or_404(story_id)
    tasks = Task.query.filter_by(storyId=story.id).order_by(Task.sort).all()

    # Fetch related questions for each task (if needed)
    for task in tasks:
        task.read_questions = ReadQuestion.query.filter_by(task_id=task.id).all()  # Fetch related questions

    if request.method == 'POST':
        # Update story fields based on the form input
        story.name = request.form.get('story_name')
        story.description = request.form.get('story_description')
        db.session.commit()
        flash('Änderungen wurden gespeichert.', 'success')
        return redirect(url_for('admin.admin'))

    return render_template('admin/edit_story.html', story=story, tasks=tasks)





    
