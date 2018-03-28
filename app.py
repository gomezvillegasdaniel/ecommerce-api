import os

from flask import Flask
from flask_restful import Api

from resources.product import Product


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get('FLASK_SECRET_KEY')
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

api.add_resource(Product, '/product', '/product/<int:id>')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000)