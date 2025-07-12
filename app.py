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


# HITUNG DAN TAMPILKAN HASIL
st.subheader("📊 Hasil Statistik")
hasil_statistik = hitung_statistik(data)
tampilkan_tabel_statistik(hasil_statistik)

# VISUALISASI
st.subheader("📉 Visualisasi Data")
tab1, tab2 = st.tabs(["Histogram", "Boxplot"])

with tab1:
    tampilkan_histogram(data)
with tab2:
    tampilkan_boxplot(data)
