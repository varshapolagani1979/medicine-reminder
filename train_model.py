import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Training dataset
data = {
    "frequency_per_day": [
        1, 1, 1, 1, 2, 2, 2, 2,
        3, 3, 3, 3, 1, 2, 3, 1,
        2, 3, 2, 1
    ],

    "doses_per_day": [
        1, 1, 2, 1, 2, 2, 3, 2,
        3, 3, 2, 3, 1, 2, 3, 1,
        2, 3, 2, 1
    ],

    "missed_reminders": [
        0, 1, 0, 2, 1, 2, 0, 3,
        2, 4, 1, 3, 0, 1, 5, 0,
        2, 4, 1, 0
    ],

    "reminder_hour": [
        9, 10, 8, 20, 9, 14, 8, 21,
        8, 13, 20, 7, 10, 15, 8, 9,
        12, 21, 14, 10
    ],

    "priority": [
        "Low", "Low", "Low", "Medium",
        "Medium", "Medium", "Medium", "High",
        "High", "High", "Medium", "High",
        "Low", "Medium", "High", "Low",
        "Medium", "High", "Medium", "Low"
    ]
}

df = pd.DataFrame(data)

# Input features
X = df[
    [
        "frequency_per_day",
        "doses_per_day",
        "missed_reminders",
        "reminder_hour"
    ]
]

# Target
y = df["priority"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)

# Create ML model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

# Train
model.fit(X_train, y_train)

# Test
predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("Model trained successfully!")
print(f"Model accuracy: {accuracy * 100:.2f}%")

# Save model
joblib.dump(model, "medicine_model.pkl")

print("Model saved as medicine_model.pkl")