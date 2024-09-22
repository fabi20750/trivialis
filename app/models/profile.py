from sqlalchemy import event

from app import db
from .main import Language
from .security import User

#Model for Profile
class Profile(db.Model):
  __tablename__ = 'profile'
  id = db.Column(db.Integer, primary_key=True)
  userId = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
  languageId = db.Column(db.Integer, db.ForeignKey('language.id', ondelete='CASCADE'))
  firstName = db.Column(db.String(255), nullable=True)
  lastName = db.Column(db.String(255), nullable=True)
  about = db.Column(db.Text, nullable=True)

  def __repr__(self):
    return '<Profile {}>'.format(self.firstName, ' ', self.lastName)

# create profile
def create_profile_for_user(mapper, connection, user):
  connection.execute(Profile.__table__.insert().values(
    userId=user.id,
    languageId=Language.query.filter_by(isDefault=True).first().id
  ))
event.listen(User, 'after_insert', create_profile_for_user)