import unittest
import pandas as pd
from StopAndSearchData.data_fetch import create_dataframe

class TestDataProcessing(unittest.TestCase):
    
    def test_create_dataframe(self):
        """Test that the data is correctly converted to a DataFrame."""
        data = [{"stop_id": "1", "force": "metropolitan", "outcome": "arrested"}]
        df = create_dataframe(data)
        
        self.assertEqual(list(df.columns), ["stop_id", "force", "outcome"])
        self.assertEqual(df.iloc[0]['stop_id'], "1")
        self.assertEqual(df.iloc[0]['force'], "metropolitan")

if __name__ == '__main__':
    unittest.main()

