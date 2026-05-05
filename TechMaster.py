# Sistem Manajemen Perpustakaan Sekolah
# Implementasi OOP dengan Encapsulation, Inheritance, dan Polymorphism

from abc import ABC, abstractmethod
from datetime import datetime, timedelta

class Koleksi(ABC):
    """Abstract class untuk semua jenis koleksi perpustakaan"""
    
    def __init__(self, judul, pengarang, tahun_terbit, stok):
        self.judul = judul
        self.pengarang = pengarang
        self.tahun_terbit = tahun_terbit
        self.__stok = stok
        self.__terpinjam = 0
    
    def get_stok(self):
        return self.__stok
    
    def get_terpinjam(self):
        return self.__terpinjam
    
    def pinjam(self, jumlah=1):
        if jumlah > self.__stok - self.__terpinjam:
            print(f"❌ Stok {self.judul} tidak cukup!")
            return False
        self.__terpinjam += jumlah
        print(f"✓ Berhasil meminjam {jumlah} {self.__class__.__name__}")
        return True
    
    def kembalikan(self, jumlah=1):
        if jumlah > self.__terpinjam:
            print(f"❌ Jumlah pengembalian tidak valid!")
            return False
        self.__terpinjam -= jumlah
        print(f"✓ Berhasil mengembalikan {jumlah} {self.__class__.__name__}")
        return True
    
    @abstractmethod
    def tampilkan_info(self):
        pass
    
    @abstractmethod
    def hitung_denda(self, hari_terlambat):
        pass


class Buku(Koleksi):
    """Class untuk jenis koleksi Buku"""
    
    def __init__(self, judul, pengarang, tahun_terbit, stok, halaman, isbn):
        super().__init__(judul, pengarang, tahun_terbit, stok)
        self.halaman = halaman
        self.isbn = isbn
        self.__denda_per_hari = 5000  # Rp 5000 per hari
    
    def tampilkan_info(self):
        print(f"\n📚 BUKU: {self.judul}")
        print(f"   Pengarang: {self.pengarang} | Tahun: {self.tahun_terbit}")
        print(f"   ISBN: {self.isbn} | Halaman: {self.halaman}")
        print(f"   Stok: {self.get_stok()} | Terpinjam: {self.get_terpinjam()}")
        print(f"   Denda per hari: Rp {self.__denda_per_hari:,}")
    
    def hitung_denda(self, hari_terlambat):
        if hari_terlambat <= 0:
            return 0
        return self.__denda_per_hari * hari_terlambat


class Majalah(Koleksi):
    """Class untuk jenis koleksi Majalah"""
    
    def __init__(self, judul, penerbit, tahun_terbit, stok, edisi):
        super().__init__(judul, penerbit, tahun_terbit, stok)
        self.edisi = edisi
        self.__denda_per_hari = 2000  # Rp 2000 per hari
    
    def tampilkan_info(self):
        print(f"\n📰 MAJALAH: {self.judul}")
        print(f"   Penerbit: {self.pengarang} | Edisi: {self.edisi}")
        print(f"   Tahun: {self.tahun_terbit}")
        print(f"   Stok: {self.get_stok()} | Terpinjam: {self.get_terpinjam()}")
        print(f"   Denda per hari: Rp {self.__denda_per_hari:,}")
    
    def hitung_denda(self, hari_terlambat):
        if hari_terlambat <= 0:
            return 0
        return self.__denda_per_hari * hari_terlambat


class DVD(Koleksi):
    """Class untuk jenis koleksi DVD"""
    
    def __init__(self, judul, sutradara, tahun_terbit, stok, durasi):
        super().__init__(judul, sutradara, tahun_terbit, stok)
        self.durasi = durasi
        self.__denda_per_hari = 8000  # Rp 8000 per hari
    
    def tampilkan_info(self):
        print(f"\n🎬 DVD: {self.judul}")
        print(f"   Sutradara: {self.pengarang} | Tahun: {self.tahun_terbit}")
        print(f"   Durasi: {self.durasi} menit")
        print(f"   Stok: {self.get_stok()} | Terpinjam: {self.get_terpinjam()}")
        print(f"   Denda per hari: Rp {self.__denda_per_hari:,}")
    
    def hitung_denda(self, hari_terlambat):
        if hari_terlambat <= 0:
            return 0
        return self.__denda_per_hari * hari_terlambat


