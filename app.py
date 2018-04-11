import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from flask_script import Manager, Command
from flask_migrate import Migrate, MigrateCommand

from db import db

from security import authenticate, identity

from resources.product_resource import (Product, ProductList,
                                        ProductLike, ProductBuy)
from resources.user_resource import UserRegister


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_AUTH_URL_RULE'] = '/api/login'
app.secret_key = os.environ.get('FLASK_SECRET_KEY')

db.init_app(app)
migrate = Migrate(app, db)


@app.before_first_request
def create_tables():
    db.create_all()


class RunServerCommand(Command):
    def run(self):
        app.run(host='0.0.0.0', port=5000, debug=False)


class RunDevServerCommand(Command):
    def run(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DEV_DATABASE_URL')
        app.run(host='0.0.0.0', port=5000, debug=True)


manager = Manager(app)
manager.add_command('run', RunServerCommand)
manager.add_command('dev', RunDevServerCommand)
manager.add_command('db', MigrateCommand)

jwt = JWT(app, authenticate, identity)

api = Api(app)
api.add_resource(Product, '/api/product', '/api/product/<int:_id>')
api.add_resource(ProductList, '/api/products')
api.add_resource(ProductLike, '/api/product/<int:_id>/like')
api.add_resource(ProductBuy, '/api/product/<int:_id>/buy')
api.add_resource(UserRegister, '/api/user/register')

if __name__ == '__main__':
    manager.run()
