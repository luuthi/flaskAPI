from flask import Flask,request,jsonify
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT,jwt_required
from models.survey import SurveyModel
class Survey(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('survey_id',
        type = str,
        required = True,
        help="this field cannot be left blank!"
    )
    parser.add_argument('survey_title',
        type = str,
        required = True,
        help="An item needs a title!"
    )
    parser.add_argument('survey_desc',
        type = str,
        required = False
    )
    parser.add_argument('survey_img',
        type = str,
        required = False
    )
    parser.add_argument('start_date',
        type = date,
        
    )
    @jwt_required()
    def get(self, name):
        item = ItemModel.get_by_name(name)
        if item:
            return item.json(),200
        return {'msg':'Item not found'},404
    
    
    def post(self, name):
        if ItemModel.get_by_name(name):
            return {'msg':'An item with name {0} already exist.'.format(name)},400
        data = Item.parser.parse_args()
        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return {'msg':'An error occurred when inserting item'},400
        
        return item.json(), 201

    
    def delete(self, name):
        item = ItemModel.get_by_name(name)
        if item:
            item.delete_from_db()

        return {'msg': 'Item deleted'}

    def put(self,name):
        data = Item.parser.parse_args()

        item = ItemModel.get_by_name(name)

        if item:
            item.price = data['price']
        else:
            item = ItemModel(name,**data)
            

        item.save_to_db()
        return item.json()

    
class ItemList(Resource):
    @jwt_required()
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]},200

        