class Perpustakaan:
    """Class untuk mengelola perpustakaan"""
    
    def __init__(self, nama):
        self.nama = nama
        self.__koleksi = []
        self.__peminjam = {}
    
    def tambah_koleksi(self, item: Koleksi):
        self.__koleksi.append(item)
        print(f"✓ Koleksi '{item.judul}' berhasil ditambahkan")
    
    def tampilkan_semua_koleksi(self):
        print(f"\n{'='*60}")
        print(f"📖 KATALOG PERPUSTAKAAN: {self.nama}")
        print(f"{'='*60}")
        for item in self.__koleksi:
            item.tampilkan_info()
    
    def cari_koleksi(self, judul):
        for item in self.__koleksi:
            if judul.lower() in item.judul.lower():
                return item
        return None
    
    def proses_peminjaman(self, nama_peminjam, judul, jumlah=1):
        koleksi = self.cari_koleksi(judul)
        if not koleksi:
            print(f"❌ Koleksi '{judul}' tidak ditemukan!")
            return False
        
        if koleksi.pinjam(jumlah):
            if nama_peminjam not in self.__peminjam:
                self.__peminjam[nama_peminjam] = []
            
            tanggal_kembali = datetime.now() + timedelta(days=7)
            self.__peminjam[nama_peminjam].append({
                'judul': koleksi.judul,
                'tanggal_pinjam': datetime.now(),
                'tanggal_kembali': tanggal_kembali,
                'jumlah': jumlah,
                'koleksi': koleksi
            })
            print(f"   Harus dikembalikan pada: {tanggal_kembali.strftime('%d-%m-%Y')}")
            return True
        return False
    
    def hitung_denda_peminjam(self, nama_peminjam):
        if nama_peminjam not in self.__peminjam:
            print(f"❌ Peminjam '{nama_peminjam}' tidak ditemukan!")
            return
        
        total_denda = 0
        print(f"\n💰 RINCIAN DENDA - {nama_peminjam}")
        print(f"{'='*60}")
        
        for pinjaman in self.__peminjam[nama_peminjam]:
            hari_terlambat = (datetime.now() - pinjaman['tanggal_kembali']).days
            if hari_terlambat > 0:
                denda = pinjaman['koleksi'].hitung_denda(hari_terlambat)
                total_denda += denda
                print(f"📚 {pinjaman['judul']}")
                print(f"   Terlambat: {hari_terlambat} hari")
                print(f"   Denda: Rp {denda:,}")
        
        print(f"{'='*60}")
        print(f"TOTAL DENDA: Rp {total_denda:,}")
        return total_denda
    
    def laporan_stok(self):
        print(f"\n{'='*60}")
        print(f"📊 LAPORAN STOK - {self.nama}")
        print(f"{'='*60}")
        
        total_stok = 0
        total_terpinjam = 0
        
        for item in self.__koleksi:
            stok = item.get_stok()
            terpinjam = item.get_terpinjam()
            tersedia = stok - terpinjam
            
            total_stok += stok
            total_terpinjam += terpinjam
            
            print(f"{item.__class__.__name__:10} | {item.judul:25} | Stok: {stok:3} | Terpinjam: {terpinjam:2} | Tersedia: {tersedia:2}")
        
        print(f"{'='*60}")
        print(f"Total Stok: {total_stok} | Total Terpinjam: {total_terpinjam}")


# ===== MAIN PROGRAM =====
if __name__ == "__main__":
    perpus = Perpustakaan("Perpustakaan SMA Telkom Indonesia")
    
    # Tambah koleksi Buku
    buku1 = Buku("Laskar Pelangi", "Andrea Hirata", 2005, 5, 529, "ISBN-001")
    buku2 = Buku("Filosofi Teras", "Henry Manampiring", 2018, 3, 287, "ISBN-002")
    buku3 = Buku("Algoritma Pemrograman", "Rinaldi Munir", 2015, 4, 450, "ISBN-003")
    
    # Tambah koleksi Majalah
    majalah1 = Majalah("National Geographic Indonesia", "National Geographic", 2024, 6, "Mei 2024")
    majalah2 = Majalah("Science Today", "Science Publishing", 2024, 8, "April 2024")
    
    # Tambah koleksi DVD
    dvd1 = DVD("Avengers: Endgame", "Anthony & Joe Russo", 2019, 2, 181)
    dvd2 = DVD("Interstellar", "Christopher Nolan", 2014, 3, 169)
    
    # Masukkan ke perpustakaan
    for item in [buku1, buku2, buku3, majalah1, majalah2, dvd1, dvd2]:
        perpus.tambah_koleksi(item)
    
    # Tampilkan katalog
    perpus.tampilkan_semua_koleksi()
    
    # Simulasi peminjaman
    print(f"\n{'='*60}")
    print("🔔 TRANSAKSI PEMINJAMAN")
    print(f"{'='*60}")
    
    perpus.proses_peminjaman("Budi Santoso", "Laskar Pelangi", 1)
    perpus.proses_peminjaman("Siti Nurhaliza", "National Geographic Indonesia", 1)
    perpus.proses_peminjaman("Budi Santoso", "Avengers: Endgame", 1)
    perpus.proses_peminjaman("Andi Wijaya", "Filosofi Teras", 2)
    
    # Laporan stok
    perpus.laporan_stok()
    
    # Hitung denda (simulasi peminjaman terlambat)
    print(f"\n💡 CATATAN: Denda dihitung dari 7 hari setelah tanggal pinjam")
    print("   (Untuk demo, denda dihitung otomatis jika sudah melewati 7 hari)")
