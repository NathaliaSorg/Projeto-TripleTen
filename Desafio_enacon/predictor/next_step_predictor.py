import pandas as pd
import numpy as np



class NextStepPredictor:
    """
    A class to predict next steps using a simple "copy last point" method for all columns.
    """
    
    def __init__(self, data: pd.DataFrame=None):
        """
        Initialize the NextStepPredictor.
        
        Args:
            data (pandas Dataframe, optional): pre-loaded data to use for prediction
        """

        self.data = data

    def predict_next_step(self, steps=1):
        """
        Predict the next step(s) using a simple "copy last point" method for all columns.
        
        Args:
            steps (int): Number of steps to predict (default: 1)
            
        Returns:
            pandas.DataFrame: DataFrame with predicted values for the next steps
        """
        if self.data is None:
            print("No data available. Please load data first.")
            return None
        
        if self.data.empty:
            print("Data is empty. Cannot make predictions.")
            return None
        
        # Get the last date and values
        last_date = self.data.index[-1]
        last_values = self.data.iloc[-1]
        
        # Create predictions for the next steps
        predictions = []
        
        for i in range(1, steps + 1):
            # Calculate next date (assuming weekly frequency based on the data)
            next_date = last_date + pd.DateOffset(weeks=i)
            
            # Create a row with the same values as the last point
            prediction_row = last_values.copy()
            prediction_row.name = next_date
            
            predictions.append(prediction_row)
        
        # Create DataFrame from predictions
        predictions_df = pd.DataFrame(predictions)
        
        return predictions_df
    
    def predict_with_confidence(self, steps=1, confidence_level=0.95):
        """
        Predict next steps with confidence intervals based on historical volatility.
        
        Args:
            steps (int): Number of steps to predict
            confidence_level (float): Confidence level for intervals (default: 0.95)
            
        Returns:
            dict: Dictionary containing predictions and confidence intervals
        """
        if self.data is None:
            return {"error": "No data available"}
        
        # Get basic prediction
        predictions = self.predict_next_step(steps)
        if predictions is None:
            return {"error": "Failed to generate predictions"}
        
        # Calculate historical volatility for each column
        returns = self.data.pct_change().dropna()
        volatilities = returns.std()
        
        # Calculate z-score for confidence level
        try:
            from scipy import stats
            z_score = stats.norm.ppf(1 - (1 - confidence_level) / 2)
        except ImportError:
            # Fallback if scipy is not available
            z_score = 1.96  # Approximate z-score for 95% confidence
        
        # Create confidence intervals
        confidence_intervals = {}
        
        for column in predictions.columns:
            if column in volatilities:
                vol = volatilities[column]
                center = predictions[column].values
                
                # Calculate confidence intervals
                upper = center * (1 + z_score * vol)
                lower = center * (1 - z_score * vol)
                
                confidence_intervals[column] = {
                    'prediction': center,
                    'upper_bound': upper,
                    'lower_bound': lower
                }
        
        return {
            'predictions': predictions,
            'confidence_intervals': confidence_intervals,
            'volatilities': volatilities.to_dict(),
            'confidence_level': confidence_level
        }
    
    def evaluate_prediction(self, test_data, steps=1):
        """
        Evaluate the prediction method on test data.
        
        Args:
            test_data (pandas.DataFrame): Test data for evaluation
            steps (int): Number of steps to predict
            
        Returns:
            dict: Evaluation metrics
        """
        if self.data is None:
            return {"error": "No training data available"}
        
        # Ensure test_data has the same columns as training data
        common_columns = set(self.data.columns) & set(test_data.columns)
        if not common_columns:
            return {"error": "No common columns between training and test data"}
        
        evaluation_results = {}
        
        for column in common_columns:
            if column in self.data.columns and column in test_data.columns:
                # Get the last value from training data
                last_value = self.data[column].iloc[-1]
                
                # Get actual values from test data
                actual_values = test_data[column].head(steps).values
                
                # Generate predictions (copy last value)
                predictions = np.full(steps, last_value)
                
                # Calculate metrics
                mae = np.mean(np.abs(predictions - actual_values))
                mse = np.mean((predictions - actual_values) ** 2)
                rmse = np.sqrt(mse)
                
                # Calculate MAPE (Mean Absolute Percentage Error)
                # Avoid division by zero
                valid_mask = actual_values != 0
                if valid_mask.any():
                    mape = np.mean(np.abs((predictions[valid_mask] - actual_values[valid_mask]) / actual_values[valid_mask])) * 100
                else:
                    mape = float('inf')
                
                evaluation_results[column] = {
                    'MAE': mae,
                    'MSE': mse,
                    'RMSE': rmse,
                    'MAPE': mape,
                    'last_value': last_value,
                    'predictions': predictions.tolist(),
                    'actual_values': actual_values.tolist()
                }
        
        return evaluation_results
    
    def get_prediction_summary(self, steps=1):
        """
        Get a summary of the next predictions.
        
        Args:
            steps (int): Number of steps to predict
            
        Returns:
            dict: Summary of predictions
        """
        predictions = self.predict_next_step(steps)
        
        if predictions is None:
            return {"error": "Failed to generate predictions"}
        
        summary = {
            'prediction_dates': predictions.index.tolist(),
            'columns': list(predictions.columns),
            'predictions': predictions.to_dict('list'),
            'data_info': {
                'last_date': self.data.index[-1] if self.data is not None else None,
                'data_shape': self.data.shape if self.data is not None else None,
                'date_range': {
                    'start': self.data.index[0] if self.data is not None else None,
                    'end': self.data.index[-1] if self.data is not None else None
                } if self.data is not None else None
            }
        }
        
        return summary


