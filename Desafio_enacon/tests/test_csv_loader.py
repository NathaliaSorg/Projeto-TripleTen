import pytest
import pandas as pd
import os
import tempfile
import shutil
from datetime import datetime

# Import the CSVLoader class
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from loaders.csv_loader import CSVLoader


class TestCSVLoader:
    """Test cases for CSVLoader class."""
    
    def setup_method(self):
        """Setup test fixtures before each test method."""
        self.test_dir = tempfile.mkdtemp()
        self.csv_path = os.path.join(self.test_dir, "test_prices.csv")
        
        # Create a test CSV file
        self.create_test_csv()
        
        # Initialize CSVLoader with test file path
        self.loader = CSVLoader(self.csv_path)
    
    def teardown_method(self):
        """Clean up test fixtures after each test method."""
        shutil.rmtree(self.test_dir)
    
    def create_test_csv(self):
        """Create a test CSV file with sample data."""
        # Create sample data
        dates = pd.date_range('2020-01-01', periods=10, freq='W')
        data = {
            'M + 0': range(100, 110),
            'M + 1': range(200, 210),
            'M + 2': range(300, 310)
        }
        
        df = pd.DataFrame(data, index=dates)
        df.index.name = 'Date'
        
        # Save to CSV (without index name to match the original format)
        df.to_csv(self.csv_path)
    
    def test_init_with_default_path(self):
        """Test initialization with default path."""
        loader = CSVLoader()
        assert loader.csv_path == "data/prices/prices.csv"
    
    def test_init_with_custom_path(self):
        """Test initialization with custom path."""
        custom_path = "custom/path/data.csv"
        loader = CSVLoader(custom_path)
        assert loader.csv_path == custom_path
    
    def test_load_csv_success(self):
        """Test successful CSV loading."""
        df = self.loader.load_csv()
        
        assert df is not None
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 10
        assert list(df.columns) == ['M + 0', 'M + 1', 'M + 2']
        assert df.index.name == 'Date'
        assert isinstance(df.index, pd.DatetimeIndex)
    
    def test_load_csv_file_not_found(self):
        """Test CSV loading when file doesn't exist."""
        loader = CSVLoader("non_existent_file.csv")
        df = loader.load_csv()
        
        assert df is None
    
    def test_get_data_info_success(self):
        """Test getting data information successfully."""
        info = self.loader.get_data_info()
        
        assert info is not None
        assert 'shape' in info
        assert 'columns' in info
        assert 'date_range' in info
        assert 'data_types' in info
        assert 'sample_data' in info
        
        assert info['shape'] == (10, 3)
        assert info['columns'] == ['M + 0', 'M + 1', 'M + 2']
        assert 'start' in info['date_range']
        assert 'end' in info['date_range']
    
    def test_get_data_info_no_data(self):
        """Test getting data information when no data is loaded."""
        loader = CSVLoader("non_existent_file.csv")
        info = loader.get_data_info()
        
        assert info == {"error": "Failed to load data"}
    
    def test_filter_by_date_range_no_filter(self):
        """Test filtering by date range with no filters applied."""
        df = self.loader.filter_by_date_range()
        
        assert df is not None
        assert len(df) == 10
    
    def test_filter_by_date_range_start_date(self):
        """Test filtering by start date."""
        start_date = '2020-01-15'
        df = self.loader.filter_by_date_range(start_date=start_date)
        
        assert df is not None
        assert len(df) < 10  # Should have fewer rows
        assert df.index[0] >= pd.to_datetime(start_date)
    
    def test_filter_by_date_range_end_date(self):
        """Test filtering by end date."""
        end_date = '2020-02-15'
        df = self.loader.filter_by_date_range(end_date=end_date)
        
        assert df is not None
        assert len(df) < 10  # Should have fewer rows
        assert df.index[-1] <= pd.to_datetime(end_date)
    
    def test_filter_by_date_range_both_dates(self):
        """Test filtering by both start and end dates."""
        start_date = '2020-01-15'
        end_date = '2020-02-15'
        df = self.loader.filter_by_date_range(start_date=start_date, end_date=end_date)
        
        assert df is not None
        assert len(df) < 10  # Should have fewer rows
        assert df.index[0] >= pd.to_datetime(start_date)
        assert df.index[-1] <= pd.to_datetime(end_date)
    
    def test_filter_by_date_range_no_data(self):
        """Test filtering when no data is loaded."""
        loader = CSVLoader("non_existent_file.csv")
        df = loader.filter_by_date_range(start_date='2020-01-01')
        
        assert df is None
    
    def test_data_types_are_numeric(self):
        """Test that all data columns have numeric data types."""
        df = self.loader.load_csv()
        
        assert df is not None
        for dtype in df.dtypes:
            assert pd.api.types.is_numeric_dtype(dtype)
    
    def test_date_index_is_sorted(self):
        """Test that the date index is sorted chronologically."""
        df = self.loader.load_csv()
        
        assert df is not None
        assert df.index.is_monotonic_increasing
    
    def test_sample_data_structure(self):
        """Test the structure of sample data returned by get_data_info."""
        info = self.loader.get_data_info()
        
        assert 'sample_data' in info
        sample_data = info['sample_data']
        
        # Check that sample data has the expected structure
        for column in info['columns']:
            assert column in sample_data
            assert isinstance(sample_data[column], dict)
    
    def test_empty_csv_file(self):
        """Test loading an empty CSV file."""
        # Create an empty CSV file
        empty_csv_path = os.path.join(self.test_dir, "empty.csv")
        with open(empty_csv_path, 'w') as f:
            f.write("")
        
        loader = CSVLoader(empty_csv_path)
        df = loader.load_csv()
        
        # Should handle empty file gracefully
        assert df is None or df.empty
    
    def test_csv_with_missing_values(self):
        """Test loading CSV with missing values."""
        # Create CSV with missing values
        missing_csv_path = os.path.join(self.test_dir, "missing_values.csv")
        
        csv_content = """Date,M + 0,M + 1,M + 2
2020-01-01,100,200,300
2020-01-08,,210,310
2020-01-15,120,,320
2020-01-22,130,230,"""
        
        with open(missing_csv_path, 'w') as f:
            f.write(csv_content)
        
        loader = CSVLoader(missing_csv_path)
        df = loader.load_csv()
        
        assert df is not None
        assert df.isna().any().any()  # Should have some missing values


if __name__ == "__main__":
    pytest.main([__file__])
