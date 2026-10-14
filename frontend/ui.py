import os
import csv
import time
import tkinter as tk
from tkinter import ttk

from backend.m1_pesanan import Array, LinkList, format_waktu, buat_baris_pesanan
from backend.m2_antrean import ke_postfix, hitung, ManajerM2
from backend.m3_laporan import (
    salin_potongan, insertion_sort, merge_sort,
    linear_search, binary_search, ManajerM3
)


# class utama jendela aplikasi tkinter untuk menghubungkan tombol menu dengan backend m1 sampai m3
class Aplikasi2EZ4U(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("2EZ4U Delivery Engine - Data Structures")
        self.geometry("1100x650")
        self.configure(bg="#eef2f0")

        # inisialisasi objek struktur data untuk m1, m2, dan m3
        self.array_m1 = Array()
        self.linklist_m1 = LinkList()
        self.manajer_m2 = ManajerM2()
        self.manajer_m3 = ManajerM3()
        self.nomor_oid_terakhir = 200000

        self.setup_ui()
        self.aksi_load_data()
        self.buka_menu_lihat("ARRAY")

    def setup_ui(self):
        # buat panel sebelah kiri untuk menampung daftar tombol menu
        panel_kiri = tk.Frame(self, width=270, bg="#dfe7e4", bd=1, relief=tk.SOLID)
        panel_kiri.pack(side=tk.LEFT, fill=tk.Y, padx=6, pady=6)
        panel_kiri.pack_propagate(False)

        # tambahkan canvas dan scrollbar supaya menu di panel kiri bisa di-scroll ke bawah
        self.canvas_menu = tk.Canvas(panel_kiri, bg="#dfe7e4", highlightthickness=0)
        scroll_menu = ttk.Scrollbar(panel_kiri, orient="vertical", command=self.canvas_menu.yview)
        self.frame_menu = tk.Frame(self.canvas_menu, bg="#dfe7e4")

        self.frame_menu.bind(
            "<Configure>",
            lambda e: self.canvas_menu.configure(scrollregion=self.canvas_menu.bbox("all"))
        )
        self.id_window_menu = self.canvas_menu.create_window((0, 0), window=self.frame_menu, anchor="nw")
        self.canvas_menu.bind(
            "<Configure>",
            lambda e: self.canvas_menu.itemconfig(self.id_window_menu, width=e.width)
        )
        self.canvas_menu.configure(yscrollcommand=scroll_menu.set)

        self.canvas_menu.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_menu.pack(side=tk.RIGHT, fill=tk.Y)

        # aktifkan scroll pakai mousewheel saat kursor diarahkan ke panel menu kiri
        self.bind_all("<MouseWheel>", self.scroll_menu_kiri)

        self.tambah_judul_grup("DATA")
        self.tambah_tombol_menu("Load Data", self.buka_menu_load)

        self.tambah_judul_grup("M1 - ORDER DATA")
        self.tambah_tombol_menu("ARRAY - VIEW ORDER", lambda: self.buka_menu_lihat("ARRAY"))
        self.tambah_tombol_menu("ARRAY - ADD REGULAR ORDER", lambda: self.buka_menu_tambah("ARRAY", "REGULAR"))
        self.tambah_tombol_menu("ARRAY - ADD PRIORITY ORDER", lambda: self.buka_menu_tambah("ARRAY", "PRIORITY"))
        self.tambah_tombol_menu("ARRAY - ADD VIP ORDER", lambda: self.buka_menu_tambah("ARRAY", "VIP"))
        self.tambah_tombol_menu("ARRAY - DELETE ORDER", lambda: self.buka_menu_hapus("ARRAY"))

        self.tambah_tombol_menu("LINKEDLIST - VIEW ORDER", lambda: self.buka_menu_lihat("LINKEDLIST"))
        self.tambah_tombol_menu("LINKEDLIST - ADD REGULAR ORDER", lambda: self.buka_menu_tambah("LINKEDLIST", "REGULAR"))
        self.tambah_tombol_menu("LINKEDLIST - ADD PRIORITY ORDER", lambda: self.buka_menu_tambah("LINKEDLIST", "PRIORITY"))
        self.tambah_tombol_menu("LINKEDLIST - ADD VIP ORDER", lambda: self.buka_menu_tambah("LINKEDLIST", "VIP"))
        self.tambah_tombol_menu("LINKEDLIST - DELETE ORDER", lambda: self.buka_menu_hapus("LINKEDLIST"))

        self.tambah_judul_grup("M2 - STACK AND QUEUE")
        self.tambah_tombol_menu("STACK - POSTFIX (CASHIER)", self.buka_menu_stack_postfix)
        self.tambah_tombol_menu("STACK - UNDO", self.buka_menu_stack_undo)
        self.tambah_tombol_menu("STACK - REDO", self.buka_menu_stack_redo)
        self.tambah_tombol_menu("QUEUE - ENQUEUE", self.buka_menu_queue_enqueue)
        self.tambah_tombol_menu("QUEUE - DEQUEUE NAIVE", self.buka_menu_queue_dequeue_naif)
        self.tambah_tombol_menu("QUEUE - DEQUEUE CIRCULAR", self.buka_menu_queue_dequeue_circular)

        self.tambah_judul_grup("M3 - SORT AND SEARCH")
        self.tambah_tombol_menu("SORT - INSERTION SORT", self.buka_menu_insertion_sort)
        self.tambah_tombol_menu("SORT - MERGE SORT", self.buka_menu_merge_sort)
        self.tambah_tombol_menu("SEARCH - LINEAR SEARCH", self.buka_menu_linear_search)
        self.tambah_tombol_menu("SEARCH - BINARY SEARCH", self.buka_menu_binary_search)

        # buat panel sebelah kanan untuk menampilkan form input, tabel data, dan log waktu
        panel_kanan = tk.Frame(self, bg="#ffffff", bd=1, relief=tk.SOLID)
        panel_kanan.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0, 6), pady=6)

        self.frame_form_atas = tk.Frame(panel_kanan, bg="#ffffff", padx=14, pady=10)
        self.frame_form_atas.pack(side=tk.TOP, fill=tk.X)

        tk.Frame(panel_kanan, bg="#cfd8d4", height=1).pack(fill=tk.X, padx=14)

        # area tengah untuk teks ringkasan hasil dan tabel treeview
        frame_tengah = tk.Frame(panel_kanan, bg="#ffffff", padx=14, pady=8)
        frame_tengah.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.label_ringkasan = tk.Label(
            frame_tengah, text="", bg="#ffffff", fg="#1b2b26",
            font=("Consolas", 10), justify=tk.LEFT, anchor="w"
        )
        self.label_ringkasan.pack(side=tk.TOP, fill=tk.X, pady=(0, 6))

        frame_tabel = tk.Frame(frame_tengah, bg="#ffffff")
        frame_tabel.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.tabel = ttk.Treeview(frame_tabel, show="headings", height=12)
        scroll_tabel = ttk.Scrollbar(frame_tabel, orient="vertical", command=self.tabel.yview)
        self.tabel.configure(yscrollcommand=scroll_tabel.set)
        self.tabel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_tabel.pack(side=tk.RIGHT, fill=tk.Y)

        # area bawah untuk menampilkan catatan waktu eksekusi tiap perintah (command log)
        frame_bawah = tk.Frame(panel_kanan, bg="#ffffff", padx=14, pady=8)
        frame_bawah.pack(side=tk.BOTTOM, fill=tk.X)

        tk.Label(
            frame_bawah, text="COMMAND LOG", bg="#ffffff", fg="#2d5a4c",
            font=("Segoe UI", 8, "bold")
        ).pack(anchor="w")

        frame_log = tk.Frame(frame_bawah, bd=1, relief=tk.SOLID)
        frame_log.pack(fill=tk.X, pady=2)

        self.teks_command = tk.Text(
            frame_log, height=5, font=("Consolas", 9), state="disabled", bg="#f7faf9"
        )
        scroll_log = ttk.Scrollbar(frame_log, orient="vertical", command=self.teks_command.yview)
        self.teks_command.configure(yscrollcommand=scroll_log.set)
        self.teks_command.pack(side=tk.LEFT, fill=tk.X, expand=True)
        scroll_log.pack(side=tk.RIGHT, fill=tk.Y)

    def scroll_menu_kiri(self, event):
        # cek apakah kursor mouse sedang berada di area panel kiri sebelum menggeser menu
        if self.winfo_containing(event.x_root, event.y_root) in (self.canvas_menu, self.frame_menu) or event.x_root - self.winfo_rootx() < 280:
            self.canvas_menu.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def tambah_judul_grup(self, teks):
        tk.Label(
            self.frame_menu, text=teks, bg="#dfe7e4", fg="#2d5a4c",
            font=("Segoe UI", 8, "bold"), anchor="w", padx=6
        ).pack(fill=tk.X, pady=(6, 1))

    def tambah_tombol_menu(self, teks, fungsi_klik):
        tk.Button(
            self.frame_menu, text=teks, command=fungsi_klik,
            anchor="w", bg="#ffffff", fg="#1b2b26", activebackground="#c7dcd4",
            font=("Segoe UI", 8), relief=tk.FLAT, bd=1, padx=6, pady=2
        ).pack(fill=tk.X, padx=5, pady=1)

    def catat_command(self, nama_cmd, kategori_modul, waktu_ms):
        # tambahkan catatan waktu eksekusi baru di baris paling atas command log
        baris = f"{nama_cmd:<24} -> {kategori_modul:<20} {waktu_ms:>7.2f} ms\n"
        self.teks_command.config(state="normal")
        self.teks_command.insert("1.0", baris)
        self.teks_command.config(state="disabled")

    def atur_tabel(self, daftar_kolom, lebar_kolom, baris_data):
        # kosongkan isi tabel lama lalu atur ulang header kolom dan masukkan data baru
        self.tabel.delete(*self.tabel.get_children())
        self.tabel["columns"] = daftar_kolom
        for i in range(len(daftar_kolom)):
            kol = daftar_kolom[i]
            self.tabel.heading(kol, text=kol)
            self.tabel.column(kol, width=lebar_kolom[i], anchor="w")
        for r in range(baris_data.jumlah):
            self.tabel.insert("", tk.END, values=baris_data.get(r))

    def tampilkan_detail_satu_pesanan(self, p):
        baris = Array()
        if p is not None:
            baris.append(("oid", p[0]))
            baris.append(("customer", p[1]))
            baris.append(("resto", p[2]))
            baris.append(("menu", p[3]))
            baris.append(("price", f"{int(p[4]):,}"))
            baris.append(("priority", str(p[5])))
            baris.append(("time_in", format_waktu(p[6])))
            baris.append(("time_out", format_waktu(p[7])))
            baris.append(("status", p[8]))
        self.atur_tabel(("column", "value"), (160, 420), baris)

    def tampilkan_daftar_pesanan(self, data_pesanan, batas_tampil=50):
        baris = Array()
        batas = data_pesanan.jumlah if data_pesanan.jumlah < batas_tampil else batas_tampil
        for i in range(batas):
            p = data_pesanan.get(i)
            baris.append((i + 1, p[0], p[1], p[2], p[3], format_waktu(p[6])))
        self.atur_tabel(("#", "oid", "customer", "resto", "menu", "time_in"), (40, 90, 180, 140, 140, 90), baris)

    def tampilkan_tabel_sort_m3(self, data_pesanan, batas_tampil=100):
        baris = Array()
        batas = data_pesanan.jumlah if data_pesanan.jumlah < batas_tampil else batas_tampil
        for i in range(batas):
            p = data_pesanan.get(i)
            baris.append((i + 1, p[0], f"{int(p[4]):,}", format_waktu(p[7]), p[2], p[3]))
        self.atur_tabel(("#", "oid", "price", "time_out", "resto", "menu"), (40, 90, 90, 100, 150, 150), baris)

    def reset_form_atas(self, judul):
        for widget in self.frame_form_atas.winfo_children():
            widget.destroy()
        tk.Label(
            self.frame_form_atas, text=judul, bg="#ffffff", fg="#2d5a4c",
            font=("Segoe UI", 11, "bold"), anchor="w"
        ).pack(fill=tk.X, pady=(0, 6))

    def buka_menu_load(self):
        self.reset_form_atas("Data: Load pesanan.csv file")
        tk.Button(
            self.frame_form_atas, text="LOAD DATA", command=self.aksi_load_data,
            bg="#2d5a4c", fg="white", font=("Segoe UI", 9, "bold"), padx=18, pady=3
        ).pack(anchor="w")

    def aksi_load_data(self):
        # baca file pesanan.csv lalu simpan datanya ke array m1, linked list m1, dan antrean m2
        mulai = time.perf_counter()
        self.array_m1 = Array()
        self.linklist_m1 = LinkList()

        jalur_csv = None
        for kandidat in ("data/pesanan.csv", "pesanan.csv", "data/data.csv"):
            if os.path.exists(kandidat):
                jalur_csv = kandidat
                break

        if jalur_csv is None:
            self.label_ringkasan.config(text="pesanan.csv file could not be found in the source folders.")
            self.atur_tabel(("#", "oid", "customer", "resto", "menu", "time_in"), (40, 90, 180, 140, 140, 90), Array())
            return

        with open(jalur_csv, "r", encoding="utf-8") as f:
            pembaca = csv.reader(f)
            baris_pertama = True
            for bagian in pembaca:
                if baris_pertama:
                    baris_pertama = False
                    continue
                if len(bagian) >= 9:
                    item = [
                        bagian[0], bagian[1], bagian[2], bagian[3],
                        int(bagian[4]), int(bagian[5]),
                        bagian[6], bagian[7], bagian[8]
                    ]
                    self.array_m1.append(item)
                    self.linklist_m1.append(item)

        self.nomor_oid_terakhir = self.array_m1.jumlah
        self.manajer_m2.reset_dan_muat(self.array_m1)
        self.manajer_m3.reset()

        waktu_ms = (time.perf_counter() - mulai) * 1000
        self.catat_command("load", "M1 - array", waktu_ms)

        st = self.manajer_m2.stats()
        self.label_ringkasan.config(
            text=f"Loaded {self.array_m1.jumlah:,} orders from {jalur_csv}.\n"
                 f"Queue contains {st[0]:,} orders with ANTRE status."
        )
        self.tampilkan_daftar_pesanan(self.array_m1, batas_tampil=20)

    def buka_menu_lihat(self, tipe):
        nama = "Array" if tipe == "ARRAY" else "Linked List"
        self.reset_form_atas(f"{nama}: View order at index i")
        baris_input = tk.Frame(self.frame_form_atas, bg="#ffffff")
        baris_input.pack(anchor="w")
        tk.Label(baris_input, text="Index i:", bg="#ffffff").pack(side=tk.LEFT)
        input_index = tk.Entry(baris_input, width=12)
        input_index.pack(side=tk.LEFT, padx=8)
        input_index.insert(0, "0")

        def eksekusi():
            try:
                i = int(input_index.get().strip())
            except ValueError:
                return
            mulai = time.perf_counter()
            hasil = self.array_m1.get(i) if tipe == "ARRAY" else self.linklist_m1.get(i)
            waktu_ms = (time.perf_counter() - mulai) * 1000
            self.catat_command(
                "array_get" if tipe == "ARRAY" else "linklist_get",
                "M1 - array" if tipe == "ARRAY" else "M1 - linklist",
                waktu_ms
            )
            if hasil is None:
                self.label_ringkasan.config(text=f"Index {i} not found.")
                self.atur_tabel(("column", "value"), (160, 420), Array())
            else:
                self.label_ringkasan.config(text=f"Order at {nama} index {i}: {hasil[0]} ({hasil[1]})")
                self.tampilkan_detail_satu_pesanan(hasil)

        tk.Button(baris_input, text="VIEW", command=eksekusi, bg="#2d5a4c", fg="white", font=("Segoe UI", 9, "bold"), padx=14).pack(side=tk.LEFT)

    def buka_menu_tambah(self, tipe, jenis_pesanan):
        nama = "Array" if tipe == "ARRAY" else "Linked List"
        kode_prio = 3 if jenis_pesanan == "REGULAR" else (2 if jenis_pesanan == "PRIORITY" else 1)
        self.reset_form_atas(f"{nama}: Add {jenis_pesanan.lower()} order")

        baris_input = tk.Frame(self.frame_form_atas, bg="#ffffff")
        baris_input.pack(anchor="w")
        tk.Label(baris_input, text="Customer name:", bg="#ffffff").pack(side=tk.LEFT)
        input_nama = tk.Entry(baris_input, width=22)
        input_nama.pack(side=tk.LEFT, padx=8)
        input_nama.insert(0, "New Customer")

        def eksekusi():
            self.nomor_oid_terakhir += 1
            pesanan = buat_baris_pesanan(self.nomor_oid_terakhir, input_nama.get(), kode_prio)
            struktur = self.array_m1 if tipe == "ARRAY" else self.linklist_m1

            mulai = time.perf_counter()
            if jenis_pesanan == "REGULAR":
                posisi = struktur.jumlah
                struktur.append(pesanan)
            elif jenis_pesanan == "PRIORITY":
                posisi = struktur.jumlah // 2
                struktur.insert(posisi, pesanan)
            else:
                posisi = 0
                struktur.insert(0, pesanan)
            waktu_ms = (time.perf_counter() - mulai) * 1000

            self.manajer_m3.reset()
            self.catat_command(
                f"{tipe.lower()}_{jenis_pesanan.lower()}",
                "M1 - array" if tipe == "ARRAY" else "M1 - linklist",
                waktu_ms
            )
            self.label_ringkasan.config(text=f"Order {pesanan[0]} inserted at index {posisi}. Total elements in {nama}: {struktur.jumlah:,}.")
            self.tampilkan_detail_satu_pesanan(pesanan)

        tk.Button(baris_input, text="ADD", command=eksekusi, bg="#2d5a4c", fg="white", font=("Segoe UI", 9, "bold"), padx=14).pack(side=tk.LEFT)

    def buka_menu_hapus(self, tipe):
        nama = "Array" if tipe == "ARRAY" else "Linked List"
        self.reset_form_atas(f"{nama}: Delete order at index i")
        baris_input = tk.Frame(self.frame_form_atas, bg="#ffffff")
        baris_input.pack(anchor="w")
        tk.Label(baris_input, text="Index i:", bg="#ffffff").pack(side=tk.LEFT)
        input_index = tk.Entry(baris_input, width=12)
        input_index.pack(side=tk.LEFT, padx=8)
        input_index.insert(0, "0")

        def eksekusi():
            try:
                i = int(input_index.get().strip())
            except ValueError:
                return
            struktur = self.array_m1 if tipe == "ARRAY" else self.linklist_m1
            mulai = time.perf_counter()
            dihapus = struktur.delete(i)
            waktu_ms = (time.perf_counter() - mulai) * 1000

            self.manajer_m3.reset()
            self.catat_command(
                "array_delete" if tipe == "ARRAY" else "linklist_delete",
                "M1 - array" if tipe == "ARRAY" else "M1 - linklist",
                waktu_ms
            )
            if dihapus is None:
                self.label_ringkasan.config(text=f"Index {i} out of bounds.")
                self.atur_tabel(("column", "value"), (160, 420), Array())
            else:
                self.label_ringkasan.config(text=f"Order {dihapus[0]} at index {i} deleted. Remaining elements in {nama}: {struktur.jumlah:,}.")
                self.tampilkan_detail_satu_pesanan(dihapus)

        tk.Button(baris_input, text="DELETE", command=eksekusi, bg="#2d5a4c", fg="white", font=("Segoe UI", 9, "bold"), padx=14).pack(side=tk.LEFT)

    def buka_menu_stack_postfix(self):
        self.reset_form_atas("Stack: Calculate receipt via postfix")
        baris_input = tk.Frame(self.frame_form_atas, bg="#ffffff")
        baris_input.pack(anchor="w")
        tk.Label(baris_input, text="Receipt (infix):", bg="#ffffff").pack(side=tk.LEFT)
        input_struk = tk.Entry(baris_input, width=34)
        input_struk.pack(side=tk.LEFT, padx=8)
        input_struk.insert(0, "(3 * 12000) + (2 * 8500) - 5000")

        def eksekusi():
            eks = input_struk.get()
            list_langkah = Array()
            mulai = time.perf_counter()
            hasil_postfix = ke_postfix(eks, list_langkah)
            total = hitung(hasil_postfix, list_langkah)
            waktu_ms = (time.perf_counter() - mulai) * 1000

            self.catat_command("stack_postfix", "M2 - stack", waktu_ms)
            self.label_ringkasan.config(
                text=f"Receipt : {eks}\nPostfix : {hasil_postfix}\nTOTAL   : Rp {total:,}"
            )
            self.atur_tabel(("step", "token", "action", "stack", "output"), (70, 80, 230, 160, 220), list_langkah)

        tk.Button(baris_input, text="CALCULATE", command=eksekusi, bg="#2d5a4c", fg="white", font=("Segoe UI", 9, "bold"), padx=14).pack(side=tk.LEFT)

    def buka_menu_stack_undo(self):
        # menu untuk membatalkan aksi terakhir pada antrean dan mengembalikan status pesanannya
        self.reset_form_atas("Stack: Undo last queue action")

        def eksekusi():
            mulai = time.perf_counter()
            catatan = self.manajer_m2.undo_last()
            waktu_ms = (time.perf_counter() - mulai) * 1000
            self.catat_command("stack_undo", "M2 - stack", waktu_ms)

            st = self.manajer_m2.stats()
            if catatan is None:
                self.label_ringkasan.config(text="Undo stack is empty.")
                self.atur_tabel(("#", "oid", "customer", "resto", "menu"), (50, 110, 180, 150, 150), Array())
                return

            jenis, data = catatan[0], catatan[1]
            if jenis == "ENQUEUE":
                # kalau membatalkan enqueue, ubah status pesanan jadi cancel
                data[8] = "CANCEL"
                self.label_ringkasan.config(
                    text=f"Undo enqueue: {data[0]} removed from the back.\n"
                         f"Current queue length: naive {st[0]:,}, circular {st[1]:,}. Undo stack remaining: {st[4]}."
                )
                baris = Array()
                baris.append((1, data[0], data[1], data[2], data[3]))
                self.atur_tabel(("#", "oid", "customer", "resto", "menu"), (40, 90, 180, 140, 140), baris)
            else:
                # kalau membatalkan dequeue, kembalikan status pesanan jadi antre dan kosongkan waktu selesainya
                for i in range(data.jumlah):
                    p = data.get(i)
                    p[8] = "ANTRE"
                    p[7] = ""
                nama_jenis = jenis.split('_')[1].lower() if '_' in jenis else jenis.lower()
                self.label_ringkasan.config(
                    text=f"Undo {nama_jenis}: {data.jumlah} orders returned to the FRONT of the queue.\n"
                         f"Current queue length: naive {st[0]:,}, circular {st[1]:,}. Undo stack remaining: {st[4]}."
                )
                self.tampilkan_daftar_pesanan(data)

        tk.Button(self.frame_form_atas, text="UNDO ACTION", command=eksekusi, bg="#2d5a4c", fg="white", font=("Segoe UI", 9, "bold"), padx=20).pack(anchor="w")

    def buka_menu_stack_redo(self):
        # menu untuk menjalankan ulang aksi yang baru saja dibatalkan lewat undo
        self.reset_form_atas("Stack: Redo reversed action")

        def eksekusi():
            mulai = time.perf_counter()
            catatan = self.manajer_m2.redo_last()
            waktu_ms = (time.perf_counter() - mulai) * 1000
            self.catat_command("stack_redo", "M2 - stack", waktu_ms)

            st = self.manajer_m2.stats()
            if catatan is None:
                self.label_ringkasan.config(text="Redo stack is empty.")
                self.atur_tabel(("#", "oid", "customer", "resto", "menu"), (50, 110, 180, 150, 150), Array())
                return

            jenis, data = catatan[0], catatan[1]
            if jenis == "ENQUEUE":
                # kembalikan status pesanan jadi antre saat enqueue dijalankan ulang
                data[8] = "ANTRE"
                self.label_ringkasan.config(
                    text=f"Redo enqueue: {data[0]} pushed back to the rear.\n"
                         f"Current queue length: naive {st[0]:,}, circular {st[1]:,}. Undo: {st[4]}, redo: {st[5]}."
                )
                baris = Array()
                baris.append((1, data[0], data[1], data[2], data[3]))
                self.atur_tabel(("#", "oid", "customer", "resto", "menu"), (40, 90, 180, 140, 140), baris)
            else:
                # ubah kembali status pesanan jadi done dan isi waktu selesainya saat dequeue dijalankan ulang
                for i in range(data.jumlah):
                    p = data.get(i)
                    p[8] = "DONE"
                    t_masuk = int(p[6]) if str(p[6]).isdigit() else 28800
                    p[7] = str(t_masuk + 1500)
                nama_jenis = jenis.split('_')[1].lower() if '_' in jenis else jenis.lower()
                self.label_ringkasan.config(
                    text=f"Redo {nama_jenis}: {data.jumlah} orders re-dequeued from the queue.\n"
                         f"Current queue length: naive {st[0]:,}, circular {st[1]:,}. Undo: {st[4]}, redo: {st[5]}."
                )
                self.tampilkan_daftar_pesanan(data)

        tk.Button(self.frame_form_atas, text="REDO ACTION", command=eksekusi, bg="#2d5a4c", fg="white", font=("Segoe UI", 9, "bold"), padx=20).pack(anchor="w")

    def buka_menu_queue_enqueue(self):
        self.reset_form_atas("Queue: Enqueue new order to the rear")
        baris_input = tk.Frame(self.frame_form_atas, bg="#ffffff")
        baris_input.pack(anchor="w")
        tk.Label(baris_input, text="Customer name:", bg="#ffffff").pack(side=tk.LEFT)
        input_nama = tk.Entry(baris_input, width=20)
        input_nama.pack(side=tk.LEFT, padx=8)
        input_nama.insert(0, "X2")

        def eksekusi():
            self.nomor_oid_terakhir += 1
            pesanan = buat_baris_pesanan(self.nomor_oid_terakhir, input_nama.get(), 2, "ANTRE")

            # simpan juga pesanan baru ke struktur data m1 supaya datanya tetap sinkron
            self.array_m1.append(pesanan)
            self.linklist_m1.append(pesanan)

            mulai = time.perf_counter()
            self.manajer_m2.enqueue_baru(pesanan)
            waktu_ms = (time.perf_counter() - mulai) * 1000
            self.catat_command("queue_enqueue", "M2 - queue", waktu_ms)

            st = self.manajer_m2.stats()
            self.label_ringkasan.config(
                text=f"Order {pesanan[0]} enqueued to the back of both queues.\n"
                     f"Current length: naive {st[0]:,}, circular {st[1]:,}."
            )
            self.tampilkan_detail_satu_pesanan(pesanan)

        tk.Button(baris_input, text="ENQUEUE", command=eksekusi, bg="#2d5a4c", fg="white", font=("Segoe UI", 9, "bold"), padx=14).pack(side=tk.LEFT)

    def buka_menu_queue_dequeue_naif(self):
        self.reset_form_atas("Queue naive: Dequeue from front by shifting elements")
        baris_input = tk.Frame(self.frame_form_atas, bg="#ffffff")
        baris_input.pack(anchor="w")
        tk.Label(baris_input, text="Dequeue count:", bg="#ffffff").pack(side=tk.LEFT)
        input_jumlah = tk.Entry(baris_input, width=10)
        input_jumlah.pack(side=tk.LEFT, padx=8)
        input_jumlah.insert(0, "2")

        def eksekusi():
            try:
                banyak = int(input_jumlah.get().strip())
            except ValueError:
                return
            mulai = time.perf_counter()
            keluar, geser_aksi = self.manajer_m2.dequeue_naif_banyak(banyak)
            waktu_ms = (time.perf_counter() - mulai) * 1000

            # update status pesanan yang sudah dilayani jadi done beserta waktu selesainya
            for i in range(keluar.jumlah):
                p = keluar.get(i)
                p[8] = "DONE"
                t_masuk = int(p[6]) if str(p[6]).isdigit() else 28800
                p[7] = str(t_masuk + 1500)

            self.catat_command("queue_dequeue_naive", "M2 - queue naive", waktu_ms)
            rata = geser_aksi // keluar.jumlah if keluar.jumlah > 0 else 0
            st = self.manajer_m2.stats()
            self.label_ringkasan.config(
                text=f"{keluar.jumlah} orders dequeued from the naive queue.\n"
                     f"Total {geser_aksi:,} elements shifted, averaging {rata:,} shifts per order.\n"
                     f"Remaining {st[0]:,} orders in the naive queue."
            )
            self.tampilkan_daftar_pesanan(keluar)

        tk.Button(baris_input, text="DEQUEUE", command=eksekusi, bg="#2d5a4c", fg="white", font=("Segoe UI", 9, "bold"), padx=14).pack(side=tk.LEFT)

    def buka_menu_queue_dequeue_circular(self):
        self.reset_form_atas("Queue circular: Dequeue by advancing front pointer")
        baris_input = tk.Frame(self.frame_form_atas, bg="#ffffff")
        baris_input.pack(anchor="w")
        tk.Label(baris_input, text="Dequeue count:", bg="#ffffff").pack(side=tk.LEFT)
        input_jumlah = tk.Entry(baris_input, width=10)
        input_jumlah.pack(side=tk.LEFT, padx=8)
        input_jumlah.insert(0, "2")

        def eksekusi():
            try:
                banyak = int(input_jumlah.get().strip())
            except ValueError:
                return
            mulai = time.perf_counter()
            keluar = self.manajer_m2.dequeue_circular_banyak(banyak)
            waktu_ms = (time.perf_counter() - mulai) * 1000

            # update status pesanan yang sudah dilayani jadi done beserta waktu selesainya
            for i in range(keluar.jumlah):
                p = keluar.get(i)
                p[8] = "DONE"
                t_masuk = int(p[6]) if str(p[6]).isdigit() else 28800
                p[7] = str(t_masuk + 1500)

            self.catat_command("queue_dequeue_circular", "M2 - queue circular", waktu_ms)
            st = self.manajer_m2.stats()
            front_skrg = self.manajer_m2.circular.front
            rear_skrg = self.manajer_m2.circular.rear
            self.label_ringkasan.config(
                text=f"{keluar.jumlah} orders dequeued from the circular queue.\n"
                     f"0 elements shifted. Front pointer moved to {front_skrg}, rear at {rear_skrg:,}, capacity {st[2]:,}.\n"
                     f"Remaining {st[1]:,} orders in the circular queue."
            )
            self.tampilkan_daftar_pesanan(keluar)

        tk.Button(baris_input, text="DEQUEUE", command=eksekusi, bg="#2d5a4c", fg="white", font=("Segoe UI", 9, "bold"), padx=14).pack(side=tk.LEFT)

    def buka_menu_insertion_sort(self):
        self.reset_form_atas("Sort: Insertion sort, O(n²)")
        baris_input = tk.Frame(self.frame_form_atas, bg="#ffffff")
        baris_input.pack(anchor="w")

        tk.Label(baris_input, text="Rows to sort:", bg="#ffffff").pack(side=tk.LEFT)
        input_jumlah = tk.Entry(baris_input, width=10)
        input_jumlah.pack(side=tk.LEFT, padx=(6, 16))
        input_jumlah.insert(0, "10")

        tk.Label(baris_input, text="Sort by:", bg="#ffffff").pack(side=tk.LEFT)
        combo_kunci = ttk.Combobox(baris_input, values=("oid", "harga", "selesai"), state="readonly", width=12)
        combo_kunci.pack(side=tk.LEFT, padx=(6, 16))
        combo_kunci.set("harga")

        def eksekusi():
            try:
                jml = int(input_jumlah.get().strip())
            except ValueError:
                return
            if jml > 20000:
                self.label_ringkasan.config(text="REJECTED: maximum capacity is 20,000 rows. Use merge sort for full data.")
                self.atur_tabel(("#", "oid", "price", "time_out", "resto", "menu"), (40, 90, 90, 100, 150, 150), Array())
                return

            kunci = combo_kunci.get()
            potongan = salin_potongan(self.array_m1, jml)
            mulai = time.perf_counter()
            terurut, banding, pindah = insertion_sort(potongan, kunci)
            waktu_ms = (time.perf_counter() - mulai) * 1000

            self.catat_command("insertion_sort", "M3 - insertion sort", waktu_ms)
            self.label_ringkasan.config(
                text=f"{terurut.jumlah:,} orders stably sorted by {kunci}.\n"
                     f"{banding:,} comparisons, {pindah:,} movements."
            )
            self.tampilkan_tabel_sort_m3(terurut, batas_tampil=100)

        tk.Button(baris_input, text="SORT", command=eksekusi, bg="#2d5a4c", fg="white", font=("Segoe UI", 9, "bold"), padx=14).pack(side=tk.LEFT)

    def buka_menu_merge_sort(self):
        self.reset_form_atas("Sort: Merge sort, O(n log n)")
        baris_input = tk.Frame(self.frame_form_atas, bg="#ffffff")
        baris_input.pack(anchor="w")

        tk.Label(baris_input, text="Rows to sort:", bg="#ffffff").pack(side=tk.LEFT)
        input_jumlah = tk.Entry(baris_input, width=10)
        input_jumlah.pack(side=tk.LEFT, padx=(6, 16))
        input_jumlah.insert(0, "4000")

        tk.Label(baris_input, text="Sort by:", bg="#ffffff").pack(side=tk.LEFT)
        combo_kunci = ttk.Combobox(baris_input, values=("oid", "harga", "selesai"), state="readonly", width=12)
        combo_kunci.pack(side=tk.LEFT, padx=(6, 16))
        combo_kunci.set("oid")

        def eksekusi():
            try:
                jml = int(input_jumlah.get().strip())
            except ValueError:
                return
            kunci = combo_kunci.get()
            potongan = salin_potongan(self.array_m1, jml)
            mulai = time.perf_counter()
            terurut, banding, pindah = merge_sort(potongan, kunci)
            waktu_ms = (time.perf_counter() - mulai) * 1000

            self.catat_command("merge_sort", "M3 - merge sort", waktu_ms)
            self.label_ringkasan.config(
                text=f"{terurut.jumlah:,} orders stably sorted by {kunci}.\n"
                     f"{banding:,} comparisons, {pindah:,} movements."
            )
            self.tampilkan_tabel_sort_m3(terurut, batas_tampil=100)

        tk.Button(baris_input, text="SORT", command=eksekusi, bg="#2d5a4c", fg="white", font=("Segoe UI", 9, "bold"), padx=14).pack(side=tk.LEFT)

    def buka_menu_linear_search(self):
        self.reset_form_atas("Search: Linear search, O(n)")
        baris_input = tk.Frame(self.frame_form_atas, bg="#ffffff")
        baris_input.pack(anchor="w")

        tk.Label(baris_input, text="Order ID (oid):", bg="#ffffff").pack(side=tk.LEFT)
        input_oid = tk.Entry(baris_input, width=18)
        input_oid.pack(side=tk.LEFT, padx=8)
        input_oid.insert(0, "O-137442")

        def eksekusi():
            target = input_oid.get().strip()
            mulai = time.perf_counter()
            idx, ketemu, banding = linear_search(self.array_m1, target)
            waktu_ms = (time.perf_counter() - mulai) * 1000

            self.catat_command("linear_search", "M3 - linear search", waktu_ms)
            if ketemu is None:
                self.label_ringkasan.config(text=f"Order {target} not found.\n{banding:,} comparisons used.")
                self.atur_tabel(("column", "value"), (160, 420), Array())
            else:
                self.label_ringkasan.config(text=f"Found at index {idx:,}.\n{banding:,} comparisons used.")
                self.tampilkan_detail_satu_pesanan(ketemu)

        tk.Button(baris_input, text="SEARCH", command=eksekusi, bg="#2d5a4c", fg="white", font=("Segoe UI", 9, "bold"), padx=14).pack(side=tk.LEFT)

    def buka_menu_binary_search(self):
        self.reset_form_atas("Search: Binary search, O(log n)")
        baris_input = tk.Frame(self.frame_form_atas, bg="#ffffff")
        baris_input.pack(anchor="w")

        tk.Label(baris_input, text="Order ID (oid):", bg="#ffffff").pack(side=tk.LEFT)
        input_oid = tk.Entry(baris_input, width=18)
        input_oid.pack(side=tk.LEFT, padx=8)
        input_oid.insert(0, "O-137442")

        def eksekusi():
            target = input_oid.get().strip()
            arr_urut, waktu_bangun = self.manajer_m3.pastikan_terurut_oid(self.array_m1)

            mulai = time.perf_counter()
            idx, ketemu, banding = binary_search(arr_urut, target)
            waktu_ms = (time.perf_counter() - mulai) * 1000

            self.catat_command("binary_search", "M3 - binary search", waktu_ms)
            if ketemu is None:
                self.label_ringkasan.config(
                    text=f"Sorted oid list built using merge sort in {waktu_bangun:.2f} ms.\n"
                         f"Order {target} not found after {banding:,} comparisons."
                )
                self.atur_tabel(("column", "value"), (160, 420), Array())
            else:
                self.label_ringkasan.config(
                    text=f"Sorted oid list built using merge sort in {waktu_bangun:.2f} ms.\n"
                         f"Found at row {idx + 1:,} out of {arr_urut.jumlah:,} rows.\n"
                         f"Requires only {banding:,} comparisons."
                )
                self.tampilkan_detail_satu_pesanan(ketemu)

        tk.Button(baris_input, text="SEARCH", command=eksekusi, bg="#2d5a4c", fg="white", font=("Segoe UI", 9, "bold"), padx=14).pack(side=tk.LEFT)