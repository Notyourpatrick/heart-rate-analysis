import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

st.title("💓 Heart Rate Data Analysis Dashboard")

# Upload CSV file
uploaded_file = st.file_uploader("heart_rate_data.csv", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("Raw Data")
    st.write(df.head())

    time = df['time']
    signal = df['value']

    # Detect peaks
    peaks, _ = find_peaks(signal, height=0.6, distance=30)
    peak_times = time[peaks]
    intervals = np.diff(peak_times)
    bpm = 60 / intervals if len(intervals) > 0 else []

    # Plot Signal with Peaks
    st.subheader("Heart Rate Signal")
    fig1, ax1 = plt.subplots(figsize=(10, 4))
    ax1.plot(time, signal, label="Pulse Signal")
    ax1.plot(time[peaks], signal[peaks], "x", label="Detected Beats", color='red')
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Amplitude")
    ax1.legend()
    st.pyplot(fig1)

    # Plot BPM
    if len(bpm) > 0:
        st.subheader("BPM Over Time")
        fig2, ax2 = plt.subplots(figsize=(10, 4))
        ax2.plot(peak_times[1:], bpm, marker='o', color='green')
        ax2.set_xlabel("Time (s)")
        ax2.set_ylabel("Beats Per Minute")
        ax2.grid()
        st.pyplot(fig2)

        st.write(f"🔍 **Average BPM**: {np.round(np.mean(bpm), 2)}")
        st.write(f"📉 **Min BPM**: {np.round(np.min(bpm), 2)}")
        st.write(f"📈 **Max BPM**: {np.round(np.max(bpm), 2)}")
    else:
        st.warning("Not enough peaks detected to calculate BPM.")
