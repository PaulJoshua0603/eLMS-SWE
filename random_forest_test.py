
import pickle
import pandas as pd

# Load model
with open('random_forest_model.pkl', 'rb') as model_file:
    loaded_model = pickle.load(model_file)

# sample data
new_data = pd.DataFrame({
    'EnglishOverall': [75],
    'MathematicsOverall': [75],
    'ScienceOverall': [75],
    'CRSOverall': [75]
})

predictions = loaded_model.predict(new_data)

# Display the predictions
print("Test Predictions:")
print(predictions)
