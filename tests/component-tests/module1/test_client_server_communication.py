import unittest
from messenger.server.server import Server
from messenger.client.test_client import TestClient
'''
The setUp() and tearDown() methods allow you to define instructions that will be executed before and after each test method.
They are covered in more detail in the section https://docs.python.org/3/library/unittest.html#organizing-tests
'''

### DUMMY Tests for now
class TestServerConnectionWithClient(unittest.TestCase):

    #def setUp(self):
       #pass
       # self.server = Server()
       # self.client = TestClient()

    #def tearDown(self):
        #pass
        #self.server.shut_down()
        #self.client.shut_down()

    #def test_LoginIN(self):
        #self.client.send_LOGIN_request()


    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)


if __name__ == '__main__':
    unittest.main()
