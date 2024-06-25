import unittest
from events import parse_events


class EventsTesting(unittest.TestCase):
    def setup():
        mock_data = {'_embedded':{'events':[{'name': "Test", 'url': "test.com", }]}}
    def test_parsingEvents(self):
        self.assertEqual(function1(1), 0)

if __name__ == '__main__':
    unittest.main()