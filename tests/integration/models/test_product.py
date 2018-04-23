from tests.base_test import BaseTest
from models.product_model import ProductModel


class ProductTest(BaseTest):

    def test_crud(self):
        with self.app_context():
            # Create
            product = ProductModel('Product X', 'PieceXYZ123', 100, 75.95)
            product.save_to_db()

            # Read
            product = next(iter(ProductModel.find_by_name('Product X').items))
            self.assertIsNotNone(product)
            product = ProductModel.find_by_id(1)
            self.assertIsNotNone(product)

            # Update
            product.name = 'Product Y'
            product.save_to_db()
            product = next(iter(ProductModel.find_by_name('Product Y').items))
            self.assertIsNotNone(product)

            # Delete
            product.delete_from_db()
            self.assertListEqual(ProductModel.find_by_name('Product Y').items, [])
