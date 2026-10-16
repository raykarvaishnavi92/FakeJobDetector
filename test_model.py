
import pickle

# Load the trained AI model
with open("job_model.pkl", "rb") as file:
    model = pickle.load(file)

# Test a job description
job = input("Enter a job description: ")

# Predict the result
result = model.predict([job])

print("Prediction:", result[0])
