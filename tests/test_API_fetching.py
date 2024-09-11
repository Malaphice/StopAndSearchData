import unittest
from unittest.mock import patch
from StopAndSearchData.data_fetch import get_stop_and_search_data

class TestAPIFetching(unittest.TestCase):

    @patch('StopAndSearchData.data_fetch.requests.get')
    def test_get_data_success(self, mock_get):
        """Test that data is successfully fetched from the API."""
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = [{"stop_id": "1", "force": "metropolitan"}]
        
        result = get_stop_and_search_data("metropolitan", "2023-01")
        self.assertEqual(result, [{"stop_id": "1", "force": "metropolitan"}])

    @patch('StopAndSearchData.data_fetch.requests.get')
    def test_get_data_empty(self, mock_get):
        """Test that an empty response is handled correctly."""
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = []
        
        result = get_stop_and_search_data("metropolitan", "2023-01")
        self.assertEqual(result, [])

    @patch('StopAndSearchData.data_fetch.requests.get')
    def test_get_data_failure(self, mock_get):
        """Test that an API failure is handled correctly."""
        mock_response = mock_get.return_value
        mock_response.status_code = 500
        
        result = get_stop_and_search_data("metropolitan", "2023-01")
        self.assertEqual(result, [])  # Expect an empty list for failed API calls

if __name__ == '__main__':
    unittest.main()