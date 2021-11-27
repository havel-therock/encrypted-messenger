import unittest
from messenger.server.server import Server
from messenger.client.client import send
#send()
'''
The setUp() and tearDown() methods allow you to define instructions that will be executed before and after each test method.
They are covered in more detail in the section https://docs.python.org/3/library/unittest.html#organizing-tests
'''

### DUMMY Tests for now
class TestServerConnectionWithClient(unittest.TestCase):
    # def __init__(self):
    #   self.server = Server()
    #   ## self.client = client class

    def test_response(self):
        pass

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOo'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)


if __name__ == '__main__':
    unittest.main()
