from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import numpy as np
import joblib


class TextAnalyzer:
    def __init__(self, method="bag_of_words"):
        self.method = method
        self.model = None

        if method == "bag_of_words":
            self.vectorizer = TfidfVectorizer()
            self.model = joblib.load("models/bag_of_words_model.pkl")
        elif method == "topic_classifier":
            self.model = joblib.load("models/topic_classifier.pkl")
        elif method == "zero_shot":
            from transformers import pipeline
            self.model = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
        else:
            raise ValueError(f"Unknown method: {method}")

    def analyze_content(self, content):
        """
        Analyze post content and return sentiment and label.
        """
        if self.method in ["bag_of_words", "topic_classifier"]:
            vectorized = self.vectorizer.transform([content])
            prediction = self.model.predict(vectorized)[0]
            sentiment = self._get_sentiment(prediction)
        elif self.method == "zero_shot":
            result = self.model(content, candidate_labels=["sport", "disaster", "politics"])
            label = result["labels"][0]
            sentiment = "POSITIVE" if label == "sport" else "NEGATIVE"
        return sentiment, label

    def _get_sentiment(self, label):
        return "POSITIVE" if label == "sport" else "NEGATIVE"
