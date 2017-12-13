# -*- coding: utf-8 -*-
from flask_restful import Resource, Api, reqparse
from flask_jwt import jwt_required
from models.survey import SurveyModel
from datetime import datetime


class Survey(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('survey_code',
                        type=str,
                        required=False)
    parser.add_argument('survey_title',
                        type=unicode,
                        required=False)
    parser.add_argument('survey_desc',
                        type=unicode,
                        required=False)
    parser.add_argument('survey_img',
                        type=str,
                        required=False)
    parser.add_argument('start_date',
                        type=lambda x: datetime.strptime(x, '%Y-%m-%d'),
                        required=True)
    parser.add_argument('end_date',
                        type=lambda x: datetime.strptime(x, '%Y-%m-%d'),
                        required=True)
    parser.add_argument('created_date',
                        type=lambda x: datetime.strptime(x, '%Y-%m-%d'),
                        required=True)
    parser.add_argument('last_edited',
                        type=lambda x: datetime.strptime(x, '%Y-%m-%d'),
                        required=True)
    parser.add_argument('folder_id',
                        type=int,
                        required=True)
    parser.add_argument('user_name',
                        type=str,
                        required=True,
                        help="A folder must belong to a user")

    def get(self, _id):
        survey = SurveyModel.get_by_id(_id)
        if survey:
            return {'Data': survey.json(), 'TotalRows': 1, 'Status': 1}
        return {'msg': 'Không tìm thấy survey', 'Status': 0}

    @jwt_required()
    def put(self, _id):
        data = Survey.parser.parse_args()
        survey = SurveyModel.get_by_id(_id)
        if survey:
            survey.survey_title = data['survey_title']
            survey.survey_desc = data['survey_desc']
            survey.survey_img = data['survey_img']
            survey.end_date = data['end_date']
            survey.start_date = data['start_date']
            survey.last_edited = data['last_edited']
            survey.user_name = data['user_name']
            survey.folder_id = data['folder_id']
            print (survey)
            print (data)
            try:
                survey.save_to_db()
            except:
                return {'msg': 'Đã có lỗi xảy ra', 'Status': 0}
            return {'msg': 'Cập nhật Survey thành công', 'Status': 1}

    @jwt_required()
    def delete(self, _id):
        survey = SurveyModel.get_by_id()

        if survey:
            survey.delete_from_db()

        return {'msg': 'Survey  đã xóa', 'Status': 1}


class SurveyList(Resource):

    @jwt_required()
    def post(self):
        data = Survey.parser.parse_args()
        survey = SurveyModel(**data)
        newid = 0
        try:
            newid = survey.save_to_db()
        except:
            return {'msg': 'Đã có lỗi xảy ra', 'Status': 0}

        return {'msg': 'Thêm mới Survey thành công', 'Status': 1, 'insertedId': newid}


class SurveyByFolder(Resource):
    @jwt_required()
    def get(self):
        parser_folder = reqparse.RequestParser()
        parser_folder.add_argument('user_name', type=str, location='args', required=False)
        parser_folder.add_argument('folder_id', type=str, location='args', required=False)
        args = parser_folder.parse_args(strict=True)
        user_name = args.get('user_name')
        folder_id = args.get('folder_id')
        print(user_name, folder_id)
        lstSurvey = SurveyModel.get_by_folder(folder_id, user_name)
        if lstSurvey:
            return {'Data': [survey.json() for survey in lstSurvey], 'TotalRows': len(lstSurvey), 'Status': 1}
        return {'msg': 'Thư mục không có survey ', 'Status': 0}


class SurveyByUser(Resource):
    @jwt_required()
    def get(self):
        parser_user = reqparse.RequestParser()
        parser_user.add_argument('user_name', type=str, location='args', required=False)
        parser_user.add_argument('status', type=int, location='args', required=False)
        args = parser_user.parse_args(strict=True)
        user_name = args.get('user_name')
        status = args.get('status')
        lstSurvey = SurveyModel.get_by_user(user_name, status)
        if lstSurvey:
            return {'Data': lstSurvey, 'TotalRows': len(lstSurvey), 'Status': 1}
        return {'msg': 'Người dùng không có survey ', 'Status': 0}


class SurveyMaxByUser(Resource):
    @jwt_required()
    def get(self):
        parser_user = reqparse.RequestParser()
        parser_user.add_argument('user_name', type=str, location='args', required=False)
        args = parser_user.parse_args(strict=True)
        user_name = args.get('user_name')
        print(user_name)
        max = SurveyModel.get_max(user_name)
        if max:
            return {'Data': max, 'Status': 1}
        return {'msg': 'Có lỗi xảy ra ', 'Status': 0}

class SurveyByName(Resource):
    @jwt_required()
    def get(self):
        parser_user = reqparse.RequestParser()
        parser_user.add_argument('survey_name', type=unicode, location='args', required=False)
        parser_user.add_argument('folder_id', type=str, location='args', required=False)
        args = parser_user.parse_args(strict=True)
        survey_name = args.get('survey_name')
        folder_id = args.get('folder_id')
        lstSurvey = SurveyModel.get_by_name(survey_name, folder_id)
        if lstSurvey:
            return {'Data': [survey.json() for survey in lstSurvey], 'TotalRows': len(lstSurvey), 'Status': 1}
        return {'msg': 'Thư mục không có survey ', 'Status': 0}