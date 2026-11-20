import os
from rich.console import Console
from data import data_kamar, data_reservasi, user, data_pengumuman, simpan
from util import table as table_util
from datetime import datetime
from getpass import getpass

FORMAT_TANGGAL = "%d-%m-%Y"

baris = ("=" * 60)

def buat_kode_reservasi():
    return f"RSV-{len(data_reservasi) + 1:03d}"

console = Console()

def reset():
    os.system("cls" if os.name == "nt" else "clear")


def tampilkan_kamar():
    reset()
    print(baris)
    print("DAFTAR KAMAR".center(60))
    print(baris)
    try:
        if not data_kamar:
            raise LookupError("Data kamar masih kosong.")
        
        table = table_util("Daftar Kamar")
        table.add_column("No", justify="center")
        table.add_column("Kode Kamar", justify="center")
        table.add_column("Tipe Kamar", justify="center")
        table.add_column("Harga Per Malam", justify="center")
        table.add_column("Fasilitas", justify="center")

        for no, (id_kamar, info), in enumerate(data_kamar.items(), start=1):
            table.add_row(
                str(no),
                id_kamar,
                info["tipe"],
                f"Rp {info['harga']:,}",
                info["fasilitas"],
            )

        console.print(table)
        console.print(f"\nTotal Kamar: {len(data_kamar)}")

    except LookupError as e:
        console.print(f"\n>> {e}")
    except KeyError as e:
        console.print(f"\n>> Data kamar tidak lengkap, kolom {e} tidak ditemukan.")
    except Exception as e:
        console.print(f"\n>> Terjadi kesalahan: {e}")
    finally:
        input("\nTekan Enter untuk kembali...")


def kamar_tersedia():
    reset()
    print(baris)
    print("KAMAR TERSEDIA".center(60))
    print(baris)
    try:
        if not data_kamar:
            raise LookupError("Data kamar masih kosong.")

        
        tersedia = {
            nomor: info for nomor, info in data_kamar.items() 
            if info["status"].lower() == "tersedia"
        }

        if not tersedia:
            raise LookupError("Tidak ada kamar yang tersedia saat ini.")


        tabel = table_util("Data Kamar Yang Tersedia")
        tabel.add_column("No", justify="center")
        tabel.add_column("No. Kamar", justify="center")
        tabel.add_column("Tipe")
        tabel.add_column("Harga/Malam", justify="right")

        for no, (nomor, info) in enumerate(tersedia.items(), start=1):
            tabel.add_row(
                str(no),
                nomor,
                info["tipe"],
                f"Rp {info['harga']:,}"
            )

        console.print(tabel)
        console.print(f"\nTotal Kamar Tersedia: {len(tersedia)}")

    except LookupError as e:
        console.print(f"\n>> {e}")
    except KeyError as e:
        console.print(f"\n>> Data kamar tidak lengkap, kolom {e} tidak ditemukan.")
    except Exception as e:
        console.print(f"\n>> Terjadi kesalahan: {e}")
    finally:
        input("\nTekan Enter untuk kembali...")


def reservasi_saya(username):
    reset()
    print(baris)
    print("DETAIL DAN STATUS RESERVASI".center(60))
    print(baris)
    try:
        milik = {k: r for k, r in data_reservasi.items() if r.get("username") == username}
        if not milik:
            raise LookupError("Anda belum memiliki reservasi.")

        tabel = table_util("Reservasi Saya")
        tabel.add_column("Kode")
        tabel.add_column("No. Kamar", justify="center")
        tabel.add_column("Check-in", justify="center")
        tabel.add_column("Check-out", justify="center")
        tabel.add_column("Status")

        for (kode, info) in milik.items():
            tabel.add_row(
                kode, 
                info["kamar"], 
                info["checkin"], 
                info["checkout"],
                info.get("status", "MENUNGGU KONFIRMASI")
            )

        console.print(tabel)

    except LookupError as e:
        console.print(f"\n>> {e}")
    except KeyError as e:
        console.print(f"\n>> Data reservasi tidak lengkap, kolom {e} tidak ditemukan.")
    except Exception as e:
        console.print(f"\n>> Terjadi kesalahan: {e}")
    finally:
        input("\nTekan Enter untuk kembali...")


