import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import os

st.set_page_config(page_title="Statistik Teknik Mesin", layout="centered")

# =======================
# FUNGSI PERHITUNGAN
# =======================
def hitung_statistik(data):
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
    df_result = pd.DataFrame({
        "Ukuran Statistik": list(stats_dict.keys()),
        "Nilai": list(stats_dict.values())
    })
    st.dataframe(df_result, use_container_width=True)

def tampilkan_histogram(data):
    fig, ax = plt.subplots()
    sns.histplot(data, kde=True, bins=10, color="steelblue", ax=ax)
    ax.set_title("Histogram Data Pengujian Mesin")
    st.pyplot(fig)

def tampilkan_boxplot(data):
    fig2, ax2 = plt.subplots()
    sns.boxplot(data, color="lightcoral", ax=ax2)
    ax2.set_title("Boxplot Pengujian")
    st.pyplot(fig2)

def buat_dataset_mesin():
    nama_file = "mesin_uji_sample.csv"
    if not os.path.exists(nama_file):
        data = {
            "Parameter": ["Temperatur", "Tekanan", "Putaran", "Getaran", "Efisiensi"],
            "Nilai": [85.0, 2.5, 1400, 0.02, 88.5]
        }
        df = pd.DataFrame(data)
        df.to_csv(nama_file, index=False)
    return nama_file

# =======================
# SIDEBAR & JUDUL
# =======================
st.sidebar.title("🛠️ Statistik Teknik Mesin")
st.sidebar.markdown("""
Aplikasi ini digunakan untuk analisis statistik dari hasil pengujian sistem mekanis seperti:

- Uji tekanan dan temperatur
- Efisiensi sistem termal
- Getaran mesin
- Kecepatan rotasi poros

**Input:**  
- Data manual (Parameter, Nilai)  
- Upload CSV  
- Dataset simulasi otomatis

**Output:**  
- Tabel statistik  
- Histogram & Boxplot visualisasi
""")

st.title("📊 Simulasi Statistik Deskriptif - Teknik Mesin")

# =======================
# PENJELASAN TEORI MESIN
# =======================
with st.expander("📘 Konsep Statistik dalam Teknik Mesin"):
    st.markdown(r"""
### 🔧 Penerapan Statistik di Teknik Mesin:

Statistik deskriptif digunakan untuk menganalisis hasil pengujian seperti:
- **Temperatur operasi mesin**
- **Tekanan fluida**
- **Kecepatan rotasi poros**
- **Efisiensi energi sistem**
- **Getaran dan noise mesin**

---

### 📐 Ukuran Statistik:

- **Mean (Rata-rata)**  
  Rumus: \( \bar{x} = \frac{1}{n} \sum_{i=1}^n x_i \)  
  ➤ Menunjukkan rata-rata pengukuran alat.

- **Median**  
  ➤ Nilai tengah — tahan terhadap nilai ekstrem saat uji coba.

- **Modus**  
  ➤ Nilai yang sering muncul saat pengukuran berulang.

- **Varians (s²)**  
  Rumus: \( s^2 = \frac{1}{n-1} \sum (x_i - \bar{x})^2 \)  
  ➤ Menyatakan sebaran dari hasil uji performa.

- **Standar Deviasi (s)**  
  \( s = \sqrt{s^2} \)  
  ➤ Stabilitas data pengukuran sistem mekanik.

---

### 📊 Visualisasi:
- **Histogram** → distribusi hasil pengujian
- **Boxplot** → identifikasi anomali (outlier)

---
*Statistik menjadi dasar dalam proses kontrol kualitas, maintenance prediktif, dan riset sistem mekanik.*
""")

# =======================
# INPUT PILIHAN
# =======================
input_mode = st.radio("Pilih metode input data:", [
    "Input Manual (Parameter, Nilai - Mesin)",
    "Upload File CSV",
    "Gunakan Contoh Otomatis"
])
data = None

if input_mode == "Input Manual (Parameter, Nilai - Mesin)":
    manual_input = st.text_area("Masukkan data uji mesin (format: Parameter,Nilai per baris):",
                                 "Temperatur,85.0\nTekanan,2.5\nPutaran,1400\nGetaran,0.02\nEfisiensi,88.5")
    try:
        rows = [row.strip() for row in manual_input.strip().split("\n") if row.strip()]
        param, nilai = [], []
        for row in rows:
            parts = row.split(",")
            if len(parts) != 2:
                raise ValueError("Format harus: Parameter,Nilai")
            param.append(parts[0].strip())
            nilai.append(float(parts[1].strip()))
        df = pd.DataFrame({"Parameter": param, "Nilai": nilai})
        st.dataframe(df)
        data = df["Nilai"].values
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
        st.stop()

elif input_mode == "Upload File CSV":
    uploaded_file = st.file_uploader("Upload file CSV hasil pengujian", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        if not numeric_cols:
            st.error("Tidak ditemukan kolom numerik.")
            st.stop()
        selected_col = st.selectbox("Pilih kolom numerik:", numeric_cols)
        data = df[selected_col].dropna().values
        st.dataframe(df)
    else:
        st.warning("Silakan upload file CSV.")
        st.stop()

else:
    nama_file = buat_dataset_mesin()
    df = pd.read_csv(nama_file)
    st.success(f"Dataset otomatis '{nama_file}' berhasil dimuat.")
    st.dataframe(df)
    data = df["Nilai"].values

# =======================
# HASIL & VISUALISASI
# =======================
st.subheader("📈 Hasil Statistik Pengujian")
hasil_statistik = hitung_statistik(data)
tampilkan_tabel_statistik(hasil_statistik)

st.subheader("📉 Visualisasi")
tab1, tab2 = st.tabs(["Histogram", "Boxplot"])
with tab1:
    tampilkan_histogram(data)
with tab2:
    tampilkan_boxplot(data)

st.markdown("---")
st.caption("Disusun untuk UAS - Aplikasi Statistik Deskriptif | Teknik Mesin | 2025")
