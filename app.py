
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# -------------------------
# Sidebar and Branding
# -------------------------
st.set_page_config(page_title="Heart Rate Analysis", layout="wide")
st.sidebar.title("📂 Upload Heart Rate CSV(s)")
uploaded_files = st.sidebar.file_uploader("Choose one or more CSV files", type=["csv"], accept_multiple_files=True)

st.sidebar.markdown("---")
st.sidebar.title("⚙️ Settings")
low_bpm = st.sidebar.number_input("Minimum Normal BPM", value=60)
high_bpm = st.sidebar.number_input("Maximum Normal BPM", value=100)

st.sidebar.markdown("---")
st.sidebar.markdown("📌 Made with ❤️ by **Shreya Shukla**")

st.title("💓 Heart Rate Analysis Dashboard")

if uploaded_files:
    tabs = st.tabs([f"📈 {file.name}" for file in uploaded_files])

    for file, tab in zip(uploaded_files, tabs):
        with tab:
            st.subheader(f"📊 Analysis for: `{file.name}`")
            df = pd.read_csv(file)

            if 'time' not in df.columns or 'value' not in df.columns:
                st.error("The file must have 'time' and 'value' columns.")
                continue

            time = df['time']
            signal = df['value']

            # Peak detection
            peaks, _ = find_peaks(signal, height=0.6, distance=30)
            peak_times = time[peaks]
            intervals = np.diff(peak_times)
            bpm = 60 / intervals if len(intervals) > 0 else []

            # Summary stats
            if len(bpm) > 0:
                avg_bpm = np.round(np.mean(bpm), 2)
                min_bpm = np.round(np.min(bpm), 2)
                max_bpm = np.round(np.max(bpm), 2)

                st.success(f"**Average BPM:** {avg_bpm}")
                st.info(f"**Min BPM:** {min_bpm} | **Max BPM:** {max_bpm}")

                if min_bpm < low_bpm:
                    st.warning(f"⚠️ Detected BPM lower than {low_bpm}: {min_bpm} BPM")
                if max_bpm > high_bpm:
                    st.warning(f"⚠️ Detected BPM higher than {high_bpm}: {max_bpm} BPM")

            # Plot: Heart Signal with Peaks
            st.write("### Pulse Signal with Detected Beats")
            fig1, ax1 = plt.subplots(figsize=(10, 4))
            ax1.plot(time, signal, label="Pulse Signal")
            ax1.plot(time[peaks], signal[peaks], "x", label="Detected Beats", color='red')
            ax1.set_xlabel("Time (s)")
            ax1.set_ylabel("Amplitude")
            ax1.legend()
            st.pyplot(fig1)

            # Plot: BPM Trend
            if len(bpm) > 0:
                st.write("### BPM Over Time")
                fig2, ax2 = plt.subplots(figsize=(10, 4))
                ax2.plot(peak_times[1:], bpm, marker='o', color='green')
                ax2.set_xlabel("Time (s)")
                ax2.set_ylabel("Beats Per Minute")
                ax2.grid()
                st.pyplot(fig2)
else:
    st.info("📥 Please upload one or more heart rate CSV files using the sidebar.")
