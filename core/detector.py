import math

def distance(a, b, c, d):
    return math.sqrt((a-c)**2 + (b-d)**2)

def classify_movement(dist):
    if dist < 0.0001:
        return "IDLE"
    elif dist < 0.005:
        return "NORMAL"
    else:
        return "FAST"

def detect_anomaly(movement, engine_on, outside_geofence):
    if movement != "IDLE" and not engine_on:
        return "THEFT", "CRITICAL"

    if outside_geofence:
        return "GEOFENCE", "HIGH"

    if movement == "FAST":
        return "SUSPICIOUS", "MEDIUM"

    return "SAFE", "LOW"