from flask_security.models import fsqla_v3 as fsqla
from app import db

# Required for FsModels class in fsqla to know about Flask SQL-Alchemy db object
fsqla.FsModels.set_db_info(db)

#Model for User
class User(fsqla.FsUserMixin, db.Model):
  __tablename__ = 'user'
  total_points = db.Column(db.Integer, default=0)
  
  def __repr__(self):
    return '<User {}>'.format(self.username)

#Model for Role
class Role(fsqla.FsRoleMixin, db.Model):
  __tablename__ = 'role'


  def __repr__(self):
    return '<Role {}>'.format(self.name)
