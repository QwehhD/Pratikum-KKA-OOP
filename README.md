# Laporan Praktikum OOP - Analisis Mendalam

Dokumentasi lengkap hasil eksperimen dan analisis konsep Object-Oriented Programming dalam Python.

---

## Tugas Analisis 1: Modifikasi Atribut Object

### Pertanyaan
Apa yang terjadi jika kamu mengubah `hero1.hp` menjadi 500 setelah baris `hero1 = Hero(...)`? Coba lakukan `print(hero1.hp)`.

### Jawaban
**Output: `500`**

Hp dari hero1 akan berubah menjadi 500 dari sebelumnya yaitu 100.

### Penjelasan
- `hp` adalah **atribut publik** (tidak ada underscore protection)
- Dapat diakses dan diubah langsung dari luar class
- Tidak ada validasi atau pengaman
- Nilai atribut berubah dari 100 menjadi 500

### Kode
```python
class Hero:
    def __init__(self, name, hp, attack_power):
        self.name = name
        self.hp = hp
        self.attack_power = attack_power

hero1 = Hero("Layla", 100, 15)
hero1.hp = 500
print(hero1.hp)  # Output: 500
```

### Output Program
```
500
```

---

## Tugas Analisis 2: Parameter Object vs String

### Pertanyaan
Perhatikan parameter `lawan` pada method `serang`. Parameter tersebut menerima sebuah object utuh, bukan hanya string nama. Mengapa ini penting?

### Jawaban
Karena dengan menerima objek utuh maka method serang bisa membaca data dari lawan yang tidak hanya berisi string nama.

### Penjelasan
Dengan menerima **object utuh**, method `serang` dapat:
- ✓ Akses semua atribut lawan (name, hp, attack_power)
- ✓ Memanggil method lawan (diserang)
- ✓ Mengubah state lawan (HP berkurang)
- ✓ Implementasi game logic yang kompleks

### Kode
```python
def serang(self, lawan):  # Parameter: object, bukan string
    print(f"{self.name} menyerang {lawan.name}!")
    lawan.diserang(self.attack_power)  # Akses method lawan
    
def diserang(self, damage):
    self.hp -= damage
    print(f"{self.name} terkena damage {damage}. Sisa HP: {self.hp}")
```

### Output Program
```
Layla menyerang Zilong!
Zilong terkena damage 15. Sisa HP: 105
Zilong menyerang Layla!
Layla terkena damage 20. Sisa HP: 480
```

---

## Tugas Analisis 3: Fungsi super()

### Pertanyaan
Pada class `Mage`, coba hapus baris kode `super().__init__(name, hp, attack_power)`. Kemudian jalankan programnya.

### Jawaban
Akan muncul error "AttributeError: 'Mage' object has no attribute 'name'", dikarenakan atribut name di class Mage tidak di definisikan secara mandiri, melainkan dengan pewarisan dari class hero.

**Peran dari fungsi super():** Peran dari fungsi super() ialah untuk mengakses class induk dengan mendefinisikan atribut dari class induk ke class anak.

### Penjelasan
`super()` berfungsi untuk:
1. **Memanggil constructor parent class** secara otomatis
2. **Menginisialisasi atribut parent** (name, hp, attack_power)
3. **Mencegah duplikasi code** - tidak perlu ulang inisialisasi
4. **Memastikan inheritance bekerja** dengan benar

### Kode
```python
class Hero:
    def __init__(self, name, hp, attack_power):
        self.name = name
        self.hp = hp
        self.attack_power = attack_power

class Mage(Hero):
    def __init__(self, name, hp, attack_power, mana):
        super().__init__(name, hp, attack_power)  # ✓ HARUS dipanggil!
        self.mana = mana
    
    def info(self):
        print(f"{self.name} [Mage] | HP: {self.hp} | Mana: {self.mana}")
```

