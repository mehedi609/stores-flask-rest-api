from flask_restful import Resource, reqparse
from models.store import StoreModel


class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'store_name',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200
        return {'message': 'Store not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message', f'A store with name {name} already exists'}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": "An error occurred creating the store."}, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {'message': f'Store with name {name} deleted'}, 200
        return {'message': 'Store not found'}, 404

    def put(self, name):
        data = Store.parser.parse_args()
        store = StoreModel.find_by_name(name=name)

        if store:
            store.name = data['store_name']
        else:
            store = StoreModel(data['store_name'])

        store.save_to_db()
        return store.json()


class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
