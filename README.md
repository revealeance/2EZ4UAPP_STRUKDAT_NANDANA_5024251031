
                                                                           
                  @@@@@@@@@@@@@@@@@@@@@@@@@@@    :::::::::::::::::::::::::::::::            
                @@@@@@@@@@@@@@@@@@@@@@@@@@@@@  :::::::::::::::::::::::::::::::::            
                @@@@@@@@@@@@@@@@@@@@@@@@@@@@@ ::::::::::::::::::::::::::::::::::            
               @@@@@@@@@@@@@@@@@@@@@@@@@@@@@  :::::::::::::::::::::::::::::::::             
               @@@@@@@@@@@@@@@@@@@@@@@@@@@@  ::::::::::::::::::::::::::::::::::             
              @@@@@@@@@@@@@@@@@@@@@@@@@@@@  ::::::::::::::::::::::::::::::::::              
              @@@@@@@@@@@@                 ::::::::::::                                     
             @@@@@@@@@@@@                  :::::::::::                                      
             @@@@@@@@@@@                  :::::::::::                                       
             @@@@@@@@@@@                  :::::::::::                                       
            @@@@@@@@@@@                 :::::::::::::                                       
            @@@@@@@@@@@  :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::      
            @@@@@@@@@@@ ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::      
            @@@@@@@@@@@ ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::      
           @@@@@@@@@@@ ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::       
           @@@@@@@@@@@ ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::       
          @@@@@@@@@@@@ :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::        
          @@@@@@@@@@@                           :::::::::::::                               
         @@@@@@@@@@@@                             :::::::::::                               
         @@@@@@@@@@@                              :::::::::::                               
         @@@@@@@@@@@                               :::::::::::                              
        @@@@@@@@@@@@                               ::::::::::::                             
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  ::::::::::::::::::::                    
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  ::::::::::::::::::::                    
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  ::::::::::::::::::                     
       @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  ::::::::::::::::::                     
       @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  :::::::::::::::::                     
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@   :::::::::::::::          

    2EZ4U Food Delivery Engine - Proyek Struktur Data dan Algoritma - Oleh Nandana Moriel (5024251031)
    PROGRESS : M1 - M2 - M3
---------------------------------------------------------
Proyek ini adalah implementasi sistem backend untuk layanan pesan antar makanan. Semua struktur data dibangun secara manual dari awal menggunakan Python murni tanpa menggunakan fungsi instan bawaan seperti dict, set, sorted(), .sort(), atau list.append(). Antarmuka aplikasi dibuat menggunakan Tkinter untuk memperlihatkan alur kerja sistem.

M1 - Data Pesanan (Array vs Linked List)
---------------------------------------------------------
Bagian ini membandingkan kinerja penyimpanan data pesanan menggunakan dua struktur dasar. Pengujian difokuskan pada operasi penambahan pesanan reguler, prioritas, dan VIP.

- Array: Menggunakan memori berukuran tetap yang disimulasikan menggunakan pengali slot kosong, lalu kapasitasnya digandakan secara manual (disalin) ketika penuh. Penambahan pesanan reguler di urutan belakang berjalan cepat dalam waktu O(1) amortized. Namun, menyisipkan pesanan prioritas ke tengah atau pesanan VIP ke posisi paling depan memakan biaya O(n) karena mengharuskan program menggeser seluruh sisa elemen di sebelah kanannya satu per satu.
- Linked List: Menggunakan simpul (node) yang saling terkait satu sama lain. Memasukkan pesanan VIP ke urutan pertama menjadi instan (O(1)) karena program hanya perlu mengubah arah penunjuk head. Namun, operasi pembacaan (get) pada indeks tertentu mewajibkan penelusuran simpul dari depan sehingga biayanya menjadi O(n).

M2 - Stack dan Queue
---------------------------------------------------------
Bagian ini menangani logika antrean pelayanan dan evaluasi perhitungan pada mesin kasir, yang seluruhnya dibangun di atas kelas Array M1.

