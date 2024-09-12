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
    
    def test_drop_location_in_dataframe(self):
        """Test that the data is correctly converted to a DataFrame."""
        data = [
            {
                "age_range": "25-34",
                "outcome": "Nothing found",
                "involved_person": True,
                "self_defined_ethnicity": "White - English/Welsh/Scottish/Northern Irish/British",
                "gender": "Male",
                "legislation": "Misuse of Drugs Act 1971 (section 23)",
                "location": {
                    "latitude": "51.5074",
                    "longitude": "-0.1278",
                    "street": {
                        "id": 12345,
                        "name": "Main Street"
                    }
                },
                "object_of_search": "Drugs"
            }
        ]
        
        # Create the DataFrame using the create_dataframe function
        df = create_dataframe(data)
        
        # Check that the 'location' column is dropped
        self.assertNotIn('location', df.columns)

        # Check that the specific nested fields are retained
        self.assertIn('location.latitude', df.columns)
        self.assertIn('location.longitude', df.columns)
        self.assertIn('location.street.id', df.columns)
        self.assertIn('location.street.name', df.columns)
        
        # Optionally, check the values for correctness
        self.assertEqual(df.iloc[0]['location.latitude'], "51.5074")
        self.assertEqual(df.iloc[0]['location.longitude'], "-0.1278")
        self.assertEqual(df.iloc[0]['location.street.id'], 12345)
        self.assertEqual(df.iloc[0]['location.street.name'], "Main Street")
        
if __name__ == '__main__':
    unittest.main()

