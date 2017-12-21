# -*- coding: utf-8 -*-
from flask_restful import Resource, Api, reqparse
from flask_jwt import jwt_required
from models.choice import ChoiceModel
from datetime import datetime
import json

class Choice(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('question_id', type=int)
    parser.add_argument('choice_ordered', type=int)
    parser.add_argument('choice_value', type=unicode)
    parser.add_argument('choice_content', type=unicode)
    parser.add_argument('last_edited',type=lambda x: datetime.strptime(x, '%Y-%m-%d'))


    @jwt_required()
    def get(self, _id):
        choice = ChoiceModel.get_by_id(_id)
        if choice:
            return {'Data': choice.json(), 'TotalRows':1, 'Status':1}
        return {'msg': 'Không có lựa chọn', 'Status':0}

    @jwt_required()
    def put(self, _id):
        data = Choice.parser.parse_args()
        choice = ChoiceModel.get_by_id(_id)
        if choice:
            choice.question_id = data['question_id']
            choice.choice_ordered = data['choice_ordered']
            choice.choice_value = data['choice_value']
            choice.choice_content = data['choice_content']
            choice.last_edited = data['last_edited']
            try:
                choice.save_to_db()
            except:
                return {'msg':' Có lỗi xả ra', 'Status': 0}
            return  {'msg': 'Cập nhật lựa chọn thành công', 'Status': 1}

    @jwt_required()
    def delete(self, _id):
        choice = ChoiceModel.get_by_id(_id)
        if choice:
            choice.delete_from_db()
        return {'msg': 'Xoá lựa chọn thành công', 'Status': 1}

class ChoiceList(Resource):
    @jwt_required()
    def post(self):
        data = Choice.parser.parse_args()
        choice = ChoiceModel(**data)
        try:
            choice.save_to_db()
        except:
            return {'msg': ' Có lỗi xả ra', 'Status': 0}
        return {'msg': 'Thêm mới lựa chọn thành công', 'Status': 1}

class ChoiceByQuestion(Resource):
    @jwt_required()
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('question_id', type=int, location='args', required=False)
        args = parser.parse_args(strict=True)
        question_id = args.get('question_id')
        lstChoice = ChoiceModel.get_by_question(question_id)
        if lstChoice:
            return {'Data': [choice.json() for choice in lstChoice], 'TotalRows': len(lstChoice), 'Status':1}
        return {'msg': 'Không có lựa chọn', 'Status': 0}

    @jwt_required()
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('question_id', type=int, location='args', required=False)
        args = parser.parse_args(strict=True)
        question_id = args.get('question_id')
        lstChoice = ChoiceModel.get_by_question(question_id)
        if lstChoice:
            for choice in lstChoice:
                choice.delete_from_db()
        return {'msg': 'Xoá lựa chọn thành công', 'Status': 1}