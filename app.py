import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from statistics import mode
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Statistik Produksi Harian", layout="wide")

# --------------------------
# Sidebar Navigation
# --------------------------
with st.sidebar:
    selected = option_menu(
        "Menu",
        ["🏭 Beranda", "📊 Statistik Produksi", "📈 Visualisasi"],
        icons=["house", "bar-chart", "graph-up"],
        default_index=0,
    )

# --------------------------
# Styling Header
# --------------------------
st.markdown("""
    <style>
        .main {background-color: #f5f5f5;}
        h1, h2, h3 {color: #1B2631;}
        .stApp {padding: 2rem;}
    </style>
""", unsafe_allow_html=True)

# --------------------------
# Halaman 1: Beranda
# --------------------------
if selected == "🏭 Beranda":
    st.title("📦 Aplikasi Statistik Produksi Harian")
    st.markdown("### Produk: **Gearbox Motor** – Analisis Output Produksi per Shift (7 Hari)")
    st.markdown("""
    Aplikasi ini digunakan untuk menganalisis data **jumlah unit yang diproduksi** setiap hari selama satu minggu.
    
    Cocok digunakan untuk:
    - Kontrol produksi harian
    - Evaluasi efisiensi shift kerja
    - Monitoring variasi produksi
    
    Gunakan menu di samping untuk memulai analisis.
    """)

# --------------------------
# Halaman 2: Statistik Produksi
# --------------------------
elif selected == "📊 Statistik Produksi":
    st.header("📋 Input Data Output Produksi Gearbox Motor")

    input_type = st.radio("Pilih metode input data:", ["Input Manual", "Upload CSV"])

    if input_type == "Input Manual":
        st.markdown("Masukkan jumlah unit produksi harian selama 7 hari (pisahkan dengan koma)")
        data_input = st.text_area("Contoh: 320, 315, 330, 340, 325, 310, 335", "320, 315, 330, 340, 325, 310, 335")
        try:
            data = list(map(int, data_input.split(",")))
            if len(data) != 7:
                st.error("⚠️ Harus terdiri dari 7 nilai (1 minggu).")
                st.stop()
            df = pd.DataFrame({
                "Hari": ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"],
                "Unit Produksi": data
            })
        except:
            st.error("Format data salah. Pastikan hanya angka dan koma.")
            st.stop()
    else:
        uploaded_file = st.file_uploader("Upload file CSV", type=["csv"])
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            if "Unit Produksi" not in df.columns:
                st.error("CSV harus mengandung kolom 'Unit Produksi'")
                st.stop()
        else:
            st.warning("Silakan upload file CSV terlebih dahulu.")
            st.stop()

    st.success("✅ Data berhasil diproses")
    st.write(df)

    st.markdown("### 📌 Statistik Deskriptif Produksi")
    st.write(f"**Mean (Rata-rata):** {np.mean(df['Unit Produksi']):.2f} unit")
    st.write(f"**Median:** {np.median(df['Unit Produksi']):.2f} unit")
    try:
        st.write(f"**Modus:** {mode(df['Unit Produksi'])} unit")
    except:
        st.write("**Modus:** Tidak ada nilai yang dominan (multimodal)")
    st.write(f"**Varians:** {np.var(df['Unit Produksi'], ddof=1):.2f}")
    st.write(f"**Standar Deviasi:** {np.std(df['Unit Produksi'], ddof=1):.2f}")

# --------------------------
# Halaman 3: Visualisasi
# --------------------------
elif selected == "📈 Visualisasi":
    st.header("📊 Visualisasi Produksi Harian – Gearbox Motor")

    if 'df' not in locals():
        st.warning("Silakan input data terlebih dahulu di menu Statistik Produksi.")
        st.stop()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Histogram Produksi")
        fig_hist = px.histogram(df, x="Unit Produksi", nbins=7, title="Distribusi Output Produksi")
        st.plotly_chart(fig_hist, use_container_width=True)

    with col2:
        st.subheader("Boxplot Produksi")
        fig_box = px.box(df, y="Unit Produksi", title="Penyebaran Produksi Harian")
        st.plotly_chart(fig_box, use_container_width=True)
