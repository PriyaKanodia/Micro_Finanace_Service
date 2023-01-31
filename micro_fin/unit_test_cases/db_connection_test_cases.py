'''
Connection Pool of max 4
'''

import unittest
import mysql.connector
import threading

MYSQL_USER = "root"
MYSQL_PASSWORD = "root123"
MYSQL_DB = "micro_finance"
MYSQL_HOST = "localhost"
MYSQL_PORT = "3306"
POOL_SIZE = 4
# POOL_SIZE = 2
# POOL_SIZE = 6

class TestDatabase(unittest.TestCase):

    connection = None

    def setUp(self):
        print("Connection set up called")
        self.connection = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            passwd=MYSQL_PASSWORD,
            database=MYSQL_DB,
            port=MYSQL_PORT,
            pool_size=POOL_SIZE)
        self.cursor = self.connection.cursor(dictionary=True)

        self.connection2 = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            passwd=MYSQL_PASSWORD,
            database=MYSQL_DB,
            port=MYSQL_PORT,
            pool_size=POOL_SIZE)
        self.cursor2 = self.connection2.cursor(dictionary=True)

        self.connection3 = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            passwd=MYSQL_PASSWORD,
            database=MYSQL_DB,
            port=MYSQL_PORT,
            pool_size=POOL_SIZE)
        self.cursor3 = self.connection3.cursor(dictionary=True)
        
        self.connection4 = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            passwd=MYSQL_PASSWORD,
            database=MYSQL_DB,
            port=MYSQL_PORT,
            pool_size=POOL_SIZE)
        self.cursor4 = self.connection4.cursor(dictionary=True)

    def tearDown(self):
        print("Connection tear down called")
        if self.connection is not None and self.connection.is_connected():
            self.connection.close()
        if self.connection2 is not None and self.connection2.is_connected():
            self.connection2.close()
        if self.connection3 is not None and self.connection3.is_connected():
            self.connection3.close()
        if self.connection4 is not None and self.connection4.is_connected():
            self.connection4.close()

    def test_connection(self):
        print("Connection test called")
        self.assertTrue(self.connection.is_connected())
        self.assertTrue(self.connection2.is_connected())
        self.assertTrue(self.connection3.is_connected())
        self.assertTrue(self.connection4.is_connected())

    def test_db_crud(self):
        print("Test CRUD called")
        t1 = threading.Thread(self.assertEqual(self.create_table_row(), 'OK'))
        t2 = threading.Thread(self.assertEqual(self.update_table_row(), 'OK'))
        t3 = threading.Thread(self.assertEqual(self.query_table(), 'OK'))
        t4 = threading.Thread(self.assertEqual(self.delete_table_row(), 'OK'))
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t1.join()
        t2.join()
        t3.join()
        t4.join()   

    def create_table_row(self):
        print("Create row called")
        create_query = "Insert Into accounts (user_id, balance, active, created_by, updated_by) values (3, 30000.0, 1, 3, 3)"
        try:
            self.cursor.execute(create_query)
            return 'OK'
        except (mysql.connector.Error, mysql.connector.Warning) as e:
            return 'NOT OK'

    def update_table_row(self):
        print("Update row called")
        update_query = "Update accounts set balance = 400000 where user_id = 3"
        try:
            self.cursor.execute(update_query)
            return 'OK'
        except (mysql.connector.Error, mysql.connector.Warning) as e:
            return 'NOT OK'

    def query_table(self):
        print("Get row called")
        get_query = "select * from accounts where user_id=3"
        try:
            self.cursor.execute(get_query)
            return 'OK'
        except (mysql.connector.Error, mysql.connector.Warning) as e:
            return 'NOT OK'

    def delete_table_row(self):
        print("Delete row called")
        delete_query = "delete from accounts where user_id=3"
        try:
            self.cursor.execute(delete_query)
            return 'OK'
        except (mysql.connector.Error, mysql.connector.Warning) as e:
            return 'NOT OK'


if __name__ == '__main__':
    unittest.main()
