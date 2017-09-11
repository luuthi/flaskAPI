from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    def get(self,name):
        store = StoreModel.get_by_name(name)
        if store:
            return store.json()
        return {'msg':'Store not found'}
    def post(self,name):
        if StoreModel.get_by_name(name):
            return {'msg','An store with name {} already exist'.format(name)},404

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'msg':'An erroe occcur in process'},500

        return store.json(),201
    def delete(self,name):    
        store = StoreModel.get_by_name(name)

        if store:
            store.delete_from_db()

        return {'msg':'Store deleted'}
class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}