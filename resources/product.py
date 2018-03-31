from flask_restful import Resource, reqparse

from sqlalchemy import desc

from math import ceil

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
    parser.add_argument('orderBy', type=str, action='append')
    parser.add_argument('searchByName', type=str)
    parser.add_argument('page', type=int, required=True,
                        help="page field cannot be left blank!")
    parser.add_argument('per_page', type=int, required=True,
                        help="per_page field cannot be left blank!")

    def get(self):
        kwargs = ProductList.parser.parse_args()
        sorting = kwargs.get('orderBy')
        by_name = kwargs.get('searchByName')
        page = kwargs.get('page')
        per_page = kwargs.get('per_page')
        order_by = []

        if sorting:
            for field in sorting:
                if field == 'likes':
                    field = desc(field)
                order_by.append(field)
        else:
            order_by.append('name')  # default order only by name

        pagination = {'page': page, 'per_page': per_page}

        if by_name:
            products = ProductModel.find_by_name(by_name, *order_by, **pagination)
        else:
            products = ProductModel.all_items(*order_by, **pagination)

        total_pages = ceil(products.total / per_page)
        link = '/products?page={}&per_page={}'
        prev_page = page - 1 if page > 1 else 1
        next_page = page + 1 if page < total_pages else total_pages

        return {
            'metadata': {
                'page': page,
                'per_page': per_page,
                'total_pages': total_pages,
                'total_products': products.total,
                'links': {
                    'self': link.format(page, per_page),
                    'first': link.format(1, per_page),
                    'prev': link.format(prev_page, per_page),
                    'next': link.format(next_page, per_page),
                    'last': link.format(total_pages, per_page)
                }
            },
            'products': tuple(map(ProductModel.to_dict, products.items))
        }, 200


class Product(Resource):

    def delete(self, id):
        product = ProductModel.find_by_id(id)
        if not product:
            return {'message': 'Product not found'}, 404
        product.delete_from_db()
        return {'message': 'Product deleted'}, 200

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
        
        return product.to_dict(), 200

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
