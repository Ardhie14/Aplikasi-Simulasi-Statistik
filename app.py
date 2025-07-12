import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from statistics import mode

st.set_page_config(layout="wide", page_title="Statistik Produksi Harian - Teknik Industri", page_icon="📊")

# UI Header
st.markdown("<h1 style='text-align: center; color: white;'>📦 Statistik Produksi Harian - Teknik Industri</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>Aplikasi Simulasi Statistik Deskriptif - UAS</h4>", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("Input Data Produksi")
data_option = st.sidebar.radio("Pilih Metode Input:", ("Manual", "Upload CSV"))

# Load data
if data_option == "Manual":
    st.sidebar.subheader("Masukkan Data Produksi Harian per Shift")
    dates = [f"2025-07-{str(i).zfill(2)}" for i in range(1, 8)]
    manual_data = []
    for tanggal in dates:
        shift1 = st.sidebar.number_input(f"{tanggal} - Shift 1", 0, 1000, 100)
        shift2 = st.sidebar.number_input(f"{tanggal} - Shift 2", 0, 1000, 120)
        shift3 = st.sidebar.number_input(f"{tanggal} - Shift 3", 0, 1000, 110)
        manual_data.append([tanggal, shift1, shift2, shift3])
    df = pd.DataFrame(manual_data, columns=["Tanggal", "Shift 1", "Shift 2", "Shift 3"])

else:
    uploaded_file = st.sidebar.file_uploader("Upload File CSV", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        st.warning("Harap unggah file CSV untuk melanjutkan.")
        st.stop()

# Perhitungan Statistik
df_melt = df.melt(id_vars=["Tanggal"], var_name="Shift", value_name="Output")
output_values = df_melt["Output"]

try:
    stats = {
        "Mean": np.mean(output_values),
        "Median": np.median(output_values),
        "Modus": mode(output_values),
        "Varians": np.var(output_values, ddof=1),
        "Standar Deviasi": np.std(output_values, ddof=1)
    }
except:
    st.error("Terjadi kesalahan saat menghitung statistik. Pastikan data valid.")
    st.stop()

# Tampilkan Tabel Statistik
st.subheader("📋 Tabel Statistik Produksi")
st.dataframe(df.style.highlight_max(axis=0))

st.markdown("### 📊 Hasil Statistik Deskriptif")
for key, val in stats.items():
    st.write(f"**{key}**: {val:.2f}")

# Visualisasi
col1, col2 = st.columns(2)
with col1:
    st.markdown("#### Histogram Produksi")
    fig1, ax1 = plt.subplots()
    sns.histplot(output_values, bins=10, kde=True, ax=ax1, color='skyblue')
    ax1.set_xlabel("Output Produksi")
    st.pyplot(fig1)

with col2:
    st.markdown("#### Boxplot Produksi")
    fig2, ax2 = plt.subplots()
    sns.boxplot(y=output_values, color='orange', ax=ax2)
    ax2.set_ylabel("Output Produksi")
    st.pyplot(fig2)

# Footer
st.markdown("---")
st.markdown("<center><small>Dikembangkan untuk UAS Aplikasi Statistik - Teknik Industri | @ardhie06</small></center>", unsafe_allow_html=True)
