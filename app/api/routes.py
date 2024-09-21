from flask import jsonify
from flask_restful import Resource
from app.models import Story, Task, User, UserAnswer
from app.api import api, bp  # Ensure both api and bp are imported
from app import db  # Import db from your main app module

class StoryListResource(Resource):
    def get(self):
        stories = Story.query.filter_by(is_active=True).all()
        return jsonify([{
            'id': story.id,
            'name': story.name,
            'description': story.description
        } for story in stories])

class StoryDetailResource(Resource):
    def get(self, story_id):
        story = Story.query.filter_by(id=story_id, is_active=True).first_or_404()
        tasks = Task.query.filter_by(storyId=story.id).order_by(Task.sort).all()
        return jsonify({
            'id': story.id,
            'name': story.name,
            'description': story.description,
            'tasks': [{
                'id': task.id,
                'name': task.name,
                'type': task.type,
                'points': task.points
            } for task in tasks]
        })
# Add resources to the api object directly
api.add_resource(StoryListResource, '/stories')
api.add_resource(StoryDetailResource, '/stories/<int:story_id>')

@bp.route('/healthcheck')
def healthcheck():
    return jsonify({"message": "API is working"})