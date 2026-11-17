import os
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from data import data_kamar
from tabulate import tabulate

baris = ("=" * 60)

def tampilan_kelola_kamar():
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
        
        harga = int(harga_kamar)
        if harga <= 0:
            raise ValueError("Harga harus lebih dari 0.")
        
        data_kamar[nomor_kamar] = {
            "tipe": tipe_kamar,
            "fasilitas": fasilitas_kamar,
            "harga": harga,
            "status": status_kamar
        }
        print("\n>> Data kamar berhasil ditambahkan!")
        
    except ValueError as e:
        print(f"\n>> Gagal! Input tidak valid: {e}")
    except KeyError as e:
        print(f"\n>> Gagal! {e.args[0]}")
    except KeyboardInterrupt:
        print("\n\n>> Input dibatalkan.")
    except Exception as e:
        print(f"\n>> Terjadi kesalahan tak terduga: {e}")
    finally:
        input("\nTekan Enter untuk kembali...")

def tampilkan_kamar():
    os.system("cls")
    print(baris)
    print("DAFTAR KAMAR".center(60))
    print(baris)
    try:
        if not data_kamar:
            raise LookupError("Data kamar masih kosong.")
        
        tabel = []
        for no, (nomor, info) in enumerate(data_kamar.items(), start=1):
            harga = f"Rp {info['harga']:,}".replace(",", ".")
            tabel.append([no, nomor, info["tipe"], info["fasilitas"], harga, info["status"]])
            
        header = ["No", "No. Kamar", "Tipe", "Fasilitas", "Harga/Malam", "Status"]
        print(tabulate(tabel, headers=header, tablefmt="grid"))
        print(f"\nTotal kamar: {len(data_kamar)}")
        
    except LookupError as e:
        print(f"\n>> {e}")
    except KeyError as e:
        print(f"\n>> Data kamar tidak lengkap, kolom {e} tidak ditemukan.")
    except Exception as e:
        print(f"\n>> Terjadi kesalahan tak terduga: {e}")
    finally:
        input("\nTekan Enter untuk kembali...")

tambah_kamar()
tampilkan_kamar()
