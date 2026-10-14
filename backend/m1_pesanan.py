# class array dengan ukuran memori statis yang otomatis membesar 2x lipat saat penuh
class Array:
    def __init__(self, kapasitas_awal=4):
        # inisialisasi kapasitas awal dan siapkan slot memori kosong pakai none
        self.kapasitas = kapasitas_awal if kapasitas_awal > 0 else 4
        self.data = [None] * self.kapasitas
        self.jumlah = 0

    def cek_penuh(self):
        # kalau jumlah data sudah sama dengan kapasitas, gandakan ukuran array lalu salin datanya
        if self.jumlah == self.kapasitas:
            kapasitas_baru = self.kapasitas * 2
            data_baru = [None] * kapasitas_baru
            for i in range(self.jumlah):
                data_baru[i] = self.data[i]
            self.data = data_baru
            self.kapasitas = kapasitas_baru

    def get(self, i):
        # ambil data pada indeks ke-i secara langsung (o(1))
        if 0 <= i < self.jumlah:
            return self.data[i]
        return None

    def set(self, i, v):
        # ubah nilai data pada indeks ke-i
        if 0 <= i < self.jumlah:
            self.data[i] = v

    def append(self, v):
        # tambah data baru di posisi paling belakang (amortized o(1))
        self.cek_penuh()
        self.data[self.jumlah] = v
        self.jumlah += 1

    def insert(self, i, v):
        # batasi indeks supaya tidak minus atau melebihi jumlah data sekarang
        if i < 0:
            i = 0
        if i > self.jumlah:
            i = self.jumlah

        self.cek_penuh()

        # geser elemen dari belakang ke kanan satu langkah buat memberi ruang di indeks i (o(n))
        for j in range(self.jumlah, i, -1):
            self.data[j] = self.data[j - 1]

        self.data[i] = v
        self.jumlah += 1

    def delete(self, i):
        # batalkan kalau indeks yang mau dihapus tidak valid
        if i < 0 or i >= self.jumlah:
            return None

        # simpan data yang dihapus lalu geser elemen di sebelah kanannya ke kiri satu langkah (o(n))
        dihapus = self.data[i]
        for j in range(i, self.jumlah - 1):
            self.data[j] = self.data[j + 1]

        self.data[self.jumlah - 1] = None
        self.jumlah -= 1
        return dihapus

    def pop_belakang(self):
        # hapus dan ambil elemen paling belakang tanpa perlu menggeser data lain (o(1))
        if self.jumlah == 0:
            return None
        idx_akhir = self.jumlah - 1
        nilai = self.data[idx_akhir]
        self.data[idx_akhir] = None
        self.jumlah -= 1
        return nilai


# class node untuk menyimpan satu data pesanan dan pointer ke node berikutnya
class Node:
    def __init__(self, val):
        self.val = val
        self.next = None


# class singly linked list dengan pointer head dan tail
class LinkList:
    def __init__(self):
        # awalnya head dan tail masih kosong karena belum ada node
        self.head = None
        self.tail = None
        self.jumlah = 0

    def get(self, i):
        # telusuri node satu per satu dari head sebanyak i langkah (o(n))
        if i < 0 or i >= self.jumlah:
            return None
        curr = self.head
        for _ in range(i):
            curr = curr.next
        return curr.val

    def append(self, v):
        # tambah node baru langsung di belakang lewat pointer tail (o(1))
        node_baru = Node(v)
        if self.head is None:
            self.head = node_baru
            self.tail = node_baru
        else:
            self.tail.next = node_baru
            self.tail = node_baru
        self.jumlah += 1

    def insert(self, i, v):
        # kalau insert di indeks 0 (vip), cukup sambungkan node baru ke head lama (o(1))
        if i <= 0 or self.head is None:
            node_baru = Node(v)
            node_baru.next = self.head
            self.head = node_baru
            if self.jumlah == 0:
                self.tail = node_baru
            self.jumlah += 1
        elif i >= self.jumlah:
            self.append(v)
        else:
            # kalau insert di tengah (prioritas), jalan dulu dari head sampai posisi i - 1 (o(n))
            node_baru = Node(v)
            curr = self.head
            for _ in range(i - 1):
                curr = curr.next
            node_baru.next = curr.next
            curr.next = node_baru
            self.jumlah += 1

    def delete(self, i):
        # cek apakah indeks valid dan list tidak kosong
        if i < 0 or i >= self.jumlah or self.head is None:
            return None

        # kalau hapus indeks 0, langsung pindahkan head ke node kedua (o(1))
        if i == 0:
            dihapus = self.head.val
            self.head = self.head.next
            if self.jumlah == 1:
                self.tail = None
            self.jumlah -= 1
            return dihapus

        # jalan dari head sampai satu node sebelum target yang mau dihapus (o(n))
        curr = self.head
        for _ in range(i - 1):
            curr = curr.next

        target = curr.next
        dihapus = target.val
        curr.next = target.next

        # kalau node yang dihapus adalah elemen paling akhir, update posisi tail
        if curr.next is None:
            self.tail = curr

        self.jumlah -= 1
        return dihapus


# fungsi bantu untuk mengubah detik menjadi format jam:menit:detik
def format_waktu(detik_str):
    if detik_str is None or detik_str == "" or detik_str == "-":
        return "-"
    detik = int(detik_str)
    jam = detik // 3600
    sisa = detik % 3600
    menit = sisa // 60
    dtk = sisa % 60
    return f"{jam:02d}:{menit:02d}:{dtk:02d}"


# fungsi untuk membuat data pesanan baru dalam bentuk list supaya statusnya bisa diupdate
def buat_baris_pesanan(nomor_urut, pelanggan, prioritas, status="ANTRE"):
    oid = f"O-{nomor_urut:06d}"
    return [oid, pelanggan, "kafe-teknik", "roti-bakar", 12000, prioritas, "28800", "", status]