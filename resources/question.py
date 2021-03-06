# -*- coding: utf-8 -*-
from flask_restful import Resource, Api, reqparse
from flask_jwt import jwt_required
from models.question import QuestionModel
from datetime import datetime
from models.choice import ChoiceModel
import json

class Question(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('page_id', type=int, required=True)
    parser.add_argument('questiontype_id', type=int, required=True)
    parser.add_argument('content', type=unicode)
    parser.add_argument('question_ordered', type=int)
    parser.add_argument('question_img', type=str)
    parser.add_argument('is_required', type=bool)
    parser.add_argument('question_status', type=bool)
    parser.add_argument('last_edited', type=lambda x: datetime.strptime(x, '%Y-%m-%d'))


    @jwt_required()
    def get(self,_id):
        question = QuestionModel.get_by_id(_id)
        if question:
            return {'Data': question.json(), 'TotalRows':1, 'Status':1}
        return {'msg': 'Không có câu hỏi', 'Status':0}

    @jwt_required()
    def put(self, _id):
        data = Question.parser.parse_args()
        question = QuestionModel.get_by_id(_id)
        if question:
            question.page_id = data['page_id']
            question.questiontype_id =data['questiontype_id']
            question.content = data['content']
            question.question_ordred = int(data['question_ordered'])
            question.question_img = data['question_img']
            question.is_required = data['is_required']
            question.question_status = data['question_status']
            question.last_edited = data['last_edited']
            try:
                question.save_to_db()
            except:
                return {'msg': 'Đã có lỗi xảy ra', 'Status': 0}
            return {'msg': 'Sửa câu hỏi thành công thành công', 'Status': 1}

    @jwt_required()
    def delete(self, _id):
        question = QuestionModel.get_by_id(_id)

        if question:
            question.delete_from_db()

        return {'msg': 'Câu hỏi đã xóa', 'Status': 1}

class QuestionList(Resource):
    @jwt_required()
    def post(self):
        data = Question.parser.parse_args()
        question = QuestionModel(**data)
        print question.json()
        try:
            newid = question.save_to_db()
        except:
            return {'msg': 'Đã có lỗi xảy ra', 'Status': 0}
        return {'msg': 'Thêm mới câu hỏi thành công thành công', 'Status': 1, 'insertedId': newid}

class QuestionByPage(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page_id', type=str, location='args', required=False)
        args = parser.parse_args(strict=False)
        page_id = args.get('page_id')
        lstQuestion = QuestionModel.get_by_page(page_id)
        result = []
        if lstQuestion:
            for question in lstQuestion:
                lstChoice = []
                print question.questiontype_code
                if question.questiontype_code not in ['PR','DT','TM']:
                    lstChoice = ChoiceModel.get_by_question(question.question_id)
                    print len(lstChoice)
                elif question.questiontype_code == 'SR':
                    for c in lstChoice:
                        c.choice_content = json.loads(str(c.choice_content))
                else:
                    lstChoice = []
                result.append({'question_id': question.question_id, 'questiontype_id': question.questiontype_id,
                'page_id': question.page_id, 'content': question.content, 'question_ordered': question.question_ordred,
                'question_img': question.question_img, 'is_required': question.is_required,
                'status': question.question_status, 'last_edited': question.last_edited.isoformat(), 'questiontype_code': question.questiontype_code,
                'questiontype_name': question.questiontype_name, 'choices' : [choice.json() for choice in lstChoice]})
            return {'Data': result, 'TotalRows': len(lstQuestion), 'Status': 1, 'Page_id' : page_id}
        return {'msg': 'Không tìm thấy câu hỏi', 'Status': 0, 'Page_id' : page_id}

class QuestionOrder(Resource):
    @jwt_required()
    def get(self):
        parser  = reqparse.RequestParser()
        parser.add_argument('page_id', type=str, location='args', required=True)
        args = parser.parse_args(strict=False)
        page_id = args.get('page_id')
        data = QuestionModel.get_max_ordered(page_id)
        print data
        if data:
            return {'Data': data, 'Status': 1}
        else:
            return {'Data': 0, 'Status': 1}
class QuestionByOrder(Resource):
    @jwt_required()
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page_id', type=str, location='args', required=True)
        parser.add_argument('position_from', type=int, location='args', required=True)
        parser.add_argument('position_to', type=int, location='args', required=True)
        args = parser.parse_args(strict=False)
        page_id = args.get('page_id')
        position_from = args.get('position_from')
        position_to = args.get('position_to')
        data = QuestionModel.get_question_from_to_position(page_id,position_from,position_to)
        if data:
            return {'Data': [q.json() for q in data], 'TotalRows' : len(data),'Status' : 1}
        return {'msg': 'Không có data', 'Status': 0}


