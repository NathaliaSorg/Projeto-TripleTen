import pandas as pd
import os
from datetime import datetime

class CSVLoader:
    """
    A class to load CSV files from the data/prices folder and return pandas DataFrames
    with the first column converted to date format.
    """
    
    def __init__(self, csv_path=None):
        """
        Initialize the CSVLoader.
        
        Args:
            csv_path (str, optional): Path to the CSV file. If None, uses default path.
        """
        if csv_path is None:
            # Default path to the prices CSV file
            self.csv_path = "data/prices/prices.csv"
        else:
            self.csv_path = csv_path
    
    def load_csv(self):
        """
        Load the CSV file and return a pandas DataFrame with the first column converted to datetime.
        
        Returns:
            pandas.DataFrame: DataFrame with dates in the first column and prices in subsequent columns
        """
        try:
            # Check if file exists
            if not os.path.exists(self.csv_path):
                raise FileNotFoundError(f"CSV file not found at: {self.csv_path}")
            
            # Read the CSV file
            # The first row appears to be headers, but there's an empty first column
            df = pd.read_csv(self.csv_path)
            
            # The first column contains dates, but it doesn't have a header
            # Let's check the structure and handle it properly
            if df.columns[0] == 'Unnamed: 0':
                # This means the first column doesn't have a header
                # We need to set the first column as the index and parse it as dates
                df = pd.read_csv(self.csv_path, index_col=0, parse_dates=True)
                
                # Rename the index to 'Date'
                df.index.name = 'Date'
                df.index = pd.to_datetime(df.index)
                
            else:
                # If the first column has a proper header, use it as date column
                date_column = df.columns[0]
                df[date_column] = pd.to_datetime(df[date_column])
                df.set_index(date_column, inplace=True)
                df.index.name = 'Date'
            
            return df
            
        except Exception as e:
            print(f"Error loading CSV file: {e}")
            return None
    
    def get_data_info(self):
        """
        Get basic information about the loaded data.
        
        Returns:
            dict: Dictionary containing data information
        """
        df = self.load_csv()
        if df is None:
            return {"error": "Failed to load data"}
        
        info = {
            "shape": df.shape,
            "columns": list(df.columns),
            "date_range": {
                "start": df.index.min(),
                "end": df.index.max()
            },
            "data_types": df.dtypes.to_dict(),
            "sample_data": df.head().to_dict()
        }
        
        return info
    
    def filter_by_date_range(self, start_date=None, end_date=None):
        """
        Filter the data by date range.
        
        Args:
            start_date (str or datetime, optional): Start date for filtering
            end_date (str or datetime, optional): End date for filtering
            
        Returns:
            pandas.DataFrame: Filtered DataFrame
        """
        df = self.load_csv()
        if df is None:
            return None
        
        if start_date:
            start_date = pd.to_datetime(start_date)
            df = df[df.index >= start_date]
        
        if end_date:
            end_date = pd.to_datetime(end_date)
            df = df[df.index <= end_date]
        
        return df


# Example usage and testing
if __name__ == "__main__":
    # Create an instance of the CSVLoader
    loader = CSVLoader()
    
    # Load the data
    df = loader.load_csv()
    
    if df is not None:
        print("CSV loaded successfully!")
        print(f"Data shape: {df.shape}")
        print(f"Date range: {df.index.min()} to {df.index.max()}")
        print(f"Columns: {list(df.columns)}")
        print("\nFirst 5 rows:")
        print(df.head())
        
        # Get data information
        info = loader.get_data_info()
        print(f"\nData information:")
        print(f"Shape: {info['shape']}")
        print(f"Date range: {info['date_range']['start']} to {info['date_range']['end']}")
        
        # Example of filtering by date range
        filtered_df = loader.filter_by_date_range("2020-01-01", "2020-12-31")
        if filtered_df is not None:
            print(f"\nFiltered data (2020): {filtered_df.shape}")
            print(filtered_df.head())
    else:
        print("Failed to load CSV file.")
