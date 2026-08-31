from flask import Flask, request, jsonify
import joblib

# Loaded once when the application starts.
model = joblib.load('model/model.pkl')
app = Flask(__name__)


@app.route('/predict', methods=['POST'])
def predict_post():
    data = request.get_json(silent=True) or {}
    features = data.get('features')
    if not isinstance(features, list) or len(features) != 2:
        return jsonify({'error': 'features must be a list of exactly 2 numbers'}), 400
    try:
        values = [float(value) for value in features]
    except (TypeError, ValueError):
        return jsonify({'error': 'features must contain only numbers'}), 400
    prediction = float(model.predict([values])[0])
    return jsonify({'prediction': prediction})


@app.route('/predict/<f1>/<f2>', methods=['GET'])
def predict_get(f1, f2):
    try:
        values = [float(f1), float(f2)]
    except ValueError:
        return jsonify({'error': 'f1 and f2 must be numbers'}), 400
    prediction = float(model.predict([values])[0])
    return jsonify({'prediction': prediction})


if __name__ == '__main__':
    app.run(port=5055)
