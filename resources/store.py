from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
     def get(self,name):
         store= StoreModel.find_by_name(name)
         if store:
             return store.json()
         return {'message': "name is not present"}

     def post(self, name):
         if StoreModel.find_by_name(name):
             return {'message': "name is already present"}
         store= StoreModel(name)
         try:
             store.save_to_db()
         except:
             return {"message":'error came while inserting the data'}

         return store.json()

     def delete(self, name):
         store= StoreModel.find_by_name(name)
         if store:
             store.delete_from_db()
             return {'message': 'store got deleted'}
         return {'message': 'store was not present to delete'}

class StoreList(Resource) :
    def get(self):
        return {"stores": list(map(lambda x : x.json(), StoreModel.query.all()))}, 201

