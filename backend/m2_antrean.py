from backend.m1_pesanan import Array


# class stack dengan prinsip lifo yang dibuat di atas class array dari m1
class Stack:
    def __init__(self):
        self.arr = Array()

    def push(self, x):
        # masukkan data ke posisi paling atas tumpukan (ujung belakang array)
        self.arr.append(x)

    def pop(self):
        # ambil dan hapus data paling atas dari tumpukan (o(1))
        if self.kosong():
            return None
        return self.arr.pop_belakang()

    def peek(self):
        # lihat data paling atas tanpa menghapusnya
        if self.kosong():
            return None
        return self.arr.get(self.arr.jumlah - 1)

    def kosong(self):
        return self.arr.jumlah == 0

    def ukuran(self):
        return self.arr.jumlah

    def bersihkan(self):
        self.arr = Array()

    def teks_isi(self):
        # gabungkan isi stack jadi string dipisah spasi untuk ditampilkan di tabel ui
        if self.kosong():
            return "kosong"
        teks = ""
        for i in range(self.arr.jumlah):
            if i > 0:
                teks += " "
            teks += str(self.arr.get(i))
        return teks


# fungsi untuk memecah string struk belanja jadi token angka dan operator
def pecah_token(ekspresi):
    tokens = Array()
    angka = ""
    for i in range(len(ekspresi)):
        kar = ekspresi[i]
        # gabungkan digit angka yang bersebelahan supaya angka ribuan tetap utuh
        if "0" <= kar <= "9":
            angka += kar
        else:
            if angka != "":
                tokens.append(angka)
                angka = ""
            if kar in "+-*/()":
                tokens.append(kar)
    if angka != "":
        tokens.append(angka)
    return tokens


# fungsi untuk menentukan tingkat prioritas operator matematika
def prioritas_operator(op):
    if op == "*" or op == "/":
        return 2
    if op == "+" or op == "-":
        return 1
    return 0


# fungsi untuk mengubah ekspresi infix menjadi postfix memakai stack operator
def ke_postfix(ekspresi, list_langkah=None):
    tokens = pecah_token(ekspresi)
    stack_op = Stack()
    output = Array()

    # fungsi bantu buat menggabungkan isi array output jadi string
    def teks_output():
        if output.jumlah == 0:
            return "kosong"
        s = ""
        for k in range(output.jumlah):
            if k > 0:
                s += " "
            s += str(output.get(k))
        return s

    for i in range(tokens.jumlah):
        tok = tokens.get(i)

        # kalau angka langsung masuk ke output, sedangkan kurung dan operator diatur lewat stack
        if "0" <= tok[0] <= "9":
            output.append(tok)
            aksi = "operand, langsung ke output"
        elif tok == "(":
            stack_op.push(tok)
            aksi = "push ( ke stack"
        elif tok == ")":
            while not stack_op.kosong() and stack_op.peek() != "(":
                output.append(stack_op.pop())
            stack_op.pop()
            aksi = "pop sampai (, lalu buang ("
        else:
            keluar = ""
            while (not stack_op.kosong() and stack_op.peek() != "(" and
                   prioritas_operator(stack_op.peek()) >= prioritas_operator(tok)):
                op_atas = stack_op.pop()
                output.append(op_atas)
                keluar += op_atas + " "
            stack_op.push(tok)
            if keluar != "":
                aksi = f"pop {keluar.strip()}, lalu push {tok}"
            else:
                aksi = f"push {tok}"

        if list_langkah is not None:
            list_langkah.append((f"1.{i + 1}", tok, aksi, stack_op.teks_isi(), teks_output()))

    # keluarkan semua sisa operator yang masih ada di dalam stack setelah token habis
    sisa_op = ""
    while not stack_op.kosong():
        op_atas = stack_op.pop()
        output.append(op_atas)
        sisa_op += op_atas + " "

    if list_langkah is not None and sisa_op != "":
        list_langkah.append(("1.akhir", "akhir", f"pop sisa stack: {sisa_op.strip()}", stack_op.teks_isi(), teks_output()))

    return teks_output()


