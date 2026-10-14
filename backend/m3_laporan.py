import time
from backend.m1_pesanan import Array


# fungsi untuk mengambil nilai kolom dari data pesanan sesuai kunci pengurutan yang dipilih
def ambil_kunci(pesanan, kunci):
    if kunci == "oid":
        return pesanan[0]
    elif kunci == "harga":
        return pesanan[4]
    elif kunci == "selesai":
        # kalau pesanan belum selesai (masih kosong), beri angka sangat besar supaya ditaruh di paling bawah
        teks = str(pesanan[7]).strip()
        if teks == "" or teks == "-":
            return 999999999
        return int(teks)
    return pesanan[0]


# fungsi untuk menyalin n baris pertama dari array utama supaya urutan data asli tidak berubah
def salin_potongan(arr_asal, jumlah_ambil):
    batas = jumlah_ambil
    if batas > arr_asal.jumlah:
        batas = arr_asal.jumlah
    if batas < 0:
        batas = 0

    hasil = Array(kapasitas_awal=batas if batas > 4 else 4)
    for i in range(batas):
        hasil.data[i] = arr_asal.data[i]
    hasil.jumlah = batas
    return hasil


# fungsi insertion sort yang menggeser elemen ke kiri sampai menemukan posisi urutannya (o(n^2))
def insertion_sort(arr, kunci="harga"):
    perbandingan = 0
    pemindahan = 0

    for i in range(1, arr.jumlah):
        item_sekarang = arr.data[i]
        nilai_sekarang = ambil_kunci(item_sekarang, kunci)
        j = i - 1

        # pakai tanda > (bukan >=) supaya urutan data yang nilainya sama tidak tertukar (tetap stabil)
        while j >= 0:
            perbandingan += 1
            if ambil_kunci(arr.data[j], kunci) > nilai_sekarang:
                arr.data[j + 1] = arr.data[j]
                pemindahan += 1
                j -= 1
            else:
                break

        arr.data[j + 1] = item_sekarang
        pemindahan += 1

    return arr, perbandingan, pemindahan


# fungsi bantu untuk menggabungkan dua potongan array yang sudah terurut
def gabung_array(kiri, kanan, kunci):
    total = kiri.jumlah + kanan.jumlah
    hasil = Array(kapasitas_awal=total if total > 4 else 4)
    i = 0
    j = 0
    k = 0
    perbandingan = 0

    d_kiri = kiri.data
    d_kanan = kanan.data
    d_hasil = hasil.data

    # bandingkan elemen terdepan kiri dan kanan, pakai <= supaya elemen kiri didahulukan kalau nilainya sama
    while i < kiri.jumlah and j < kanan.jumlah:
        perbandingan += 1
        if ambil_kunci(d_kiri[i], kunci) <= ambil_kunci(d_kanan[j], kunci):
            d_hasil[k] = d_kiri[i]
            i += 1
        else:
            d_hasil[k] = d_kanan[j]
            j += 1
        k += 1

    # salin sisa elemen dari bagian kiri kalau masih ada
    while i < kiri.jumlah:
        d_hasil[k] = d_kiri[i]
        i += 1
        k += 1

    # salin sisa elemen dari bagian kanan kalau masih ada
    while j < kanan.jumlah:
        d_hasil[k] = d_kanan[j]
        j += 1
        k += 1

    hasil.jumlah = total
    return hasil, perbandingan, total


# fungsi merge sort yang membelah array jadi dua secara rekursif lalu menggabungkannya kembali (o(n log n))
def merge_sort(arr, kunci="oid"):
    n = arr.jumlah
    if n <= 1:
        return arr, 0, 0

    tengah = n // 2
    sisa = n - tengah

    kiri = Array(kapasitas_awal=tengah if tengah > 4 else 4)
    kanan = Array(kapasitas_awal=sisa if sisa > 4 else 4)

    # bagi isi array ke potongan kiri dan kanan
    for i in range(tengah):
        kiri.data[i] = arr.data[i]
    kiri.jumlah = tengah

    for i in range(tengah, n):
        kanan.data[i - tengah] = arr.data[i]
    kanan.jumlah = sisa

    kiri_urut, b_kiri, p_kiri = merge_sort(kiri, kunci)
    kanan_urut, b_kanan, p_kanan = merge_sort(kanan, kunci)

    gabungan, b_gab, p_gab = gabung_array(kiri_urut, kanan_urut, kunci)
    return gabungan, b_kiri + b_kanan + b_gab, p_kiri + p_kanan + p_gab


# fungsi linear search untuk mencari oid satu per satu dari indeks awal sampai akhir (o(n))
def linear_search(arr, target_oid):
    perbandingan = 0
    target = str(target_oid).strip()

    for i in range(arr.jumlah):
        perbandingan += 1
        pesanan = arr.data[i]
        if pesanan[0] == target:
            return i, pesanan, perbandingan

    return -1, None, perbandingan


# fungsi binary search untuk mencari oid dengan memotong separuh area pencarian tiap langkah (o(log n))
def binary_search(arr_terurut, target_oid):
    lo = 0
    hi = arr_terurut.jumlah - 1
    perbandingan = 0
    target = str(target_oid).strip()

    while lo <= hi:
        mid = (lo + hi) // 2
        perbandingan += 1
        pesanan_tengah = arr_terurut.data[mid]
        oid_tengah = pesanan_tengah[0]

        if oid_tengah == target:
            return mid, pesanan_tengah, perbandingan
        elif oid_tengah < target:
            lo = mid + 1
        else:
            hi = mid - 1

    return -1, None, perbandingan


# class untuk menyimpan hasil pengurutan oid supaya binary search cukup mengurutkan data sekali saja
class ManajerM3:
    def __init__(self):
        self.arr_urut_oid = None
        self.waktu_bangun_ms = 0.0

    def reset(self):
        self.arr_urut_oid = None
        self.waktu_bangun_ms = 0.0

    def pastikan_terurut_oid(self, arr_utama):
        # urutkan data berdasarkan oid memakai merge sort kalau belum pernah diurutkan atau jumlah datanya berubah
        if self.arr_urut_oid is None or self.arr_urut_oid.jumlah != arr_utama.jumlah:
            salinan = salin_potongan(arr_utama, arr_utama.jumlah)
            mulai = time.perf_counter()
            terurut, _, _ = merge_sort(salinan, "oid")
            self.waktu_bangun_ms = (time.perf_counter() - mulai) * 1000
            self.arr_urut_oid = terurut
        return self.arr_urut_oid, self.waktu_bangun_ms