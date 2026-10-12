# backend/m2_antrean.py

# note to self: konsep stack (tumpukan) - lifo

class Stack:
    def __init__(self):
        # pakai list bawaan python sebagai wadah tumpukan
        self.data = []

    def push(self, val):
        # tambah data baru di posisi paling atas (o(1))
        self.data.append(val)

    def pop(self):
        # pastikan tumpukan tidak kosong sebelum ambil data
        if len(self.data) > 0:
            # fungsi pop otomatis ambil dan hapus elemen terakhir
            return self.data.pop()
        
        # kembalikan none kalau kosong biar program tidak error
        return None

    def peek(self):
        # sekadar mengintip data paling atas tanpa menghapus
        if len(self.data) > 0:
            # indeks [-1] menunjuk ke elemen paling akhir di python
            return self.data[-1]
        return None


# queue naif (antrean menggeser) - fifo
# kalau orang terdepan selesai, semua di belakangnya maju satu langkah (sangat lambat)
class QueueNaif:
    def __init__(self):
        # wadah antrean pakai list biasa
        self.data = []
        
        # variabel buat menghitung jumlah geseran data untuk demo ke dosen
        self.total_geseran = 0

    def enqueue(self, val):
        # orang baru selalu masuk dari belakang (o(1))
        self.data.append(val)

    def dequeue(self):
        # kalau antrean kosong tidak ada yang dikeluarkan
        if len(self.data) == 0:
            return None

        # simpan data orang terdepan untuk dikembalikan nanti
        depan = self.data[0]

        # proses menggeser maju dengan kompleksitas o(n) yang berat
        for i in range(1, len(self.data)):
            # elemen saat ini menimpa elemen di depannya
            self.data[i - 1] = self.data[i]
            
            # catat setiap pergeseran buat ditampilkan di ui
            self.total_geseran += 1

        # hapus slot paling belakang karena semua sudah maju
        self.data.pop()

        # kembalikan data orang terdepan
        return depan


# queue circular (antrean melingkar) - fifo
# orangnya diam tapi loket pelayanannya yang bergerak maju pakai rumus modulo
class QueueCircular:
    def __init__(self, kapasitas_awal=4):
        # tentukan kapasitas awal memori
        self.kapasitas = kapasitas_awal
        
        # pesan blok memori statis pakai [none]
        self.data = [None] * self.kapasitas
        
        # pointer front menunjuk ke orang terdepan
        self.front = 0
        
        # pointer rear menunjuk ke indeks kosong selanjutnya buat orang baru
        self.rear = 0
        
        # hitung jumlah orang aktual di dalam antrean
        self.jumlah = 0

    def cek_penuh(self):
        # kalau antrean penuh bikin memori 2x lipat lebih besar
        if self.jumlah == self.kapasitas:
            kapasitas_baru = self.kapasitas * 2
            data_baru = [None] * kapasitas_baru

            # pindahkan data lama ke memori baru berurutan dari front
            curr = self.front
            for i in range(self.jumlah):
                data_baru[i] = self.data[curr]
                
                # rumus modulo memastikan kalau mentok di ujung akan balik ke indeks 0
                curr = (curr + 1) % self.kapasitas

            # timpa array lama dengan array baru
            self.data = data_baru
            # reset front ke awal karena data baru sudah lurus
            self.front = 0
            # taruh rear tepat setelah elemen terakhir
            self.rear = self.jumlah
            self.kapasitas = kapasitas_baru

    def enqueue(self, val):
        # pastikan memori tidak penuh sebelum memasukkan orang baru
        self.cek_penuh()
        
        # masukkan orang baru di pintu belakang (o(1))
        self.data[self.rear] = val
        
        # geser pintu belakang dan gunakan modulo untuk putar balik kalau mentok
        self.rear = (self.rear + 1) % self.kapasitas
        
        # tambah jumlah orang
        self.jumlah += 1

    def dequeue(self):
        # kembalikan none kalau tidak ada orang di antrean
        if self.jumlah == 0:
            return None

        # ambil data dari loket terdepan
        depan = self.data[self.front]
        
        # hapus data secara fisik dari memori
        self.data[self.front] = None

        # geser loket terdepan 1 langkah pakai modulo (o(1) karena cuma geser pointer)
        self.front = (self.front + 1) % self.kapasitas
        
        # kurangi jumlah orang
        self.jumlah -= 1
        
        # kembalikan data orang yang dilayani
        return depan