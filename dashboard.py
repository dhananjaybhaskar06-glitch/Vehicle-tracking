import streamlit as st
import requests
from streamlit_autorefresh import st_autorefresh
import pandas as pd
import math

# ========================
# AUTO REFRESH
# ========================
st_autorefresh(interval=3000, key="tracker")

st.set_page_config(page_title="Spoofy AI Tracker", layout="wide")

st.title("🚗 AI Vehicle Intelligence System")

# ========================
# SESSION STATE
# ========================
if "history" not in st.session_state:
    st.session_state.history = []

if "alerts" not in st.session_state:
    st.session_state.alerts = []

if "fuel" not in st.session_state:
    st.session_state.fuel = 100

if "distance" not in st.session_state:
    st.session_state.distance = 0

# ========================
# FETCH DATA
# ========================
try:
    data = requests.get("http://127.0.0.1:5000/location").json()
except:
    st.error("🚨 API not running!")
    st.stop()

lat = data["latitude"]
lon = data["longitude"]
time_now = data["time"]

# ========================
# STORE HISTORY
# ========================
st.session_state.history.append({
    "lat": lat,
    "lon": lon,
    "time": time_now
})

st.session_state.history = st.session_state.history[-20:]
df = pd.DataFrame(st.session_state.history)

# ========================
# DISTANCE CALCULATION
# ========================
def calc_dist(a, b, c, d):
    return math.sqrt((a-c)**2 + (b-d)**2)

if len(df) > 1:
    prev = df.iloc[-2]
    curr = df.iloc[-1]
    dist = calc_dist(prev["lat"], prev["lon"], curr["lat"], curr["lon"])
    st.session_state.distance += dist * 111  # approx km

# ========================
# SPEED (FAKE BUT REALISTIC)
# ========================
speed = round(abs(lat - 28.6139) * 10000, 2)

# ========================
# FUEL LOGIC
# ========================
st.session_state.fuel -= speed * 0.001
if st.session_state.fuel < 0:
    st.session_state.fuel = 0

# ========================
# STATUS + ALERT
# ========================
status = "SAFE"
alert_msg = None

if abs(lat - 28.6139) > 0.015:
    status = "🚨 THEFT"
    alert_msg = "Vehicle stolen / far away"
elif abs(lat - 28.6139) > 0.01:
    status = "⚠️ ALERT"
    alert_msg = "Outside geofence"

if alert_msg:
    st.session_state.alerts.append({
        "time": time_now,
        "alert": alert_msg
    })

# ========================
# KPI SECTION
# ========================
col1, col2, col3, col4 = st.columns(4)

col1.metric("🚗 Speed", f"{speed} km/h")
col2.metric("📍 Latitude", lat)
col3.metric("📍 Longitude", lon)
col4.metric("🧠 Status", status)

# ========================
# FUEL + DISTANCE
# ========================
col5, col6 = st.columns(2)

col5.metric("⛽ Fuel Level", f"{round(st.session_state.fuel,2)}%")
col6.metric("🛣️ Distance", f"{round(st.session_state.distance,2)} km")

# ========================
# ALERT PANEL
# ========================
st.subheader("🚨 Alerts")

if status == "🚨 THEFT":
    st.error(alert_msg)
elif status == "⚠️ ALERT":
    st.warning(alert_msg)
else:
    st.success("All Good")

# ========================
# GRAPH SECTION
# ========================
st.subheader("📈 Speed Trend")

speed_list = [round(abs(row["lat"] - 28.6139) * 10000, 2) for _, row in df.iterrows()]
st.line_chart(speed_list)

# ========================
# MAP
# ========================
st.subheader("📍 Live Map")
st.map(df.rename(columns={"lat":"lat","lon":"lon"}))

# ========================
# SIDE PANEL
# ========================
st.subheader("📜 Alert History")

if st.session_state.alerts:
    st.dataframe(pd.DataFrame(st.session_state.alerts))
else:
    st.write("No alerts yet")

# ========================
# GOOGLE MAP LINK
# ========================
st.markdown(f"[🌍 Open Live Location](https://maps.google.com/?q={lat},{lon})")