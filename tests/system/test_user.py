from tests.base_test import BaseTest
from models.user_model import UserModel
import json


class UserTest(BaseTest):

    def test_register_user(self):
        with self.api_client() as c:
            with self.app_context():
                response = c.post('/api/user/register',
                                  data={"username": "test_admin",
                                        "password": "1234567890",
                                        "role": "admin"})
                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username('test_admin'))

    def test_register_and_login(self):
        with self.api_client() as c:
            with self.app_context():
                data = {
                    "username": "test_customer",
                    "password": "1234567890",
                    "role": "customer"
                }
                c.post('/api/user/register', data=data)

                auth_response = c.post('/api/login',
                                       headers={'Content-Type': 'application/json'},
                                       data=json.dumps({
                                         'username': 'test_customer',
                                         'password': '1234567890'
                                       }))

                self.assertIn('access_token', json.loads(auth_response.data).keys())

    def test_register_duplicate_user(self):
        with self.api_client() as c:
            with self.app_context():
                c.post('/api/user/register', data={'username': 'test',
                                                   'password': '1234',
                                                   'role': 'customer'})
                r = c.post('/api/user/register', data={'username': 'test',
                                                       'password': '1234',
                                                       'role': 'customer'})

                self.assertEqual(r.status_code, 400)
                self.assertDictEqual(d1={'message': 'That username already exists'},
                                     d2=json.loads(r.data))
