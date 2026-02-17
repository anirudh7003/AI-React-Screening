"""
MODEL TRAINING SCRIPT – EMOTION CLASSIFICATION

Instructions:

1. Open this file in Google Colab (recommended) or any Python environment.
2. Upload the emotion dataset CSV file (must contain columns: 'text' and 'Emotion').
3. Update the dataset path if required.
4. Run all cells to train the model.
5. After successful training, two files will be generated:

    - emotion_model.pkl
    - vectorizer.pkl

6. Download these .pkl files and place them inside the backend/ directory.
7. The Flask backend loads these files for real-time emotion prediction.

Note:
- This script is only for training.
- The production backend uses the exported .pkl files.
"""


import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# Load dataset
df = pd.read_csv("/content/EmotionDetection.csv")

# Basic cleanup
df = df.dropna()

X = df["text"]
y = df["Emotion"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Vectorizer
vectorizer = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1,2),
    stop_words="english"
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Model
model = LogisticRegression(max_iter=1000)
model.fit(X_train_vec, y_train)

# Evaluation
y_pred = model.predict(X_test_vec)
print(classification_report(y_test, y_pred))
