"""Baseline for exercise 4 (same settings as the prompt)."""
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split, cross_val_score
X, y = load_iris(return_X_y=True)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
m = LogisticRegression(max_iter=200).fit(Xtr, ytr)
p = m.predict(Xte)
print(f"test accuracy      : {accuracy_score(yte, p):.4f}")
print(f"test macro F1      : {f1_score(yte, p, average='macro'):.4f}")
print(f"train accuracy     : {m.score(Xtr, ytr):.4f}")
cv = cross_val_score(LogisticRegression(max_iter=200), X, y, cv=5)
print(f"5-fold CV accuracy : {cv.mean():.4f}  (folds: {[round(float(v),3) for v in cv]})")
print("\nNote: different sklearn versions can change the 3rd-4th decimal; say which version you used.")
