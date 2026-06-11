from flask import Flask, jsonify
import random
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return {"status": "Vehicle API Running"}

@app.route("/location")
def location():
    lat = round(28.6139 + random.uniform(-0.02, 0.02), 6)
    lon = round(77.2090 + random.uniform(-0.02, 0.02), 6)

    return jsonify({
        "time": datetime.now().strftime("%H:%M:%S"),
        "latitude": lat,
        "longitude": lon,
        "status": "LIVE",
        "map": f"https://maps.google.com/?q={lat},{lon}"
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)