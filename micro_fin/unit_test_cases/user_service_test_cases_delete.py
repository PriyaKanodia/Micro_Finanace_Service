import unittest
from micro_fin.services.user_service import UserService
from micro_fin import app as app


class DeleteUserTestCases(unittest.TestCase):
    
    def setUp(self):
        print('setUp method called')
        self.app = app.test_client()
        self.current_user_id = 2

    def tearDown(self):
        print('tearDown method called')
        self.app = None
        self.current_user_id = None

    def test_delete_user(self):
        print('Delete user method called')
        with app.app_context():
            response = UserService().delete_user(self.current_user_id)
            statuscode = response[1]
            self.assertEqual(statuscode, 200)
            response = response[0]
            self.assertEqual(response['message'], 'User deleted successfully')


if __name__ == "__main__":
    unittest.main()