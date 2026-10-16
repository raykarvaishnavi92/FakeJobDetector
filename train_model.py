
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
import pickle

# Load dataset
data = pd.read_csv("job_dataset.csv")

# Input and output
X = data["job_description"]
y = data["label"]

# Create AI model
model = make_pipeline(
    CountVectorizer(),
    LogisticRegression()
)

# Train the model
model.fit(X, y)

# Save the model
with open("job_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("AI model trained successfully!")
print("Model saved successfully!")
