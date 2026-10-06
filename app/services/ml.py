from pathlib import Path
import joblib
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_PATH = BASE_DIR / 'models' / 'sentiment_model.pkl'

TRAINING_DATA = [
    ('excellent support and quick resolution', 'Positive'),
    ('thank you the issue was solved quickly', 'Positive'),
    ('very happy with the service', 'Positive'),
    ('great experience and helpful agent', 'Positive'),
    ('the product works perfectly now', 'Positive'),
    ('terrible service and no response', 'Negative'),
    ('I am frustrated and disappointed', 'Negative'),
    ('issue is still not fixed', 'Negative'),
    ('very poor support experience', 'Negative'),
    ('this is unacceptable and urgent', 'Negative'),
    ('I need more information about my account', 'Neutral'),
    ('can you explain the billing details', 'Neutral'),
    ('please provide an update on my request', 'Neutral'),
    ('I have a question about the product', 'Neutral'),
    ('how can I change my profile settings', 'Neutral'),
]


def train_model():
    texts, labels = zip(*TRAINING_DATA)
    model = Pipeline([
        ('tfidf', TfidfVectorizer(ngram_range=(1, 2), lowercase=True)),
        ('classifier', LogisticRegression(max_iter=1000)),
    ])
    model.fit(texts, labels)
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    return model


def get_model():
    if MODEL_PATH.exists():
        try:
            return joblib.load(MODEL_PATH)
        except Exception:
            pass
    return train_model()


def predict_sentiment(text):
    model = get_model()
    return str(model.predict([text])[0])
