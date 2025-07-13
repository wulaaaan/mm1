import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time

st.set_page_config(page_title="Simulasi Antrian M/M/1", layout="centered")

st.title("📈 Simulasi Antrian ")

st.write("""
Aplikasi ini menghitung parameter sistem antrian dengan model M/M/1 serta menampilkan grafik dan simulasi animasi.
""")

# Input user
lambd = st.number_input("λ (arrival rate)", min_value=0.0, format="%.2f")
mu = st.number_input("μ (service rate)", min_value=0.0, format="%.2f")

if lambd > 0 and mu > 0:
    if lambd >= mu:
        st.error("λ harus lebih kecil dari μ agar sistem stabil.")
    else:
        # 🧮 Perhitungan parameter
        rho = lambd / mu
        L = rho / (1 - rho)
        Lq = rho**2 / (1 - rho)
        W = 1 / (mu - lambd)
        Wq = rho / (mu - lambd)

        st.subheader("📊 Hasil Perhitungan:")
        st.write(f"**Utilisasi (ρ):** {rho:.4f}")
        st.write(f"**Rata-rata pelanggan di sistem (L):** {L:.4f}")
        st.write(f"**Rata-rata pelanggan di antrian (Lq):** {Lq:.4f}")
        st.write(f"**Rata-rata waktu dalam sistem (W):** {W:.4f}")
        st.write(f"**Rata-rata waktu dalam antrian (Wq):** {Wq:.4f}")

        # 🕒 SIMULASI ANIMASI PELANGGAN
        st.subheader("🕒 Simulasi Animasi Kedatangan Pelanggan:")

        total_customers = 5
        queue_slots = ["[ ]", "[ ]", "[ ]", "[ ]", "[ ]"]
        status_text = st.empty()
        queue_display = st.empty()

        for i in range(total_customers):
            # Update slot
            queue_slots[i] = "[👤]"
            queue_display.text("Antrian: " + " ".join(queue_slots))
            status_text.text(f"Pelanggan {i+1} sedang dilayani...")
            time.sleep(1)

            # Kosongkan slot setelah dilayani
            queue_slots[i] = "[✔️]"
            queue_display.text("Antrian: " + " ".join(queue_slots))
            time.sleep(0.5)

        status_text.text("✅ Semua pelanggan telah dilayani.")

       # 📊 GRAFIK BATANG PARAMETER LENGKAP

        st.subheader("📊 Grafik Batang Parameter:")
        
        fig_bar, ax_bar = plt.subplots()
        
        # Parameter yang ditampilkan di grafik
        param_names = ["Utilisasi (ρ)", "L", "Lq", "W", "Wq"]
        param_values = [rho, L, Lq, W, Wq]
        
        # Warna untuk tiap batang
        colors = ["skyblue", "lightgreen", "salmon", "gold", "lightcoral"]
        
        # Membuat grafik batang
        ax_bar.bar(param_names, param_values, color=colors)
        
        # Label sumbu Y
        ax_bar.set_ylabel("Nilai")
        
        # Tampilkan grafik di Streamlit
        st.pyplot(fig_bar)


        # 📈 GRAFIK GABUNGAN: Semua Parameter terhadap λ
        st.subheader("📈 Grafik ρ, L, Lq, W, dan Wq terhadap Arrival Rate (λ)")

        # Pilih style lebih elegan
        plt.style.use("seaborn-v0_8")

        # Range λ (jangan terlalu dekat μ biar gak meledak)
        lambd_range = np.linspace(0.01, mu * 0.90, 100)

        # Hitung semua parameter
        rho_range = lambd_range / mu
        L_range = rho_range / (1 - rho_range)
        Lq_range = rho_range**2 / (1 - rho_range)
        W_range = 1 / (mu - lambd_range)
        Wq_range = rho_range / (mu - lambd_range)

        # Buat figure
        fig, ax = plt.subplots(figsize=(9,6))

        # Plot dengan linewidth lebih tebal
        ax.plot(lambd_range, rho_range, label="Utilisasi (ρ)", color="purple", linewidth=2)
        ax.plot(lambd_range, L_range, label="Rata-rata Pelanggan (L)", color="blue", linewidth=2)
        ax.plot(lambd_range, Lq_range, label="Rata-rata Antrian (Lq)", color="orange", linewidth=2)
        ax.plot(lambd_range, W_range, label="Waktu Sistem (W)", color="green", linewidth=2)
        ax.plot(lambd_range, Wq_range, label="Waktu Antrian (Wq)", color="red", linewidth=2)

        # Label dan judul
        ax.set_xlabel("λ (arrival rate)")
        ax.set_ylabel("Nilai Parameter")
        ax.set_title("Grafik ρ, L, Lq, W, dan Wq terhadap λ")
        ax.legend()

        # Grid
        ax.grid(True, linestyle='--', alpha=0.7)

        # Batas Y max biar gak terlalu tinggi
        ax.set_ylim(0, np.nanmax([L_range, W_range]) * 1.2)

        # Tampilkan grafik
        st.pyplot(fig)


else:
    st.info("Masukkan λ dan μ > 0 untuk memulai perhitungan.")
