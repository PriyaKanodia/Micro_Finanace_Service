import unittest
from micro_fin.services.user_service import UserService
from micro_fin import app as app


class CreateUserTestCases(unittest.TestCase):
    
    def setUp(self):
        print('setUp method called')
        self.app = app.test_client()
        self.email = 'priyakanodia93@gmail.com'
        self.password = 'abc1234'
        self.user_data = {
        "first_name": "Priya",
        "last_name": "ABC",
        "country_code": "+91",
        "mobile_number": "99887799699",
        "username": "pk345",
        "gender": "Female",
        "location": "Delhi",
        "pan_number": "ABCD",
        "address": "Jeevan Park",
        "city": "New Delhi",
        "state": "Delhi",
        "country": "India",
        "zip_code": "110059"
    }

    def tearDown(self):
        print('tearDown method called')
        self.app = None
        self.email = ''
        self.password = ''
        self.user_data = {}

    def test_create_user(self):
        print('Create user method called')
        with app.app_context():
            response = UserService().user_signup(self.email, self.password, self.user_data)
            statuscode = response[1]
            response = response[0]
            self.assertEqual(statuscode, 201)
            self.assertEqual(response['data'], {'email': 'priyakanodia93@gmail.com', 'username': 'pk345'})
            self.assertEqual(response['message'], 'User has been created successfully!')


if __name__ == "__main__":
    unittest.main()