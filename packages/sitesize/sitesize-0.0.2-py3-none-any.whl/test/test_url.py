

import unittest
import sitesize

test_url1 = 'http://www.google.com'
test_url2 = 'www.google.com'
test_url_list = [
    'https://www.yahoo.com/',
    'http://www.cnn.com',
    'http://www.python.org',
    'http://www.jython.org',
    'http://www.pypy.org',
]

class MyTestCase(unittest.TestCase):

    def test_url_checker(self):
        self.assertEqual(sitesize.url_checker(test_url1), test_url1)
        self.assertEqual(sitesize.url_checker(test_url2), test_url1)

    def test_get_webpage_size(self):
        self.assertIsNotNone(sitesize.get_webpage_size(test_url1))

    def test_get_webpages_size(self):
        self.assertIsNotNone(sitesize.get_webpages_size(test_url_list))


if __name__ == '__main__':
    unittest.main()