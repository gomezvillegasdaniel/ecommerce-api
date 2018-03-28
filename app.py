import os

from flask import Flask
from flask_restful import Api


app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY')
api = Api(app)

if __name__ == '__main__':
    app.run(port=5000)