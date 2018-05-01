from tests.base_test import BaseTest

from models.user_model import UserModel


class UserTest(BaseTest):

    def setUp(self):
        super().setUp()
        with self.app_context():
            self.user = UserModel('test_admin', '0123456789', 'admin')
            self.user.save_to_db()

    def test_create_user(self):
        with self.app_context():
            self.user.save_to_db()
            user = UserModel.find_by_id(self.user.id)

            self.assertEqual(user.username, 'test_admin')
            self.assertEqual(user.password, '0123456789')
    
    def test_fail_create_user(self):
        with self.assertRaises(BaseException):
            UserModel()

    def test_update_user(self):
        with self.app_context():
            self.user.username = 'administrator'
            self.user.save_to_db()
            user = UserModel.find_by_id(self.user.id)

            self.assertEqual(user.username, 'administrator')
    
    def test_fail_update_user(self):
        with self.app_context():
            with self.assertRaises(BaseException):
                self.user = None
                self.user.save_to_db()

    def test_delete_user(self):
        with self.app_context():
            self.user.delete_from_db()
            user = UserModel.find_by_id(self.user.id)

            self.assertIsNone(user)
