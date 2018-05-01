from tests.base_test import BaseTest
import json


class ProductTest(BaseTest):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        with cls.api_client() as c:
            with cls.app_context():
                c.post('/api/user/register', data={"username": "test",
                                                   "password": "1234",
                                                   "role": "admin"})
                auth_response = c.post('/api/login',
                                       headers={'Content-Type': 'application/json'},
                                       data=json.dumps({
                                           'username': 'test',
                                           'password': '1234'
                                       }))
                response_data = json.loads(auth_response.data)
                cls.auth_header = 'JWT {}'.format(response_data.get('access_token'))

    def test_create_product(self):
        with self.api_client() as c:
            with self.app_context():
                response = c.post('/api/product',
                                  headers={'Authorization': self.auth_header},
                                  data={'name': 'test product',
                                        'npc': 'AX21BH',
                                        'stock': 500,
                                        'price': 1250})
                response_data = json.loads(response.data)

                self.assertEqual(response.status_code, 201)
                self.assertEqual(response_data.get('name'), 'test product')

    def test_get_product(self):
        with self.api_client() as c:
            with self.app_context():
                response = c.post('/api/product',
                                  headers={'Authorization': self.auth_header},
                                  data={'name': 'test product 2',
                                        'npc': 'AX21BH',
                                        'stock': 500,
                                        'price': 1250})
                response_data = json.loads(response.data)

                response = c.get('/api/product/{}'
                                 .format(response_data.get('id')))
                response_data = json.loads(response.data)

                self.assertEqual(response.status_code, 200)
                self.assertEqual(response_data.get('name'), 'test product 2')

    def test_update_product(self):
        with self.api_client() as c:
            with self.app_context():
                response = c.post('/api/product',
                                  headers={'Authorization': self.auth_header},
                                  data={'name': 'test product 3',
                                        'npc': 'AX21BH',
                                        'stock': 500,
                                        'price': 1250})
                response_data = json.loads(response.data)

                response = c.patch('/api/product/{}'
                                   .format(response_data.get('id')),
                                   headers={'Authorization': self.auth_header},
                                   data={'name': 'test product 3.1', 'price': 1300})
                response_data = json.loads(response.data)

                self.assertEqual(response.status_code, 200)
                self.assertEqual(response_data.get('name'), 'test product 3.1')
                self.assertEqual(response_data.get('price'), 1300)

    def test_delete_product(self):
        with self.api_client() as c:
            with self.app_context():
                response = c.post('/api/product',
                                  headers={'Authorization': self.auth_header},
                                  data={'name': 'test product 4',
                                        'npc': 'AX21BH',
                                        'stock': 500,
                                        'price': 1250})
                response_data = json.loads(response.data)

                response = c.delete('/api/product/{}'
                                    .format(response_data.get('id')),
                                    headers={'Authorization': self.auth_header})

                self.assertEqual(response.status_code, 200)

                response = c.get('/api/product/{}'
                                 .format(response_data.get('id')))

                self.assertEqual(response.status_code, 404)

    def test_product_list(self):
        with self.api_client() as c:
            with self.app_context():
                for i in range(5, 10):
                    c.post('/api/product',
                           headers={'Authorization': self.auth_header},
                           data={'name': 'test product {}'.format(i),
                                 'npc': 'AX21BH',
                                 'stock': 500,
                                 'price': 1250})
                response = c.get('/api/products?page=1&per_page=5')
                response_data = json.loads(response.data)

                self.assertEqual(response.status_code, 200)
                self.assertEqual(len(response_data.get('products')), 5)

    def test_product_like(self):
        with self.api_client() as c:
            with self.app_context():
                response = c.post('/api/product',
                                  headers={'Authorization': self.auth_header},
                                  data={'name': 'test product 11',
                                        'npc': 'AX21BH',
                                        'stock': 500,
                                        'price': 1250})
                response_data = json.loads(response.data)

                response = c.patch('/api/product/{}/like'
                                   .format(response_data.get('id')),
                                   headers={'Authorization': self.auth_header})
                response_data = json.loads(response.data)

                self.assertEqual(response.status_code, 200)
                self.assertEqual(response_data.get('likes'), 1)

    def test_product_buy(self):
        with self.api_client() as c:
            with self.app_context():
                response = c.post('/api/product',
                                  headers={'Authorization': self.auth_header},
                                  data={'name': 'test product 12',
                                        'npc': 'AX21BH',
                                        'stock': 500,
                                        'price': 1250})
                response_data = json.loads(response.data)

                response = c.patch('/api/product/{}/buy?quantity=2'
                                   .format(response_data.get('id')),
                                   headers={'Authorization': self.auth_header})
                response_data = json.loads(response.data)

                self.assertEqual(response.status_code, 200)
                self.assertEqual(response_data.get('successful_purchase')
                                 .get('product').get('current_stock'), 498)