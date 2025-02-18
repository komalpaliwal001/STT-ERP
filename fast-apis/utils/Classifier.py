from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import os
import pickle

# Define emotion labels
def getEmotions ():
    return {0: 'angry', 1: 'disgust', 2: 'fear', 3: 'happy', 4: 'neutral', 5: 'sad', 6: 'surprise'}

# Function to assign rule-based labels
def assign_rule_based_label(features):
    pitch = features[0]  # Example: First MFCC as proxy for pitch
    loudness = features[1]  # Example: Second MFCC as proxy for loudness

    if pitch > 20 and loudness > 10:
        return 3  # Happy
    elif pitch < 10 and loudness < 5:
        return 5  # Sad
    elif pitch > 25 and loudness < 8:
        return 0  # Angry
    elif pitch < 5 and loudness > 15:
        return 2  # Fear
    else:
        return 4  # Neutral

# Function to process and assign combined labels
def assign_labels(features_array, metadata=None):
    labels = []
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features_array)  # Normalize features for clustering

    # Step 1: Clustering-Based Labels
    num_clusters = len(getEmotions())
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    cluster_labels = kmeans.fit_predict(features_scaled)

    for i, feature in enumerate(features_array):
        # Step 2: Use metadata for initial label assignment if available
        if metadata is not None and len(metadata) > 0:
            speaker_id = metadata[i]  # Example: Use speaker_id or other metadata
            label = speaker_id % num_clusters  # Assign based on speaker_id
        else:
            label = cluster_labels[i]  # Use clustering label as default

        # Step 3: Refine labels using rule-based logic
        rule_based_label = assign_rule_based_label(feature)
        if label == 4:  # Neutral cluster refinement example
            label = rule_based_label

        labels.append(label)

    return labels


def getClassifier(model_type='svm', ker='linear'):
    """
    Initialize and return a classifier based on the specified model type.

    Args:
        model_type (str): Type of classifier ('svm', 'rf', 'dt').
        ker (str): Kernel type for SVM (default: 'linear').

    Returns:
        sklearn classifier: An initialized classifier.
    """
    if model_type == 'svm':
        return svm.SVC(kernel=ker)
    elif model_type == 'rf':
        return RandomForestClassifier(n_estimators=100, random_state=42)
    elif model_type == 'dt':
        return DecisionTreeClassifier(random_state=42)
    else:
        raise ValueError(f"Unsupported model type: {model_type}")


def preProcessing(X, Y, clf_type):
    """
    Split the dataset, train the classifier, and return the processed data.

    Args:
        X (pd.DataFrame or np.ndarray): Features.
        Y (pd.Series or np.ndarray): Labels.
        clf_type (str): Classifier type ('svm', 'rf', 'dt').

    Returns:
        dict: Contains the classifier, training/test splits, and labels.
    """
    # Split the dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X, Y, test_size=0.30, shuffle=True, random_state=42
    )
    
    # Initialize and train the classifier
    clf = getClassifier(clf_type)
    clf.fit(X_train, y_train)

    return {
        "clf": clf,
        "X_train": X_train,
        "y_train": y_train,
        "X_test": X_test,
        "y_test": y_test,
    }


def getClassificationReport(X, Y, model_type='svm'):
    """
    Generate a classification report for the given features and labels.

    Args:
        X (pd.DataFrame or np.ndarray): Features.
        Y (pd.Series or np.ndarray): Labels.
        model_type (str): Classifier type ('svm', 'rf', 'dt').

    Returns:
        str: Classification report.
    """
    preProData = preProcessing(X, Y, model_type)
    clf = preProData["clf"]

    # Make predictions on the test set
    y_pred = clf.predict(preProData["X_test"])

    # Evaluate performance
    return classification_report(preProData["y_test"], y_pred)


def trainingModel(X, Y, model_type='svm', model_path=''):
    """
    Train the specified model and save it as a pickle file.

    Args:
        X (pd.DataFrame or np.ndarray): Features.
        Y (pd.Series or np.ndarray): Labels.
        model_type (str): Classifier type ('svm', 'rf', 'dt').
        model_path (str): Path to save the model file (optional).

    Returns:
        None
    """
    preProData = preProcessing(X, Y, model_type)
    clf = preProData["clf"]
    
    # Test the classifier and calculate accuracy
    y_pred = clf.predict(preProData["X_test"])
    accuracy = f"{accuracy_score(preProData['y_test'], y_pred) * 100:.2f}%"
    print(f"The accuracy of the model is {accuracy}")
    
    # Define default model path if not provided
    if not model_path:
        model_path = f"./models/{model_type}_classifier.pkl"

    # Ensure the directory exists
    os.makedirs(os.path.dirname(model_path), exist_ok=True)

    # Save the trained model
    with open(model_path, "wb") as f:
        pickle.dump(clf, f)

    print(f"Model saved to {model_path}")
    return {
        "model_path": model_path,
        "accuracy": accuracy
    }

def get_accuracy(y_test, y_pred):
    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy:", accuracy)
    return accuracy

def get_confusion_matrix(y_test, y_pred):
    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    print("Confusion Matrix:\n", cm)
    return cm
