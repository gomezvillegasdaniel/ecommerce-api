import os
from unittest import TestCase
from app import app
from db import db


class BaseTest(TestCase):

    @classmethod
    def setUpClass(cls):
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('TEST_DATABASE_URL')
        app.config['DEBUG'] = False
        with app.app_context():
            db.init_app(app)
            db.create_all()
        cls.api_client = app.test_client
        cls.app_context = app.app_context

    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            db.session.remove()
            db.drop_all()