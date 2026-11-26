import os
from datetime import datetime
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from rich.console import Console
from rich.markup import escape
from data import data_pengumuman, simpan
from util import table as table_util

baris = ("=" * 60)
console = Console()
FORMAT_TANGGAL = "%d-%m-%Y"


def tampilan_kelola_pengumuman():
    while True:
        os.system("cls")
        print(baris)
        pilihan = inquirer.select(
            message="PILIHAN KELOLA PENGUMUMAN: ",
            choices=[
                Choice(value=1, name="[1] Buat Pengumuman"),
                Choice(value=2, name="[2] Tampil Data Pengumuman"),
                Choice(value=3, name="[3] Ubah Pengumuman"),
                Choice(value=4, name="[4] Hapus Pengumuman"),
                Choice(value=5, name="[5] Kembali Ke Menu Admin"),
                Separator(baris)
            ]
        ).execute()
        if pilihan == 1:
            buat_pengumuman()
        elif pilihan == 2:
            tampilkan_pengumuman()
        elif pilihan == 3:
            ubah_pengumuman()
        elif pilihan == 4:
            hapus_pengumuman()
        elif pilihan == 5:
            return


def ambil_pengumuman(teks_nomor):
    nomor = int(teks_nomor)
    if nomor < 1 or nomor > len(data_pengumuman):
        raise IndexError
    return data_pengumuman[nomor - 1]


def buat_pengumuman():
    os.system("cls")
    print(baris)
    print("BUAT PENGUMUMAN".center(60))
    print(baris)
    try:
        isi = input("Isi Pengumuman: ").strip()
        if isi == "":
            raise ValueError("Isi pengumuman tidak boleh kosong.")

        tanggal = datetime.now().strftime(FORMAT_TANGGAL)
        data_pengumuman.insert(0, {"tanggal": tanggal, "isi": isi})
        simpan()

        print(f"\n>> Pengumuman berhasil dibuat! (tanggal {tanggal})")
    except ValueError as e:
        print(f"\n>> Gagal! {e}")
    except KeyboardInterrupt:
        print("\n\n>> Input dibatalkan.")
    finally:
        input("\nTekan Enter untuk kembali...")


def tampilkan_pengumuman():
    os.system("cls")
    print(baris)
    print("DAFTAR PENGUMUMAN".center(60))
    print(baris)
    try:
        if not data_pengumuman:
            console.print("\n>> Belum ada pengumuman.")
            return  

        tabel = table_util("Data Pengumuman Hotel")
        tabel.add_column("No", justify="center")
        tabel.add_column("Tanggal", justify="center")
        tabel.add_column("Isi")

        for no, p in enumerate(data_pengumuman, start=1):
            tabel.add_row(str(no), p["tanggal"], escape(p["isi"]))

        console.print(tabel)
        console.print(f"\nTotal pengumuman: {len(data_pengumuman)}")

    except KeyError as e:
        console.print(f"\n>> Data pengumuman tidak lengkap, kolom {e} tidak ditemukan.")
    except Exception as e:
        console.print(f"\n>> Terjadi kesalahan: {e}")
    finally:
        input("\nTekan Enter untuk kembali...")


def ubah_pengumuman():
    os.system("cls")
    print(baris)
    print("UBAH PENGUMUMAN".center(60))
    print(baris)
    try:
        if not data_pengumuman:
            print("\n>> Belum ada pengumuman.")
            return

        nomor = input("Masukkan nomor pengumuman yang diubah: ").strip()
        p = ambil_pengumuman(nomor)

        print(f"\nIsi saat ini : {p['isi']}")
        print("\nKosongkan jika tidak diubah")
        isi_baru = input("Isi baru : ").strip()

        p["isi"] = isi_baru or p["isi"]
        simpan()

        print("\n>> Pengumuman berhasil diubah!")
    except IndexError:
        print("\n>> Nomor pengumuman tidak ditemukan.")
    except ValueError:
        print("\n>> Gagal! Nomor harus berupa angka.")
    finally:
        input("\nTekan Enter untuk kembali...")


def hapus_pengumuman():
    os.system("cls")
    print(baris)
    print("HAPUS PENGUMUMAN".center(60))
    print(baris)
    try:
        if not data_pengumuman:
            print("\n>> Belum ada pengumuman.")
            return

        nomor = input("Masukkan nomor pengumuman yang dihapus: ").strip()
        p = ambil_pengumuman(nomor)

        print(f"\nTanggal : {p['tanggal']}")
        print(f"Isi     : {p['isi']}")

        konfirmasi = input("\nYakin ingin menghapus? (y/n): ").strip().lower()
        if konfirmasi == "y":
            del data_pengumuman[int(nomor) - 1]
            simpan()
            print("\n>> Pengumuman berhasil dihapus!")
        else:
            print("\n>> Penghapusan dibatalkan.")
    except IndexError:
        print("\n>> Nomor pengumuman tidak ditemukan.")
    except ValueError:
        print("\n>> Gagal! Nomor harus berupa angka.")
    finally:
        input("\nTekan Enter untuk kembali...")