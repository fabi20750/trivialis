from .main import Language
from .profile import Profile
from .story import School, Story, Task, Answer, Resource, Hint, Tag, UserAnswer, ReadQuestion
from .security import Role, User

# Force SQLAlchemy to configure all models
from app import db
db.configure_mappers()