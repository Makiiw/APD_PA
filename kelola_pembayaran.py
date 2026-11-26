import os
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from rich.console import Console
from data import data_reservasi, simpan
from util import table as table_util, rupiah

baris = ("=" * 60)
console = Console()


def tampilan_kelola_pembayaran():
    while True:
        os.system("cls")
        print(baris)
        pilihan = inquirer.select(
            message="PILIHAN KELOLA PEMBAYARAN: ",
            choices=[
                Choice(value=1, name="Tampil Data Pembayaran"),
                Choice(value=2, name="Ubah Status Pelunasan"),
                Choice(value=3, name="Kembali Ke Menu Admin"),
                Separator(baris)
            ]
        ).execute()
        if pilihan == 1:
            tampilkan_pembayaran()
        elif pilihan == 2:
            ubah_status_pelunasan()
        elif pilihan == 3:
            return


def tampilkan_pembayaran():
    os.system("cls")
    print(baris)
    print("DAFTAR PEMBAYARAN".center(60))
    print(baris)
    try:
        if not data_reservasi:
            console.print("\n>> Data pembayaran masih kosong.")
            return 

        tabel = table_util("Data Pembayaran Hotel")
        tabel.add_column("No", justify="center")
        tabel.add_column("Kode")
        tabel.add_column("Username")
        tabel.add_column("Total Biaya", justify="right")
        tabel.add_column("Status Reservasi")
        tabel.add_column("Pembayaran")

        jumlah_lunas = jumlah_belum = 0
        total_lunas = total_belum = 0

        for no, (kode, r) in enumerate(data_reservasi.items(), start=1):
            pembayaran = r.get("pembayaran", "BELUM LUNAS")
            status = r.get("status", "MENUNGGU KONFIRMASI")
            tabel.add_row(str(no), kode, r["username"], rupiah(r["total"]), status, pembayaran)

            if pembayaran == "LUNAS":
                jumlah_lunas += 1
                total_lunas += r["total"]
            elif status != "DIBATALKAN": 
                jumlah_belum += 1
                total_belum += r["total"]

        console.print(tabel)
        console.print(f"\nLunas       : {jumlah_lunas} pembayaran  ({rupiah(total_lunas)})")
        console.print(f"Belum lunas : {jumlah_belum} pembayaran  ({rupiah(total_belum)})")

    except KeyError as e:
        console.print(f"\n>> Data reservasi tidak lengkap, kolom {e} tidak ditemukan.")
    except Exception as e:
        console.print(f"\n>> Terjadi kesalahan: {e}")
    finally:
        input("\nTekan Enter untuk kembali...")


def ubah_status_pelunasan():
    os.system("cls")
    print(baris)
    print("UBAH STATUS PELUNASAN".center(60))
    print(baris)
    try:
        kode = input("Masukkan kode reservasi: ").strip().upper()
        r = data_reservasi[kode]  

        pembayaran = r.get("pembayaran", "BELUM LUNAS")
        status = r.get("status", "MENUNGGU KONFIRMASI")

        if status == "DIBATALKAN":
            raise PermissionError("Reservasi DIBATALKAN, status pembayaran tidak dapat diubah.")
        if pembayaran == "LUNAS":
            raise PermissionError(f"Pembayaran {kode} sudah berstatus LUNAS.")

        print(f"\nTamu            : {r['username']}")
        print(f"Total Biaya     : {rupiah(r['total'])}")
        print(f"Pembayaran      : {pembayaran}\n")

        status_baru = inquirer.select(
            message="Ubah status pembayaran menjadi: ",
            choices=["LUNAS"]
        ).execute()

        r["pembayaran"] = status_baru
        simpan()

        print(f"\n>> Status pembayaran {kode} berhasil diubah menjadi {status_baru}!")
    except KeyError:
        print("\n>> Kode reservasi tidak ditemukan.")
    except PermissionError as e:
        print(f"\n>> Gagal! {e}")
    finally:
        input("\nTekan Enter untuk kembali...")