import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from statistics import mode
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Statistik Deskriptif Industri", layout="wide")

# --------------------------
# Sidebar Navigation
# --------------------------
with st.sidebar:
    selected = option_menu(
        "Menu",
        ["🏭 Beranda", "📊 Statistik", "📈 Visualisasi"],
        icons=["house", "bar-chart", "graph-up"],
        default_index=0,
    )

# --------------------------
# Styling Header
# --------------------------
st.markdown("""
    <style>
        .main {background-color: #f5f5f5;}
        h1, h2, h3 {color: #154360;}
        .stApp {padding: 2rem;}
    </style>
""", unsafe_allow_html=True)

# --------------------------
# Halaman 1: Beranda
# --------------------------
if selected == "🏭 Beranda":
    st.title("📦 Aplikasi Statistik Deskriptif")
    st.markdown("### Teknik Industri – Analisis Data Produksi, Kualitas, dan Efisiensi")
    st.markdown("""
    Aplikasi ini dirancang untuk membantu analisis data statistik deskriptif pada berbagai proses industri, seperti:
    - Waktu produksi unit
    - Jumlah produk cacat
    - Setup mesin
    - Output produksi
    - Waktu tunggu logistik

    **Gunakan menu di samping untuk memulai analisis data Anda.**
    """)

# --------------------------
# Halaman 2: Statistik
# --------------------------
elif selected == "📊 Statistik":
    st.header("📋 Input Data Statistik Deskriptif")

    input_type = st.radio("Pilih metode input data:", ["Input Manual", "Upload CSV"])

    if input_type == "Input Manual":
        data_input = st.text_area("Masukkan data angka (pisahkan dengan koma):", "12, 13, 12, 14, 15, 12, 13, 14")
        try:
            data = list(map(float, data_input.split(",")))
            df = pd.DataFrame(data, columns=["Data"])
        except:
            st.error("Format data salah. Pastikan hanya angka dan koma.")
            st.stop()
    else:
        uploaded_file = st.file_uploader("Upload file CSV", type=["csv"])
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            if df.shape[1] > 1:
                selected_column = st.selectbox("Pilih kolom numerik:", df.select_dtypes(include=np.number).columns)
                df = df[[selected_column]]
                df.columns = ["Data"]
            else:
                df.columns = ["Data"]
        else:
            st.warning("Silakan upload file CSV terlebih dahulu.")
            st.stop()

    st.success("✅ Data berhasil diproses")
    st.write(df)

    st.markdown("### 📌 Statistik Deskriptif")
    st.write(f"**Mean (Rata-rata):** {np.mean(df['Data']):.2f}")
    st.write(f"**Median:** {np.median(df['Data']):.2f}")
    try:
        st.write(f"**Modus:** {mode(df['Data'])}")
    except:
        st.write("**Modus:** Tidak ada nilai yang dominan (multimodal)")
    st.write(f"**Varians:** {np.var(df['Data'], ddof=1):.2f}")
    st.write(f"**Standar Deviasi:** {np.std(df['Data'], ddof=1):.2f}")

# --------------------------
# Halaman 3: Visualisasi
# --------------------------
elif selected == "📈 Visualisasi":
    st.header("📊 Visualisasi Data")

    if 'df' not in locals():
        st.warning("Silakan input data terlebih dahulu di menu Statistik.")
        st.stop()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Histogram")
        fig_hist = px.histogram(df, x="Data", nbins=10, title="Distribusi Data Produksi")
        st.plotly_chart(fig_hist, use_container_width=True)

    with col2:
        st.subheader("Boxplot")
        fig_box = px.box(df, y="Data", title="Penyebaran Data (Boxplot)")
        st.plotly_chart(fig_box, use_container_width=True)
        
st.markdown("---")
st.caption("Dibuat untuk UAS - Statistik Deskriptif | Artificial Intelligence | 2025")
