

class Array:
    def __init__(self):
        self.kapasitas = 4
        self.data = [None] * self.kapasitas
        self.jumlah = 0

    def cek_penuh(self):
        # HELPER: Fungsi ini dipanggil sebelum menambah data agar array tidak jebol
        if self.jumlah == self.kapasitas:
            self.kapasitas *= 2
            baru = [None] * self.kapasitas
            for j in range(self.jumlah):
                baru[j] = self.data[j]
            self.data = baru

    def get(self, i):
        if 0 <= i < self.jumlah:
            return self.data[i]
        return None

    def append(self, v):
        self.cek_penuh()
        self.data[self.jumlah] = v
        self.jumlah += 1

    def insert(self, i, v):
        self.cek_penuh()
        for j in range(self.jumlah, i, -1):
            self.data[j] = self.data[j - 1]
        self.data[i] = v
        self.jumlah += 1

    def delete(self, i):
        if 0 <= i < self.jumlah:
            for j in range(i, self.jumlah - 1):
                self.data[j] = self.data[j + 1]
            self.data[self.jumlah - 1] = None
            self.jumlah -= 1



class Node:
    def __init__(self, val):
        self.val = val
        self.next = None

class LinkList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.jumlah = 0

    def get(self, i):
        if i < 0 or i >= self.jumlah: return None
        curr = self.head
        for _ in range(i):
            curr = curr.next
        return curr.val

    def append(self, v):
        baru = Node(v)
        if self.head is None:
            self.head = self.tail = baru
        else:
            self.tail.next = baru
            self.tail = baru
        self.jumlah += 1

    def insert(self, i, v):
        if i == 0:
            baru = Node(v)
            baru.next = self.head
            self.head = baru
            if self.jumlah == 0: self.tail = baru
            self.jumlah += 1
        elif i >= self.jumlah:
            self.append(v)
        else:
            baru = Node(v)
            curr = self.head
            for _ in range(i - 1):
                curr = curr.next
            baru.next = curr.next
            curr.next = baru
            self.jumlah += 1

    def delete(self, i):
        if i < 0 or i >= self.jumlah or self.head is None: return
        
        if i == 0:
            self.head = self.head.next
            if self.jumlah == 1: self.tail = None
        else:
            curr = self.head
            for _ in range(i - 1):
                curr = curr.next
            curr.next = curr.next.next
            if curr.next is None: self.tail = curr
        self.jumlah -= 1