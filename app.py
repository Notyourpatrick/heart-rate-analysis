import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import time

# -------------------------
# Config & Branding
# -------------------------
st.set_page_config(page_title="Heart Rate Monitor", layout="wide")
st.title("💓 Heart Rate Monitor & Analysis")
st.markdown("Built with ❤️ by **Shreya Shukla** | Real & Simulated BPM Insights")
st.markdown("---")

# -------------------------
# Sidebar Controls
# -------------------------
st.sidebar.title("⚙️ Choose Mode")
mode = st.sidebar.radio(
    "Select how you want to analyze heart rate data:",
    ["📂 Upload File", "⚡ Simulate Live Data"]
)

low_bpm = st.sidebar.number_input("Minimum Normal BPM", value=60)
high_bpm = st.sidebar.number_input("Maximum Normal BPM", value=100)

# -------------------------
# Mode 1: File Upload
# -------------------------
if mode == "📂 Upload File":
    st.sidebar.markdown("---")
    uploaded_files = st.sidebar.file_uploader(
        "Upload one or more CSV files",
        type=["csv"],
        accept_multiple_files=True
    )

    if uploaded_files:
        tabs = st.tabs([f"📈 {file.name}" for file in uploaded_files])
        for file, tab in zip(uploaded_files, tabs):
            with tab:
                st.subheader(f"📊 Analysis: `{file.name}`")
                df = pd.read_csv(file)

                if 'time' not in df.columns or 'value' not in df.columns:
                    st.error("CSV must contain 'time' and 'value' columns.")
                    continue

                time_vals = df['time']
                signal = df['value']

                peaks, _ = find_peaks(signal, height=0.6, distance=30)
                peak_times = time_vals[peaks]
                intervals = np.diff(peak_times)
                bpm = 60 / intervals if len(intervals) > 0 else []

                if len(bpm) > 0:
                    avg_bpm = np.round(np.mean(bpm), 2)
                    min_bpm = np.round(np.min(bpm), 2)
                    max_bpm = np.round(np.max(bpm), 2)

                    st.success(f"**Average BPM:** {avg_bpm}")
                    st.info(f"**Min BPM:** {min_bpm} | **Max BPM:** {max_bpm}")

                    if min_bpm < low_bpm:
                        st.warning(f"⚠️ BPM lower than {low_bpm}: {min_bpm}")
                    if max_bpm > high_bpm:
                        st.warning(f"⚠️ BPM higher than {high_bpm}: {max_bpm}")

                    # Plot signal
                    st.write("### Pulse Signal with Detected Beats")
                    fig1, ax1 = plt.subplots(figsize=(10, 4))
                    ax1.plot(time_vals, signal, label="Pulse Signal")
                    ax1.plot(time_vals[peaks], signal[peaks], "x", label="Peaks", color='red')
                    ax1.set_xlabel("Time (s)")
                    ax1.set_ylabel("Amplitude")
                    ax1.legend()
                    st.pyplot(fig1)

                    # Plot BPM trend
                    st.write("### BPM Over Time")
                    fig2, ax2 = plt.subplots(figsize=(10, 4))
                    ax2.plot(peak_times[1:], bpm, marker='o', color='green')
                    ax2.set_xlabel("Time (s)")
                    ax2.set_ylabel("BPM")
                    ax2.grid()
                    st.pyplot(fig2)

                    # Export BPM report
                    bpm_df = pd.DataFrame({
                        "Time (s)": peak_times[1:].values,
                        "BPM": bpm
                    })
                    csv = bpm_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download BPM Report (CSV)",
                        data=csv,
                        file_name=f"{file.name.split('.')[0]}_bpm_report.csv",
                        mime='text/csv'
                    )
                else:
                    st.warning("Not enough data to calculate BPM.")
    else:
        st.info("📥 Upload CSV(s) using the sidebar.")

# -------------------------
# Mode 2: Live Simulation
# -------------------------
else:  # mode == "⚡ Simulate Live Data"
    st.sidebar.markdown("---")
    duration = st.sidebar.slider("Simulation Duration (sec)", 10, 60, 30, 5)
    refresh_rate = st.sidebar.slider("Update Interval (sec)", 1, 5, 2, 1)

    placeholder = st.empty()
    bpm_placeholder = st.empty()

    time_series = []
    bpm_series = []
    start_time = time.time()

    while time.time() - start_time < duration:
        elapsed = round(time.time() - start_time, 2)
        simulated_bpm = np.random.normal(loc=75, scale=10)
        simulated_bpm = max(30, min(160, simulated_bpm))

        time_series.append(elapsed)
        bpm_series.append(simulated_bpm)

        with bpm_placeholder.container():
            if simulated_bpm < low_bpm:
                st.warning(f"⚠️ Low BPM: {int(simulated_bpm)}")
            elif simulated_bpm > high_bpm:
                st.warning(f"⚠️ High BPM: {int(simulated_bpm)}")
            else:
                st.success(f"✅ Normal BPM: {int(simulated_bpm)}")

        with placeholder.container():
            st.line_chart(pd.DataFrame({"BPM": bpm_series}, index=time_series))

        time.sleep(refresh_rate)

    st.markdown("---")
    st.subheader("📊 Simulation Summary")
    st.write(f"🕒 Duration: {duration} sec")
    st.write(f"📈 Average BPM: {round(np.mean(bpm_series),2)}")
    st.write(f"📉 Min: {int(np.min(bpm_series))} | Max: {int(np.max(bpm_series))}")

    bpm_df = pd.DataFrame({"Time (s)": time_series, "BPM": bpm_series})
    csv = bpm_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Simulated BPM Report (CSV)",
        data=csv,
        file_name="simulated_bpm_report.csv",
        mime='text/csv'
    )

# -------------------------
# Footer
# -------------------------
st.markdown("---")
st.markdown(
    "<center><sub>© 2025 Shreya Shukla | Unified Heart Rate Monitor</sub></center>",
    unsafe_allow_html=True
)