### Output Program
```
Eudora [Mage] | HP: 80 | Mana: 100
Eudora menyerang Balmond!
Balmond terkena damage 30. Sisa HP: 170
Eudora menggunakan Fireball ke Balmond!
Balmond terkena damage 60. Sisa HP: 110
```

---

## Tugas Analisis 4: Encapsulation & Name Mangling

### 4.1 - Percobaan Hacking (Name Mangling)

#### Pertanyaan
Coba tambahkan baris: `print(f"Mencoba akses paksa: {hero1._Hero__hp}")`
Apakah nilai HP muncul atau Error?

#### Jawaban
Nilai HP muncul. Alasan mengapa Python masih mengizinkan Name Mangling ialah untuk mencegah subclass menimpa variabel milik parent class. Kita tidak melakukannya dikarenakan itu akan melanggar kontrak encapsulation dan bisa menyebabkan kerusakan data.

#### Penjelasan
- **Nilai HP MUNCUL** (Tidak Error)
- Python izinkan dengan name mangling
- `__hp` internally disebut `_Hero__hp`
- Tapi JANGAN dilakukan karena melanggar encapsulation contract

#### Kode
```python
class Hero:
    def __init__(self, nama, hp_awal):
        self.nama = nama
        self.__hp = hp_awal  # Private attribute

hero1 = Hero("Layla", 100)
print(f"Mencoba akses paksa: {hero1._Hero__hp}")  # Ini bisa tapi JANGAN!
```

#### Output Program
```
Mencoba akses paksa: 0
```

### 4.2 - Uji Validasi: Setter Tanpa Validasi

#### Pertanyaan
Hapus logika if/elif di dalam `set_hp`. Kemudian lakukan `hero1.set_hp(-100)`. Apa yang terjadi pada data HP Hero?

#### Jawaban
Data HP Hero akan muncul dengan nilai -100. Alasan mengapa method setter sangat penting ialah untuk memberikan validasi pada data game karena bila hal seperti HP yang bernilai -100 ini muncul maka itu akan menjadi bug yang tak masuk akal karena karakter game tidak seharusnya memiliki HP -100.

#### Penjelasan
Setter sangat penting karena:
1. **Validasi input** - Pastikan data yang disimpan valid
2. **Maintain invariants** - HP tidak boleh negatif atau melebihi max
3. **Prevent bugs** - Catch invalid data sejak awal
4. **Game consistency** - Memastikan game logic tetap berjalan

#### Kode
```python
class Hero:
    def __init__(self, nama, hp_awal):
        self.__hp = hp_awal
    
    def get_hp(self):
        return self.__hp
    
    def set_hp(self, nilai_baru):
        if nilai_baru < 0:
            self.__hp = 0  # ✓ Validasi: tidak boleh negatif
        elif nilai_baru > 1000:
            print("Cheat terdeteksi!")
            self.__hp = 1000
        else:
            self.__hp = nilai_baru

hero1 = Hero("Layla", 100)
hero1.set_hp(-100)
print(hero1.get_hp())  # Output: 0 (safe, bukan -100!)
```

#### Output Program
```
0
```

---

## Tugas Analisis 5: Abstract Class & Interface

### 5.1 - Melanggar Kontrak

#### Pertanyaan
Pada class `Hero`, hapus (atau jadikan komentar) seluruh method `def serang(self, target):`. Error apa yang muncul?

#### Jawaban
Error yang muncul adalah "TypeError: Can't instantiate abstract class Hero without an implementation for abstract method 'serang'". Menurut saya arti error itu adalah kita menetapkan sebuah abstract class bernama Hero yang memiliki abstract method "serang" tanpa mengimplementasikannya di class konkret. Konsekuensinya adalah akan muncul error yang sama.

#### Penjelasan
- Abstract class adalah **KONTRAK**: semua child class HARUS implement method abstract
- Python enforce: Jika tidak implement, ERROR!
- Ini GOOD karena prevent incomplete implementation

