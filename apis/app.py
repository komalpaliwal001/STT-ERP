from flask import Flask, request, jsonify
import pickle
import pandas as pd
from utils.Classifier import getClassificationReport, trainingModel

# Initialize the Flask app
app = Flask(__name__)

@app.route("/get_classification_report", methods=["GET"])
def get_classification_report():
    """
    Endpoint to get the classification report from a pre-defined function.
    """
    try:
        report = getClassificationReport()
        return jsonify({"classification_report": report})
    except Exception as e:
        return jsonify({"error": f"Failed to get classification report: {str(e)}"}), 500


@app.route("/prediction", methods=["POST"])
def prediction():
    """
    Endpoint to predict using a trained model.
    """
    try:
        payload = request.json
        if 'feature' not in payload or 'model' not in payload:
            return jsonify({"error": "Feature and model name must be provided in the payload"}), 400

        X_unknown = pd.DataFrame([payload['feature']])  # Convert feature to DataFrame
        model_path = "./model/" + payload['model'] + ".pkl"

        # Load the model
        with open(model_path, "rb") as f:
            clf = pickle.load(f)

        # Make predictions
        prediction = clf.predict(X_unknown)
        return jsonify({"predicted_value": prediction[0]})
    except FileNotFoundError:
        return jsonify({"error": "The specified model file does not exist"}), 404
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500


@app.route("/training", methods=["POST"])
def training():
    """
    Endpoint to train a model. Accepts either a CSV file or JSON payload.
    """
    try:
        payload = request.json
        uploaded_file = request.files.get('file')  # Retrieve uploaded file from the request

        if uploaded_file:  # If a CSV file is uploaded
            try:
                # Read the CSV file into a DataFrame
                df = pd.read_csv(uploaded_file)

                # Extract features and labels
                features = df.drop(columns=['labels'], errors='ignore')  # Drop the label column if it exists
                labels = df['labels'] if 'labels' in df.columns else payload.get('labels')

                if labels is None:
                    return jsonify({"error": "Labels are not provided in the CSV or payload"}), 400

            except Exception as e:
                return jsonify({"error": f"Failed to process the uploaded CSV: {str(e)}"}), 500
        else:  # If no file is uploaded, use features and labels from the payload
            features = pd.DataFrame(payload.get('features'))
            labels = payload.get('labels')

            if features.empty or labels is None:
                return jsonify({"error": "Features and labels must be provided"}), 400

        # Train the model
        trainingModel(features, labels, model_type='svm')
        return jsonify({"message": "Model file created successfully"})
    except Exception as e:
        return jsonify({"error": f"Model training failed: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5003)
