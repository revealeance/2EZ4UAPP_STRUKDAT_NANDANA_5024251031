
class Array:
    def __init__(self):
        # Kita inialisasi kapasitas memori awal sebanyak 4 slot
        self.kapasitas = 4
        
        # simulasi alokasi memori blok statis menggunakan [None] (note to self: basically ada alokasinya tapi valuenya tidak ada)
        # memori dipesan di awal dengan ukuran tetap sesuai kapasitas
        self.data = [None] * self.kapasitas
        
        # untuk melacak jumlah elemen riil yang terisi, bukan kapasitas total
        self.jumlah = 0

    def cek_penuh(self):
        # disini kita memakai sesuatu dari OOP (namanya helper) untuk menangani alokasi memori dinamis 
        # ada if pengecekan sebelum operasi penambahan data
        if self.jumlah == self.kapasitas:
            # Jika memori penuh, alokasikan blok memori baru berukuran 2x lipat
            self.kapasitas *= 2
            baru = [None] * self.kapasitas
            
            # Salin seluruh data dari memori lama ke memori baru secara berurutan
            for j in range(self.jumlah):
                baru[j] = self.data[j]
                
            # point referensi array ke blok memori yang baru
            self.data = baru

    def get(self, i):
        # untuk periksa apakah indeks yang diminta berada dalam batas elemen yang terisi
        if 0 <= i < self.jumlah:
            # akses elemen langsung melalui alamat indeks memori
            return self.data[i]
        return None

    def append(self, v):
        # pertama kita harus memastikan kapasitas mencukupi sebelum nambah
        self.cek_penuh()
        
        # Lalu kita tempatkan data baru tepat di indeks elemen terakhir + 1
        self.data[self.jumlah] = v
        self.jumlah += 1

    def insert(self, i, v):
        # pertama kita harus memastikan kapasitas mencukupi sebelum nambah
        self.cek_penuh()
        
        # geser memori ke kanan
        # mulai dari indeks terakhir (self.jumlah) dan mundur sampai ke indeks target (i).
        # tujuannya untuk mengosongkan slot pada indeks i tanpa overwrite data yang udah ada
        for j in range(self.jumlah, i, -1):
            self.data[j] = self.data[j - 1]
            
        # insert data baru di slot yang sudah dikosongkan.
        self.data[i] = v
        self.jumlah += 1

    def delete(self, i):
        # pertama kita harus validasi batas indeks
        if 0 <= i < self.jumlah:
            
            # geser memori ke kiri
            # mulai dari indeks i, timpa elemen tersebut dengan elemen di sebelah kanannya
            for j in range(i, self.jumlah - 1):
                self.data[j] = self.data[j + 1]
                
            # kosongkan slot paling belakang karena seluruh elemen sudah bergeser ke kiri
            self.data[self.jumlah - 1] = None
            self.jumlah -= 1


# ==========================================


class Node:
    def __init__(self, val):
        # ini adalah struktur dasar untuk elemen linked list
        # val menyimpan nilai data pesanan
        self.val = val
        # next sebagai pointer yang menyimpan referensi ke memori node berikutnya
        self.next = None

class LinkList:
    def __init__(self):
        # menyimpan referensi node terdepan.
        self.head = None
        # menyimpan referensi node paling belakang agar penambahan datanya optimized
        self.tail = None
        # untuk melacak jumlah elemen dalam list
        self.jumlah = 0

    def get(self, i):
        # untuk validasi batas indeks.
        if i < 0 or i >= self.jumlah: return None
        
        # karena memorinya tidak kontinu, pencarian harus dimulai dari head
        curr = self.head
        for _ in range(i):
            # berpindah ke node selanjutnya mengikuti pointer next
            curr = curr.next
        return curr.val

    def append(self, v):
        # membuat instansiasi node baru di memori
        baru = Node(v)
        
        # in case, semisal kondisi linked list nya masih kosong
        if self.head is None:
            self.head = self.tail = baru
        else:
            # arahkan pointer next dari elemen terakhir ke node baru
            self.tail.next = baru
            # update reference tail ke node yang baru saja ditambahkan
            self.tail = baru
            
        self.jumlah += 1

    def insert(self, i, v):
        # kasus 1: menyisipkan di awal
        if i == 0:
            baru = Node(v)
            # point pointer Node baru langsung ke head saat ini
            baru.next = self.head
            # update head agar menunjuk ke node baru
            self.head = baru
            # jika sebelumnya list kosong, node ini juga bertindak sebagai tail.
            if self.jumlah == 0: self.tail = baru
            self.jumlah += 1
            
        # kasus 2: menyisipkan di akhir tapi indeksnya ga cukup, jadi di append
        elif i >= self.jumlah:
            self.append(v)
            
        # kasus 3: menyisipkan di tengah
        else:
            baru = Node(v)
            curr = self.head
            
            # traversal hingga tepat 1 posisi sebelum indeks penyisipan (i - 1)
            for _ in range(i - 1):
                curr = curr.next
                
           # untuk operasi penyambungan pointer ada dua tahap, pertama kita hubungan node baru ke node setelahnya, lalu kita hubungkan node sebelumnya ke node baru
            baru.next = curr.next
            curr.next = baru
            self.jumlah += 1

    def delete(self, i):
        # validasi agar tidak menghapus dari list kosong atau indeks di luar batas
        if i < 0 or i >= self.jumlah or self.head is None: return
        
        # kasus 1: menghapus elemen pertama (head)
        if i == 0:
            # pindahkan reference head ke node kedua. Memori node pertama akan otomatis dibersihkan oleh garbage collector.
            self.head = self.head.next
            # jika itu satu-satunya elemen, kita kosongkan juga reference tail
            if self.jumlah == 1: self.tail = None
            
        # kasus 2: menghapus elemen di tengah atau belakang 
        else:
            curr = self.head
            # traversal hingga tepat 1 posisi sebelum node yang akan dihapus
            for _ in range(i - 1):
                curr = curr.next
                
           # untuk operasi pemutusan pointer, kita arahkan pointer next dari node sebelumnya ke node setelah node yang akan dihapus, sehingga node yang dihapus tidak lagi terhubung ke list
            curr.next = curr.next.next
            if curr.next is None: self.tail = curr
            
        self.jumlah -= 1