#### Kode
```python
from abc import ABC, abstractmethod

class GameUnit(ABC):
    @abstractmethod
    def serang(self, target):
        pass
    
    @abstractmethod
    def info(self):
        pass

class Hero(GameUnit):
    def __init__(self, nama):
        self.nama = nama
    
    def serang(self, target):
        print(f"Hero {self.nama} menebas {target}!")
    
    def info(self):
        print(f"Saya adalah Hero: {self.nama}")
```

#### Output Program
```
Saya adalah Hero: Alucard
```

### 5.2 - Abstract Class Tidak Bisa Diinstantiate

#### Pertanyaan
Mengapa class `GameUnit` dilarang untuk dibuat menjadi object? Apa gunanya ada class `GameUnit` jika tidak bisa dibuat menjadi object nyata?

#### Jawaban
Karena class GameUnit adalah abstract class yang memang dari python dilarang untuk dibuat menjadi objek. Gunanya ialah sebagai interface atau template atribut untuk class anaknya.

#### Penjelasan
Abstract class gunanya untuk:
- ✓ **Interface/Kontrak** - Mendefinisikan contract yang harus diikuti
- ✓ **Enforcement** - Memastikan semua child implement method penting
- ✓ **Code organization** - Grup behavior dan responsibilities
- ✓ **Polymorphism** - Bisa pakai parent type untuk reference child
- ✓ **Design pattern** - Template method pattern, strategy pattern, dll

#### Output Program
```
Saya adalah Hero: Alucard
Saya adalah Monster: Serigala
```

---

## Tugas Analisis 6: Polymorphism & Method Naming

### 6.1 - Uji Skalabilitas

#### Pertanyaan
Tanpa mengubah satu huruf pun pada kode looping, buatlah class baru `Healer(Hero)`. Apakah program berjalan lancar?

#### Jawaban
Ya program berjalan lancar. Keuntungan utama menurut saya adalah untuk mempermudah dan mempercepat proses penambahan atau pembaruan karakter baru di masa depan karena tidak perlu membongkar seluruh program seperti bila tidak menggunakan Polimorfisme.

#### Penjelasan
Polymorphism enable **extensibility**:
- ✓ **Open/Closed Principle** - Open untuk extension, closed untuk modification
- ✓ **Scalability** - Tambah class baru tanpa risik code existing
- ✓ **Reusability** - Loop umum bisa handle semua hero type

#### Kode
```python
class Healer(Hero):
    def serang(self):
        print(f"{self.nama} tidak menyerang, tapi menyembuhkan teman!")

pasukan = [
    Mage("Eudora"),
    Archer("Miya"),
    Fighter("Zilong"),
    Healer("Angela")  # ✓ Tambah class baru!
]

# ✓ Loop TIDAK DIUBAH sama sekali
for pahlawan in pasukan:
    pahlawan.serang()
```

#### Output Program
```
Eudora (Mage) menembakkan Bola Api! Boom!
Miya (Archer) memanah dari jauh! Jleb!
Zilong (Fighter) memukul dengan pedang! Slash!
Gord (Mage) menembakkan Bola Api! Boom!
Healer tidak menyerang, tapi menyembuhkan teman!
```

### 6.2 - Konsistensi Penamaan

#### Pertanyaan
Ubah nama method `serang` pada class `Archer` menjadi `tembak_panah`. Apa yang terjadi? Mengapa nama method harus persis sama?

#### Jawaban
Program di class archer tidak dijalankan melainkan menjalankan program di method serang yang berada di class Hero. Dikarenakan kontrak antar class mengharuskan method yang ada di Child Class harus sama dengan yang ada di Parent Class supaya program bisa dijalankan.

#### Penjelasan
Method name HARUS sama karena:
- ✓ **Override mechanism** - Nama sama = override, nama beda = new method
- ✓ **Polymorphism principle** - Semua child implement interface yang sama
- ✓ **Method resolution** - Python cari dari derived class, lalu parent
- ✓ **Predictability** - Kode lebih konsisten dan maintainable

