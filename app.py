import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

# =======================
# FUNGSI BANTU OPSIONAL
# =======================

def hitung_statistik(data):
    """Mengembalikan dictionary statistik deskriptif"""
    mean_val = np.mean(data)
    median_val = np.median(data)
    mode_val = stats.mode(data, keepdims=True)[0][0]
    var_val = np.var(data, ddof=1)
    std_val = np.std(data, ddof=1)
    return {
        "Mean": mean_val,
        "Median": median_val,
        "Modus": mode_val,
        "Varians": var_val,
        "Standar Deviasi": std_val
    }

def tampilkan_tabel_statistik(stats_dict):
    """Menampilkan dataframe statistik dalam Streamlit"""
    df_result = pd.DataFrame({
        "Ukuran Statistik": list(stats_dict.keys()),
        "Nilai": list(stats_dict.values())
    })
    st.dataframe(df_result, use_container_width=True)

def tampilkan_histogram(data):
    fig, ax = plt.subplots()
    sns.histplot(data, kde=True, bins=10, color="skyblue", ax=ax)
    ax.set_title("Histogram Data")
    st.pyplot(fig)

def tampilkan_boxplot(data):
    fig2, ax2 = plt.subplots()
    sns.boxplot(data, color="lightgreen", ax=ax2)
    ax2.set_title("Boxplot Data")
    st.pyplot(fig2)


# Konfigurasi halaman
st.set_page_config(page_title="Simulasi Statistik Deskriptif", layout="centered")

# Sidebar - Dokumentasi Aplikasi
st.sidebar.title("📊 Simulasi Statistik Deskriptif")
st.sidebar.markdown("""
Aplikasi ini menghitung dan memvisualisasikan statistik deskriptif dasar:

**Ukuran yang dihitung:**
- Mean (Rata-rata)
- Median
- Modus
- Varians
- Standar Deviasi

**Fitur Input:**
- Input data manual
- Upload file CSV

**Output:**
- Tabel hasil statistik
- Grafik histogram & boxplot
""")

# Judul Halaman
st.title("📈 Aplikasi Simulasi Statistik Deskriptif")

# PILIHAN INPUT
input_mode = st.radio("Pilih metode input data:", ["Input Manual", "Upload File CSV"])

data = None

if input_mode == "Input Manual":
    manual_input = st.text_area("Masukkan data numerik (pisahkan dengan koma):", "10, 15, 12, 18, 20, 20, 21")
    try:
        data = np.array([float(i.strip()) for i in manual_input.split(",") if i.strip() != ""])
    except:
        st.error("Format data tidak valid. Gunakan angka yang dipisahkan koma.")
        st.stop()
else:
    uploaded_file = st.file_uploader("Upload file CSV", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        if not numeric_cols:
            st.error("Tidak ditemukan kolom numerik dalam file.")
            st.stop()
        selected_col = st.selectbox("Pilih kolom numerik:", numeric_cols)
        data = df[selected_col].dropna().values
    else:
        st.warning("Silakan upload file CSV untuk melanjutkan.")
        st.stop()

# HITUNG STATISTIK DESKRIPTIF
mean_val = np.mean(data)
median_val = np.median(data)
mode_val = stats.mode(data, keepdims=True)[0][0]
var_val = np.var(data, ddof=1)
std_val = np.std(data, ddof=1)

# TAMPILKAN HASIL
st.subheader("📊 Hasil Statistik")
df_result = pd.DataFrame({
    "Ukuran Statistik": ["Mean", "Median", "Modus", "Varians", "Standar Deviasi"],
    "Nilai": [mean_val, median_val, mode_val, var_val, std_val]
})
st.dataframe(df_result, use_container_width=True)

# VISUALISASI GRAFIK
st.subheader("📉 Visualisasi Data")

tab1, tab2 = st.tabs(["Histogram", "Boxplot"])

with tab1:
    fig, ax = plt.subplots()
    sns.histplot(data, kde=True, bins=10, color="skyblue", ax=ax)
    ax.set_title("Histogram Data")
    st.pyplot(fig)

with tab2:
    fig2, ax2 = plt.subplots()
    sns.boxplot(data, color="lightgreen", ax=ax2)
    ax2.set_title("Boxplot Data")
    st.pyplot(fig2)

# Penutup
st.markdown("---")
st.caption("Dibuat untuk memenuhi UAS - Aplikasi Simulasi Statistik Deskriptif")
