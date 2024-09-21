from flask import current_app, Flask, request, session

# Flask Plugins
from flask_babel import Babel
from flask_migrate import Migrate
from flask_security import current_user, Security, SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy

babel = Babel()
db = SQLAlchemy()
migrate = Migrate()

# get locale from browser
def get_locale():
  from app.models import Language, Profile
  #language = request.accept_languages.best_match(current_app.config['LANGUAGES'])
  language = 'en'
  if Language.query.filter_by(isDefault=True).first():
    language = Language.query.filter_by(isDefault=True).first().isoCode
  if current_user:
    profile = Profile.query.filter_by(userId=current_user.id).first()
    language = Language.query.filter_by(id=profile.languageId).first().isoCode
  if request.args.get('lang') and Language.query.filter_by(isoCode=request.args.get('lang')):
    session['userLanguage'] = request.args.get('lang')
  return session.get('userLanguage', language)

def create_app(config_class):
  # Flask Initialisierung
  app = Flask(__name__)

  # Get config from class
  app.config.from_object(config_class)

  #############################################################
  # Initialize Flask extensions here                          #
  #############################################################
  # Localization: Flask-Babel
  babel.init_app(app, locale_selector=get_locale)
  # Database: Flask-SQLAlchemy
  db.init_app(app)
  migrate.init_app(app, db)
  # User authentication: Flask-Security
  from app import models
  user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
  app.security = Security(app, user_datastore)

  #############################################################
  # Register blueprints here                                  #
  #############################################################

  from app.admin import bp as admin_bp
  app.register_blueprint(admin_bp, url_prefix='/admin')

  from app.api import bp as api_bp
  app.register_blueprint(api_bp, url_prefix='/api') 

  from app.main import bp as main_bp
  app.register_blueprint(main_bp)

  from app.story import bp as story_bp
  app.register_blueprint(story_bp, url_prefix='/stories')
  
  from app.profile import bp as profile_bp
  app.register_blueprint(profile_bp, url_prefix='/profile')

 

  #############################################################
  # Register custom context processors                        #
  #############################################################
  # Make languages available in jinja templates
  @app.context_processor
  def language_processor():
    return dict(languages=models.Language.query.all())

  return app

from app import models
