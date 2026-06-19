import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report
)
df = pd.read_csv("data/Churn.csv")
report_df = df.copy()
df.dropna(inplace=True)
le = LabelEncoder()

df["Churn"] = le.fit_transform(df["Churn"])
df_ml = df.drop("customerID", axis=1)
df_ml = pd.get_dummies(
    df_ml,
    drop_first=True
)
X = df_ml.drop("Churn", axis=1)

y = df_ml["Churn"]
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)
model = LogisticRegression(
    max_iter=2000
)
model.fit(
    X_train,
    y_train
)
predictions = model.predict(
    X_test
)
accuracy = accuracy_score(
    y_test,
    predictions
)

print(
    "Accuracy:",
    accuracy
)
cm = confusion_matrix(
    y_test,
    predictions
)

print(cm)
print(
    classification_report(
        y_test,
        predictions
    )
)
results = report_df.loc[
    X_test.index
].copy()
results["Predicted_Churn"] = predictions
results["Prediction"] = (
    results["Predicted_Churn"]
    .map({
        0: "Stay",
        1: "Leave"
    })
)
results["Churn_Probability"] = (
    model.predict_proba(X_test)[:,1]
)
def risk_level(prob):

    if prob >= 0.8:
        return "High Risk"

    elif prob >= 0.5:
        return "Medium Risk"

    else:
        return "Low Risk"

results["Risk_Category"] = (
    results["Churn_Probability"]
    .apply(risk_level)
)
results.to_csv(
    "predictions_clean.csv",
    index=False
)