# fungsi untuk menghitung hasil akhir dari ekspresi postfix memakai stack angka
def hitung(postfix, list_langkah=None):
    potongan = postfix.split(" ") if isinstance(postfix, str) else []
    stack_angka = Stack()
    no_eval = 1

    for tok in potongan:
        if tok == "" or tok == "kosong":
            continue

        if "0" <= tok[0] <= "9":
            stack_angka.push(int(tok))
            if list_langkah is not None:
                list_langkah.append((f"2.{no_eval}", tok, f"operand, push {tok}", stack_angka.teks_isi(), "kosong"))
        else:
            # pop pertama adalah angka sebelah kanan (b) dan pop kedua adalah angka sebelah kiri (a)
            b = stack_angka.pop()
            a = stack_angka.pop()
            if b is None or a is None:
                return 0

            if tok == "+":
                hasil = a + b
            elif tok == "-":
                hasil = a - b
            elif tok == "*":
                hasil = a * b
            elif tok == "/":
                hasil = a // b if b != 0 else 0
            else:
                hasil = 0

            stack_angka.push(hasil)
            if list_langkah is not None:
                list_langkah.append((f"2.{no_eval}", tok, f"pop {b} dan {a} -> {a} {tok} {b} = {hasil}", stack_angka.teks_isi(), str(hasil)))

        no_eval += 1

    total = stack_angka.pop()
    return total if total is not None else 0


# class queue naif yang menggeser seluruh sisa elemen ke kiri setiap kali ada data keluar
class QueueNaif:
    def __init__(self):
        self.arr = Array()
        self.total_geseran = 0

    def enqueue(self, x):
        self.arr.append(x)

    def dequeue(self):
        if self.arr.jumlah == 0:
            return None

        # ambil data paling depan (indeks 0), lalu geser sisa data di belakangnya maju satu langkah (o(n))
        depan = self.arr.get(0)
        banyak_geser = self.arr.jumlah - 1

        for i in range(1, self.arr.jumlah):
            self.arr.data[i - 1] = self.arr.data[i]

        self.arr.data[self.arr.jumlah - 1] = None
        self.arr.jumlah -= 1
        self.total_geseran += banyak_geser
        return depan

    def is_empty(self):
        return self.arr.jumlah == 0

    def ukuran(self):
        return self.arr.jumlah

    def pop_belakang(self):
        # hapus elemen paling belakang saat membatalkan enqueue lewat undo
        return self.arr.pop_belakang()

    def kembalikan_ke_depan(self, data_pesanan):
        # masukkan kembali pesanan ke posisi paling depan saat membatalkan dequeue lewat undo
        for i in range(data_pesanan.jumlah - 1, -1, -1):
            self.arr.insert(0, data_pesanan.get(i))


# class circular queue yang hanya memajukan pointer front dan rear memakai modulo (o(1))
class QueueCircular:
    def __init__(self, kapasitas_awal=4):
        self.kapasitas = kapasitas_awal
        self.data = [None] * self.kapasitas
        self.front = 0
        self.rear = 0
        # variabel count dipakai untuk membedakan kondisi antrean kosong dan penuh
        self.count = 0

    def cek_penuh(self):
        # kalau penuh, gandakan kapasitas lalu salin isi antrean berurutan mulai dari posisi front
        if self.count == self.kapasitas:
            kapasitas_baru = self.kapasitas * 2
            data_baru = [None] * kapasitas_baru
            curr = self.front
            for i in range(self.count):
                data_baru[i] = self.data[curr]
                curr = (curr + 1) % self.kapasitas
            self.data = data_baru
            self.front = 0
            self.rear = self.count
            self.kapasitas = kapasitas_baru

    def enqueue(self, x):
        # masukkan data di posisi rear lalu geser rear maju satu langkah pakai modulo
        self.cek_penuh()
        self.data[self.rear] = x
        self.rear = (self.rear + 1) % self.kapasitas
        self.count += 1

    def dequeue(self):
        # ambil data di posisi front lalu geser pointer front tanpa menggeser elemen lain
        if self.count == 0:
            return None
        depan = self.data[self.front]
        self.data[self.front] = None
        self.front = (self.front + 1) % self.kapasitas
        self.count -= 1
        return depan

    def is_empty(self):
        return self.count == 0

    def ukuran(self):
        return self.count

    def pop_belakang(self):
        # mundurkan pointer rear satu langkah untuk membatalkan pesanan yang baru masuk
        if self.count == 0:
            return None
        self.rear = (self.rear - 1 + self.kapasitas) % self.kapasitas
        nilai = self.data[self.rear]
        self.data[self.rear] = None
        self.count -= 1
        return nilai

    def kembalikan_ke_depan(self, data_pesanan):
        # mundurkan pointer front untuk mengembalikan pesanan yang batal dilayani ke paling depan
        for i in range(data_pesanan.jumlah - 1, -1, -1):
            self.cek_penuh()
            self.front = (self.front - 1 + self.kapasitas) % self.kapasitas
            self.data[self.front] = data_pesanan.get(i)
            self.count += 1


