import pandas as pd
import joblib
import matplotlib.pyplot as plt   
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

data = pd.read_csv("../data/crop_dataset_expanded_with_season-1.csv")

# Encode Soil
soil_mapping = {
    "clay": 0,
    "loamy": 1,
    "sandy": 2,
    "black": 3,
    "alluvial": 4
}
data["soil_type"] = data["soil_type"].map(soil_mapping)

# Encode Season
season_mapping = {
    "Kharif": 0,
    "Rabi": 1,
    "Zaid": 2
}
data["season"] = data["season"].map(season_mapping)

# Features
X = data[["soil_type", "season", "temperature", "humidity", "rainfall"]]
y = data["crop"]

# Encode target
crop_categories = y.unique()
crop_mapping = {crop: idx for idx, crop in enumerate(crop_categories)}
y = y.map(crop_mapping)

# Train test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model
model = RandomForestClassifier(
    n_estimators=300,
    max_depth=12,
    random_state=42
)

model.fit(X_train, y_train)

# Accuracy
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)

print("Accuracy:", acc)


# =========================
# 📊 ADD GRAPH HERE
# =========================
plt.figure()
plt.bar(["Model Accuracy"], [acc * 100])
plt.title("Crop Prediction Model Accuracy")
plt.ylabel("Accuracy (%)")

# Show graph
plt.show()

# Save graph (for report)
plt.savefig("../models/accuracy_chart.png")
# =========================


# Save model
joblib.dump(model, "../models/crop_model.pkl")
joblib.dump(crop_categories, "../models/crop_labels.pkl")

print("Model trained successfully!")