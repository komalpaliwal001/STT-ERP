from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import pickle

def getClassifier(clf = 'svm', ker ='linear'):
    if clf == 'svm':
        # Train SVM classifier
        clf = svm.SVC(kernel=ker)
    elif clf == 'rf':
        # Train Random Forest classifier
        clf = RandomForestClassifier(n_estimators=100, random_state=42)
    elif clf == 'dt':
        # Train Decision Tree classifier
        clf = DecisionTreeClassifier() 

    return clf

def preProcessing (X, Y, clf):
    # Split the dataset
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.30, shuffle=True, random_state=42)
    
    # Initialize and train the classifier
    clf = getClassifier(clf)
    clf.fit(X_train, y_train)

    return {
        clf: clf, 
        X_train: X_train,
        y_train: y_train,
        X_test: X_test, 
        y_test: y_test
    }

def getClassificationReport(x, y, classSel = 'svm'):

    preProData = preProcessing(x, y, classSel)

    classifier = preProData.clf

    # Make predictions on the test set
    y_pred = classifier.predict(preProData.X_test)

    # Evaluate performance
    return classification_report(preProData.y_test, y_pred)


def trainingModel(x, y, classifier, model_path = ''): 

    preProData = preProcessing(x, y, classifier)

    classifier = preProData.clf
    
    # Test the classifier and calculate accuracy
    y_pred = classifier.predict(preProData.X_test)
    print(f"The accuracy of the model is {accuracy_score(preProData.y_test, y_pred) * 100:.2f}%")
    
    if model_path == '':
        model_path = './../models/' + classifier + '.pkl'
    # Save the trained model
    with open(model_path, "wb") as f:
        pickle.dump(classifier, f)

    print(f"Model saved to {model_path}")