#### Kode - SALAH (Nama Berbeda)
```python
class Archer(Hero):
    def tembak_panah(self):  # ✗ NAMA BERBEDA!
        print(f"{self.nama} (Archer) memanah dari jauh!")

for pahlawan in pasukan:
    pahlawan.serang()  # Mencari "serang", bukan "tembak_panah"!
```

#### Kode - BENAR (Nama Sama)
```python
class Archer(Hero):
    def serang(self):  # ✓ NAMA SAMA!
        print(f"{self.nama} (Archer) memanah dari jauh!")

for pahlawan in pasukan:
    pahlawan.serang()  # Method Archer ini dipanggil ✓
```

---

## Program Praktik: TechMaster.py - Sistem Manajemen Perpustakaan

### Deskripsi Program
Program implementasi lengkap OOP dengan konsep:
- **Encapsulation**: Private attributes dengan getter/setter
- **Inheritance**: Class Buku, Majalah, DVD mewarisi dari Koleksi
- **Polymorphism**: Method yang sama, behavior berbeda
- **Abstraction**: Abstract class Koleksi dengan abstract methods

### Fitur Utama
✓ Manajemen koleksi perpustakaan (Buku, Majalah, DVD)
✓ Sistem peminjaman dengan validasi stok
✓ Perhitungan denda berdasarkan tipe koleksi
✓ Laporan stok dan analisis peminjaman
✓ Private attributes untuk data protection

### Output Program

```
✓ Koleksi 'Laskar Pelangi' berhasil ditambahkan
✓ Koleksi 'Filosofi Teras' berhasil ditambahkan
✓ Koleksi 'Algoritma Pemrograman' berhasil ditambahkan
✓ Koleksi 'National Geographic Indonesia' berhasil ditambahkan
✓ Koleksi 'Science Today' berhasil ditambahkan
✓ Koleksi 'Avengers: Endgame' berhasil ditambahkan
✓ Koleksi 'Interstellar' berhasil ditambahkan

============================================================
📖 KATALOG PERPUSTAKAAN: Perpustakaan SMA Telkom Indonesia
============================================================

📚 BUKU: Laskar Pelangi
   Pengarang: Andrea Hirata | Tahun: 2005
   ISBN: ISBN-001 | Halaman: 529
   Stok: 5 | Terpinjam: 0
   Denda per hari: Rp 5,000

📚 BUKU: Filosofi Teras
   Pengarang: Henry Manampiring | Tahun: 2018
   ISBN: ISBN-002 | Halaman: 287
   Stok: 3 | Terpinjam: 0
   Denda per hari: Rp 5,000

📚 BUKU: Algoritma Pemrograman
   Pengarang: Rinaldi Munir | Tahun: 2015
   ISBN: ISBN-003 | Halaman: 450
   Stok: 4 | Terpinjam: 0
   Denda per hari: Rp 5,000

📰 MAJALAH: National Geographic Indonesia
   Penerbit: National Geographic | Edisi: Mei 2024
   Tahun: 2024
   Stok: 6 | Terpinjam: 0
   Denda per hari: Rp 2,000

📰 MAJALAH: Science Today
   Penerbit: Science Publishing | Edisi: April 2024
   Tahun: 2024
   Stok: 8 | Terpinjam: 0
   Denda per hari: Rp 2,000

🎬 DVD: Avengers: Endgame
   Sutradara: Anthony & Joe Russo | Tahun: 2019
   Durasi: 181 menit
   Stok: 2 | Terpinjam: 0
   Denda per hari: Rp 8,000

🎬 DVD: Interstellar
   Sutradara: Christopher Nolan | Tahun: 2014
   Durasi: 169 menit
   Stok: 3 | Terpinjam: 0
   Denda per hari: Rp 8,000

============================================================
🔔 TRANSAKSI PEMINJAMAN
============================================================
✓ Berhasil meminjam 1 Buku
   Harus dikembalikan pada: 12-05-2026
✓ Berhasil meminjam 1 Majalah
   Harus dikembalikan pada: 12-05-2026
✓ Berhasil meminjam 1 DVD
   Harus dikembalikan pada: 12-05-2026
✓ Berhasil meminjam 2 Buku
   Harus dikembalikan pada: 12-05-2026

============================================================
📊 LAPORAN STOK - Perpustakaan SMA Telkom Indonesia
============================================================
Buku       | Laskar Pelangi            | Stok:   5 | Terpinjam:  1 | Tersedia:  4
Buku       | Filosofi Teras            | Stok:   3 | Terpinjam:  2 | Tersedia:  1
Buku       | Algoritma Pemrograman     | Stok:   4 | Terpinjam:  0 | Tersedia:  4
Majalah    | National Geographic Indonesia | Stok:   6 | Terpinjam:  1 | Tersedia:  5
Majalah    | Science Today             | Stok:   8 | Terpinjam:  0 | Tersedia:  8
DVD        | Avengers: Endgame         | Stok:   2 | Terpinjam:  1 | Tersedia:  1
DVD        | Interstellar              | Stok:   3 | Terpinjam:  0 | Tersedia:  3
============================================================
Total Stok: 31 | Total Terpinjam: 5

💡 CATATAN: Denda dihitung dari 7 hari setelah tanggal pinjam
```

