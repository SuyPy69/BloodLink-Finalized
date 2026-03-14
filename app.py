from flask import Flask, jsonify, json
from flask_cors import CORS
import pandas as pd
import joblib
import os
import threading
import time
import subprocess

app = Flask(__name__)
CORS(app)

print("\n" + "=" * 50)
print(" BLOOD-LINK PREDICTIVE ENGINE V5.0 (LIVE DATA ONLY)")
print(" INITIALIZING FLASK SERVER WITH BACKGROUND CLIENT.PY RUNNER...")
print("=" * 50 + "\n")

# Use the JSON as the ONLY data source
JSON_FILE = 'live_data/hospitals.json'


def load_live_data():
    """Helper function to strictly load the latest JSON data on every request"""
    if not os.path.exists(JSON_FILE):
        print(f"[!] ERROR: {JSON_FILE} missing! Waiting for client.py to generate it...")
        return []

    try:
        with open(JSON_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"[!] ERROR reading JSON: {e}")
        return []


# Load ML brain
try:
    ml_engine = joblib.load('blood_predictor.pkl')
    print(">> ML Engine loaded.")
except Exception:
    ml_engine = None


def run_client_script():
    """Background task to run client.py every 60 seconds"""
    while True:
        try:
            print("\n[SYNC] Triggering client.py to fetch/update live_data...")
            # Execute client.py just like running it in the terminal
            subprocess.run(["python", "client.py"], check=True)
            print("[SYNC] client.py update complete. Sleeping for 60 seconds.")
        except Exception as e:
            print(f"[!] ERROR running client.py: {e}")

        # Wait 60 seconds before running again
        time.sleep(60)


@app.route('/live_data/hospitals.json', methods=['GET'])
def get_live_hospitals():
    """This route allows your React frontend to fetch the JSON directly"""
    data = load_live_data()
    return jsonify(data)


@app.route('/hospitals', methods=['GET'])
def get_hospitals():
    """Legacy route for backward compatibility"""
    data = load_live_data()
    return jsonify(data)


@app.route('/predict_all_nodes', methods=['GET'])
def predict_all_nodes():
    results = []
    live_data = load_live_data()
    blood_types = ['O_pos', 'O_neg', 'A_pos', 'A_neg', 'B_pos', 'B_neg', 'AB_pos', 'AB_neg']

    for row in live_data:
        h_id = row.get('id')
        analysis = {}

        # Default fallback values if weather/altitude aren't in the JSON
        temp = float(row.get('Temperature', 25.0))
        rain = float(row.get('Rain_mm', 0.0))
        alt = float(row.get('Altitude', 900.0))

        for bt in blood_types:
            current_stock = int(row.get(bt, 0))
            prediction = 0

            try:
                # Try to use the ML Engine
                features = pd.DataFrame([{
                    'Total_Units': current_stock,
                    'Temperature': temp,
                    'Rain_mm': rain,
                    'Altitude': alt
                }])
                prediction = ml_engine.predict(features)[0]
            except Exception as e:
                # 5-MINUTE HACKATHON FALLBACK
                prediction = int(max(0, (rain * 0.15) + (alt * 0.02) - (current_stock * 0.05)))

            is_crit = bool(prediction > 10 or current_stock < 15)

            analysis[bt] = {
                "is_critical": is_crit,
                "stock": current_stock,
                "predicted_deficit": int(prediction)
            }

        results.append({
            "id": int(h_id),
            "analysis": analysis
        })

    return jsonify({"nodes": results})


if __name__ == '__main__':
    # Ensure the live_data folder exists
    if not os.path.exists('live_data'):
        os.makedirs('live_data')

    # Start the background thread for client.py BEFORE running Flask
    client_thread = threading.Thread(target=run_client_script, daemon=True)
    client_thread.start()

    # Run the server.
    # NOTE: use_reloader=False is REQUIRED here, otherwise Flask will spawn the client_thread twice!
    app.run(host='0.0.0.0', port=8000, debug=True, use_reloader=False)