import random, string
from datetime import datetime
from flask import flash, redirect, render_template, request, url_for
from flask_babel import _
from flask_security import auth_required, current_user

from app import db
from app.forms import RegisterSchoolForm, SetupForm
from app.main import bp
from app.models import Language, School, User, Story  # Stellen Sie sicher, dass das Story-Modell importiert wird
from .setup import create_languages, create_roles, create_stories, create_tasks, create_users

#Standard Route for Users
@bp.route('/')
def index():
  # Redirect to setup page if no users are in database
  users = User.query.all()
  if not users:
    return redirect(url_for('main.setup'), code=307)
  return render_template('main/index.html')
  
#Route for Setup
@bp.route('/setup/', methods=['GET', 'POST'])
def setup():
  # Redirect to homepage if one or more users are already in the database
  users = User.query.all()
  if users:
    return redirect(url_for('main.index'))
  if not Language.query.all():
    # No languages are defined in database
    create_languages()
  form = SetupForm()
  choices = [(l.id, l.name) for l in Language.query.all()]
  form.adminLanguage.choices = choices
  form.websiteLanguage.choices = choices
  if form.validate_on_submit():
    # Set websites default language with selected language
    websiteLanguage = Language.query.filter_by(id=form.websiteLanguage.data).first()
    websiteLanguage.isDefault = True
    db.session.commit()
    # Create default roles and users from config
    create_roles()
    create_users(form.username.data, form.email.data, form.password.data, form.adminLanguage.data)
    create_stories()
    create_tasks()
    flash(_('Successfully setup website.'))
    return redirect(url_for('main.index'))
  return render_template('main/setup.html', form=form)
