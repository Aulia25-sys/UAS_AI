import tkinter as tk
from tkinter import messagebox  # Import messagebox modul

from sklearn.datasets import load_iris
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load dataset Iris
iris = load_iris()
X = iris.data
y = iris.target

# Normalisasi fitur
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Buat model k-NN
model = KNeighborsClassifier(n_neighbors=3)
model.fit(X_train, y_train)

# Nama fitur dan target
feature_names = [name.capitalize() for name in iris.feature_names]
target_names = iris.target_names

# Warna untuk hasil prediksi
colors = {
    "setosa": "#ff6b6b",
    "versicolor": "#6e9ecf",
    "virginica": "#7cb796"
}

# Fungsi prediksi
def predict():
    try:
        input_values = [float(entries[i].get()) for i in range(4)]
        input_scaled = scaler.transform([input_values])
        prediction = model.predict(input_scaled)[0]
        predicted_class = target_names[prediction]

        # Tampilkan hasil prediksi
        result_label.config(text=f"🌸 Prediksi Jenis Bunga: {predicted_class}", fg=colors[predicted_class])
    except ValueError:
        messagebox.showerror("Input Error", "Harap masukkan nilai numerik untuk semua fitur!")

# Setup GUI
root = tk.Tk()
root.title("🌸 Klasifikasi Ukuran Bunga Iris Menggunakan k-NN")

tk.Label(root, text="Masukkan Ukuran Bunga Iris", font=("Helvetica", 12)).grid(row=0, columnspan=2)

entries = []
for i in range(4):
    tk.Label(root, text=feature_names[i]).grid(row=i+1, column=0)
    entry = tk.Entry(root)
    entry.grid(row=i+1, column=1)
    entries.append(entry)

# Tombol prediksi
predict_btn = tk.Button(root, text="🔍 Prediksi Jenis Bunga", command=predict)
predict_btn.grid(row=5, columnspan=2, pady=20)

# Hasil prediksi
result_label = tk.Label(root, text="🌸 Prediksi: Belum Ada", font=("Helvetica", 14, "italic"))
result_label.grid(row=6, columnspan=2, pady=10)

# Jalankan aplikasi
root.mainloop()