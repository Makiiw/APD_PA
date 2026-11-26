import os
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from data import data_kamar, data_reservasi, simpan
from rich.console import Console
from rich.table import Table

baris = ("=" * 60)
STATUS_KAMAR = ("TERSEDIA", "DIPESAN", "TERISI", "PERBAIKAN")
STATUS_MANUAL = ("TERSEDIA", "PERBAIKAN")

def tampilan_kelola_kamar():
    while True:
        os.system("cls")
        print (baris)
        pilihan = inquirer.select(
            message= "PILIHAN KELOLA KAMAR: ",
            choices = [
                    Choice(value= 1, name="Tambah Kamar"),
                    Choice(value=2, name="Tampil Data Kamar"),
                    Choice(value=3, name="Ubah Data Kamar"),
                    Choice(value=4, name="Hapus Data Kamar"),
                    Choice(value=5, name="Kembali Ke Menu Admin"),
                    Separator(baris)
                    ]
        ).execute()
        if pilihan == 1:
            tambah_kamar()
        elif pilihan == 2:
            tampilkan_kamar()
        elif pilihan == 3:
            ubah_kamar()
        elif pilihan == 4:
            hapus_kamar()
        elif pilihan == 5:
            break     

def tambah_kamar():
    os.system("cls")
    print(baris)
    print("TAMBAH KAMAR".center(60))
    print(baris)
    try:
        nomor_kamar = input("Nomor Kamar: ").strip().upper()
        tipe_kamar = input("Tipe Kamar: ").strip().upper()
        fasilitas_kamar = input("Fasilitas: ").strip().upper()
        harga_kamar = input("Harga per malam: ").strip()
        status_kamar = input("Status: ").strip().upper()
        
        if "" in (nomor_kamar, tipe_kamar, fasilitas_kamar, harga_kamar, status_kamar):
            raise ValueError("Semua data wajib diisi.")
        if nomor_kamar in data_kamar:
            raise KeyError(f"Nomor kamar {nomor_kamar} sudah terdaftar.")
        if status_kamar not in STATUS_MANUAL:
            raise ValueError("Status awal harus TERSEDIA atau PERBAIKAN (DIPESAN/TERISI mengikuti reservasi).")
        if not harga_kamar.isdigit():
            raise ValueError("Harga harus berupa angka.")
        harga = int(harga_kamar)
        if harga <= 0:
            raise ValueError("Harga harus lebih dari 0.")
        data_kamar[nomor_kamar] = {
            "tipe": tipe_kamar,
            "fasilitas": fasilitas_kamar,
            "harga": harga,
            "status": status_kamar
        }
        simpan()
        print("\n>> Data kamar berhasil ditambahkan!")
    except ValueError as e:
        print(f"\n>> Input tidak valid: {e}")
    except KeyError as e:
        print(f"\n>> Gagal! {e.args[0]}")
    except KeyboardInterrupt:
        print("\n\n>> Input dibatalkan.")
    except Exception as e:
        print(f"\n>> Terjadi kesalahan: {e}")
    finally:
        input("\nTekan Enter untuk kembali...")


def ubah_kamar():
    os.system("cls")
    print(baris)
    print("UBAH DATA KAMAR".center(60))
    print(baris)
    try:
        nomor = input("Masukkan nomor kamar yang diubah: ").strip().upper()
        kamar = data_kamar[nomor]
        print("\nKosongkan jika tidak diubah")
        tipe = input(f"Tipe [{kamar['tipe']}]: ").strip().upper()
        fasilitas = input(f"Fasilitas [{kamar['fasilitas']}]: ").strip().upper()
        harga = input(f"Harga [{kamar['harga']}]: ").strip()
        status = input(f"Status [{kamar['status']}]: ").strip().upper()
        if harga and not harga.isdigit():
            raise ValueError("Harga harus berupa angka.")
        harga_baru = int(harga) if harga else kamar["harga"]
        if harga_baru <= 0:
            raise ValueError("Harga harus lebih dari 0.")
        if status and status != kamar["status"] and status not in STATUS_MANUAL:
            raise ValueError("Status hanya boleh TERSEDIA atau PERBAIKAN (DIPESAN/TERISI mengikuti reservasi).")
        aktif = any(
            reservasi.get("kamar") == nomor
            and reservasi.get("status") not in ("SELESAI", "DIBATALKAN")
            for reservasi in data_reservasi.values()
        )
        if aktif and status and status != kamar["status"]:
            raise PermissionError("Status kamar mengikuti status reservasi aktif.")
        kamar["tipe"] = tipe or kamar["tipe"]
        kamar["fasilitas"] = fasilitas or kamar["fasilitas"]
        kamar["harga"] = harga_baru
        kamar["status"] = status or kamar["status"]
        simpan()
        print("\n>> Data kamar berhasil diubah!")
    except KeyError:
        print("\n>> Nomor kamar tidak ditemukan.")
    except ValueError as e:
        print(f"\n>> {e}")
    except PermissionError as e:
        print(f"\n>> {e}")
    finally:
        input("\nTekan Enter untuk kembali...")

console = Console()
def tampilkan_kamar():
    os.system("cls")
    try:
        if not data_kamar:
            raise LookupError("Data kamar masih kosong.")
        
        tabel = Table(title="Data Kamar Hotel", show_lines=True)
        tabel.add_column("No", justify="center")
        tabel.add_column("No. Kamar", justify="center")
        tabel.add_column("Tipe")
        tabel.add_column("Fasilitas")
        tabel.add_column("Harga/Malam", justify="right")
        tabel.add_column("Status", justify="center")
        
        for no, (nomor, info) in enumerate(data_kamar.items(), start=1):
            harga = f"Rp {info['harga']:,}".replace(",", ".")
            tabel.add_row(str(no), nomor, info["tipe"], info["fasilitas"], harga, info["status"])
            
        console.print(tabel)
        console.print(f"\nTotal kamar: {len(data_kamar)}")
        
    except LookupError as e:
        console.print(f"\n>> {e}")
    except KeyError as e:
        console.print(f"\n>> Data kamar tidak lengkap, kolom {e} tidak ditemukan.")
    except Exception as e:
        console.print(f"\n>> Terjadi kesalahan tak terduga: {e}")
    finally:
        input("\nTekan Enter untuk kembali...")
        
def hapus_kamar():
    os.system("cls")
    print(baris)
    print("HAPUS DATA KAMAR".center(60))
    print(baris)
    try:
        nomor = input("Masukkan nomor kamar yang dihapus: ").strip().upper()
        kamar = data_kamar[nomor]
        ada_reservasi_aktif = any(
            reservasi.get("kamar") == nomor
            and reservasi.get("status") not in ("SELESAI", "DIBATALKAN")
            for reservasi in data_reservasi.values()
        )
        if ada_reservasi_aktif:
            raise PermissionError("Kamar memiliki reservasi aktif, tidak dapat dihapus.")
        print(f"\nTipe      : {kamar['tipe']}")
        print(f"Fasilitas : {kamar['fasilitas']}")
        print(f"Harga     : {kamar['harga']}")
        print(f"Status    : {kamar['status']}")
        konfirmasi = input("\nYakin ingin menghapus? (y/n): ").strip().lower()
        if konfirmasi == "y":
            del data_kamar[nomor]
            simpan()
            print("\n>> Data kamar berhasil dihapus!")
        else:
            print("\n>> Penghapusan dibatalkan.")
    except KeyError:
        print("\n>> Nomor kamar tidak ditemukan.")
    except PermissionError as e:
        print(f"\n>> Gagal! {e}")
    finally:
        input("\nTekan Enter untuk kembali...")
