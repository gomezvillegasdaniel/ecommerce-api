from models.product_model import ProductModel

from services.log_service import log_purchase

from sqlalchemy import desc

from math import ceil


class ProductService:

    @staticmethod
    def get_product_list(search_by, order_by, page, per_page):
        sorting = []

        if order_by:
            for field in order_by:
                if field == 'likes':
                    field = desc(field)
                    sorting.append(field)
        else:
            sorting.append('name')  # default order only by name
        order_by = sorting

        pagination = {'page': page, 'per_page': per_page}

        if search_by:
            products = ProductModel.find_by_name(search_by, *order_by, **pagination)
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
        }

    @staticmethod
    @log_purchase()
    def buy_product(_id, quantity):
        product = ProductModel.find_by_id(_id)

        if not product:
            return {'not_found': 'Product not found'}

        if product.stock < quantity:
            return {'stock_not_enough': {'current_stock': product.stock}}

        product.stock -= quantity

        try:
            product.save_to_db()
        except:
            return {'error': 'An error occurred buying a product.'}

        return {
            'successful_purchase': {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'npc': product.npc,
                    'current_stock': product.stock,
                    'price': product.price
                },
                'purchase_quantity': quantity
            }
        }

    @staticmethod
    def give_like_product(_id):
        product = ProductModel.find_by_id(_id)
        if not product:
            return {'not_found': 'Product not found'}

        product.likes += 1

        try:
            product.save_to_db()
        except:
            return {"error": "An error occurred giving a like to the product."}

        return product.to_dict()

    @staticmethod
    def create_product(*args, **data):
        product = ProductModel.find_by_name(data.get('name')).items
        if product:
            return {'exists':
                    "A product with name '{}' already exists."
                        .format(data.get('name'))}
        try:
            product = ProductModel(data.get('name'),
                                   data.get('npc'),
                                   data.get('stock'),
                                   data.get('price'))
            product.save_to_db()
        except:
            return {"error": "An error occurred inserting the product."}

        return product.to_dict()

    @staticmethod
    def delete_product(_id):
        product = ProductModel.find_by_id(_id)
        if not product:
            return {'not_found': 'Product not found'}

        product.delete_from_db()
        return {'ok': 'Product deleted'}

    @staticmethod
    def update_product(_id, *args, **data):
        product = ProductModel.find_by_id(_id)
        if not product:
            return {'not_found': 'Product not found'}

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
            return {"error": "An error occurred updating the product."}

        return product.to_dict()

    @staticmethod
    def get_product(_id):
        product = ProductModel.find_by_id(_id)
        if not product:
            return {'not_found': 'Product not found'}

        return product.to_dict()
