import pandas as pd

class NewaveLoader:
    """
    A class to load CSV files from the data/prices folder and return pandas DataFrames
    with the first column converted to date format.
    """
    
    def __init__(self, newave_path=None):
        """
        Initialize the CSVLoader.
        
        Args:
            newave_path (str, optional): Path to the energy marginal costs file. If None, uses default path.
        """
        if newave_path is None:
            # Default path to the prices CSV file
            self.newave_path = "data/newave/cmarg001.out"
        else:
            self.newave_path = newave_path
    
    def load_newave(self):
        """
        Load the cmargX.out file and return a pandas DataFrame with simulations order in the columns and
        dates in the index.
        
        Returns:
            pandas.DataFrame: DataFrame with dates in the index and the simulations marginal costs in the columns
        """
        #TODO create newave loader
        return None

    def filter_by_date_range(self, start_date=None, end_date=None):
        """
        Filter the data by date range.
        
        Args:
            start_date (str or datetime, optional): Start date for filtering
            end_date (str or datetime, optional): End date for filtering
            
        Returns:
            pandas.DataFrame: Filtered DataFrame
        """
        df = self.load_newave()
        if df is None:
            return None
        
        if start_date:
            start_date = pd.to_datetime(start_date)
            df = df[df.index >= start_date]
        
        if end_date:
            end_date = pd.to_datetime(end_date)
            df = df[df.index <= end_date]
        
        return df