def riwayat_pembayaran(username):
    reset()
    print(baris)
    print("RIWAYAT PEMBAYARAN".center(60))
    print(baris)
    try:
        milik = {k: r for k, r in data_reservasi.items() if r.get("username") == username}
        if not milik:
            raise LookupError("Anda belum memiliki reservasi.")

        tabel = table_util("Riwayat Pembayaran")
        tabel.add_column("Kode")
        tabel.add_column("No. Kamar", justify="center")
        tabel.add_column("Check-in", justify="center")
        tabel.add_column("Check-out", justify="center")
        tabel.add_column("Status")

        for (kode, info) in milik.items():
            tabel.add_row(
                kode, 
                info["kamar"], 
                info["checkin"], 
                info["checkout"],
                info.get("status", "MENUNGGU KONFIRMASI")
            )

        console.print(tabel)

    except LookupError as e:
        console.print(f"\n>> {e}")
    except KeyError as e:
        console.print(f"\n>> Data reservasi tidak lengkap, kolom {e} tidak ditemukan.")
    except Exception as e:
        console.print(f"\n>> Terjadi kesalahan: {e}")
    finally:
        input("\nTekan Enter untuk kembali...")


def pengumuman_hotel():
    reset()
    print(baris)
    print("PENGUMUMAN HOTEL".center(60))
    print(baris)
    try:
        if not data_pengumuman:
            raise LookupError("Belum ada pengumuman.")
        
        table = table_util("Pengumuman Hotel")
        table.add_column("No", justify="center")
        table.add_column("Tanggal", justify="center")
        table.add_column("isi")

        for i, p in enumerate(data_pengumuman, start=1):
            table.add_row(
                i, 
                p['tanggal'], 
                p['isi'])

        console.print(table)

    except LookupError as e:
        console.print(f"\n>> {e}")
    except KeyError as e:
        console.print(f"\n>> Data pengumuman tidak lengkap, kolom {e} tidak ditemukan.")
    except Exception as e:
        console.print(f"\n>> Terjadi kesalahan: {e}")
    finally:
        input("\nTekan Enter untuk kembali...")


def reservasi_kamar(username):
    reset()
    print(baris)
    print("RESERVASI KAMAR".center(60))
    print(baris)
    try:
        nomor = input("Nomor Kamar       : ").strip().upper()
        kamar = data_kamar[nomor]

        masuk = input("Tanggal Check-in  : ").strip()
        keluar = input("Tanggal Check-out : ").strip()


        if kamar["status"].lower() != "tersedia":
            raise PermissionError

        masuk = datetime.strptime(masuk, FORMAT_TANGGAL)
        keluar = datetime.strptime(keluar, FORMAT_TANGGAL)
        if keluar <= masuk:
            raise ArithmeticError

        malam = (keluar - masuk).days
        total = malam * kamar["harga"]
        kode = buat_kode_reservasi()

        data_reservasi[kode] = {
            "username": username,
            "kamar": nomor,
            "checkin": masuk.strftime(FORMAT_TANGGAL),
            "checkout": keluar.strftime(FORMAT_TANGGAL),
            "malam": malam,
            "total": total,
            "status": "MENUNGGU KONFIRMASI",
            "pembayaran": "BELUM LUNAS",
        }
        kamar["status"] = "TERISI"
        simpan()

        print(f"\nKamar     : {nomor} ({kamar['tipe']})")
        print(f"Lama Inap : {malam} malam")
        print(f"Total     : Rp {total:,}".replace(",", "."))
        print(f"\n>> Reservasi berhasil! Kode reservasi: {kode}")

    except KeyError:
        print("\n>> Nomor kamar tidak ditemukan.")
    except PermissionError:
        print("\n>> Kamar sedang tidak tersedia.")
    except ArithmeticError:
        print("\n>> Tanggal check-out harus setelah tanggal check-in.")
    except ValueError:
        print("\n>> Format tanggal harus DD-MM-YYYY, contoh 20-11-2026.")
    finally:
        input("\nTekan Enter untuk kembali...")


def ubah_profil(username):
    reset()
    print(baris)
    print("UBAH DATA DIRI".center(60))
    print(baris)
    print(f"Username saat ini : {username}")
    try:
                
        print("\nKosongkan jika tidak diubah")
        user_baru = input("Username baru        : ").strip()
        pass_lama = getpass("Password lama        : ")
        pass_baru = getpass("Password baru        : ")

        akun = next((a for a in user if a[0] == username), None)
        if akun is None:
            raise KeyError("Akun tidak ditemukan.")
        if pass_lama != akun[1]:
            raise PermissionError("Password lama tidak sesuai.")
        if user_baru and user_baru != username and any(a[0] == user_baru for a in user):
            raise KeyError("Username sudah dipakai.")

        if pass_baru:
            akun[1] = pass_baru
        if user_baru and user_baru != username:
            akun[0] = user_baru
            for r in data_reservasi.values():
                if r.get("username") == username:
                    r["username"] = user_baru
            username = user_baru

        simpan()
        console.print("\n>> Data diri berhasil diperbarui.")

    except KeyError:
        console.print("\n>> Data pengguna tidak ditemukan.")
    except Exception as e:
        console.print(f"\n>> Terjadi kesalahan: {e}")
    finally:
        input("\nTekan Enter untuk kembali...")


