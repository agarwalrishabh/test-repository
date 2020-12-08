import sqlite3

from flask_restful import Resource, reqparse

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",
                        type=float,
                        required=True,
                        help="this field can not be blank")

    parser.add_argument("store_id",
                        type=int,
                        required=True,
                        help="every item needs a tore id")

    # @jwt_required()
    def get(self, name):
        item=ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "item not present"}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "name is already present"},400
        data = Item.parser.parse_args()
        item = ItemModel( name, **data)
        try:
            item.save_to_db()
        except:
            return {'message': "error occurred while inserting the data to a database"},500

        return item.json(), 201

    def delete(self, name):
        item= Item.find_by_name(name)
        if item:
            item.delete_from_db()
        return {"message": "row has been deleted"}, 200

    def put(self, name):
        data = Item.parser.parse_args()
        item=ItemModel.find_by_name(name)

        if item is None:
           item= ItemModel(name,**data)
        else:
           item.price= data['price']
        item.save_to_db()

        return item.json()


class Items(Resource):
    def get(self):
        return {"items": list(map(lambda x : x.json(), ItemModel.query.all()))}, 201
