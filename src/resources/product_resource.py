from flask_restful import Resource, reqparse, inputs
from flask_jwt import jwt_required

from services.product_service import ProductService
from services.user_service import is_admin


class ProductBuy(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('quantity', type=inputs.positive, required=True)

    @jwt_required()
    def patch(self, _id):
        kwargs = ProductBuy.parser.parse_args()
        data = ProductService.buy_product(_id, kwargs.get('quantity'))

        if data.get('not_found'):
            return data, 404
        elif data.get('stock_not_enough'):
            return data, 200
        elif data.get('error'):
            return data, 500

        return data, 200


class ProductLike(Resource):

    @jwt_required()
    def patch(self, _id):

        data = ProductService.give_like_product(_id)

        if data.get('not_found'):
            return data, 404
        elif data.get('error'):
            return data, 500

        return data, 200


class ProductList(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('orderBy', type=str, action='append')
    parser.add_argument('searchByName', type=str)
    parser.add_argument('page', type=inputs.positive, required=True,
                        help="page field cannot be left blank!")
    parser.add_argument('per_page', type=inputs.positive, required=True,
                        help="per_page field cannot be left blank!")

    def get(self):
        kwargs = ProductList.parser.parse_args()
        order_by = kwargs.get('orderBy')
        search_by = kwargs.get('searchByName')
        page = kwargs.get('page')
        per_page = kwargs.get('per_page')

        data = ProductService.get_product_list(search_by, order_by,
                                               page, per_page)
        return data, 200


class Product(Resource):

    @jwt_required()
    @is_admin()
    def delete(self, _id):
        data = ProductService.delete_product(_id)

        if data.get('not_found'):
            return data, 404

        return data, 200

    @jwt_required()
    @is_admin()
    def patch(self, _id):

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('npc', type=str)
        parser.add_argument('stock', type=inputs.positive)
        parser.add_argument('price', type=float)
        data = parser.parse_args()

        data = ProductService.update_product(_id, **data)

        if data.get('not_found'):
            return data, 404
        elif data.get('error'):
            return data, 500

        return data, 200

    def get(self, _id):
        data = ProductService.get_product(_id)
        if data.get('not_found'):
            return data, 404

        return data, 200

    @jwt_required()
    @is_admin()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True,
            help="name field cannot be left blank!")
        parser.add_argument('npc', type=str, required=True,
            help="npc field cannot be left blank!")
        parser.add_argument('stock', type=inputs.positive, required=True,
            help="stock field cannot be left blank!")
        parser.add_argument('price', type=float, required=True,
            help="price field cannot be left blank!")
        data = parser.parse_args()

        data = ProductService.create_product(**data)
        if data.get('exists'):
            return data, 400
        elif data.get('error'):
            return data, 500

        return data, 201
