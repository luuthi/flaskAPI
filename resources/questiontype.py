# -*- coding: utf-8 -*-
from flask_restful import Resource, Api, reqparse
from flask_jwt import jwt_required
from models.question_type import QuestionTypeModel

class QuestionType(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('questiontype_name', type=unicode)
    parser.add_argument('questiontype_code', type=str)
    parser.add_argument('questiontype_desc', type=unicode)
    parser.add_argument('questiontype_status', type = bool)

    @jwt_required()
    def get(self, _id):
        qt = QuestionTypeModel.get_by_id(_id)
        if qt:
            return {'Data': qt.json(), 'TotalRows': 1, 'Status': 1}
        return {'msg': 'Không tìm thấy loại câu hỏi'}

    def put(self, _id):
        data = QuestionType.parser.parse_args()
        qt = QuestionTypeModel.get_by_id(_id)
        if qt:
            qt.questiontype_name = data['questiontype_name']
            qt.questiontype_code = data['questiontype_code']
            qt.questiontype_desc = data['questiontype_desc']
            qt.questiontype_status = data['questiontype_status']

            try:
                qt.save_to_db()
            except:
                return {'msg': 'Đã có lỗi xảy ra', 'Status': 0}
            return {'msg': 'Cập nhật loại câu hỏi thành công thành công', 'Status': 1}

    @jwt_required()
    def delete(self, _id):
        question = QuestionTypeModel.get_by_id()

        if question:
            question.delete_from_db()

        return {'msg': 'Loại câu hỏi đã xóa', 'Status': 1}


class QuestionTypeList(Resource):

    @jwt_required()
    def post(self):
        data = QuestionType.parser.parse_args()
        qt = QuestionTypeModel(**data)
        try:
            qt.save_to_db()
        except:
            return {'msg': 'Đã có lỗi xảy ra', 'Status': 0}
        return {'msg': 'Thêm mới loại câu hỏi thành công thành công', 'Status': 1}

    @jwt_required()
    def get(self):
        data = QuestionTypeModel.get_all()
        if data:
            return {'Data': [qt.json() for qt in data], 'TotalRows': len(data), 'Status':1}
        return {'msg':' Không có loại câu hỏi', 'Status':0}