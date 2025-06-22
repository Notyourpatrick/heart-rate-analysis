import streamlit as st
import pandas as pd
import numpy as np
import time

# -------------------------
# Config & Branding
# -------------------------
st.set_page_config(page_title="Live Heart Rate Simulation", layout="wide")
st.title("💓 Live Heart Rate Simulation")
st.markdown("Simulated real-time data updates for BPM tracking")
st.markdown("---")

# -------------------------
# Sidebar Controls
# -------------------------
st.sidebar.title("⚙️ Simulation Settings")
duration = st.sidebar.slider("Simulation Duration (seconds)", min_value=10, max_value=60, value=30, step=5)
refresh_rate = st.sidebar.slider("Update Interval (seconds)", min_value=1, max_value=5, value=2, step=1)
low_bpm = st.sidebar.number_input("Minimum Normal BPM", value=60)
high_bpm = st.sidebar.number_input("Maximum Normal BPM", value=100)

# -------------------------
# Real-Time Data Simulation
# -------------------------
placeholder = st.empty()
bpm_placeholder = st.empty()

time_series = []
bpm_series = []

start_time = time.time()
while time.time() - start_time < duration:
    elapsed = round(time.time() - start_time, 2)
    simulated_bpm = np.random.normal(loc=75, scale=10)  # Random around 75 BPM
    simulated_bpm = max(30, min(160, simulated_bpm))    # Clamp to 30–160 BPM

    time_series.append(elapsed)
    bpm_series.append(simulated_bpm)

    # Display alert for abnormal BPM
    with bpm_placeholder.container():
        if simulated_bpm < low_bpm:
            st.warning(f"⚠️ Low BPM detected: {int(simulated_bpm)}")
        elif simulated_bpm > high_bpm:
            st.warning(f"⚠️ High BPM detected: {int(simulated_bpm)}")
        else:
            st.success(f"✅ Normal BPM: {int(simulated_bpm)}")

    # Update live chart
    with placeholder.container():
        st.line_chart(pd.DataFrame({"BPM": bpm_series}, index=time_series))

    time.sleep(refresh_rate)

# -------------------------
# Summary
# -------------------------
st.markdown("---")
st.subheader("📊 Simulation Summary")
st.write(f"🕒 Total Duration: {duration} seconds")
st.write(f"📈 Average BPM: {round(np.mean(bpm_series), 2)}")
st.write(f"📉 Min BPM: {int(np.min(bpm_series))} | 📈 Max BPM: {int(np.max(bpm_series))}")

# -------------------------
# Footer
# -------------------------
st.markdown("---")
st.markdown("<center><sub>© 2025 Shreya Shukla | Simulated Real-Time Analysis</sub></center>", unsafe_allow_html=True)
