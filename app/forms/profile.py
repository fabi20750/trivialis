from flask_babel import _
from flask_wtf import FlaskForm
from wtforms import EmailField, SelectField, StringField, SubmitField
from wtforms.validators import Email, Length, Optional

class EditProfileForm(FlaskForm):
  firstName = StringField(_('First Name'), validators=[Length(max=255)]) # Max length of db-column
  lastName = StringField(_('Last Name'), validators=[Length(max=255)]) # Max length of db-column
  email = EmailField(_('Email'), validators=[Optional(), Email()])
  languageId = SelectField(_('Language'), coerce=int)
  submit = SubmitField(_('Update'))