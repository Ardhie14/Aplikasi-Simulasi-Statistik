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
st.set_page_config(page_title="Simulasi Statistik Deskriptif", layout="centered")

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
    nama_file = "data_numerik.csv"
    if not os.path.exists(nama_file):
        data = {
            "No": list(range(1, 11)),
            "Nama": ["Andi", "Budi", "Cici", "Dina", "Eka", "Fani", "Gilang", "Hana", "Indra", "Joko"],
            "Nilai": [78, 82, 90, 75, 88, 85, 80, 92, 84, 89]
        }
        df = pd.DataFrame(data)
        df.to_csv(nama_file, index=False)
    return nama_file

# =======================
# UI APLIKASI
# =======================
st.sidebar.title("📊 Simulasi Statistik Deskriptif")
st.sidebar.markdown("""
Aplikasi ini menghitung dan memvisualisasikan statistik deskriptif dasar:

**Ukuran yang dihitung:**
- Mean
- Median
- Modus
- Varians
- Standar Deviasi

**Fitur Input:**
- Input data manual (nama, nilai)
- Upload file CSV
- Gunakan dataset otomatis

**Output:**
- Tabel statistik
- Histogram dan boxplot
""")

st.title("📈 Aplikasi Simulasi Statistik Deskriptif")

# ===================
# PENJELASAN TEORI (Informatika)
# ===================
with st.expander("🧠 Konsep Statistik Deskriptif dalam Matematika Teknik Informatika"):
    st.markdown(r"""
### 🎯 Relevansi dalam Teknik Informatika:

Statistik deskriptif membantu dalam:
- **Menganalisis waktu eksekusi algoritma**
- **Mengukur performa sistem (respon server, waktu proses)**
- **Mengetahui sebaran error atau output dari suatu sistem**
- **Evaluasi model Machine Learning**

---

### 📐 Ukuran Statistik yang Dihitung:

- **Mean (Rata-rata)**  
  Rumus: \( \bar{x} = \frac{1}{n} \sum_{i=1}^n x_i \)  
  ➤ Menunjukkan nilai rata-rata performa atau nilai hasil uji.

- **Median**  
  ➤ Berguna saat data mengandung outlier (misalnya data delay yang tiba-tiba tinggi).

- **Modus**  
  ➤ Mengetahui nilai yang paling sering muncul. Berguna dalam analisis penggunaan fitur atau event logging.

- **Varians (s²)**  
  Rumus: \( s^2 = \frac{1}{n-1} \sum (x_i - \bar{x})^2 \)  
  ➤ Mengukur sebaran dari waktu eksekusi atau distribusi nilai dalam dataset.

- **Standar Deviasi (s)**  
  \( s = \sqrt{s^2} \)  
  ➤ Semakin kecil deviasi, semakin stabil performa sistem/algoritma.

---

### 📊 Visualisasi:

- **Histogram**: Menunjukkan distribusi frekuensi data log, latency, atau error.
- **Boxplot**: Mendeteksi anomali performa atau outlier dalam hasil pengujian.

---

### ✅ Contoh Aplikasi Nyata:
- Menganalisis hasil uji aplikasi web/mobile
- Menilai stabilitas respons server API
- Statistik evaluasi model klasifikasi atau regresi
- Pengolahan data pengguna sistem informasi

---
*Statistik deskriptif adalah dasar penting dalam pengolahan data teknik informatika, analitik sistem, dan machine learning.*
""")

# =====================
# PILIH INPUT DATA
# =====================
input_mode = st.radio("Pilih metode input data:", ["Input Manual (Nama,Nilai)", "Upload File CSV", "Gunakan Contoh Otomatis"])
data = None

if input_mode == "Input Manual (Nama,Nilai)":
    manual_input = st.text_area("Masukkan data (format: Nama,Nilai per baris):", "Andi,78\nBudi,85\nCici,90")
    try:
        rows = [row.strip() for row in manual_input.strip().split("\n") if row.strip()]
        nama, nilai = [], []
        for row in rows:
            parts = row.split(",")
            if len(parts) != 2:
                raise ValueError("Format harus: Nama,Nilai")
            nama.append(parts[0].strip())
            nilai.append(float(parts[1].strip()))
        df = pd.DataFrame({"Nama": nama, "Nilai": nilai})
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
        selected_col = st.selectbox("Pilih kolom n_
