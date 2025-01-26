from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import os
import pickle


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
        return DecisionTreeClassifier()
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
    print(f"The accuracy of the model is {accuracy_score(preProData['y_test'], y_pred) * 100:.2f}%")
    
    # Define default model path if not provided
    if not model_path:
        model_path = f"./models/{model_type}_classifier.pkl"

    # Ensure the directory exists
    os.makedirs(os.path.dirname(model_path), exist_ok=True)

    # Save the trained model
    with open(model_path, "wb") as f:
        pickle.dump(clf, f)

    print(f"Model saved to {model_path}")

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