---

## Program Praktik: game_rpg.py - 6 Latihan OOP Hero

### Deskripsi Program
Program demonstrasi lengkap dari 6 latihan OOP:
- **Latihan 1-3**: Dasar class, method, inheritance dengan super()
- **Latihan 4**: Encapsulation dengan private attributes dan getter/setter
- **Latihan 5**: Abstract class dan interface
- **Latihan 6**: Polymorphism dengan konsistensi nama method

### Output Program

```
500
Hero: Layla | HP: 500 | Power: 15
Hero: Zilong | HP: 120 | Power: 20

--- Pertarungan Dimulai ---
Layla menyerang Zilong!
Zilong terkena damage 15. Sisa HP: 105
Zilong menyerang Layla!
Layla terkena damage 20. Sisa HP: 480

--- Update Class Hero ---
Eudora [Mage] | HP: 80 | Mana: 100
Eudora menyerang Balmond!
Balmond terkena damage 30. Sisa HP: 170
Eudora menggunakan Fireball ke Balmond!
Balmond terkena damage 60. Sisa HP: 110
0
Mencoba akses paksa: 0
Saya adalah Hero: Alucard
Saya adalah Monster: Serigala
--- PERANG DIMULAI ---
Eudora (Mage) menembakkan Bola Api! Boom!
Hero menyerang dengan tangan kosong.
Zilong (Fighter) memukul dengan pedang! Slash!
Gord (Mage) menembakkan Bola Api! Boom!
Healer tidak menyerang, tapi menyembuhkan teman!
```

### Penjelasan Output

**Bagian 1: Analisis 1 & 2 - Object Reference**
```
500                                  # Perubahan hero1.hp menjadi 500
Hero: Layla | HP: 500 | Power: 15   # Info dengan HP baru
```

**Bagian 2: Analisis 3 - Inheritance & super()**
```
Eudora [Mage] | HP: 80 | Mana: 100  # Atribut parent + child
Eudora menyerang Balmond!            # Method inheritance
```

**Bagian 3: Analisis 4 - Encapsulation**
```
0                                    # set_hp(-100) → validasi menjadi 0
Mencoba akses paksa: 0               # Name mangling _Hero__hp
```

**Bagian 4: Analisis 5 - Abstract Class**
```
Saya adalah Hero: Alucard            # Implement abstract method
Saya adalah Monster: Serigala        # Polymorphic behavior
```

**Bagian 5: Analisis 6 - Polymorphism**
```
Eudora (Mage) menembakkan Bola Api! Boom!
Hero menyerang dengan tangan kosong.
Zilong (Fighter) memukul dengan pedang! Slash!
Healer tidak menyerang, tapi menyembuhkan teman!
```
→ Loop sama, behavior berbeda! ✓
