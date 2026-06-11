import random
import time
from core.detector import distance, classify_movement, detect_anomaly
from core.logger import log_event

SAFE_LAT = 28.6139
SAFE_LON = 77.2090
RADIUS = 0.01

ENGINE_ON = False

def outside_geofence(lat, lon):
    return abs(lat - SAFE_LAT) > RADIUS or abs(lon - SAFE_LON) > RADIUS

def generate_location(lat, lon):
    move = random.choice(["idle", "normal", "theft"])

    if move == "idle":
        return lat, lon
    elif move == "normal":
        return lat + random.uniform(-0.001, 0.001), lon + random.uniform(-0.001, 0.001)
    else:
        return lat + random.uniform(0.01, 0.02), lon + random.uniform(0.01, 0.02)

def run_engine():
    lat, lon = SAFE_LAT, SAFE_LON
    prev_lat, prev_lon = lat, lon

    current_state = "SAFE"

    while True:
        lat, lon = generate_location(prev_lat, prev_lon)

        dist = distance(prev_lat, prev_lon, lat, lon)
        movement = classify_movement(dist)

        state, severity = detect_anomaly(
            movement,
            ENGINE_ON,
            outside_geofence(lat, lon)
        )

        if state != current_state:
            print(f"🚨 EVENT: {current_state} → {state}")
            log_event(f"{current_state} -> {state}", severity)
            current_state = state

        print(f"{movement} | {state} | {severity}")

        prev_lat, prev_lon = lat, lon
        time.sleep(2)