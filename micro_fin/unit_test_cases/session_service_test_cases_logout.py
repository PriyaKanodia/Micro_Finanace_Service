import unittest
from micro_fin.services.session_service import SessionService
from micro_fin import app as app


class LogoutUserTestCase1(unittest.TestCase):
    
    def setUp(self):
        print('setUp method called')
        self.app = app.test_client()
        self.user_id = 2
        self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3NTE1ODQ5MiwianRpIjoiMmYwYTk0Y2MtMGU1Yy00MDRhLWExNzQtY2JlZDZlNDEwZDFlIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InByaXlha2Fub2RpYTkzQGdtYWlsLmNvbSIsIm5iZiI6MTY3NTE1ODQ5Mn0.1T0L29KwwQbZVgbzwaJMel78CNXfF3GQlTlep_lEzY0'

    def tearDown(self):
        print('tearDown method called')
        self.app = None
        self.user_id = None
        self.token = ''

    def test_user_logout(self):
        print('User logout method called')
        with app.app_context():
            response = SessionService().user_logout(self.user_id , self.token)
            statuscode = response[1]
            response = response[0]
            self.assertEqual(statuscode, 200)
            self.assertEqual(response['message'], 'You are logged out successfully')


class LogoutUserTestCase2(unittest.TestCase):
    
    def setUp(self):
        print('setUp method called')
        self.app = app.test_client()
        self.user_id = 2
        self.token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3NTE0ODY4OSwianRpIjoiNjE5Nzk1NTAtNjE0NC00ZGUxLThiODAtZmE2MGMwYmMyOGI1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InByaXlha2Fub2RpYTkzQGdtYWlsLmNvbSIsIm5iZiI6MTY3NTE0ODY4OX0.m2XWuGGEahJ6YeIhwtqAil5I_l-ZtmjpQWYls3OfQuQ'

    def tearDown(self):
        print('tearDown method called')
        self.app = None
        self.user_id = None
        self.token = ''

    def test_user_logout(self):
        print('User logout method called')
        with app.app_context():
            response = SessionService().user_logout(self.user_id , self.token)
            statuscode = response[1]
            response = response[0]
            self.assertEqual(statuscode, 200)
            self.assertEqual(response['message'], 'You are logged out successfully')


if __name__ == "__main__":
    unittest.main()