class ai:
    svr="""import numpy as np
from sklearn import datasets
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, explained_variance_score
from sklearn.utils import shuffle
# Load housing data
data = datasets.load_boston()
# Shuffle the data
X, y = shuffle(data.data, data.target, random_state=7)
# Split the data into training and testing datasets
num_training = int(0.8 * len(X))
X_train, y_train = X[:num_training], y[:num_training]
X_test, y_test = X[num_training:], y[num_training:]
# Create Support Vector Regression model
sv_regressor = SVR(kernel='linear', C=1.0, epsilon=0.1)
# Train Support Vector Regressor
sv_regressor.fit(X_train, y_train)
# Evaluate performance of Support Vector Regressor
y_test_pred = sv_regressor.predict(X_test)
mse = mean_squared_error(y_test, y_test_pred)
evs = explained_variance_score(y_test, y_test_pred)
print("\n#### Performance ####")
print("Mean squared error =", round(mse, 2))
print("Explained variance score =", round(evs, 2))
# Test the regressor on test datapoint
test_data = [3.7, 0, 18.4, 1, 0.87, 5.95, 91, 2.5052, 26, 666, 20.2, 351.34, 15.27]
print("\nPredicted price:", sv_regressor.predict([test_data])[0])"""
    cluster_quality="""import numpy as np
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.cluster import KMeans
# Load data from input file
X = np.loadtxt('data_quality.txt', delimiter=',')
# Plot input data
plt.figure()
plt.scatter(X[:,0], X[:,1], color='black', s=80, marker='o', facecolors='none')
x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
plt.title('Input data')
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)
plt.xticks(())
plt.yticks(())
# Initialize variables
scores = []
values = np.arange(2, 10)
# Iterate through the defined range
for num_clusters in values:
 # Train the KMeans clustering model
 kmeans = KMeans(init='k-means++', n_clusters=num_clusters, n_init=10)
 kmeans.fit(X)
 score = metrics.silhouette_score(X, kmeans.labels_,
 metric='euclidean', sample_size=len(X))
 print("\nNumber of clusters =", num_clusters)
 print("Silhouette score =", score)

 scores.append(score)
# Plot silhouette scores
plt.figure()
plt.bar(values, scores, width=0.7, color='black', align='center')
plt.title('Silhouette score vs number of clusters')
# Extract best score and optimal number of clusters
num_clusters = np.argmax(scores) + values[0]
print('\nOptimal number of clusters =', num_clusters)
plt.show()"""
    confusion="""import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
# Define sample labels
true_labels = [2, 0, 0, 2, 4, 4, 1, 0, 3, 3, 3]
pred_labels = [2, 1, 0, 2, 4, 3, 1, 0, 1, 3, 3]
# Create confusion matrix
confusion_mat = confusion_matrix(true_labels, pred_labels)
# Visualize confusion matrix
plt.imshow(confusion_mat, interpolation='nearest', cmap=plt.cm.gray)
plt.title('Confusion matrix')
plt.colorbar()
ticks = np.arange(5)
plt.xticks(ticks, ticks)
plt.yticks(ticks, ticks)
plt.ylabel('True labels')
plt.xlabel('Predicted labels')
plt.show()
# Classification report
targets = ['Class-0', 'Class-1', 'Class-2', 'Class-3', 'Class-4']
print('\n', classification_report(true_labels, pred_labels, target_names=targets))"""
    decesion_tree="""import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
#from sklearn import cross_validation
from sklearn.model_selection import cross_validate
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from utilities2 import visualize_classifier
from sklearn import tree
import graphviz
# Load input data
input_file = 'data_decision_trees.txt'
data = np.loadtxt(input_file, delimiter=',')
X, y = data[:, :-1], data[:, -1]
# Separate input data into two classes based on labels
class_0 = np.array(X[y==0])
class_1 = np.array(X[y==1])
# Visualize input data
plt.figure()
plt.scatter(class_0[:, 0], class_0[:, 1], s=None, facecolors='black',
 edgecolors='blue', linewidth=1, marker='x')
plt.scatter(class_1[:, 0], class_1[:, 1], s=None, facecolors='white',
 edgecolors='red', linewidth=1, marker='o')
plt.title('Input data')
# Split data into training and testing datasets
X_train, X_test, y_train, y_test = train_test_split(
 X, y, test_size=0.25, random_state=5)
# Decision Trees classifier
params = {'random_state': 0, 'max_depth': 4}
classifier = DecisionTreeClassifier(**params)
classifier.fit(X_train, y_train)
visualize_classifier(classifier, X_train, y_train, 'Training dataset')
y_test_pred = classifier.predict(X_test)
visualize_classifier(classifier, X_test, y_test, 'Test dataset')
# Evaluate classifier performance
class_names = ['Class-0', 'Class-1']
print("\n" + "#"*40)
print("\nClassifier performance on training dataset\n")
print(classification_report(y_train, classifier.predict(X_train), target_names=class_names))
print("#"*40 + "\n")
print("#"*40)
print("\nClassifier performance on test dataset\n")
print(classification_report(y_test, y_test_pred, target_names=class_names))
print("#"*40 + "\n")
plt.show()
from sklearn.tree import export_graphviz
# Export as dot file
export_graphviz(classifier, out_file='tree1.dot',class_names=['0', '1'],rounded = True, proportion =
False, precision = 2, filled = True)"""
    eye="""import cv2
import numpy as np
# Load the Haar cascade files for face and eye
face_cascade = cv2.CascadeClassifier('haar_cascade_files/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haar_cascade_files/haarcascade_eye.xml')
# Check if the face cascade file has been loaded correctly
if face_cascade.empty():
raise IOError('Unable to load the face cascade classifier xml file')
# Check if the eye cascade file has been loaded correctly
if eye_cascade.empty():
raise IOError('Unable to load the eye cascade classifier xml file')
# Initialize the video capture object
cap = cv2.VideoCapture("head-pose-face-detection-male.mp4")
# Define the scaling factor
ds_factor = 0.5
# Iterate until the user hits the 'Esc' key
while True:
 # Capture the current frame
 _, frame = cap.read()
 # Resize the frame
 frame = cv2.resize(frame, None, fx=ds_factor, fy=ds_factor, interpolation=cv2.INTER_AREA)
 # Convert to grayscale
 gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
 # Run the face detector on the grayscale image
 faces = face_cascade.detectMultiScale(gray, 1.3, 5)
 # For each face that's detected, run the eye detector
 for (x,y,w,h) in faces:
 # Extract the grayscale face ROI
 roi_gray = gray[y:y+h, x:x+w]
 # Extract the color face ROI
 roi_color = frame[y:y+h, x:x+w]
 # Run the eye detector on the grayscale ROI
 eyes = eye_cascade.detectMultiScale(roi_gray)
 # Draw circles around the eyes
 for (x_eye,y_eye,w_eye,h_eye) in eyes:
 center = (int(x_eye + 0.5*w_eye), int(y_eye + 0.5*h_eye))
 radius = int(0.3 * (w_eye + h_eye))
 color = (0, 255, 0)
 thickness = 3
 cv2.circle(roi_color, center, radius, color, thickness)
 # Display the output
 cv2.imshow('Eye Detector', frame)
 # Check if the user hit the 'Esc' key
 c = cv2.waitKey(1)
 if c == 27:
 break
# Release the video capture object
cap.release()
# Close all the windows
cv2.destroyAllWindows()"""
    svc="""import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.svm import LinearSVC
from sklearn.multiclass import OneVsOneClassifier
import warnings
warnings.filterwarnings("ignore")
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
# Input file containing data
input_file = 'income_data.txt'
# Read the data
X = []
y = []
count_class1 = 0
count_class2 = 0
max_datapoints = 25000
with open(input_file, 'r') as f:
 for line in f.readlines():
 if count_class1 >= max_datapoints and count_class2 >= max_datapoints:
 break
 if '?' in line:
 continue
 data = line[:-1].split(', ')
 if data[-1] == '<=50K' and count_class1 < max_datapoints:
 X.append(data)
 count_class1 += 1
 if data[-1] == '>50K' and count_class2 < max_datapoints:
 X.append(data)
 count_class2 += 1
# Convert to numpy array
X = np.array(X)
# Convert string data to numerical data
label_encoder = []
X_encoded = np.empty(X.shape)
for i,item in enumerate(X[0]):
 if item.isdigit():
 X_encoded[:, i] = X[:, i]
 else:
 label_encoder.append(preprocessing.LabelEncoder())
 X_encoded[:, i] = label_encoder[-1].fit_transform(X[:, i])
X = X_encoded[:, :-1].astype(int)
y = X_encoded[:, -1].astype(int)
# Create SVM classifier
classifier = OneVsOneClassifier(LinearSVC(random_state=0))
# Train the classifier
classifier.fit(X, y)
# Cross validation
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=5)
classifier = OneVsOneClassifier(LinearSVC(random_state=0))
classifier.fit(X_train, y_train)
y_test_pred = classifier.predict(X_test)
# Compute the F1 score of the SVM classifier
f1 = cross_val_score(classifier, X, y, scoring='f1_weighted', cv=3)
print("F1 score: " + str(round(100*f1.mean(), 2)) + "%")"""
    kmeans="""import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn import metrics
# Load input data
X = np.loadtxt('data_clustering.txt', delimiter=',')
num_clusters = 5
# Plot input data
plt.figure()
plt.scatter(X[:,0], X[:,1], marker='o', facecolors='none',
 edgecolors='black', s=80)
x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
plt.title('Input data')
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)
plt.xticks(())
plt.yticks(())
# Create KMeans object
kmeans = KMeans(init='k-means++', n_clusters=num_clusters, n_init=10)
# Train the KMeans clustering model
kmeans.fit(X)
# Step size of the mesh
step_size = 0.01
# Define the grid of points to plot the boundaries
x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
x_vals, y_vals = np.meshgrid(np.arange(x_min, x_max, step_size),
 np.arange(y_min, y_max, step_size))
# Predict output labels for all the points on the grid
output = kmeans.predict(np.c_[x_vals.ravel(), y_vals.ravel()])
# Plot different regions and color them 
output = output.reshape(x_vals.shape)
plt.figure()
plt.clf()
plt.imshow(output, interpolation='nearest',
 extent=(x_vals.min(), x_vals.max(),
 y_vals.min(), y_vals.max()),
 cmap=plt.cm.Paired,
 aspect='auto',
 origin='lower')
# Overlay input points
plt.scatter(X[:,0], X[:,1], marker='o', facecolors='none',
 edgecolors='black', s=80)
# Plot the centers of clusters
cluster_centers = kmeans.cluster_centers_
plt.scatter(cluster_centers[:,0], cluster_centers[:,1],
 marker='o', s=210, linewidths=4, color='black',
 zorder=12, facecolors='black')
x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
plt.title('Boundaries of clusters')
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)
plt.xticks(())
plt.yticks(())
plt.show()"""
    linear_regression="""import pickle
import numpy as np
from sklearn import linear_model
import sklearn.metrics as sm
import matplotlib.pyplot as plt
# Input file containing data
input_file = 'data_singlevar_regr.txt'
# Read data
data = np.loadtxt(input_file, delimiter=',')
X, y = data[:, :-1], data[:, -1]
# Train and test split
num_training = int(0.8 * len(X))
num_test = len(X) - num_training
# Training data
X_train, y_train = X[:num_training], y[:num_training]
# Test data
X_test, y_test = X[num_training:], y[num_training:]
# Create linear regressor object
regressor = linear_model.LinearRegression()
# Train the model using the training sets
regressor.fit(X_train, y_train)
# Predict the output
y_test_pred = regressor.predict(X_test)
# Plot outputs
plt.scatter(X_test, y_test, color='green')
plt.plot(X_test, y_test_pred, color='black', linewidth=4)
plt.xticks(())
plt.yticks(())
plt.show()
# Compute performance metrics
print("Linear regressor performance:")
print("Mean absolute error =", round(sm.mean_absolute_error(y_test, y_test_pred), 2))
print("Mean squared error =", round(sm.mean_squared_error(y_test, y_test_pred), 2))
print("Median absolute error =", round(sm.median_absolute_error(y_test, y_test_pred), 2))
print("Explain variance score =", round(sm.explained_variance_score(y_test, y_test_pred), 2))
print("R2 score =", round(sm.r2_score(y_test, y_test_pred), 2))
# Model persistence
output_model_file = 'model.pkl'
# Save the model
with open(output_model_file, 'wb') as f:
 pickle.dump(regressor, f)
# Load the model
with open(output_model_file, 'rb') as f:
 regressor_model = pickle.load(f)
# Perform prediction on test data
y_test_pred_new = regressor_model.predict(X_test)
print("\nNew mean absolute error =", round(sm.mean_absolute_error(y_test, y_test_pred_new), 2))"""
    logistic="""import numpy as np
from sklearn import linear_model
import matplotlib.pyplot as plt
from utilities import visualize_classifier
# Define sample input data
X = np.array([[3.1, 7.2], [4, 6.7], [2.9, 8], [5.1, 4.5], [6, 5], [5.6, 5], [3.3, 0.4], [3.9, 0.9], [2.8, 1], [0.5,
3.4], [1, 4], [0.6, 4.9]])
y = np.array([0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3])
# Create the logistic regression classifier
classifier = linear_model.LogisticRegression(solver='liblinear', C=1)
#classifier = linear_model.LogisticRegression(solver='liblinear', C=100)
# Train the classifier
classifier.fit(X, y)
# Visualize the performance of the classifier
visualize_classifier(classifier, X, y)"""
    mean_shift="""import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import MeanShift, estimate_bandwidth
from itertools import cycle
# Load data from input file
X = np.loadtxt('data_clustering.txt', delimiter=',')
# Estimate the bandwidth of X
bandwidth_X = estimate_bandwidth(X, quantile=0.1, n_samples=len(X))
# Cluster data with MeanShift
meanshift_model = MeanShift(bandwidth=bandwidth_X, bin_seeding=True)
meanshift_model.fit(X)
# Extract the centers of clusters
cluster_centers = meanshift_model.cluster_centers_
print('\nCenters of clusters:\n', cluster_centers)
# Estimate the number of clusters
labels = meanshift_model.labels_
num_clusters = len(np.unique(labels))
print("\nNumber of clusters in input data =", num_clusters)
# Plot the points and cluster centers
plt.figure()
markers = 'o*xvs'
for i, marker in zip(range(num_clusters), markers):
 # Plot points that belong to the current cluster
 plt.scatter(X[labels==i, 0], X[labels==i, 1], marker=marker, color='black')
 # Plot the cluster center
 cluster_center = cluster_centers[i]
 plt.plot(cluster_center[0], cluster_center[1], marker='o', 
 markerfacecolor='black', markeredgecolor='black',
 markersize=15)
plt.title('Clusters')
plt.show()"""
    naive_bayes="""import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from utilities import visualize_classifier
import sklearn
# Input file containing data
input_file = 'data_multivar_nb.txt'
# Load data from input file
data = np.loadtxt(input_file, delimiter=',')
X, y = data[:, :-1], data[:, -1]
# Create Naive Bayes classifier
classifier = GaussianNB()
# Train the classifier
classifier.fit(X, y)
# Predict the values for training data
y_pred = classifier.predict(X)
# Compute accuracy
accuracy = 100.0 * (y == y_pred).sum() / X.shape[0]
print("Accuracy of Naive Bayes classifier =", round(accuracy, 2), "%")
# Visualize the performance of the classifier
visualize_classifier(classifier, X, y)
###############################################
# Cross validation
# Split data into training and test data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=3)
classifier_new = GaussianNB()
classifier_new.fit(X_train, y_train)
y_test_pred = classifier_new.predict(X_test)
# compute accuracy of the classifier
accuracy = 100.0 * (y_test == y_test_pred).sum() / X_test.shape[0]
print("Accuracy of the new classifier =", round(accuracy, 2), "%")
# Visualize the performance of the classifier
visualize_classifier(classifier_new, X_test, y_test)
###############################################
# Scoring functions
num_folds = 3
accuracy_values = sklearn.model_selection.cross_val_score(classifier,
 X, y, scoring='accuracy', cv=num_folds)
print("Accuracy: " + str(round(100*accuracy_values.mean(), 2)) + "%")
precision_values = sklearn.model_selection.cross_val_score(classifier,
 X, y, scoring='precision_weighted', cv=num_folds)
print("Precision: " + str(round(100*precision_values.mean(), 2)) + "%")
recall_values = sklearn.model_selection.cross_val_score(classifier,
 X, y, scoring='recall_weighted', cv=num_folds)
print("Recall: " + str(round(100*recall_values.mean(), 2)) + "%")
f1_values =sklearn.model_selection.cross_val_score(classifier,
 X, y, scoring='f1_weighted', cv=num_folds)
print("F1: " + str(round(100*f1_values.mean(), 2)) + "%")"""

    
