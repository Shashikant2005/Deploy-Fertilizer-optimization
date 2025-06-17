
import os
import pickle
import gdown
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Download model from Google Drive if not already present
model_file = 'clr.pkl'
if not os.path.exists(model_file):
    print("Downloading model from Google Drive...")
    FILE_ID = '1GK0gso_r9AIO0xOhE6Sh7n6ony2PXEUE'  # ⬅️ Replace with your actual file ID
    gdown.download(f"https://drive.google.com/uc?id={FILE_ID}", model_file, quiet=False)

# Load the trained model
model = pickle.load(open(model_file, 'rb'))

# Fertilizer output map
output_map = {
    0: "10:10:10 NPK", 1: "10:26:26 NPK", 2: "12:32:16 NPK", 3: "13:32:26 NPK",
    4: "18:46:00 NPK", 5: "19:19:19 NPK", 6: "20:20:20 NPK", 7: "50:26:26 NPK",
    8: "Ammonium Sulphate", 9: "Chilated Micronutrient", 10: "DAP", 11: "Ferrous Sulphate",
    12: "Hydrated Lime", 13: "MOP", 14: "Magnesium Sulphate", 15: "SSP",
    16: "Sulphur", 17: "Urea", 18: "White Potash"
}

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    try:
        features = [
            data['Soil_color'],
            data['Nitrogen'],
            data['Phosphorus'],
            data['Potassium'],
            data['pH'],
            data['Rainfall'],
            data['Temperature'],
            data['Crop']
        ]
        prediction = model.predict([features])[0]
        result = output_map.get(int(prediction), "Unknown Fertilizer")
        return jsonify({'fertilizer': result})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/ck')
def check():
    return "✅ Flask API is running"

if __name__ == '__main__':
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    app.run(host=host, port=port, debug=True)
