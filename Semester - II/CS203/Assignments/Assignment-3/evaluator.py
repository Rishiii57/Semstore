"""
BlackBoxEvaluator -- Provided to students for Assignment 3, Task 5.
Do not modify this file.
"""
import torch
import pandas as pd
from transformers import AutoTokenizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import warnings

warnings.filterwarnings("ignore")


class BlackBoxEvaluator:
    def __init__(self, embedder_path="text_embedder.pt"):
        """Initializes the frozen PyTorch model for feature extraction."""
        print("Initializing Black-Box Embedder...")
        self.model = torch.jit.load(embedder_path)
        self.model.eval()
        self.tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
        print("Embedder loaded successfully.\n")

    def extract_features(self, texts):
        """Converts raw text into numerical feature arrays."""
        inputs = self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=128,
            return_tensors="pt",
        )
        with torch.no_grad():
            features = self.model(inputs["input_ids"], inputs["attention_mask"])
        return features.numpy()

    def run_evaluation(
        self,
        train_df,
        test_df,
        text_col="review",
        label_col="label",
        model_name="Model",
    ):
        """Extracts features, trains a classifier, and evaluates performance.
        Automatically removes any test reviews from the training set to prevent data leakage."""
        print(f"--- Evaluating: {model_name} ---")

        test_reviews = set(test_df[text_col].tolist())
        clean_train = train_df[~train_df[text_col].isin(test_reviews)].copy()
        print(f"Training on {len(clean_train)} samples (excluded {len(train_df) - len(clean_train)} test overlaps)...")

        X_train = self.extract_features(clean_train[text_col].tolist())
        y_train = clean_train[label_col].tolist()

        X_test = self.extract_features(test_df[text_col].tolist())
        y_test = test_df[label_col].tolist()

        clf = LogisticRegression(max_iter=1000, class_weight="balanced")
        clf.fit(X_train, y_train)

        y_pred = clf.predict(X_test)
        acc = accuracy_score(y_test, y_pred)

        print(f"Accuracy: {acc * 100:.2f}%")
        print("Classification Report:")
        print(classification_report(y_test, y_pred))
        print("-" * 40 + "\n")
        return acc
