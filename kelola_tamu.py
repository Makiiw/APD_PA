import os
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from data import data_kamar, simpan, data_tamu
from rich.console import Console
from rich.table import Table
console = Console()
baris = ("=" * 60)

def tampilan_kelola_tamu():
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
            tambah_tamu()
        elif pilihan == 2:
            tampilkan_tamu()
        elif pilihan == 3:
            ubah_tamu()
        elif pilihan == 4:
            hapus_tamu()

def tambah_tamu():
        os.system("cls")
        print(baris)
        print("TAMBAH TAMU".center(60))
        print(baris)
        try:
            id_tamu = input("Masukan Id Tamu: ").strip().upper()
            nama_tamu = input("Masukan Nama Tamu: ").strip().upper()
            no_hp = input("Masukan No HP: ").strip().upper()
            alamat = input("Masukan Alamat: ").strip()
            
            if "" in (id_tamu, nama_tamu, no_hp, alamat):
                raise ValueError("Semua data wajib diisi.")
            if id_tamu in data_tamu:
                raise KeyError(f"Nomor kamar sudah terdaftar.")
            no_hp = int(no_hp)
            if no_hp <= 0:
                raise ValueError("Harga harus lebih dari 0.")
            data_tamu[id_tamu] = {
                "ID TAMU": id_tamu,
                "Nama": nama_tamu,
                "NO. HP": no_hp,
                "Alamat": alamat
            }
            simpan()
            print("\n>> Data tamu berhasil ditambahkan!")
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

