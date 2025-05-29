from flask_restx import Namespace, Resource

api = Namespace('health', description='Health related operations')

@api.route('/')
class Health(Resource):
    def get(self):
        return {"message": "Health endpoint working!"}
