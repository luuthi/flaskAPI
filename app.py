import os
import sys
from flask import Flask, request,send_from_directory
from flask_restful import Api,reqparse
from flask_jwt import JWT,jwt_required
from flask_cors import CORS
import json
import os
from werkzeug.utils import secure_filename

from security import authenticate, identity
from resources.register import UserRegister
from resources.user import User,UserByName
from resources.folder import Folder, FolderList, FolderByName, FolderByUsername
from resources.survey import Survey, SurveyByFolder, SurveyList, SurveyByUser, SurveyByName,SurveyMaxByUser
from resources.page import Page, PageBySurvey, PageList
from resources.questiontype import QuestionType, QuestionTypeList
from resources.question import Question, QuestionByPage, QuestionList, QuestionOrder,QuestionByOrder
from resources.answerpaper import AnswerPaper, AnswerPaperBySurvey,AnswerPaperList
from resources.choice import Choice, ChoiceByQuestion, ChoiceList
from resources.answer import Answer, AnswerByPaper, AnswerByQuestion, AnswerList, CountAnswerByQuestion

UPLOAD_FOLDER = 'D:\Flask-API\upload\image'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
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
api.add_resource(UserRegister, '/api/v1/ register', endpoint='register')
api.add_resource(UserByName, '/api/v1/user_by_name/<string:username>', endpoint='user_by_name')
api.add_resource(User,'/api/v1/user/<string:_id>', endpoint='user')

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

#question type
api.add_resource(QuestionType, '/api/v1/questiontype/<_id>', endpoint='questiontype')
api.add_resource(QuestionTypeList, '/api/v1/questiontypes', endpoint='questiontypes')

#page
api.add_resource(Page, '/api/v1/page/<_id>', endpoint='page')
api.add_resource(PageList, '/api/v1/pages', endpoint='pages')
api.add_resource(PageBySurvey, '/api/v1/page_survey', endpoint='page_survey')

#question
api.add_resource(Question, '/api/v1/question/<_id>', endpoint='question')
api.add_resource(QuestionList, '/api/v1/questions', endpoint='questions')
api.add_resource(QuestionByPage, '/api/v1/question_page', endpoint='question_page')
api.add_resource(QuestionOrder, '/api/v1/get_order_question_page', endpoint='question_order')
api.add_resource(QuestionByOrder, '/api/v1/get_question_from_to', endpoint='question_from_to')

#answer paper
api.add_resource(AnswerPaper, '/api/v1/answerpaper/<_id>', endpoint='answerpaper')
api.add_resource(AnswerPaperList, '/api/v1/answerpapers', endpoint='answerapers')
api.add_resource(AnswerPaperBySurvey, '/api/v1/answerpaper_survey', endpoint='answerpaper_survey')

#choice
api.add_resource(Choice, '/api/v1/choice/<_id>', endpoint='choice')
api.add_resource(ChoiceList, '/api/v1/choices', endpoint='choices')
api.add_resource(ChoiceByQuestion, '/api/v1/choice_question', endpoint='choice_question')
api.add_resource(ChoiceByQuestion, '/api/v1/delete_by_question', endpoint='delete_choice_question')

#answer
api.add_resource(Answer, '/api/v1/answer/<_id>', endpoint='answer')
api.add_resource(AnswerList, '/api/v1/answers', endpoint='answers')
api.add_resource(AnswerByQuestion, '/api/v1/answer_question', endpoint='answer_question')
api.add_resource(CountAnswerByQuestion, '/api/v1/count_answer_question', endpoint='count_answer_question')
api.add_resource(AnswerByPaper, '/api/v1/answer_paper', endpoint='answer_paper')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/api/v1/image-upload', methods=['POST','GET'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'files' not in request.files:
            return  {'msg' : 'Not found file', 'Status': 0}
        file = request.files['files']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return {'msg': 'Not found file', 'Status': 0}
        if file :
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                print os.path.join(app.config['UPLOAD_FOLDER'], filename)
                data = {'Data': os.path.join(app.config['UPLOAD_FOLDER'], filename), 'Status' : 1}
                return json.dumps(data)
            else:
                return {'msg': 'File denied!', 'Status': 0}
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
