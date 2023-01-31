import unittest
from micro_fin.services.session_service import SessionService
from micro_fin import app as app

class LoginUserTestCase1(unittest.TestCase):
    
    def setUp(self):
        print('setUp method called')
        self.app = app.test_client()

    def tearDown(self):
        print('tearDown method called')
        self.app = None

    def test_user_login_status(self):
        print('User login method called')
        with app.app_context():
            email = 'priyakanodia@gmail.com'
            password = 'abc123'
            response = SessionService().user_login(email , password)
            statuscode = response[1]
            response = response[0]
            self.assertEqual(statuscode, 200)
            self.assertEqual(response['message'], 'You are logged in successfully')


class LoginUserTestCase2(unittest.TestCase):
    
    def setUp(self):
        print('setUp method called')
        self.app = app.test_client()

    def tearDown(self):
        print('tearDown method called')
        self.app = None

    def test_user_login_status(self):
        print('User login method called')
        with app.app_context():
            email = 'priyakanodia93@gmail.com'
            password = 'abc1234'
            response = SessionService().user_login(email , password)
            statuscode = response[1]
            response = response[0]
            self.assertEqual(statuscode, 200)
            self.assertEqual(response['message'], 'You are logged in successfully')

if __name__ == "__main__":
    unittest.main()