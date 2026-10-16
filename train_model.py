
import pandas as pd
import pickle

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Load dataset
data = pd.read_csv("job_dataset.csv")

# Remove missing values
data = data.dropna(subset=["job_description", "label"])

# Input and output
X = data["job_description"].astype(str)
y = data["label"]

# Check dataset size and labels
print("Total records:", len(data))
print("\nLabel distribution:")
print(y.value_counts())

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Create AI model
model = make_pipeline(
    CountVectorizer(),
    LogisticRegression(max_iter=1000)
)

# Train model
model.fit(X_train, y_train)

# Test model
predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("\nModel Accuracy:", round(accuracy * 100, 2), "%")
print("\nClassification Report:")
print(classification_report(y_test, predictions, zero_division=0))

# Train final model on the full dataset for website use
model.fit(X, y)

# Save the final model
with open("job_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("\nAI model trained successfully!")
print("Final model saved successfully!")
