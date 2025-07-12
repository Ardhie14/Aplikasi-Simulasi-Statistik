import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Konfigurasi halaman
st.set_page_config(page_title="Statistik Produksi Industri", layout="centered")

# ==== Custom CSS Dark Mode ====
st.markdown("""
<style>
body {
    background-color: #1e1e1e;
    color: white;
}
[data-testid="stAppViewContainer"] {
    background-color: #1e1e1e;
}
h1, h2, h3, h4 {
    color: #ffcc00;
}
.stDataFrame, .stTable {
    background-color: #2c2c2c;
    border-radius: 10px;
    padding: 10px;
}
.stTextArea, .stSelectbox, .stFileUploader {
    background-color: #333333 !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# ==== Judul Aplikasi ====
st.title("🏭 Statistik Produksi Harian per Shift")
st.markdown("Analisis sederhana untuk melihat performa dan kestabilan hasil produksi di pabrik.")

# ==== Fungsi Statistik ====
def hitung_statistik(data):
    return {
        "Mean": np.mean(data),
        "Median": np.median(data),
        "Modus": stats.mode(data, keepdims=True)[0][0],
        "Varians": np.var(data, ddof=1),
        "Standar Deviasi": np.std(data, ddof=1)
    }

# ==== Input Manual ====
input_data = st.text_area("📥 Masukkan data produksi (format: Barang,Jumlah):", 
                          "Botol,1200\nBaut,980\nGear,1100\nPipa,950\nPlat,1000")

try:
    rows = [x.split(",") for x in input_data.strip().split("\n")]
    barang = [r[0].strip() for r in rows]
    jumlah = [float(r[1].strip()) for r in rows]
    df = pd.DataFrame({"Barang": barang, "Jumlah": jumlah})
    
    st.write("### 📋 Data Produksi")
    st.dataframe(df)

    # ==== Statistik Deskriptif ====
    st.write("### 📊 Ringkasan Statistik")
    hasil = hitung_statistik(jumlah)
    st.dataframe(pd.DataFrame(hasil.items(), columns=["Ukuran", "Nilai"]))

    # ==== Visualisasi ====
    st.write("### 📈 Visualisasi Produksi")
    
    fig1, ax1 = plt.subplots()
    sns.set_theme(style="darkgrid")
    sns.histplot(jumlah, bins=5, kde=True, ax=ax1, color="orange")
    ax1.set_facecolor("#1e1e1e")
    ax1.set_title("Histogram Produksi", color="white")
    ax1.tick_params(colors='white')
    st.pyplot(fig1)

    fig2, ax2 = plt.subplots()
    sns.boxplot(jumlah, ax=ax2, color="gold")
    ax2.set_facecolor("#1e1e1e")
    ax2.set_title("Boxplot Produksi", color="white")
    ax2.tick_params(colors='white')
    st.pyplot(fig2)

except Exception as e:
    st.error(f"⚠️ Format input salah: {e}")
