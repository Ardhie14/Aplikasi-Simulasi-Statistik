import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import os

st.set_page_config(page_title="Statistik Produksi Teknik Industri", layout="centered")

# =======================
# FUNGSI STATISTIK
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
    sns.histplot(data, kde=True, bins=10, color="orange", ax=ax)
    ax.set_title("Distribusi Output Produksi per Shift")
    st.pyplot(fig)

def tampilkan_boxplot(data):
    fig2, ax2 = plt.subplots()
    sns.boxplot(data, color="gold", ax=ax2)
    ax2.set_title("Boxplot Jumlah Produksi")
    st.pyplot(fig2)

def buat_dataset_produksi():
    nama_file = "produksi_shift_sample.csv"
    if not os.path.exists(nama_file):
        data = {
            "Barang": ["Botol Plastik", "Baut", "Roda Baja", "Pipa Besi", "Gear Motor"],
            "Jumlah Produksi": [1200, 980, 1100, 950, 1000]
        }
        df = pd.DataFrame(data)
        df.to_csv(nama_file, index=False)
    return nama_file

# =======================
# SIDEBAR & JUDUL
# =======================
st.sidebar.title("🏭 Statistik Produksi Harian")
st.sidebar.markdown("""
Aplikasi ini digunakan untuk menganalisis data produksi harian di pabrik atau lini manufaktur.

**Contoh Barang:**
- Botol Plastik
- Baut dan Mur
- Roda Baja
- Komponen Gear
- Produk Pipa

**Input:**  
- Manual (Barang, Jumlah)  
- Upload CSV  
- Dataset otomatis

**Output:**  
- Statistik produksi  
- Grafik histogram & boxplot
""")

st.title("📈 Simulasi Statistik Produksi Harian per Shift")

# =======================
# PENJELASAN TEORI
# =======================
with st.expander("📘 Konsep Statistik dalam Teknik Industri"):
    st.markdown(r"""
### 🏭 Peran Statistik di Industri:

Statistik digunakan untuk:
- Mengukur konsistensi hasil produksi
- Menganalisis efisiensi lini per shift
- Menilai kebutuhan perbaikan pada sistem produksi
- Dasar pengambilan keputusan pada manajemen industri

---

### 📐 Ukuran Statistik:

- **Mean (Rata-rata):** jumlah produksi rata-rata per shift  
- **Median:** nilai tengah dari distribusi  
- **Modus:** jumlah produksi yang paling sering muncul  
- **Varians & Standar Deviasi:** mengukur stabilitas atau variasi produksi

---

### 📊 Visualisasi:
- **Histogram:** distribusi output barang
- **Boxplot:** deteksi anomali dalam jumlah produksi

---

*Statistik membantu memastikan proses industri berjalan stabil, efisien, dan dapat dikontrol.*
""")

# =======================
# INPUT DATA
# =======================
input_mode = st.radio("Pilih metode input data:", [
    "Input Manual (Barang, Jumlah)",
    "Upload File CSV",
    "Gunakan Contoh Otomatis"
])
data = None

if input_mode == "Input Manual (Barang, Jumlah)":
    manual_input = st.text_area("Masukkan data produksi (format: Barang,Jumlah per baris):",
                                 "Botol Plastik,1200\nBaut,980\nRoda Baja,1100\nPipa Besi,950\nGear Motor,1000")
    try:
        rows = [row.strip() for row in manual_input.strip().split("\n") if row.strip()]
        barang, jumlah = [], []
        for row in rows:
            parts = row.split(",")
            if len(parts) != 2:
                raise ValueError("Format harus: Barang,Jumlah")
            barang.append(parts[0].strip())
            jumlah.append(float(parts[1].strip()))
        df = pd.DataFrame({"Barang": barang, "Jumlah Produksi": jumlah})
        st.dataframe(df)
        data = df["Jumlah Produksi"].values
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
        st.stop()

elif input_mode == "Upload File CSV":
    uploaded_file = st.file_uploader("Upload file CSV produksi", type=["csv"])
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
    nama_file = buat_dataset_produksi()
    df = pd.read_csv(nama_file)
    st.success(f"Dataset otomatis '{nama_file}' berhasil dimuat.")
    st.dataframe(df)
    data = df["Jumlah Produksi"].values

# =======================
# HASIL & VISUALISASI
# =======================
st.subheader("📊 Hasil Statistik Produksi")
hasil_statistik = hitung_statistik(data)
tampilkan_tabel_statistik(hasil_statistik)

st.subheader("📉 Visualisasi Data")
tab1, tab2 = st.tabs(["Histogram", "Boxplot"])
with tab1:
    tampilkan_histogram(data)
with tab2:
    tampilkan_boxplot(data)

st.markdown("---")
st.caption("Disusun untuk UAS - Statistik Produksi | Teknik Industri | 2025")
