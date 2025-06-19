# app.py
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

# Judul Aplikasi
st.set_page_config(page_title="Deteksi Penipuan Kartu Kredit", layout="wide")
st.title("💳 Deteksi Penipuan Kartu Kredit Menggunakan SVM")
st.markdown("Aplikasi ini mendeteksi apakah transaksi kartu kredit mencurigakan.")

# Load Dataset Lokal
@st.cache_data
def load_data():
    data = pd.read_csv("creditcard.csv")  # File lokal
    return data

data = load_data()

# Tampilkan Data Sample
st.subheader("📊 Sampel Data")
st.write(data.head())

# Pisahkan fitur dan label
X = data.drop('Class', axis=1)
y = data['Class']

# Normalisasi fitur
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Latih Model
model = SVC(kernel='linear')
model.fit(X_train, y_train)

# Evaluasi
y_pred = model.predict(X_test)

# Sidebar untuk input manual
st.sidebar.header("🔧 Masukkan Data Transaksi")
input_data = {}
for col in X.columns:
    input_data[col] = st.sidebar.number_input(f"{col}", value=float(0))

# Tombol Prediksi
if st.sidebar.button("🔍 Deteksi"):
    input_df = pd.DataFrame([input_data])
    input_scaled = scaler.transform(input_df)
    prediction = model.predict(input_scaled)

    if prediction[0] == 1:
        st.sidebar.error("🚨 Transaksi Mencurigakan (Penipuan)")
    else:
        st.sidebar.success("✅ Transaksi Aman")

# Evaluasi Model
st.subheader("📈 Evaluasi Model")
st.write("Akurasi:", accuracy_score(y_test, y_pred))
st.text("Laporan Klasifikasi:\n" + classification_report(y_test, y_pred))

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
fig, ax = plt.subplots(figsize=(6, 4))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
ax.set_xlabel("Prediksi")
ax.set_ylabel("Aktual")
ax.set_title("Confusion Matrix")
st.pyplot(fig)
