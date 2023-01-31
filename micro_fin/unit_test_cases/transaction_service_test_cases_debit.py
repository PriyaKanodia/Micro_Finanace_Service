import unittest
from micro_fin.services.transaction_service import TransactionService
from micro_fin import app as app

class DebitTransactionTestCases(unittest.TestCase):
    
    def setUp(self):
        print('setUp method called')
        self.app = app.test_client()
        self.current_user_id = 2
        self.transaction_type = 'debit'
        self.amount = 200000

    def tearDown(self):
        print('tearDown method called')
        self.app = None
        self.amount = 0

    def test_debit_transaction(self):
        print('Debit transaction method')
        with app.app_context():
            response = TransactionService().user_transaction(self.current_user_id , self.transaction_type, self.amount)
            statuscode = response[1]
            response = response[0]
            self.assertEqual(statuscode, 201)
            self.assertEqual(response['data'], {'user_id': 2, 'amount': 200000, 'transaction_type': 'debit'})
            self.assertEqual(response['message'], 'Debit operation has been done successfully!!!')


if __name__ == "__main__":
    unittest.main()