from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired, Email

#Form for Registering School
class RegisterSchoolForm(FlaskForm):
    school_name = StringField('School Name', validators=[DataRequired()])
    teacher_name = StringField('Teacher Name', validators=[DataRequired()])
    teacher_email = StringField('Teacher Email', validators=[DataRequired(), Email()])
    address = StringField('School Address')
    num_students = IntegerField('Number of Students')
    registration_code = StringField('Registration Code', validators=[DataRequired()])
    submit = SubmitField('Generate Code')

#Form for Registration Code
class RegistrationCodeForm(FlaskForm):
    registration_code = StringField('Registration Code', validators=[DataRequired()])
    submit = SubmitField('Submit')