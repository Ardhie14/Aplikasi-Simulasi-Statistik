import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import os

# =======================
# SETUP HALAMAN
# =======================
st.set_page_config(page_title="Simulasi Statistik Deskriptif - ML", layout="centered")

# =======================
# FUNGSI BANTU
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
    sns.histplot(data, kde=True, bins=10, color="skyblue", ax=ax)
    ax.set_title("Histogram Data")
    st.pyplot(fig)

def tampilkan_boxplot(data):
    fig2, ax2 = plt.subplots()
    sns.boxplot(data, color="lightgreen", ax=ax2)
    ax2.set_title("Boxplot Data")
    st.pyplot(fig2)

def buat_dataset_numerik():
    nama_file = "ml_metrics_sample.csv"
    if not os.path.exists(nama_file):
        data = {
            "Fitur": ["Akurasi", "Presisi", "Recall", "F1-Score", "Loss"],
            "Nilai": [0.91, 0.88, 0.84, 0.86, 0.12]
        }
        df = pd.DataFrame(data)
        df.to_csv(nama_file, index=False)
    return nama_file

# =======================
# SIDEBAR & JUDUL
# =======================
st.sidebar.title("📊 Statistik Deskriptif - Machine Learning")
st.sidebar.markdown("""
Aplikasi ini menghitung dan memvisualisasikan statistik deskriptif untuk data hasil evaluasi model:

**Ukuran yang dihitung:**
- Mean
- Median
- Modus
- Varians
- Standar Deviasi

**Input:**
- Data manual (Fitur, Nilai)
- File CSV
- Dataset contoh

**Visualisasi:**
- Histogram & Boxplot
""")

st.title("📈 Simulasi Statistik Deskriptif - Data Machine Learning")

# =======================
# PENJELASAN TEORI
# =======================
with st.expander("🧠 Konsep Statistik Deskriptif dalam Matematika Teknik Informatika (ML)"):
    st.markdown(r"""
### 🎯 Relevansi dalam Machine Learning:

Statistik deskriptif membantu:
- **Evaluasi performa model (akurasi, presisi, recall, loss, dll.)**
- **Analisis distribusi error**
- **Preprocessing & normalisasi data**
- **Menganalisis hasil tuning hyperparameter**

---

### 📐 Ukuran Statistik:

- **Mean (Rata-rata)**  
  \( \bar{x} = \frac{1}{n} \sum_{i=1}^n x_i \)  
  ➤ Rata-rata dari semua metrik.

- **Median**  
  ➤ Nilai tengah, tahan terhadap outlier.

- **Modus**  
  ➤ Nilai paling sering muncul.

- **Varians (s²)**  
  \( s^2 = \frac{1}{n-1} \sum (x_i - \bar{x})^2 \)  
  ➤ Mengukur sebaran metrik.

- **Standar Deviasi (s)**  
  \( s = \sqrt{s^2} \)  
  ➤ Seberapa jauh nilai menyimpang dari rata-rata.

---

### 📊 Visualisasi:
- **Histogram**: Distribusi nilai performa
- **Boxplot**: Deteksi outlier dalam hasil eksperimen

---

*Digunakan dalam: evaluasi model, eksperimen hyperparameter, riset ML, analitik sistem cerdas.*
""")

# =======================
# INPUT PILIHAN
# =======================
input_mode = st.radio("Pilih metode input data:", [
    "Input Manual (Fitur,Nilai - ML)", 
    "Upload File CSV", 
    "Gunakan Contoh Otomatis"
])
data = None

if input_mode == "Input Manual (Fitur,Nilai - ML)":
    manual_input = st.text_area("Masukkan data metrik ML (format: Fitur,Nilai per baris):", 
                                 "Akurasi,0.91\nPresisi,0.88\nRecall,0.84\nF1-Score,0.86\nLoss,0.12")
    try:
        rows = [row.strip() for row in manual_input.strip().split("\n") if row.strip()]
        fitur, nilai = [], []
        for row in rows:
            parts = row.split(",")
            if len(parts) != 2:
                raise ValueError("Format harus: Fitur,Nilai")
            fitur.append(parts[0].strip())
            nilai.append(float(parts[1].strip()))
        df = pd.DataFrame({"Fitur": fitur, "Nilai": nilai})
        st.dataframe(df)
        data = df["Nilai"].values
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
        st.stop()

elif input_mode == "Upload File CSV":
    uploaded_file = st.file_uploader("Upload file CSV", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        if not numeric_cols:
            st.error("Tidak ditemukan kolom numerik dalam file.")
            st.stop()
        selected_col = st.selectbox("Pilih kolom numerik:", numeric_cols)
        data = df[selected_col].dropna().values
        st.dataframe(df)
    else:
        st.warning("Silakan upload file CSV.")
        st.stop()

else:
    nama_file = buat_dataset_numerik()
    df = pd.read_csv(nama_file)
    st.success(f"Dataset otomatis '{nama_file}' berhasil dimuat.")
    st.dataframe(df)
    data = df["Nilai"].values

# =======================
# HASIL & VISUALISASI
# =======================
st.subheader("📊 Hasil Statistik")
hasil_statistik = hitung_statistik(data)
tampilkan_tabel_statistik(hasil_statistik)

st.subheader("📉 Visualisasi Data")
tab1, tab2 = st.tabs(["Histogram", "Boxplot"])
with tab1:
    tampilkan_histogram(data)
with tab2:
    tampilkan_boxplot(data)

st.markdown("---")
st.caption("Dibuat untuk UAS - Aplikasi Simulasi Statistik Deskriptif | Teknik Informatika | 2025")
