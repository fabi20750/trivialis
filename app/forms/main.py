from flask_babel import _
from flask_security.forms import RegisterForm
from wtforms import SelectField, SubmitField

#Form for Setup
class SetupForm(RegisterForm):
  submit = SubmitField(_('Submit'))
  adminLanguage = SelectField(_('Select Your Language'), coerce=int)
  websiteLanguage = SelectField(_('Select Website Language'), coerce=int)