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
def tampilkan_kamar():
    os.system("cls" if os.name == "nt" else "clear")
    print(baris)
    print("DAFTAR KAMAR".center(60))
    print(baris)
    try:
        if not data_kamar:
            raise LookupError("Informasi Kamar Tidak Tersedia.")

        tabel = table_util("Data Kamar Hotel")
        tabel.add_column("No", justify="center")
        tabel.add_column("No. Kamar", justify="center")
        tabel.add_column("Tipe")
        tabel.add_column("Fasilitas")
        tabel.add_column("Harga/Malam", justify="right")

        for no, (nomor, info) in enumerate(data_kamar.items(), start=1):
            harga = f"Rp {info['harga']:,}".replace(",", ".")
            tabel.add_row(str(no), nomor, info["tipe"], info["fasilitas"], harga)
            
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

def kamar_tersedia():
    os.system("cls" if os.name == "nt" else "clear")
    print(baris)
    print("DAFTAR KAMAR TERSEDIA".center(60))
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
            harga = f"Rp {info['harga']:,}".replace(",", ".")
            tabel.add_row(str(no), nomor, info["tipe"], harga)
            
        console.print(tabel)
        console.print(f"\nTotal kamar: {len(tersedia)}")
        
    except LookupError as e:
        console.print(f"\n>> {e}")
    except KeyError as e:
        console.print(f"\n>> Data kamar tidak lengkap, kolom {e} tidak ditemukan.")
    except Exception as e:
        console.print(f"\n>> Terjadi kesalahan tak terduga: {e}")
    finally:
        input("\nTekan Enter untuk kembali...")

def reservasi_kamar(username):
    os.system("cls" if os.name == "nt" else "clear")
    print(baris)
    print("RESERVASI KAMAR".center(60))
    print(baris)
    try:
        nomor = input("Nomor Kamar       : ").strip().upper()
        try:
            masuk = datetime.strptime(input("Tanggal Check-in  : ").strip(), FORMAT_TANGGAL)
            keluar = datetime.strptime(input("Tanggal Check-out : ").strip(), FORMAT_TANGGAL)
        except ValueError:
            raise ValueError("Format tanggal harus DD-MM-YYYY, contoh 20-11-2026.")

        kamar = data_kamar[nomor]
        if kamar["status"].lower() != "tersedia":
            raise PermissionError(f"Kamar {nomor} sedang tidak tersedia.")
        if keluar <= masuk:
            raise ValueError("Tanggal check-out harus setelah tanggal check-in.")

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
        print("\n>> Gagal! Nomor kamar tidak ditemukan.")
    except (PermissionError, ValueError) as e:
        print(f"\n>> Gagal! {e}")
    finally:
        input("\nTekan Enter untuk kembali...")

def reservasi_saya(username):
    os.system("cls" if os.name == "nt" else "clear")
    print(baris)
    print("RESERVASI SAYA".center(60))
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

        for kode, r in milik.items():
            tabel.add_row(kode, r["kamar"], r["checkin"], r["checkout"],
                          r.get("status", "MENUNGGU KONFIRMASI"))
        console.print(tabel)
    except LookupError as e:
        console.print(f"\n>> {e}")
    except KeyError as e:
        console.print(f"\n>> Data reservasi tidak lengkap, kolom {e} tidak ditemukan.")
    finally:
        input("\nTekan Enter untuk kembali...")


def riwayat_pembayaran(username):
    os.system("cls" if os.name == "nt" else "clear")
    print(baris)
    print("RIWAYAT PEMBAYARAN".center(60))
    print(baris)
    try:
        milik = {k: r for k, r in data_reservasi.items() if r.get("username") == username}
        if not milik:
            raise LookupError("Belum ada riwayat pembayaran.")

        tabel = table_util("Riwayat Pembayaran")
        tabel.add_column("Kode")
        tabel.add_column("Total Biaya", justify="right")
        tabel.add_column("Status")

        for kode, r in milik.items():
            total = f"Rp {r['total']:,}".replace(",", ".")
            tabel.add_row(kode, total, r.get("pembayaran", "BELUM LUNAS"))
        console.print(tabel)
    except LookupError as e:
        console.print(f"\n>> {e}")
    except KeyError as e:
        console.print(f"\n>> Data reservasi tidak lengkap, kolom {e} tidak ditemukan.")
    finally:
        input("\nTekan Enter untuk kembali...")


def ubah_profil(username):
    os.system("cls" if os.name == "nt" else "clear")
    print(baris)
    print("UBAH PROFIL".center(60))
    print(baris)
    print(f"Username saat ini : {username}")
    try:
        print("\nKosongkan jika tidak diubah")
        user_baru = input("Username baru        : ").strip()
        pass_lama = input("Password lama        : ")
        pass_baru = input("Password baru        : ")

        # akun di JSON berbentuk list: [username, password, "User"]
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
        print("\n>> Profil berhasil diperbarui!")
    except PermissionError as e:
        print(f"\n>> Gagal! {e}")
    except KeyError as e:
        print(f"\n>> Gagal! {e.args[0]}")
    finally:
        input("\nTekan Enter untuk kembali...")
    return username


def pengumuman_hotel():
    os.system("cls" if os.name == "nt" else "clear")
    print(baris)
    print("PENGUMUMAN HOTEL".center(60))
    print(baris)
    try:
        if not data_pengumuman:
            raise LookupError("Belum ada pengumuman.")
        for p in data_pengumuman:
            print(f"[{p['tanggal']}] {p['isi']}")
    except LookupError as e:
        print(f"\n>> {e}")
    finally:
        input("\nTekan Enter untuk kembali...")