# -*- coding: utf-8 -*-
from flask_restful import Resource, Api, reqparse
from flask_jwt import jwt_required
from models.answerpaper import AnswerPaperModel as Model
from datetime import datetime
import json

class AnswerPaper(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('survey_id', type=int, required=True)
    parser.add_argument('created_date', type=lambda x: datetime.strptime(x, '%Y-%m-%d'))
    parser.add_argument('status', type=bool)

    @jwt_required()
    def get(self, _id):
        anwp = Model.get_by_id(_id)
        if anwp:
            return {'Data': anwp.json(), 'TotalRows': 1, 'Status':1}
        return {'msg': 'Không có bảng trả lời', 'Status':0}

    @jwt_required()
    def put(self, _id):
        data = AnswerPaper.parser.parse_args()
        ansp = Model.get_by_id(_id)
        if ansp:
            ansp.survey_id = data['survey_id']
            ansp.created_date = data['created_date']
            ansp.status = data['status']
            try:
                ansp.save_to_db()
            except:
                return {'msg':'Đã có lỗi xảy ra', 'Status':0}
            return {'msg': 'Đã cập nhật thành công', 'Status':1}
    @jwt_required()
    def delete(self, _id):
        ansp = Model.get_by_id(_id)
        if ansp:
            ansp.delete_from_db()
        return {'msg': 'Thư mục đã xóa', 'Status': 1}

class AnswerPaperList(Resource):
    @jwt_required()
    def post(self):
        data = AnswerPaper.parser.parse_args()
        ansp = Model(**data)
        try:
            ansp.save_to_db()
        except:
            return {'msg': 'Đã có lỗi xảy ra', 'Status': 0}

        return {'msg': 'Thêm mới bảng trả lời thành công', 'Status': 1}
class AnswerPaperBySurvey(Resource):
    @jwt_required()
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('survey_id', type=int, location='args', required=False)
        args = parser.parse_args(strict=False)
        survey_id = args.get('survey_id')
        lstAnsp = Model.get_by_survey(survey_id)
        if lstAnsp:
            return {'Data': [ansp.json() for ansp in lstAnsp], 'TotalRows': len(lstAnsp), 'Status':1 }
        return {'msg': 'Không có bảng trả lời', 'Status': 0}