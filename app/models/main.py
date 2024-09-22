from app import db

#Model for Language
class Language(db.Model):
  __tablename__ = 'language'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(64))
  isoCode = db.Column(db.String(6))
  icon = db.Column(db.String(16))
  isDefault = db.Column(db.Boolean, default=False)
  description = db.Column(db.Text)

  def __repr__(self):
    return '<Language {}'.format(self.name)

#Model for Tenant
class Tenant(db.Model):
  __tablename__ = 'tenant'
  id = db.Column(db.Integer, primary_key=True)
  languageId = db.Column(db.Integer, db.ForeignKey('language.id', ondelete='CASCADE'))
  name = db.Column(db.String(150))
  
  def __repr__(self):
    return '<Tenant {}>'.format(self.name)