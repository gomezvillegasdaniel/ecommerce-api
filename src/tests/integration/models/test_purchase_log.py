from tests.base_test import BaseTest
from models.purchase_log_model import PurchaseLogModel
from models.user_model import UserModel
from models.product_model import ProductModel


class PurchaseLogTest(BaseTest):

    def test_crud(self):
        with self.app_context():
            # Creating dependencies
            user = UserModel('test_user', 'password', 'admin')
            user.save_to_db()
            product = ProductModel('Product X', 'PieceXYZ123', 100, 75.95)
            product.save_to_db()

            # Create
            purchase = PurchaseLogModel(user, product.id, 1)
            purchase.save_to_db()

            # Read
            purchase = next(iter(PurchaseLogModel.find_by_user(user)))
            self.assertIsNotNone(purchase)
            product = PurchaseLogModel.find_by_id(1)
            self.assertIsNotNone(product)

            # Update
            # In this case is not necessary to update a log, each log should be unique

            # Delete
            # In this case is not necessary to delete a log