- Stack: Menggunakan prinsip LIFO (Last In First Out). Struktur ini dipakai untuk mengonversi perhitungan struk kasir dari bentuk infix menjadi postfix, lalu mengevaluasi nilai akhirnya. Stack juga dipakai untuk menyimpan riwayat tindakan pada antrean sehingga fitur undo dan redo bisa dieksekusi secara tepat.
- Queue: Menggunakan prinsip FIFO (First In First Out) untuk urutan pelayanan. Terdapat dua algoritma yang digunakan untuk pembuktian performa:
- Queue Naif: Setiap kali pesanan di indeks 0 selesai dilayani (dequeue), seluruh sisa pesanan di belakangnya dipaksa bergeser maju satu petak. Algoritma ini menelan kompleksitas O(n) setiap kali melayani satu pesanan.
- Queue Circular: Menempatkan elemen agar tetap diam di posisinya, dan yang bergerak maju memutar hanyalah penunjuk front dan rear dengan bantuan operasi modulo (sisa bagi). Algoritma ini mengeksekusi layanan secara instan dengan kompleksitas konstan O(1).

M3 - Sort dan Search
---------------------------------------------------------
Bagian ini diperlukan untuk pembuatan laporan harian terurut dan pencarian riwayat pesanan spesifik. Kedua metode pengurutan dibangun secara stabil (stable sort) agar pesanan yang memiliki nilai kunci kembar tidak bergeser dari urutan kedatangan awalnya.

- Insertion Sort: Menggeser elemen secara mundur sampai menemukan posisi indeks yang tepat. Kerjanya tumbuh secara kuadratik (O(n^2)), sehingga hanya efisien pada data kecil. Program ini menerapkan batasan keamanan yang menolak proses insertion sort jika beban data melebihi 20.000 baris.
- Merge Sort: Membelah memori data menjadi dua bagian secara rekursif lalu menggabungkannya kembali secara terurut. Logika ini berjalan jauh lebih efisien pada kompleksitas O(n log n) dan digunakan sebagai algoritma utama untuk mengurutkan keseluruhan beban 200.000 baris data pesanan.
- Linear Search: Memeriksa pesanan satu per satu secara berurutan dari depan dengan biaya O(n).
- Binary Search: Membuang separuh sisa daftar pencarian pada setiap langkah (O(log n)). Sangat ringan dan instan, dengan prasyarat bahwa daftar data harus sudah diurutkan menurut kunci pencariannya terlebih dahulu memakai merge sort.

Perbandingan Algoritma Pengurutan (n vs Jumlah Perbandingan)
---------------------------------------------------------
Data di bawah menunjukkan jumlah perbandingan yang dieksekusi oleh program pada pengurutan berdasarkan harga. Sesuai dengan teori kompleksitasnya, saat beban baris data dilipatgandakan, perbandingan pada insertion sort membengkak sekitar empat kali lipat, sementara pada merge sort hanya membesar sekitar dua kali lipat.

- Untuk jumlah baris (n) = 2.000
  Insertion Sort O(n^2) mengeksekusi 962.430 perbandingan
  Merge Sort O(n log n) mengeksekusi 19.240 perbandingan

- Untuk jumlah baris (n) = 4.000
  Insertion Sort O(n^2) mengeksekusi 3.849.720 perbandingan
  Merge Sort O(n log n) mengeksekusi 42.328 perbandingan

- Untuk jumlah baris (n) = 8.000
  Insertion Sort O(n^2) mengeksekusi 15.398.880 perbandingan
  Merge Sort O(n log n) mengeksekusi 93.121 perbandingan

- Untuk jumlah baris (n) = 16.000
  Insertion Sort O(n^2) mengeksekusi 61.595.520 perbandingan
  Merge Sort O(n log n) mengeksekusi 204.866 perbandingan


Cara Menjalankan Program
---------------------------------------------------------
- Tempatkan file pesanan.csv yang berisi 200.000 baris pesanan ke dalam folder data/
- Buka terminal dan jalankan perintah: python app.py
- Jendela antarmuka pengguna akan muncul, klik Load Data untuk membaca seluruh file CSV ke dalam struktur Array, Linked List, dan Queue.
