from flask_restful import Resource, reqparse
from models.product import ProductModel


class Product(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True,
            help="name field cannot be left blank!")
        parser.add_argument('npc', type=str, required=True,
            help="npc field cannot be left blank!")
        parser.add_argument('stock', type=int, required=True,
            help="stock field cannot be left blank!")
        parser.add_argument('price', type=float, required=True,
            help="price field cannot be left blank!")

        data = parser.parse_args()

        if ProductModel.find_by_name(data['name']):
            return {'message': "A product with name '{}' already exists.".format(data['name'])}, 400

        try:
            product = ProductModel(data['name'], data['npc'], data['stock'], data['price'])
            product.save_to_db()
        except:
            return {"message": "An error occurred inserting the product."}, 500

        return product.toDict(), 201
