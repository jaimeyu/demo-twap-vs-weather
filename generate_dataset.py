import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Define cities with lat/lon
cities = {
    "Paris": (48.8566, 2.3522),
    "Lyon": (45.75, 4.85),
    "Berlin": (52.52, 13.405),
    "London": (51.5074, -0.1278),
    "Rome": (41.9028, 12.4964),
    "Madrid": (40.4168, -3.7038),
    "Amsterdam": (52.3676, 4.9041),
    "Brussels": (50.8503, 4.3517),
    "Vienna": (48.2082, 16.3738),
    "Prague": (50.0755, 14.4378)
}

link_types = ["underground fiber", "underwater fiber", "microwave tower"]

np.random.seed(42)

# Generate 100 nodes randomly distributed over cities with small lat/lon noise and assigned link type
nodes = []
for i in range(100):
    city = np.random.choice(list(cities.keys()))
    lat, lon = cities[city]
    lat += np.random.normal(0, 0.05)
    lon += np.random.normal(0, 0.05)
    link_type = np.random.choice(link_types)
    nodes.append({
        "node_id": f"node_{i+1}",
        "city": city,
        "lat": lat,
        "lon": lon,
        "link_type": link_type
    })
nodes_df = pd.DataFrame(nodes)

# Create datetime range covering 6 months, hourly increments
start_date = datetime(2025, 1, 1)
end_date = start_date + timedelta(days=30*6)
timestamps = pd.date_range(start_date, end_date, freq='H')[:-1]

# Generate weather dataset with rain intensity (mm) per city, per hour
# Rain intensity probabilities:
# - 70% no rain (0 mm)
# - 15% light rain (0 < rain <= 5mm)
# - 10% moderate rain (5 < rain <= 10mm)
# - 5% heavy rain (> 10mm)
weather_data = []
for city in cities.keys():
    for ts in timestamps:
        rain_chance = np.random.random()
        if rain_chance <= 0.7:
            rain_mm = 0.0
        elif rain_chance <= 0.85:
            rain_mm = np.random.uniform(0.1, 5.0)
        elif rain_chance <= 0.95:
            rain_mm = np.random.uniform(5.01, 10.0)
        else:
            rain_mm = np.random.uniform(10.01, 20.0)
        weather_data.append({
            "city": city,
            "timestamp": ts,
            "rain_mm": rain_mm
        })
weather_df = pd.DataFrame(weather_data)

# Function to simulate baseline performance metrics with noise and day/time patterns
def simulate_performance(city, timestamp, link_type):
    base_rtt = {
        "underground fiber": 10,
        "underwater fiber": 20,
        "microwave tower": 30
    }[link_type]
    base_jitter = {
        "underground fiber": 1,
        "underwater fiber": 3,
        "microwave tower": 5
    }[link_type]

    # Workday vs weekend impact on base RTT and jitter
    if timestamp.weekday() < 5:  # weekday
        hour_factor = 1 + np.sin((timestamp.hour - 9) / 12 * np.pi)
        rtt = np.random.normal(base_rtt * (1 + 0.3 * hour_factor), 2)
        jitter = np.random.normal(base_jitter * (1 + 0.2 * hour_factor), 0.5)
    else:  # weekend
        rtt = np.random.normal(base_rtt * 0.8, 1.5)
        jitter = np.random.normal(base_jitter * 0.7, 0.3)

    rtt = max(0, rtt)
    jitter = max(0, jitter)

    # Packet loss ratio small random 0 to 0.02
    loss_ratio = np.clip(np.random.normal(0.005, 0.002), 0, 0.02)
    tx_count = 1000
    rx_count = int(tx_count * (1 - loss_ratio))
    return tx_count, rx_count, loss_ratio, jitter, rtt

# Generate TWAMP measurements adjusting performance for rain impact on microwave links
measurements = []
for node in nodes:
    node_city = node["city"]
    node_link = node["link_type"]
    node_lat = node["lat"]
    node_lon = node["lon"]
    node_id = node["node_id"]

    # Filter weather data for the city once for efficiency
    city_weather = weather_df[weather_df["city"] == node_city].set_index("timestamp")

    for ts in timestamps:
        rain_mm = city_weather.at[ts, "rain_mm"]
        tx, rx, loss, jitter, rtt = simulate_performance(node_city, ts, node_link)

        # Apply rain-based performance degradation if link is microwave tower and raining
        if node_link == "microwave tower" and rain_mm > 0:
            if rain_mm >= 10:
                # 35% average drop with 35% variance
                drop_pct = 0.35 + np.random.normal(0, 0.35)
            elif rain_mm >= 5:
                # 15% average drop with 35% variance
                drop_pct = 0.15 + np.random.normal(0, 0.35)
            else:
                drop_pct = 0.0  # Under 5 mm no drop specified

            drop_pct = max(0, min(drop_pct, 1))  # Clamp between 0 and 1

            jitter *= (1 + drop_pct)
            rtt *= (1 + drop_pct)

        measurements.append({
            "node_id": node_id,
            "city": node_city,
            "timestamp": ts,
            "tx_count": tx,
            "rx_count": rx,
            "packet_loss_ratio": loss,
            "jitter_ms": jitter,
            "rtt_ms": rtt,
            "link_type": node_link,
            "lat": node_lat,
            "lon": node_lon
        })

measurements_df = pd.DataFrame(measurements)

# Save CSV files
nodes_df.to_csv("nodes.csv", index=False)
weather_df.to_csv("weather_patterns.csv", index=False)
measurements_df.to_csv("twamp_measurements_with_rain.csv", index=False)

print("Datasets generated: nodes.csv, weather_patterns.csv, twamp_measurements_with_rain.csv")

