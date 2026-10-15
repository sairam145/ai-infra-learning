import json, joblib
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score

# STAGE 1: DATA (tiny sample; real systems pull this from S3 or a database)
data = [
    ("Win a free iPhone now, click here", "spam"), ("You won $1000 cash prize", "spam"),
    ("Urgent: verify your bank account", "spam"), ("Cheap meds, no prescription", "spam"),
    ("Claim your free vacation today", "spam"), ("Limited offer: earn money fast", "spam"),
    ("Congratulations, you are selected", "spam"), ("Get rich quick with crypto", "spam"),
    ("Free gift card, act now", "spam"), ("Lowest price loans, apply today", "spam"),
        ("Your package is held, pay the fee now", "spam"), ("Your account is locked, login here", "spam"),
    ("Are we still meeting at 3pm?", "ham"), ("Can you send me the report?", "ham"),
    ("Dinner at my place tonight?", "ham"), ("The deploy finished successfully", "ham"),
    ("Happy birthday, have a great day", "ham"), ("Let's review the PR tomorrow", "ham"),
    ("Call me when you land", "ham"), ("Thanks for the help yesterday", "ham"),
    ("The meeting moved to Friday", "ham"), ("Can you pick up milk?", "ham"),
]
texts, labels = zip(*data)
X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.3, random_state=42, stratify=labels)

# STAGE 2: TRAIN
model = make_pipeline(TfidfVectorizer(), LogisticRegression())
model.fit(X_train, y_train)

# STAGE 3: EVALUATE on messages the model has never seen
pred = model.predict(X_test)
metrics = {
    "accuracy": accuracy_score(y_test, pred),
    "precision": precision_score(y_test, pred, pos_label="spam"),
    "recall": recall_score(y_test, pred, pos_label="spam"),
}

# VERSION IT: every model gets a unique name and its scores saved next to it
version = datetime.now().strftime("v%Y%m%d-%H%M%S")
joblib.dump(model, f"models/spam-{version}.joblib")
json.dump({"version": version, **metrics}, open(f"models/spam-{version}.json", "w"), indent=2)
print(f"Saved model {version}: {metrics}")
