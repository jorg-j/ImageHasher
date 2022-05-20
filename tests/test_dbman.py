import unittest
from dbman import Db
import os

# "Test the Db class by creating a database and checking that it exists."
# 
# The first thing we do is create a class called TestDBM. This class inherits from unittest.TestCase.
# This is a requirement for all test classes
class TestDBM(unittest.TestCase):
    def test_create(self):
        """
        It creates a database file called 'test.db' and checks to see if it exists
        """
        self.dbname = 'test.db'
        self.db = Db(self.dbname)

        self.check = os.path.exists(self.dbname)

        self.assertEqual(self.check, True)
        os.remove(self.dbname)


if __name__ == '__main__':
    unittest.main()