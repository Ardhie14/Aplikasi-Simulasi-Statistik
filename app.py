import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import io

st.set_page_config(page_title="Statistik Deskriptif", layout="centered")
st.title("📊 Aplikasi Simulasi Statistik Deskriptif")

# Upload CSV atau Input Manual
input_method = st.radio("Pilih metode input data:", ("Upload CSV", "Input Manual"))

if input_method == "Upload CSV":
    uploaded_file = st.file_uploader("Upload file CSV", type=["csv"])
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.success("File berhasil diupload!")
elif input_method == "Input Manual":
    manual_data = st.text_area("Masukkan data (pisahkan dengan koma):", "12, 15, 14, 16, 15, 14, 16, 18")
    try:
        data = pd.DataFrame({'Data': [float(x.strip()) for x in manual_data.split(',')]})
        st.success("Data berhasil dibaca!")
    except:
        st.warning("Pastikan data berupa angka yang dipisahkan koma!")

# Tampilkan tabel data
if 'data' in locals():
    st.subheader("📋 Tabel Data")
    st.dataframe(data)

    nilai = data.iloc[:, 0]

    # Hitung Statistik
    mean = np.mean(nilai)
    median = np.median(nilai)
    modus = stats.mode(nilai, keepdims=True)[0][0]
    varian = np.var(nilai, ddof=1)
    std_dev = np.std(nilai, ddof=1)

    st.subheader("📈 Hasil Statistik Deskriptif")
    st.write(f"**Mean (Rata-rata):** {mean:.2f}")
    st.write(f"**Median (Tengah):** {median:.2f}")
    st.write(f"**Modus (Sering Muncul):** {modus}")
    st.write(f"**Varians:** {varian:.2f}")
    st.write(f"**Standar Deviasi:** {std_dev:.2f}")

    # Visualisasi
    st.subheader("📊 Visualisasi")
    chart_type = st.selectbox("Pilih jenis grafik:", ["Histogram", "Boxplot"])

    fig, ax = plt.subplots()
    if chart_type == "Histogram":
        sns.histplot(nilai, kde=True, bins=10, ax=ax)
    else:
        sns.boxplot(x=nilai, ax=ax)
    st.pyplot(fig)
