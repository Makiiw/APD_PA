import os
from datetime import datetime
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from rich.console import Console
from data import data_kamar, data_reservasi, data_tamu, user as data_user, cari_tamu, simpan
from util import table as table_util
from fitur_user import buat_kode_reservasi

baris = ("=" * 60)
console = Console()
FORMAT_TANGGAL = "%d-%m-%Y"

ALUR = {
    "MENUNGGU KONFIRMASI": ["DIKONFIRMASI", "DIBATALKAN"],
    "DIKONFIRMASI": ["CHECK-IN", "DIBATALKAN"],
    "CHECK-IN": ["SELESAI"],
    "SELESAI": [],
    "DIBATALKAN": [],
}


def tampilan_kelola_reservasi():
    while True:
        os.system("cls")
        print(baris)
        pilihan = inquirer.select(
            message="PILIHAN KELOLA RESERVASI: ",
            choices=[
                Choice(value=1, name="Tambah Reservasi"),
                Choice(value=2, name="Tampil Data Reservasi"),
                Choice(value=3, name="Ubah Status Reservasi"),
                Choice(value=4, name="Hapus Reservasi"),
                Choice(value=5, name="Kembali Ke Menu Admin"),
                Separator(baris)
            ]
        ).execute()
        if pilihan == 1:
            tambah_reservasi()
        elif pilihan == 2:
            tampilkan_reservasi()
        elif pilihan == 3:
            ubah_status_reservasi()
        elif pilihan == 4:
            hapus_reservasi()
        elif pilihan == 5:
            return


def tambah_reservasi():
    os.system("cls")
    print(baris)
    print("TAMBAH RESERVASI".center(60))
    print(baris)
    try:
        username = input("Username Tamu     : ").strip()
        nomor = input("Nomor Kamar       : ").strip().upper()
        try:
            masuk = datetime.strptime(input("Tanggal Check-in  : ").strip(), FORMAT_TANGGAL)
            keluar = datetime.strptime(input("Tanggal Check-out : ").strip(), FORMAT_TANGGAL)
        except ValueError:
            raise ValueError("Format tanggal harus DD-MM-YYYY, contoh 20-11-2026.")

        if not any(akun[0] == username for akun in data_user):
            raise ValueError("Username tamu tidak terdaftar.")
        id_tamu, tamu = cari_tamu(username)
        if not tamu:
            raise ValueError("Tamu belum punya data tamu. Tambahkan dulu di Kelola Data Tamu.")
        kamar = data_kamar[nomor]
        if kamar["status"].upper() != "TERSEDIA":
            raise PermissionError(f"Kamar {nomor} sedang tidak tersedia.")
        if masuk.date() < datetime.now().date():
            raise ValueError("Tanggal check-in tidak boleh sebelum hari ini.")
        if keluar <= masuk:
            raise ValueError("Tanggal check-out harus setelah tanggal check-in.")

        malam = (keluar - masuk).days
        total = malam * kamar["harga"]
        kode = buat_kode_reservasi()

        data_reservasi[kode] = {
            "username": username,
            "id_tamu": id_tamu,
            "kamar": nomor,
            "checkin": masuk.strftime(FORMAT_TANGGAL),
            "checkout": keluar.strftime(FORMAT_TANGGAL),
            "malam": malam,
            "total": total,
            "status": "DIKONFIRMASI",
            "pembayaran": "BELUM LUNAS",
        }
        kamar["status"] = "DIPESAN"
        simpan()

        print(f"\nKamar     : {nomor} ({kamar['tipe']})")
        print(f"Lama Inap : {malam} malam")
        print(f"Total     : Rp {total:,}".replace(",", "."))
        print(f"\n>> Reservasi berhasil ditambahkan! Kode reservasi: {kode}")
    except KeyError:
        print("\n>> Gagal! Nomor kamar tidak ditemukan.")
    except (PermissionError, ValueError) as e:
        print(f"\n>> Gagal! {e}")
    finally:
        input("\nTekan Enter untuk kembali...")


