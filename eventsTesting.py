import unittest
from events import parse_events
from format import format_date, format_time, format_price_range, get


class EventsTesting(unittest.TestCase):
    def setUp(self):
        self.mockData = {
            "data": [
                {
                    "name": "Test",
                    "error": "Nothing Past Here"
                    }
                ]
        }
    

    # GET TESTS
    def test_CorrectGetFunction(self):
        self.assertEqual(get(self.mockData, ["data"]), [{"name": "Test", "error": "Nothing Past Here"}])
    
    def test_CorrectNestedGetFunction(self):
        self.assertEqual(get(self.mockData, ["data", 0, "name"]), "Test")

    def test_MissingGetFunction(self):
        self.assertEqual(get(self.mockData, ["data", 0, "error", "money"]), None)


    # DATE TESTS
    def test_CorrectFormatDate(self):
        self.assertEqual(format_date("2020-01-20"), "January 20, 2020")

    def test_MissingFormatDate(self):
        self.assertEqual(format_date(None), "TBA")
    

    # TIME TESTS
    def test_CorrectFormatTime(self):
        self.assertEqual(format_time("13:35:00"), "1:35 PM")
    
    def test_MissingFormatTime(self):
        self.assertEqual(format_time(None), "TBA")
    

    # PRICE TESTS
    def test_CorrectFormatPriceRange(self):
        self.assertEqual(format_price_range(27.0, 42.0, "CAD"), "27.00 - 42.00 CAD")

    def test_OneCorrectFormatPriceRange(self):
        self.assertEqual(format_price_range(None, 42.0, "USD"), "42.00 USD")

        self.assertEqual(format_price_range(27.0, None, "USD"), "27.00 USD")

    def test_MissingFormatPriceRange(self):
        self.assertEqual(format_price_range(None, None, "CAD"), "TBA")

if __name__ == '__main__':
    unittest.main()