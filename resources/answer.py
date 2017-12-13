# -*- coding: utf-8 -*-
from flask_restful import Resource, Api, reqparse
from flask_jwt import jwt_required
from models.answer import AnswerModel
from datetime import datetime
import json

class Answer(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('answerpaper_id', type=int)
    parser.add_argument('question_id', type=int)
    parser.add_argument('answer_value', type=unicode)

    @jwt_required()
    def get(self, _id):
        answer = AnswerModel.get_by_id(_id)
        if answer:
            return {'Data': answer.json(), 'TotalRows': 1, 'Status': 1}
        return {'msg': 'Không có câu trả lời', 'Status' :0}

    @jwt_required()
    def put(self, _id):
        data = Answer.parser.parse_args()
        answer = AnswerModel.get_by_id(_id)
        if answer:
            answer.answerpaper_id = data['answerpaper_id']
            answer.question_id = data['question_id']
            answer.answer_value = data['answer_value']

            try:
                answer.save_to_db()
            except:
                return {'msg': ' Có lỗi xảy ra', 'Status': 0}
            return {'msg': 'Cập nhật câu trả lời thành công', 'Status': 1}
    @jwt_required()
    def delete(self, _id):
        answer = AnswerModel.get_by_id(_id)
        if answer:
            answer.delete_from_db()
        return {'msg': 'Xóa thành công câu trả lời', 'Status': 0}

class AnswerList(Resource):
    @jwt_required()
    def post(self):
        data = Answer.parser.parse_args()
        answer = AnswerModel(**data)
        try:
            answer.save_to_db()
        except:
            return {'msg': ' Có lỗi xảy ra', 'Status': 0}
        return {'msg': 'Thêm mới câu trả lời thành công', 'Status': 1}

class AnswerByQuestion(Resource):
    @jwt_required()
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('question_id', type=int, location='args', required=False)
        args = parser.parse_args(strict=True)
        question_id = args.get('question_id')
        lstAnswer = AnswerModel.get_by_question(question_id)
        if lstAnswer:
            return {'Data': lstAnswer , 'TotalRows': len(lstAnswer), 'Status': 1}
        return {'msg': 'Không có lựa chọn', 'Status': 0}

class CountAnswerByQuestion(Resource):
    @jwt_required()
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('question_id', type=int, location='args', required=False)
        args = parser.parse_args(strict=True)
        question_id = args.get('question_id')
        lstAnswer = AnswerModel.get_count_answer_by_question(question_id)
        if lstAnswer:
            return {'Data': lstAnswer , 'TotalRows': len(lstAnswer), 'Status': 1}
        return {'msg': 'Không có lựa chọn', 'Status': 0}

class AnswerByPaper(Resource):
    @jwt_required()
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('answerpaper_id', type=int, location='args', required=False)
        args = parser.parse_args(strict=True)
        answerpaper_id = args.get('answerpaper_id')
        lstAnswer = AnswerModel.get_by_ansp(answerpaper_id)
        if lstAnswer:
            return {'Data': [answer.json() for answer in lstAnswer], 'TotalRows': len(lstAnswer), 'Status': 1}
        return {'msg': 'Không có lựa chọn', 'Status': 0}