import os
import sys
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from flask_cors import CORS

from security import authenticate, identity
from resources.register import UserRegister
from resources.user import User
from resources.folder import Folder, FolderList, FolderByName, FolderByUsername
from resources.survey import Survey, SurveyByFolder, SurveyList, SurveyByUser, SurveyByName,SurveyMaxByUser

app = Flask(__name__)
app.config['DEBUG'] = True
cors = CORS(app, resources={r"/*": {"origins": "*"}})

#sqlite:///data.db
#postgres://qpdggmnrmhrsim:7452f8111d18456b355d432280661f87eacc3c5236c8ca1f55be3b861bb55127@ec2-54-225-237-64.compute-1.amazonaws.com:5432/d4i7ve72ue4i15
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'thild'
api = Api(app)
jwt = JWT(app, authenticate, identity) #/auth

#add resources
#register, user
api.add_resource(UserRegister, '/api/v1/register', endpoint='register')
api.add_resource(User, '/api/v1/user_by_name/<string:username>')

#folder
api.add_resource(Folder, '/api/v1/folder/<_id>', endpoint='folder')
api.add_resource(FolderList, '/api/v1/folders', endpoint='folders')
api.add_resource(FolderByUsername, '/api/v1/folders_user', endpoint='folder_by_username')
# api.add_resource(FolderByUsername, '/api/v1/folders/username=<string:user_name>', endpoint='folder_by_username')
api.add_resource(FolderByName, '/api/v1/folders_name',  endpoint='folder_by_name')

#survey
api.add_resource(Survey, '/api/v1/survey/<_id>', endpoint='survey')
api.add_resource(SurveyList, '/api/v1/surveys', endpoint='surveys')
api.add_resource(SurveyByFolder, '/api/v1/surveys_folder', endpoint='survey_by_folder')
api.add_resource(SurveyByUser, '/api/v1/surveys_user', endpoint='survey_by_user')
api.add_resource(SurveyMaxByUser, '/api/v1/surveys_max', endpoint='survey_by_max')
api.add_resource(SurveyByName, '/api/v1/surveys_name', endpoint='survey_by_name')
if __name__ == '__main__':
    from db import db
    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    reload(sys)
    sys.setdefaultencoding('utf-8')
    app.run(port=5000)
