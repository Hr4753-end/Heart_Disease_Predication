import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, precision_score, recall_score, f1_score # metrics(how your model is working on the dataset)
from sklearn.model_selection import train_test_split
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
data = pd.read_csv(os.path.join(base_dir, "Heart_Disease_Prediction.csv"))
print(data.head())

#Define Feature x&y
x = data.drop(columns =['Heart Disease'])
y = data['Heart Disease']

#3 Train test split
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size = 0.2,random_state = 42,stratify = y)

#4 featue Sclaing
scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

#5 Train logistic Regression Model
model = LogisticRegression(max_iter=1000)
model.fit(x_train,y_train )

#6 prediciton
y_pred = model.predict(x_test)

#7Evaluation
print("Accuracy:", accuracy_score(y_test,y_pred))
print("\nconfusionnMatrix:\n", confusion_matrix(y_test,y_pred))
print("\nclassification report:\n", classification_report(y_test,y_pred))

#8 NEw DAta
new_data = np.array([[35, 0, 3, 130, 250, 0, 1, 150, 0, 1.5, 2, 0, 2]])
new_data_scaled = scaler.transform(new_data)

prediction = model.predict(new_data_scaled)
print(prediction)

# --- Visualizations ---
sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle('Heart Disease Prediction - Model Evaluation', fontsize=16)

# 1. Class Distribution (Healthy vs Disease)
sns.countplot(x=y, ax=axes[0, 0], palette='Set2')
axes[0, 0].set_title('Class Distribution (Healthy vs Disease)')
axes[0, 0].set_xlabel('Heart Disease Status')
axes[0, 0].set_ylabel('Count')

# 2. Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[0, 1], 
            xticklabels=model.classes_, yticklabels=model.classes_)
axes[0, 1].set_title('Confusion Matrix')
axes[0, 1].set_xlabel('Predicted Label')
axes[0, 1].set_ylabel('True Label')

# 3. Performance Metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, pos_label='Presence')
recall = recall_score(y_test, y_pred, pos_label='Presence')
f1 = f1_score(y_test, y_pred, pos_label='Presence')

metrics_names = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
metrics_values = [accuracy, precision, recall, f1]

# Passing palette without hue is deprecated in newer seaborn, but it works. Better to set hue.
sns.barplot(x=metrics_names, y=metrics_values, ax=axes[1, 0], palette='viridis', hue=metrics_names, legend=False)
axes[1, 0].set_ylim(0, 1)
axes[1, 0].set_title('Performance Metrics')
axes[1, 0].set_ylabel('Score')
for i, v in enumerate(metrics_values):
    axes[1, 0].text(i, v + 0.02, f'{v:.2f}', ha='center', fontweight='bold')

# 4. Prediction Probability Distribution
prob_presence = model.predict_proba(x_test)[:, list(model.classes_).index('Presence')]
sns.histplot(prob_presence, bins=20, kde=True, ax=axes[1, 1], color='coral')
axes[1, 1].set_title('Prediction Probability Distribution (Presence)')
axes[1, 1].set_xlabel('Probability of Presence')
axes[1, 1].set_ylabel('Frequency')

plt.tight_layout()
plt.show()