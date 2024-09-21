from app import db
from datetime import datetime


taskTag = db.Table(
  'task_tag',
  db.Column('task_id', db.Integer, db.ForeignKey('task.id', ondelete='CASCADE')),
  db.Column('tag_id', db.Integer, db.ForeignKey('tag.id', ondelete='CASCADE'))
  )

# Used to allow teachers to enable or disable certain stories in their tenant
tenantStory = db.Table(
  'tenant_story',
  db.Column('tenant_id', db.Integer, db.ForeignKey('tenant.id', ondelete='CASCADE')),
  db.Column('story_id', db.Integer, db.ForeignKey('story.id', ondelete='CASCADE'))
)

# Used to build the story when one task is only available after one or more other tasks are answered
taskRequirement = db.Table(
  'task_requirement',
  db.Column('task_id', db.Integer, db.ForeignKey('task.id', ondelete='CASCADE')),
  db.Column('requirement_id', db.Integer, db.ForeignKey('task.id', ondelete='CASCADE'))
)

# Used to build the hint story when one hint is only available after one or more other hints are used
hintRequirement = db.Table(
  'hint_reuquirement',
  db.Column('hint_id', db.Integer, db.ForeignKey('hint.id', ondelete='CASCADE')),
  db.Column('requirement_id', db.Integer, db.ForeignKey('hint.id', ondelete='CASCADE'))
)


class School(db.Model):
  __tablename__ = 'school'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  registrationCode = db.Column(db.String(100), unique=True, nullable=False)
  teacherName = db.Column(db.String(100), nullable=False)
  teacherEmail = db.Column(db.String(100), nullable=False)
  address = db.Column(db.String(100), nullable=False)
  numStudents = db.Column(db.Integer, nullable=False)
  createdAt = db.Column(db.DateTime)
  updatedAt = db.Column(db.DateTime)

class Story(db.Model):
  __tablename__ = 'story'
  id = db.Column(db.Integer, primary_key=True)
  languageId = db.Column(db.Integer, db.ForeignKey('language.id', ondelete='CASCADE')) # TODO nk20240502: Verify if CASCADE is correct
  name = db.Column(db.String(150))
  description = db.Column(db.Text) # Short introduction to the story
  is_active = db.Column(db.Boolean, default=True)

  def __repr__(self):
    return '<Story {}>'.format(self.name)
  
class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    next = db.Column(db.Integer, db.ForeignKey('task.id', ondelete='CASCADE'))
    name = db.Column(db.String(150))
    description = db.Column(db.Text)
    task = db.Column(db.String(150))
    sort = db.Column(db.Integer)
    maxAttempts = db.Column(db.Integer)
    storyId = db.Column(db.Integer, db.ForeignKey('story.id', ondelete='CASCADE'))
    type = db.Column(db.String(50))
    points = db.Column(db.Integer)
    correct_text = db.Column(db.Text)
    read_text = db.Column(db.Text)
    read_questions = db.relationship('ReadQuestion', back_populates='task', lazy='dynamic')
    
    answers = db.relationship('Answer', back_populates='task', lazy='dynamic')
    hints = db.relationship('Hint', back_populates='task', lazy='dynamic')
    # Remove the resource relationship from here

    def __repr__(self):
        return '<Task {}>'.format(self.name)

class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id', ondelete='CASCADE'), nullable=False)
    text = db.Column(db.String(150))
    is_correct = db.Column(db.Boolean)
    sort_order = db.Column(db.Integer)

    task = db.relationship('Task', back_populates='answers')

    def __repr__(self):
        return '<Answer {}>'.format(self.text)
        
class UserAnswer(db.Model):
    __tablename__ = 'user_answer'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    task_id = db.Column(db.Integer, db.ForeignKey('task.id', ondelete='CASCADE'))
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'))
    text_answer = db.Column(db.Text, nullable=True)
    points_earned = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('user_answers', lazy='dynamic'))
    task = db.relationship('Task', backref=db.backref('user_answers', lazy='dynamic'))
    answer = db.relationship('Answer', backref=db.backref('user_answers', lazy='dynamic'))

    def __repr__(self):
        return '<UserAnswer {}>'.format(self.id)


    def __repr__(self):
        return '<UserAnswer {}>'.format(self.id)
  
class Resource(db.Model):
  __tablename__ = 'resource'
  id = db.Column(db.Integer, primary_key=True)
  task_id = db.Column(db.Integer, db.ForeignKey('task.id', ondelete='CASCADE'), nullable=False)
  name = db.Column(db.String(150))
  description = db.Column(db.Text)
  # TODO nk20240502: Extend with resource types: url, video, image, etc.

  task = db.relationship('Task', backref=db.backref('resource', uselist=False))

  def __repr__(self):
    return '<Resource {}>'.format(self.name)

class Hint(db.Model):
  __tablename__ = 'hint'
  id = db.Column(db.Integer, primary_key=True)
  task_id = db.Column(db.Integer, db.ForeignKey('task.id', ondelete='CASCADE'), nullable=False)
  hint = db.Column(db.Text)
  cost = db.Column(db.Integer) # Used for scoreboard points
  sort = db.Column(db.Integer)

  task = db.relationship('Task', back_populates='hints')

  def __repr__(self):
    return '<Hint {}>'.format(self.hint)

class Tag(db.Model):
  __tablename__ = 'tag'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(150))
  urlName = db.Column(db.String(150))

  def __repr__(self):
    return '<Tag {}>'.format(self.name)

class ReadQuestion(db.Model):
    __tablename__ = 'read_question'
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id', ondelete='CASCADE'))
    question = db.Column(db.Text)
    correct_answer = db.Column(db.Text)

    task = db.relationship('Task', back_populates='read_questions')

    def __repr__(self):
        return '<ReadQuestion {}>'.format(self.question)

  