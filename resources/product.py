from flask_restful import Resource, reqparse
from models.product import ProductModel


class Product(Resource):

    def patch(self, id):
        product = ProductModel.find_by_id(id)
        if not product:
            return {'message': 'Product not found'}, 404
        
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('npc', type=str)
        parser.add_argument('stock', type=int)
        parser.add_argument('price', type=float)
        data = parser.parse_args()

        name = data.get('name')
        npc = data.get('npc')
        stock = data.get('stock')
        price = data.get('price')

        if name:
            product.name = name
        if npc:
            product.npc = npc
        if stock:
            product.stock = stock
        if price:
            product.price = price
        try:
            product.save_to_db()
        except:
            return {"message": "An error occurred updating the product."}, 500
        
        return product.toDict()

    def get(self, id):
        product = ProductModel.find_by_id(id)
        return product.toDict() if product else {'message': 'Product not found'}, 404

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