# class untuk mengelola antrean m2 sekaligus mencatat riwayat aksi di stack undo dan redo
class ManajerM2:
    def __init__(self):
        self.naif = QueueNaif()
        self.circular = QueueCircular(kapasitas_awal=4)
        self.undo_stack = Stack()
        self.redo_stack = Stack()

    def reset_dan_muat(self, data_pesanan):
        # kosongkan antrean lalu masukkan semua pesanan yang berstatus antre ke kedua versi queue
        self.naif = QueueNaif()
        self.circular = QueueCircular(kapasitas_awal=4)
        self.undo_stack = Stack()
        self.redo_stack = Stack()
        for i in range(data_pesanan.jumlah):
            p = data_pesanan.get(i)
            if p[8] == "ANTRE":
                self.naif.enqueue(p)
                self.circular.enqueue(p)

    def enqueue_baru(self, pesanan):
        # masukkan pesanan ke kedua antrean, simpan catatannya ke undo, dan kosongkan redo
        self.naif.enqueue(pesanan)
        self.circular.enqueue(pesanan)
        self.undo_stack.push(("ENQUEUE", pesanan))
        self.redo_stack.bersihkan()

    def dequeue_naif_banyak(self, banyak):
        # keluarkan sejumlah pesanan dari queue naif lalu simpan daftarnya ke stack undo
        keluar = Array()
        geser_awal = self.naif.total_geseran
        for _ in range(banyak):
            if not self.naif.is_empty():
                keluar.append(self.naif.dequeue())
        geser_aksi_ini = self.naif.total_geseran - geser_awal
        if keluar.jumlah > 0:
            self.undo_stack.push(("DEQUEUE_NAIF", keluar))
            self.redo_stack.bersihkan()
        return keluar, geser_aksi_ini

    def dequeue_circular_banyak(self, banyak):
        # keluarkan sejumlah pesanan dari circular queue lalu simpan daftarnya ke stack undo
        keluar = Array()
        for _ in range(banyak):
            if not self.circular.is_empty():
                keluar.append(self.circular.dequeue())
        if keluar.jumlah > 0:
            self.undo_stack.push(("DEQUEUE_CIRCULAR", keluar))
            self.redo_stack.bersihkan()
        return keluar

    def undo_last(self):
        # ambil catatan aksi terakhir dari stack undo, jalankan kebalikannya, lalu simpan ke stack redo
        if self.undo_stack.kosong():
            return None

        catatan = self.undo_stack.pop()
        jenis, data = catatan[0], catatan[1]

        if jenis == "ENQUEUE":
            self.naif.pop_belakang()
            self.circular.pop_belakang()
        elif jenis == "DEQUEUE_NAIF":
            self.naif.kembalikan_ke_depan(data)
        elif jenis == "DEQUEUE_CIRCULAR":
            self.circular.kembalikan_ke_depan(data)

        self.redo_stack.push(catatan)
        return catatan

    def redo_last(self):
        # ambil catatan dari stack redo, jalankan ulang aksi aslinya, lalu kembalikan ke stack undo
        if self.redo_stack.kosong():
            return None

        catatan = self.redo_stack.pop()
        jenis, data = catatan[0], catatan[1]

        if jenis == "ENQUEUE":
            self.naif.enqueue(data)
            self.circular.enqueue(data)
        elif jenis == "DEQUEUE_NAIF":
            for _ in range(data.jumlah):
                self.naif.dequeue()
        elif jenis == "DEQUEUE_CIRCULAR":
            for _ in range(data.jumlah):
                self.circular.dequeue()

        self.undo_stack.push(catatan)
        return catatan

    def stats(self):
        return (
            self.naif.ukuran(),
            self.circular.ukuran(),
            self.circular.kapasitas,
            self.naif.total_geseran,
            self.undo_stack.ukuran(),
            self.redo_stack.ukuran()
        )