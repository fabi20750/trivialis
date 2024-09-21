from flask import flash, redirect, render_template, request, url_for
from flask_babel import _
from flask_security import auth_required, current_user

from app import db
from app.forms import EditProfileForm
from app.models import Language, Profile
from app.profile import bp

@bp.route('/')
@auth_required()
def profile():
  profile = db.first_or_404(Profile.query.filter_by(userId=current_user.id))
  language = db.first_or_404(Language.query.filter_by(id=profile.languageId))
  points = current_user.total_points
  return render_template('profile/index.html', profile=profile, language=language, points=points)

@bp.route('/edit/', methods=['GET', 'POST'])
@auth_required()
def edit():
  profile = db.first_or_404(Profile.query.filter_by(userId=current_user.id))
  form = EditProfileForm(formdata=request.form, obj=profile, data={'email': current_user.email})
  form.languageId.choices = [(l.id, l.name) for l in Language.query.all()]
  if form.validate_on_submit():
    # POST
    if profile.userId != current_user.id:
      # Trying to change someone elses profile
      return redirect(url_for('profile.profile'))
    form.populate_obj(profile)
    current_user.email = form.email.data
    db.session.commit()
    flash(_('Profile successfully updated.'))
    return redirect(url_for('profile.profile'))
  return render_template('profile/edit.html', profile=profile, form=form)