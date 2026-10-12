# frontend/ui.py
import tkinter as tk
import time

# Impor struktur data yang sudah kita buat
from backend.m1_pesanan import Array, LinkList
from backend.m2_antrean import Stack, QueueNaif, QueueCircular

def buka_jendela():
    # ini untuk memori/data
    # note to self: buat jadi variabel biasa jangan OOP, biar bisa diakses langsung di fungsi tombol
    data_array = Array()
    data_linklist = LinkList()
    antrean_naif = QueueNaif()
    antrean_circular = QueueCircular()

    
    # JENDELA UTAMA
    
    layar = tk.Tk()
    layar.title("2EZ4U Food Delivery - Demo Pemula")
    layar.geometry("900x550")

    # fungsi - fungsi tombol yang langsung membaca data dari memori di atas
    
    def catat_waktu(nama_aksi, waktu_ms):
        # Nulis ke kotak log bawah
        teks = f"{nama_aksi} selesai dalam {waktu_ms:.4f} ms\n"
        kotak_log.config(state="normal")
        kotak_log.insert(tk.END, teks)
        kotak_log.see(tk.END) # Scroll otomatis ke bawah
        kotak_log.config(state="disabled")

    def tulis_ke_layar(pesan):
        # Nulis ke kotak output utama
        kotak_output.config(state="normal")
        kotak_output.insert(tk.END, pesan + "\n")
        kotak_output.see(tk.END)
        kotak_output.config(state="disabled")

    def klik_array_vip():
        pesanan = input_pesanan.get()
        jumlah = int(input_jumlah.get())
        
        mulai = time.perf_counter()
        for i in range(jumlah):
            data_array.insert(0, pesanan)
        selesai = time.perf_counter()
        
        waktu = (selesai - mulai) * 1000
        catat_waktu("Array VIP (Geser Data)", waktu)
        tulis_ke_layar(f"Array: {jumlah} pesanan masuk ke depan. Total = {data_array.jumlah}")

    def klik_linklist_vip():
        pesanan = input_pesanan.get()
        jumlah = int(input_jumlah.get())
        
        mulai = time.perf_counter()
        for i in range(jumlah):
            data_linklist.insert(0, pesanan)
        selesai = time.perf_counter()
        
        waktu = (selesai - mulai) * 1000
        catat_waktu("LinkList VIP (Ubah Pointer)", waktu)
        tulis_ke_layar(f"LinkList: {jumlah} pesanan masuk ke depan. Total = {data_linklist.jumlah}")

    def klik_masuk_antrean():
        pesanan = input_pesanan.get()
        jumlah = int(input_jumlah.get())
        
        mulai = time.perf_counter()
        for i in range(jumlah):
            antrean_naif.enqueue(pesanan)
            antrean_circular.enqueue(pesanan)
        selesai = time.perf_counter()
        
        waktu = (selesai - mulai) * 1000
        catat_waktu("Enqueue (Masuk Antrean)", waktu)
        tulis_ke_layar(f"Queue: Masuk {jumlah} orang. Naif = {len(antrean_naif.data)}, Circular = {antrean_circular.jumlah}")

    def klik_keluar_naif():
        jumlah = int(input_jumlah.get())
        antrean_naif.total_geseran = 0 # reset hitungan geser
        
        mulai = time.perf_counter()
        for i in range(jumlah):
            if len(antrean_naif.data) > 0:
                antrean_naif.dequeue()
        selesai = time.perf_counter()
        
        waktu = (selesai - mulai) * 1000
        catat_waktu("Dequeue Naif", waktu)
        tulis_ke_layar(f"Queue Naif melayani {jumlah} pesanan.")
        tulis_ke_layar(f"-> BUKTI LAMBAT: Ada {antrean_naif.total_geseran} geseran data secara manual!")

    def klik_keluar_circular():
        jumlah = int(input_jumlah.get())
        
        mulai = time.perf_counter()
        for i in range(jumlah):
            if antrean_circular.jumlah > 0:
                antrean_circular.dequeue()
        selesai = time.perf_counter()
        
        waktu = (selesai - mulai) * 1000
        catat_waktu("Dequeue Circular", waktu)
        tulis_ke_layar(f"Queue Circular melayani {jumlah} pesanan.")
        tulis_ke_layar(f"-> BUKTI CEPAT: 0 geseran. Cuma loket front yang maju!")

    # BAGIAN UI DAN LAYOUT
    
    # bagian kiri (menu)
    kiri = tk.Frame(layar, bg="lightgrey", width=200)
    kiri.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
    
    tk.Label(kiri, text="MENU M1", bg="lightgrey", font=("Arial", 10, "bold")).pack(pady=5)
    tk.Button(kiri, text="Array: VIP (Depan)", command=klik_array_vip, width=20).pack(pady=5)
    tk.Button(kiri, text="LinkList: VIP (Depan)", command=klik_linklist_vip, width=20).pack(pady=5)
    
    tk.Label(kiri, text="MENU M2", bg="lightgrey", font=("Arial", 10, "bold")).pack(pady=(20, 5))
    tk.Button(kiri, text="Masuk Antrean (Enqueue)", command=klik_masuk_antrean, width=20).pack(pady=5)
    tk.Button(kiri, text="Keluar Naif (Geser)", command=klik_keluar_naif, width=20).pack(pady=5)
    tk.Button(kiri, text="Keluar Circular (Putar)", command=klik_keluar_circular, width=20).pack(pady=5)

    # bagian kanan (area output)
    kanan = tk.Frame(layar)
    kanan.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Baris atas (utk input form)
    atas = tk.Frame(kanan)
    atas.pack(fill=tk.X)
    
    tk.Label(atas, text="Nama Pesanan:").pack(side=tk.LEFT)
    input_pesanan = tk.Entry(atas)
    input_pesanan.pack(side=tk.LEFT, padx=5)
    input_pesanan.insert(0, "Ayam Geprek")

    tk.Label(atas, text="Jumlah Simulasi Data:").pack(side=tk.LEFT, padx=(20, 0))
    input_jumlah = tk.Entry(atas, width=10)
    input_jumlah.pack(side=tk.LEFT, padx=5)
    input_jumlah.insert(0, "1000")

    # Kotak Teks Utama
    tk.Label(kanan, text="\nLayar Output:", font=("Arial", 10, "bold")).pack(anchor="w")
    kotak_output = tk.Text(kanan, height=12)
    kotak_output.pack(fill=tk.BOTH, expand=True)
    kotak_output.config(state="disabled")

    # Kotak Log Waktu
    tk.Label(kanan, text="Catatan Waktu:", font=("Arial", 10, "bold")).pack(anchor="w")
    kotak_log = tk.Text(kanan, height=8, bg="#e8f4f8")
    kotak_log.pack(fill=tk.X)
    kotak_log.config(state="disabled")

    # buat ngeoutput jendela
    layar.mainloop()