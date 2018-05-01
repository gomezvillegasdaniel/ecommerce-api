from tests.base_test import BaseTest
from models.user_model import UserModel


class UserTest(BaseTest):

    def test_crud(self):
        with self.app_context():
            # Create
            user = UserModel('test_user', 'password', 'admin')
            user.save_to_db()

            # Read
            user = UserModel.find_by_username('test_user')
            self.assertIsNotNone(user)
            user = UserModel.find_by_id(1)
            self.assertIsNotNone(user)
            user = next(iter(UserModel.find_by_role('admin')))
            self.assertIsNotNone(user)

            # Update
            user.username = 'administrator'
            user.save_to_db()
            user = UserModel.find_by_username('administrator')
            self.assertIsNotNone(user)

            # Delete
            user.delete_from_db()
            self.assertIsNone(UserModel.find_by_username('administrator'))