def tampilkan_reservasi():
    os.system("cls")
    try:
        if not data_reservasi:
            console.print("\n>> Data reservasi masih kosong.")
            return

        tabel = table_util("Data Reservasi Hotel")
        tabel.add_column("Kode")
        tabel.add_column("Username")
        tabel.add_column("Nama Tamu")
        tabel.add_column("No. Kamar", justify="center")
        tabel.add_column("Check-in", justify="center")
        tabel.add_column("Check-out", justify="center")
        tabel.add_column("Malam", justify="center")
        tabel.add_column("Total", justify="right")
        tabel.add_column("Status")
        tabel.add_column("Pembayaran")

        for kode, r in data_reservasi.items():
            total = f"Rp {r['total']:,}".replace(",", ".")
            tabel.add_row(kode, r["username"], data_tamu.get(r.get("id_tamu"), {}).get("Nama", "-"), r["kamar"], r["checkin"], r["checkout"],
                          str(r["malam"]), total,
                          r.get("status", "MENUNGGU KONFIRMASI"),
                          r.get("pembayaran", "BELUM LUNAS"))

        console.print(tabel)
        console.print(f"\nTotal reservasi: {len(data_reservasi)}")

    except KeyError as e:
        console.print(f"\n>> Data reservasi tidak lengkap, kolom {e} tidak ditemukan.")
    except Exception as e:
        console.print(f"\n>> Terjadi kesalahan: {e}")
    finally:
        input("\nTekan Enter untuk kembali...")


def ubah_status_reservasi():
    os.system("cls")
    print(baris)
    print("UBAH STATUS RESERVASI".center(60))
    print(baris)
    try:
        kode = input("Masukkan kode reservasi: ").strip().upper()
        r = data_reservasi[kode]

        status_lama = r.get("status", "MENUNGGU KONFIRMASI")
        tujuan = ALUR.get(status_lama, [])
        if not tujuan:
            raise PermissionError(f"Reservasi berstatus {status_lama}, tidak dapat diubah lagi.")

        print(f"\nTamu            : {r['username']}")
        print(f"Kamar           : {r['kamar']}")
        print(f"Status saat ini : {status_lama}\n")

        status_baru = inquirer.select(
            message="Ubah status menjadi: ",
            choices=tujuan
        ).execute()

        r["status"] = status_baru
        if r["kamar"] in data_kamar:
            if status_baru == "CHECK-IN":
                data_kamar[r["kamar"]]["status"] = "TERISI"
            elif status_baru in ("SELESAI", "DIBATALKAN"):
                data_kamar[r["kamar"]]["status"] = "TERSEDIA"
            else:
                data_kamar[r["kamar"]]["status"] = "DIPESAN"
        simpan()

        print(f"\n>> Status reservasi {kode} berhasil diubah menjadi {status_baru}!")
    except KeyError:
        print("\n>> Kode reservasi tidak ditemukan.")
    except PermissionError as e:
        print(f"\n>> Gagal! {e}")
    finally:
        input("\nTekan Enter untuk kembali...")


def hapus_reservasi():
    os.system("cls")
    print(baris)
    print("HAPUS RESERVASI".center(60))
    print(baris)
    try:
        kode = input("Masukkan kode reservasi yang dihapus: ").strip().upper()
        r = data_reservasi[kode]
        status = r.get("status", "MENUNGGU KONFIRMASI")

        if status == "CHECK-IN":
            raise PermissionError("Tamu sedang check-in, reservasi tidak dapat dihapus.")

        print(f"\nTamu      : {r['username']}")
        print(f"Kamar     : {r['kamar']}")
        print(f"Check-in  : {r['checkin']}")
        print(f"Check-out : {r['checkout']}")
        print(f"Status    : {status}")

        konfirmasi = input("\nYakin ingin menghapus? (y/n): ").strip().lower()
        if konfirmasi == "y":
            if status not in ("SELESAI", "DIBATALKAN") and r["kamar"] in data_kamar:
                data_kamar[r["kamar"]]["status"] = "TERSEDIA"
            del data_reservasi[kode]
            simpan()
            print("\n>> Data reservasi berhasil dihapus!")
        else:
            print("\n>> Penghapusan dibatalkan.")
    except KeyError:
        print("\n>> Kode reservasi tidak ditemukan.")
    except PermissionError as e:
        print(f"\n>> Gagal! {e}")
    finally:
        input("Tekan enter untuk lanjut")
