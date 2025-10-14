import pytest
import pandas as pd
import numpy as np
import tempfile
import shutil
import os
from datetime import datetime
from predictor.next_step_predictor import NextStepPredictor


class TestNextStepPredictor:
    """Test cases for NextStepPredictor class."""
    
    def setup_method(self):
        """Setup test fixtures before each test method."""
        # Create test data
        dates = pd.date_range('2020-01-01', periods=20, freq='W')
        data = {
            'M + 0': np.arange(100, 120),
            'M + 1': np.arange(200, 220),
            'M + 2': np.arange(300, 320)
        }
        
        self.test_data = pd.DataFrame(data, index=dates)
        self.test_data.index.name = 'Date'
        
        # Initialize predictor with test data
        self.predictor = NextStepPredictor(data=self.test_data)
    
    def test_init_with_data(self):
        """Test initialization with data parameter."""
        predictor = NextStepPredictor(data=self.test_data)
        assert predictor.data is not None
        assert predictor.data.equals(self.test_data)
    
    def test_init_without_data(self):
        """Test initialization without data parameter."""
        predictor = NextStepPredictor()
        assert predictor.data is None
    
    def test_predict_next_step_success(self):
        """Test successful next step prediction."""
        predictions = self.predictor.predict_next_step(steps=3)
        
        assert predictions is not None
        assert isinstance(predictions, pd.DataFrame)
        assert len(predictions) == 3
        assert list(predictions.columns) == ['M + 0', 'M + 1', 'M + 2']
        
        # Check that predictions are the same as last values
        last_values = self.test_data.iloc[-1]
        for col in predictions.columns:
            # Compare values directly (ignore index for comparison)
            assert predictions[col].tolist() == [last_values[col]] * 3
    
    def test_predict_next_step_no_data(self):
        """Test prediction when no data is available."""
        predictor = NextStepPredictor()  # No data
        predictions = predictor.predict_next_step()
        
        assert predictions is None
    
    def test_predict_next_step_empty_data(self):
        """Test prediction when data is empty."""
        empty_data = pd.DataFrame()
        predictor = NextStepPredictor(data=empty_data)
        predictions = predictor.predict_next_step()
        
        assert predictions is None
    
    def test_predict_next_step_default_steps(self):
        """Test prediction with default steps parameter."""
        predictions = self.predictor.predict_next_step()
        
        assert predictions is not None
        assert len(predictions) == 1  # Default should be 1 step
    
    def test_predict_next_step_date_calculation(self):
        """Test that dates are calculated correctly."""
        predictions = self.predictor.predict_next_step(steps=2)
        
        assert predictions is not None
        last_date = self.test_data.index[-1]
        
        # Check that dates are incremented by weeks
        expected_dates = [last_date + pd.DateOffset(weeks=1), 
                         last_date + pd.DateOffset(weeks=2)]
        assert predictions.index.tolist() == expected_dates
    
    def test_predict_with_confidence_success(self):
        """Test prediction with confidence intervals."""
        result = self.predictor.predict_with_confidence(steps=2)
        
        assert result is not None
        assert 'predictions' in result
        assert 'confidence_intervals' in result
        assert 'volatilities' in result
        assert 'confidence_level' in result
        
        assert isinstance(result['predictions'], pd.DataFrame)
        assert len(result['predictions']) == 2
        assert result['confidence_level'] == 0.95
    
    def test_predict_with_confidence_no_data(self):
        """Test confidence prediction when no data is available."""
        predictor = NextStepPredictor()  # No data
        result = predictor.predict_with_confidence()
        
        assert result == {"error": "No data available"}
    
    def test_predict_with_confidence_custom_level(self):
        """Test prediction with custom confidence level."""
        result = self.predictor.predict_with_confidence(confidence_level=0.90)
        
        assert result is not None
        assert result['confidence_level'] == 0.90
    
    def test_evaluate_prediction_success(self):
        """Test evaluation of prediction method."""
        # Create test data for evaluation
        test_dates = pd.date_range('2020-05-01', periods=5, freq='W')
        test_data = pd.DataFrame({
            'M + 0': [115, 116, 117, 118, 119],
            'M + 1': [215, 216, 217, 218, 219]
        }, index=test_dates)
        
        evaluation = self.predictor.evaluate_prediction(test_data, steps=3)
        
        assert evaluation is not None
        assert 'M + 0' in evaluation
        assert 'M + 1' in evaluation
        
        # Check evaluation metrics structure
        for col in ['M + 0', 'M + 1']:
            metrics = evaluation[col]
            assert 'MAE' in metrics
            assert 'MSE' in metrics
            assert 'RMSE' in metrics
            assert 'MAPE' in metrics
            assert 'last_value' in metrics
            assert 'predictions' in metrics
            assert 'actual_values' in metrics
    
    def test_evaluate_prediction_no_training_data(self):
        """Test evaluation when no training data is available."""
        predictor = NextStepPredictor()  # No data
        test_data = pd.DataFrame({'col': [1, 2, 3]})
        
        result = predictor.evaluate_prediction(test_data)
        
        assert result == {"error": "No training data available"}
    
    def test_evaluate_prediction_no_common_columns(self):
        """Test evaluation when there are no common columns."""
        test_data = pd.DataFrame({'different_col': [1, 2, 3]})
        
        result = self.predictor.evaluate_prediction(test_data)
        
        assert result == {"error": "No common columns between training and test data"}
    
    def test_evaluate_prediction_with_zero_values(self):
        """Test evaluation when actual values contain zeros."""
        test_data = pd.DataFrame({
            'M + 0': [0, 0, 0],  # Zero values
            'M + 1': [215, 216, 217]
        })
        
        evaluation = self.predictor.evaluate_prediction(test_data, steps=3)
        
        assert evaluation is not None
        # MAPE should be infinity for columns with zero values
        assert evaluation['M + 0']['MAPE'] == float('inf')
        assert evaluation['M + 1']['MAPE'] != float('inf')
    
    def test_get_prediction_summary_success(self):
        """Test getting prediction summary."""
        summary = self.predictor.get_prediction_summary(steps=2)
        
        assert summary is not None
        assert 'prediction_dates' in summary
        assert 'columns' in summary
        assert 'predictions' in summary
        assert 'data_info' in summary
        
        assert isinstance(summary['prediction_dates'], list)
        assert len(summary['prediction_dates']) == 2
        assert summary['columns'] == ['M + 0', 'M + 1', 'M + 2']
    
    def test_get_prediction_summary_no_data(self):
        """Test getting summary when no data is available."""
        predictor = NextStepPredictor()  # No data
        summary = predictor.get_prediction_summary()
        
        assert summary == {"error": "Failed to generate predictions"}
    
    def test_prediction_accuracy_metrics(self):
        """Test that prediction accuracy metrics are calculated correctly."""
        # Create simple test case
        train_data = pd.DataFrame({'col': [10, 20, 30]}, 
                                 index=pd.date_range('2020-01-01', periods=3, freq='W'))
        test_data = pd.DataFrame({'col': [40, 50]}, 
                                index=pd.date_range('2020-01-22', periods=2, freq='W'))
        
        predictor = NextStepPredictor(data=train_data)
        evaluation = predictor.evaluate_prediction(test_data, steps=2)
        
        # Last value in training data is 30
        # Test values are [40, 50]
        # MAE should be (|30-40| + |30-50|)/2 = (10 + 20)/2 = 15
        assert evaluation['col']['MAE'] == 15.0
        assert evaluation['col']['MSE'] == 250.0  # (100 + 400)/2 = 250
        assert evaluation['col']['RMSE'] == pytest.approx(15.811388, rel=1e-6)
    
    def test_confidence_intervals_structure(self):
        """Test that confidence intervals have correct structure."""
        result = self.predictor.predict_with_confidence(steps=1)
        
        assert 'confidence_intervals' in result
        intervals = result['confidence_intervals']
        
        for col in self.test_data.columns:
            if col in intervals:
                col_intervals = intervals[col]
                assert 'prediction' in col_intervals
                assert 'upper_bound' in col_intervals
                assert 'lower_bound' in col_intervals
                
                # Upper bound should be >= prediction >= lower bound
                pred = col_intervals['prediction'][0]
                upper = col_intervals['upper_bound'][0]
                lower = col_intervals['lower_bound'][0]
                
                assert upper >= pred >= lower
    
    def test_data_info_in_summary(self):
        """Test that data information is included in summary."""
        summary = self.predictor.get_prediction_summary()
        
        assert 'data_info' in summary
        data_info = summary['data_info']
        
        assert 'last_date' in data_info
        assert 'data_shape' in data_info
        assert 'date_range' in data_info
        
        assert data_info['data_shape'] == self.test_data.shape
        assert data_info['last_date'] == self.test_data.index[-1]


if __name__ == "__main__":
    pytest.main([__file__])
