import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

st.set_page_config(page_title="Statistik Produksi Industri", layout="centered")

# === UI GELAP ===
st.markdown("""
<style>
body { background-color: #1e1e1e; color: white; }
[data-testid="stAppViewContainer"] { background-color: #1e1e1e; }
h1, h2, h3 { color: #ffcc00; }
.stDataFrame, .stTable { background-color: #2c2c2c; border-radius: 10px; padding: 10px; }
.stTextArea, .stFileUploader, .stSelectbox, .stRadio { background-color: #2e2e2e !important; color: white !important; }
</style>
""", unsafe_allow_html=True)

# === JUDUL ===
st.title("🏭 Statistik Produksi Harian per Shift")
st.markdown("Analisis output produksi berdasarkan data per shift, menggunakan statistik deskriptif.")

# === FUNGSI STATISTIK ===
def hitung_statistik(data):
    return {
        "Mean": np.mean(data),
        "Median": np.median(data),
        "Modus": stats.mode(data, keepdims=True)[0][0],
        "Varians": np.var(data, ddof=1),
        "Standar Deviasi": np.std(data, ddof=1)
    }

# === PILIH INPUT ===
input_mode = st.radio("📥 Pilih metode input data:", ["Input Manual", "Upload File CSV"])
data = None

if input_mode == "Input Manual":
    input_text = st.text_area("Masukkan data produksi (format: Barang,Jumlah):", 
                              "Botol,1200\nBaut,980\nGear,1100\nPipa,950\nPlat,1000")
    try:
        rows = [x.split(",") for x in input_text.strip().split("\n")]
        df = pd.DataFrame(rows, columns=["Barang", "Jumlah"])
        df["Jumlah"] = df["Jumlah"].astype(float)
        data = df["Jumlah"].values
        st.write("### 📋 Data Produksi (Manual)")
        st.dataframe(df)
    except:
        st.error("⚠️ Format salah. Pastikan input seperti: Barang,1234")

elif input_mode == "Upload File CSV":
    file = st.file_uploader("Upload file CSV", type=["csv"])
    if file:
        df = pd.read_csv(file)
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if numeric_cols.any():
            col = st.selectbox("Pilih kolom jumlah produksi:", numeric_cols)
            data = df[col].dropna().values
            st.write("### 📋 Data Produksi (CSV)")
            st.dataframe(df)
        else:
            st.error("⚠️ Tidak ada kolom numerik ditemukan.")

# === OUTPUT ===
if data is not None:
    st.write("### 📊 Statistik Deskriptif")
    hasil = hitung_statistik(data)
    st.dataframe(pd.DataFrame(hasil.items(), columns=["Ukuran", "Nilai"]))

    # === Grafik ===
    st.write("### 📈 Visualisasi")
    chart_type = st.radio("Pilih grafik:", ["Histogram", "Boxplot"])

    if chart_type == "Histogram":
        fig, ax = plt.subplots()
        sns.histplot(data, bins=5, kde=True, color="orange", ax=ax)
        ax.set_facecolor("#1e1e1e")
        ax.set_title("Histogram Jumlah Produksi", color="white")
        ax.tick_params(colors='white')
        st.pyplot(fig)
    else:
        fig, ax = plt.subplots()
        sns.boxplot(data, color="gold", ax=ax)
        ax.set_facecolor("#1e1e1e")
        ax.set_title("Boxplot Jumlah Produksi", color="white")
        ax.tick_params(colors='white')
        st.pyplot(fig)

st.markdown("---")
st.info("Disusun untuk UAS Teknik Industri - 2025")