# Example usage and testing
if __name__ == "__main__":
    # Create an instance of the NextStepPredictor
    predictor = NextStepPredictor()
    
    if predictor.data is not None:
        print("Data loaded successfully!")
        print(f"Data shape: {predictor.data.shape}")
        print(f"Date range: {predictor.data.index[0]} to {predictor.data.index[-1]}")
        print(f"Columns: {list(predictor.data.columns)}")
        
        # Test basic prediction
        print("\n=== Basic Prediction Test ===")
        predictions = predictor.predict_next_step(steps=3)
        if predictions is not None:
            print("Next 3 steps predictions:")
            print(predictions)
        
        # Test prediction with confidence intervals
        print("\n=== Prediction with Confidence Intervals ===")
        confidence_pred = predictor.predict_with_confidence(steps=2)
        if 'predictions' in confidence_pred:
            print("Predictions with 95% confidence intervals:")
            print(confidence_pred['predictions'])
            print("\nVolatilities:")
            for col, vol in confidence_pred['volatilities'].items():
                print(f"{col}: {vol:.4f}")
        
        # Test prediction summary
        print("\n=== Prediction Summary ===")
        summary = predictor.get_prediction_summary(steps=2)
        if 'predictions' in summary:
            print("Prediction summary:")
            print(f"Prediction dates: {summary['prediction_dates']}")
            print(f"Columns: {summary['columns']}")
        
        # Example of evaluation (using last 10 rows as test data)
        print("\n=== Evaluation Example ===")
        if len(predictor.data) > 10:
            train_data = predictor.data.iloc[:-10]
            test_data = predictor.data.iloc[-10:]
            
            # Create a new predictor with training data only
            eval_predictor = NextStepPredictor()
            eval_predictor.data = train_data
            
            evaluation = eval_predictor.evaluate_prediction(test_data, steps=3)
            if 'error' not in evaluation:
                print("Evaluation results for first 3 columns:")
                for i, (col, metrics) in enumerate(evaluation.items()):
                    if i < 3:  # Show only first 3 columns for brevity
                        print(f"\n{col}:")
                        print(f"  MAE: {metrics['MAE']:.4f}")
                        print(f"  RMSE: {metrics['RMSE']:.4f}")
                        print(f"  MAPE: {metrics['MAPE']:.2f}%")
