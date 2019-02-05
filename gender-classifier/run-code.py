from sklearn import tree
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import numpy as np

# Data and labels
X = [[181, 80, 44], [177, 70, 43], [160, 60, 38], [154, 54, 37], [166, 65, 40],
     [190, 90, 47], [175, 64, 39], [177, 70, 40], [159, 55, 37], [171, 75, 42],
     [181, 85, 43]]

Y = ['male', 'female', 'female', 'female', 'male', 'male', 'male', 'female',
     'male', 'female', 'male']

# Classifiers - use default hyperparameters
clf_tree = tree.DecisionTreeClassifier()
clf_svc = SVC()
clf_knn = KNeighborsClassifier()
clf_rf = RandomForestClassifier()

# Train the models
clf_tree.fit(X, Y)
clf_svc.fit(X, Y)
clf_knn.fit(X, Y)
clf_rf.fit(X, Y)

# Test the models using the initial data
pred_tree = clf_tree.predict(X)
acc_tree = accuracy_score(Y, pred_tree) * 100
print('Accuracy for Decision Tree: {}'.format(acc_tree))

pred_svc = clf_svc.predict(X)
acc_svc = accuracy_score(Y, pred_svc) * 100
print('Accuracy for SVC: {}'.format(acc_svc))

pred_knn = clf_knn.predict(X)
acc_knn = accuracy_score(Y, pred_knn) * 100
print('Accuracy for KNN: {}'.format(acc_knn))

pred_rf = clf_rf.predict(X)
acc_rf = accuracy_score(Y, pred_rf) * 100
print('Accuracy for Random Forest: {}'.format(acc_rf))

# What is the best classifier of SVC, KNN, and RF?
index = np.argmax([acc_svc, acc_knn, acc_rf])
classifiers = {0: 'SVC', 1: 'KNN', 2: 'Random Forest'}
print('The best gender classifier is {}.'.format(classifiers[index]))
