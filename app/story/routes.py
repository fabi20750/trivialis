from flask import render_template, redirect, url_for, flash, request, current_app, jsonify
from flask_security import auth_required, current_user, roles_accepted
from app.story import bp
from app.models import Story, Task, Answer, UserAnswer, Hint, Resource, ReadQuestion, User
from app import db
from sqlalchemy.orm import joinedload

@bp.route('/')
@auth_required()
def stories():
    stories = Story.query.filter_by(is_active=True).all()
    return render_template('story/geschichten.html', stories=stories)

@bp.route('/<int:story_id>')
@auth_required()
def story(story_id):
    story = Story.query.filter_by(id=story_id, is_active=True).first_or_404()
    tasks = Task.query.filter_by(storyId=story.id).order_by(Task.sort).all()
    
    current_app.logger.info(f"Story: {story.name}, Number of tasks: {len(tasks)}")
    
    for task in tasks:
        answer_count = task.answers.count()
        current_app.logger.info(f"Task: {task.name}, Type: {task.type}, Number of answers: {answer_count}")
        for answer in task.answers:
            current_app.logger.info(f"  Answer: {answer.text}, Correct: {answer.is_correct}")
    
    return render_template('story/geschichte.html', story=story, tasks=tasks)

@bp.route('/<int:story_id>/task/<int:task_id>/answer', methods=['POST'])
@auth_required()
def answer_question(story_id, task_id):
    task = Task.query.get_or_404(task_id)
    points_earned = 0

    if task.type == 'multiple_choice':
        answer_id = request.form.get('answer')
        if answer_id:
            answer = Answer.query.get(answer_id)
            user_answer = UserAnswer(user_id=current_user.id, task_id=task.id, answer_id=answer.id)
            
            if answer.is_correct:
                points_earned = task.points  
                user_answer.points_earned = points_earned
                flash(f'Richtige Antwort! Sie haben {points_earned} Punkte verdient.', 'success')
            else:
                flash('Leider falsch. Versuchen Sie es nochmal!', 'error')
            
            db.session.add(user_answer)
        else:
            flash('Bitte wählen Sie eine Antwort aus.', 'error')
    
    elif task.type == 'read':
        
        points_earned = task.points  
        user_answer = UserAnswer(user_id=current_user.id, task_id=task.id, points_earned=points_earned)
        
        db.session.add(user_answer)
        
        flash(f'Sie haben {points_earned} Punkte für das Lesen verdient.', 'success')

    if points_earned > 0:
        current_user.total_points = (current_user.total_points or 0) + points_earned
    
    db.session.commit()

    return redirect(url_for('story.story', story_id=story_id))
