
from predictor.next_step_predictor import NextStepPredictor
from loaders.csv_loader import CSVLoader

# Example usage and testing
# Create an instance of the NextStepPredictor

data = CSVLoader().load_csv()
predictor = NextStepPredictor(data)

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
        eval_predictor = NextStepPredictor(None)
        eval_predictor.data = train_data
        
        evaluation = eval_predictor.evaluate_prediction(test_data, steps=3)
        if 'error' not in evaluation:
            print("Evaluation results:")
            for i, (col, metrics) in enumerate(evaluation.items()):
                
                print(f"\n{col}:")
                print(f"  MAE: {metrics['MAE']:.4f}")
                print(f"  RMSE: {metrics['RMSE']:.4f}")
                print(f"  MAPE: {metrics['MAPE']:.2f}%")
        else:
            print(f"Evaluation error: {evaluation['error']}")
    
else:
    print("Failed to load data.")
