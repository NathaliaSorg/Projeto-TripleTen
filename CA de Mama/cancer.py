from sklearn.datasets import load_breast_cancer
from sklearn.inspection import DecisionBoundaryDisplay
from sklearn.svm import SVC
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import StandardScaler

#load cancer dataset
cancer = load_breast_cancer()
X = cancer.data[:, :2]
y = cancer.target #[0,1] ie malignent:0, benign:1

#map y to signed labels t in {-1, +1}
t = np.where(y == 0, -1, +1)

# optional: scaling often helps SVM (uncomment if desired)
scaler = StandardScaler()
X = scaler.fit_transform(X)

#train svm
svm = SVC(kernel='linear', C=1)
svm.fit(X, y)

w = svm.coef_.ravel()
b = svm.intercept_[0]
norm_w = np.linalg.norm(w)
dist = (X @ w + b) / norm_w

margin_val = t * dist

tol = 1e-3
on_margin_idx = np.where(np.isclose(margin_val, 1.0, atol=tol))[0]
inside_idx = np.where((margin_val > 0) & (margin_val < 1 - tol))[0]   # strictly inside
misclassified_idx = np.where(margin_val <= 0 + tol)[0]
outside_idx = np.where(margin_val > 1 + tol)[0]

print("On margin (with tol):", on_margin_idx)
print("Inside margin:", inside_idx)
print("Misclassified:", misclassified_idx)
print("Outside margin:", outside_idx)
print("w (normal vector):", w)
print("b (bias):", b)
print("||w|| (norm):", norm_w)
print("Margin width (gamma = 1/||w||):", 1.0 / norm_w)

# --- get Lagrange multipliers (alphas) for all samples ---
# For binary SVC, svm.support_ lists indices of support vectors,
# and svm.dual_coef_[0] gives (t_i * alpha_i) for each support vector in the same order.
dual = svm.dual_coef_[0]              # shape (n_SV,) = t_i * alpha_i for SVs
alphas = np.zeros(X.shape[0])
alphas[svm.support_] = np.abs(dual)   # alp

# categorize alphas relative to C
C = svm.C
sv_at_C = np.where(np.isclose(alphas, C, atol=1e-8))[0]
sv_between = np.where((alphas > 1e-12) & (alphas < C - 1e-8))[0]
print("Number of support vectors:", len(svm.support_))
print("Support vector indices:", svm.support_)
print("SVs with alpha == C (likely inside/misclassified):", sv_at_C)
print("SVs with 0 < alpha < C (on-margin):", sv_between)

plt.figure(figsize=(8,6))
DecisionBoundaryDisplay.from_estimator(
    svm, X, response_method='predict',
    alpha=0.8, cmap='Pastel1',
    xlabel=cancer.feature_names[0],
    ylabel=cancer.feature_names[1],
)

plt.scatter(X[:, 0], X[:, 1], s=120, 
          c=y,  edgecolors='k', label='data')
# mark categories
plt.scatter(X[outside_idx,0], X[outside_idx,1], marker='o', s=35, facecolors='none', edgecolors='green', label='Outside margin')
plt.scatter(X[inside_idx,0], X[inside_idx,1], marker='s', s=60, facecolors='none', edgecolors='orange', label='Inside margin')
plt.scatter(X[misclassified_idx,0], X[misclassified_idx,1], marker='x', s=60, color='red', label='Misclassified')

# highlight support vectors
plt.scatter(X[svm.support_,0], X[svm.support_,1], s=140, facecolors='none', edgecolors='red', linewidths=2, label='Support Vectors')

plt.legend(loc='best')
plt.title("SVM decision regions + categorized samples")
plt.show()