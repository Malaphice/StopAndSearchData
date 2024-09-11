import unittest
from unittest.mock import patch, mock_open
import pandas as pd
from StopAndSearchData.data_fetch import update_data

class TestFileOperations(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists')
    @patch('pandas.DataFrame.to_csv')
    def test_save_data_to_csv(self, mock_to_csv, mock_exists, mock_open_file):
        """Test that data is saved to a CSV file."""
        mock_exists.return_value = False  # Simulate the file doesn't exist

        data = [{"stop_id": "1", "force": "metropolitan", "outcome": "arrested"}]
        df = pd.DataFrame(data)
        result = update_data(force="metropolitan", year="2023", month="01")
        
        # Ensure that to_csv is called to save the DataFrame
        mock_to_csv.assert_called_once()

    @patch('os.path.exists')
    @patch('pandas.read_csv')
    @patch('pandas.DataFrame.to_csv')
    def test_append_data_to_csv(self, mock_to_csv, mock_read_csv, mock_exists):
        """Test that data is appended to an existing CSV file."""
        mock_exists.return_value = True  # Simulate the file exists
        mock_read_csv.return_value = pd.DataFrame([{"stop_id": "1", "force": "metropolitan"}])
        
        result = update_data(force="metropolitan", year="2023", month="01")

        # Ensure that to_csv is called to save the updated data
        mock_to_csv.assert_called_once()

if __name__ == '__main__':
    unittest.main()