import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from statistics import mode

# Konfigurasi halaman
st.set_page_config(page_title="Statistik Produksi Harian", layout="wide", page_icon="📊")

# Header Aplikasi
st.markdown("<h1 style='text-align: center; color: #00BFFF;'>📦 Statistik Produksi Harian</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #AAAAAA;'>Aplikasi Simulasi Statistik Deskriptif - Menghitung Output Hasil Produksi Selama 1 minggu</h4>", unsafe_allow_html=True)
st.markdown("---")

# Sidebar Input
st.sidebar.title("📥 Input Data Produksi")
input_mode = st.sidebar.radio("Pilih metode input:", ["Manual", "Upload CSV"])

# Input Manual
if input_mode == "Manual":
    st.sidebar.subheader("Masukkan Data Produksi Harian per Shift")
    dates = [f"2025-07-{str(i).zfill(2)}" for i in range(1, 8)]
    manual_data = []
    for tgl in dates:
        s1 = st.sidebar.number_input(f"{tgl} - Shift 1", 0, 1000, 100)
        s2 = st.sidebar.number_input(f"{tgl} - Shift 2", 0, 1000, 120)
        s3 = st.sidebar.number_input(f"{tgl} - Shift 3", 0, 1000, 110)
        manual_data.append([tgl, s1, s2, s3])
    df = pd.DataFrame(manual_data, columns=["Tanggal", "Shift 1", "Shift 2", "Shift 3"])
# Input dari CSV
else:
    uploaded_file = st.sidebar.file_uploader("Upload file CSV", type="csv")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
    else:
        st.warning("Silakan unggah file CSV untuk melanjutkan.")
        st.stop()

# Tabel Data Produksi
st.subheader("📋 Tabel Data Produksi")
st.dataframe(df, use_container_width=True)

# Olah data menjadi satu kolom output
df_melt = df.melt(id_vars=["Tanggal"], var_name="Shift", value_name="Output")
values = df_melt["Output"]

# Hitung Statistik
try:
    stats = {
        "Rata-rata (Mean)": np.mean(values),
        "Median": np.median(values),
        "Modus": mode(values),
        "Varians": np.var(values, ddof=1),
        "Standar Deviasi": np.std(values, ddof=1)
    }
except:
    st.error("Data tidak valid atau modus tidak unik.")
    st.stop()

# Tampilkan Statistik
st.subheader("📊 Statistik Deskriptif")
st.write(pd.DataFrame.from_dict(stats, orient='index', columns=["Nilai"]).round(2))

# Visualisasi Histogram dan Boxplot
col1, col2 = st.columns(2)
with col1:
    st.markdown("### Histogram Produksi")
    fig1, ax1 = plt.subplots()
    sns.histplot(values, bins=10, kde=True, ax=ax1, color="#00BFFF")
    ax1.set_xlabel("Output Produksi")
    ax1.set_ylabel("Frekuensi")
    st.pyplot(fig1)

with col2:
    st.markdown("### Boxplot Produksi")
    fig2, ax2 = plt.subplots()
    sns.boxplot(y=values, ax=ax2, color="#00BFFF")
    ax2.set_ylabel("Output Produksi")
    st.pyplot(fig2)

# 🔽 DESKRIPSI KHUSUS: PT SUKA MAJU - PRODUKSI KNALPOT
st.subheader("🏭 Studi Kasus: Produksi Knalpot di PT Suka Maju")
st.markdown("""
PT Suka Maju adalah perusahaan manufaktur otomotif yang memproduksi **knalpot kendaraan bermotor**. Dalam satu minggu terakhir, tim produksi ingin mengetahui seberapa stabil hasil produksi harian dari ketiga shift kerja (Shift 1, 2, dan 3).

Dengan menggunakan aplikasi ini, manajemen dapat:
- Menginput data produksi harian knalpot dari tiap shift.
- Melihat fluktuasi produksi melalui grafik.
- Mengetahui **rata-rata, variansi, dan deviasi** sebagai indikator kestabilan produksi.
Hasil analisis ini sangat berguna untuk mengevaluasi performa tiap shift dan mengidentifikasi potensi inefisiensi pada proses produksi.
""")

# 🧮 Penerapan Konsep Matematika
st.subheader("🧮 Penerapan Konsep Matematika")
st.markdown("""
Aplikasi ini menerapkan **Statistik Deskriptif**, bagian dari Matematika Teknik Industri, untuk menganalisis output produksi harian:
- **Mean (μ)** = jumlah seluruh data / banyaknya data
- **Median** = nilai tengah dari data terurut
- **Modus** = nilai yang paling sering muncul
- **Varians (σ²)** = rata-rata kuadrat selisih nilai dengan mean
- **Standar Deviasi (σ)** = akar dari varians

Statistik ini penting dalam mengukur **kestabilan dan penyebaran hasil produksi antar shift**.
""")

# ✅ Kebenaran Perhitungan
st.subheader("✅ Kebenaran Perhitungan")
st.markdown("""
Perhitungan menggunakan pustaka Python terpercaya:
- `numpy.mean`, `numpy.median`, `numpy.var`, `numpy.std`
- `statistics.mode` untuk modus

Semua perhitungan dilakukan **otomatis dan presisi tinggi**. Hasil visualisasi (histogram & boxplot) mencerminkan kebenaran data input dan output statistik.
""")

# Footer
st.markdown("---")
st.markdown("<center><small>🛠️ Dibuat oleh Mahasiswa Teknik Informatika Universitas Pelita Bangsa - UAS Aplikasi Statistik Deskriptif</small></center>", unsafe_allow_html=True)
