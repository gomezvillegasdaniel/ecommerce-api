from flask_restful import Resource, reqparse

from models.product import ProductModel


class ProductLike(Resource):

    def patch(self, id):
        product = ProductModel.find_by_id(id)
        if not product:
            return {'message': 'Product not found'}, 404

        product.likes += 1

        try:
            product.save_to_db()
        except:
            return {"message": "An error occurred giving a like to the product."}, 500

        return product.to_dict(), 200

class ProductList(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('orderBy', type=str)
    parser.add_argument('searchByName', type=str)

    def get(self):
        kwargs = ProductList.parser.parse_args()
        order_by = ['name']
        ordering = kwargs.get('orderBy')

        if ordering:
            if isinstance(ordering, list):
                for field in ordering:
                    order_by.append(field)
            else:
                order_by.append(ordering)

        print('order_by', order_by)
        name = kwargs.get('searchByName')
        if name:
            products = list(map(lambda p: p.to_dict(), ProductModel.find_by_name(name, *order_by)))
        else:
            products = list(map(lambda p: p.to_dict(), ProductModel.all(*order_by)))

        return {'products': products}


class Product(Resource):

    def delete(self, id):
        product = ProductModel.find_by_id(id)
        if not product:
            return {'message': 'Product not found'}, 404
        product.delete_from_db()
        return {'message': 'Product deleted'}

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
        
        return product.to_dict()

    def get(self, id):
        product = ProductModel.find_by_id(id)
        return product.to_dict() if product else {'message': 'Product not found'}, 404

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

        return product.to_dict(), 201
