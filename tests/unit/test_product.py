from tests.base_test import BaseTest

from models.product_model import ProductModel


class ProductTest(BaseTest):

    def setUp(self):
        super().setUp()
        with self.app_context():
            self.product = ProductModel('Product X', 'PieceXYZ123', 100, 75.95)
            self.product.save_to_db()

    def test_create_product(self):
        with self.app_context():
            self.product.save_to_db()
            product = ProductModel.find_by_id(self.product.id)

            self.assertEqual(product.name, 'Product X')
    
    def test_fail_create_product(self):
        with self.assertRaises(BaseException):
            ProductModel()

    def test_update_product(self):
        with self.app_context():
            self.product.price = 90.55
            self.product.save_to_db()
            product = ProductModel.find_by_id(self.product.id)

            self.assertEqual(product.price, 90.55)
    
    def test_fail_update_product(self):
        with self.app_context():
            with self.assertRaises(BaseException):
                self.product = None
                self.product.save_to_db()
                
    def test_delete_product(self):
        with self.app_context():
            self.product.delete_from_db()
            product = ProductModel.find_by_id(self.product.id)

            self.assertIsNone(product)
    