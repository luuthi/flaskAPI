# -*- coding: utf-8 -*-
from flask_restful import Resource, Api, reqparse
from flask_jwt import jwt_required
from models.page import PageModel


class Page(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('page_title',
                        type=unicode)

    parser.add_argument('page_ordered',
                        type=int)
    parser.add_argument('survey_id',
                        type=int)

    @jwt_required()
    def get(self, _id):
        page = PageModel.get_by_id(_id)
        print (_id)
        if page:
            return {'Data': page.json(), 'TotalRows': 1, 'Status': 1}
        return {'msg': 'Không tìm thấy câu hỏi', 'Status' :0}


    @jwt_required()
    def put(self, _id):
        data = Page.parser.parse_args()
        page = PageModel.get_by_id(_id)
        if page:
            page.page_title = data['page_title']
            page.page_ordered = data['page_ordered']
            try:
                page.save_to_db()
            except:
                return {'msg': 'Đã có lỗi xảy ra', 'Status': 0}
            return {'msg': 'Cập nhật Page thành công', 'Status': 1}

    @jwt_required()
    def delete(self, _id):
        page = PageModel.get_by_id(_id)

        if page:
            page.delete_from_db()

        return {'msg': 'Page đã xóa', 'Status': 1}


class PageList(Resource):

    @jwt_required()
    def post(self):
        data = Page.parser.parse_args()
        page = PageModel(**data)
        try:
            newid = page.save_to_db()
        except:
            return {'msg': 'Đã có lỗi xảy ra', 'Status': 0}

        return {'msg': 'Thêm mới Page thành công', 'Status': 1, 'insertedId': newid}


class PageBySurvey(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('survey_id', type=int, location='args')
        args = parser.parse_args(strict=True)
        survey_id = args.get('survey_id')
        lstPage = PageModel.get_by_survey(survey_id)
        if lstPage:
            return {'Data': [page.json() for page in lstPage], 'TotalRows': len(lstPage), 'Status': 1}
        return {'msg': 'Survey không cáo page', 'Status': 0}


