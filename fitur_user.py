import os
from rich.console import Console
from data import data_kamar, data_reservasi, user, data_pengumuman, simpan
from util import table as table_util, rupiah
from datetime import datetime
from pwinput import pwinput
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator

FORMAT_TANGGAL = "%d-%m-%Y"

baris = ("=" * 60)

def buat_kode_reservasi():
    nomor_terbesar = 0
    for kode in data_reservasi:
        try:
            nomor = int(kode.split("-")[1])
        except (IndexError, ValueError):
            continue
        nomor_terbesar = max(nomor_terbesar, nomor)
    return f"RSV-{nomor_terbesar + 1:03d}"

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
        table.add_column("Status", justify="center")

        for no, (id_kamar, info), in enumerate(data_kamar.items(), start=1):
            table.add_row(
                str(no),
                id_kamar,
                info["tipe"],
                rupiah(info["harga"]),
                info["fasilitas"],
                info["status"],
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
        tabel.add_column("Total", justify="right")
        tabel.add_column("Pembayaran", justify="center")
        tabel.add_column("Status")

        total_belum_lunas = 0
        for (kode, info) in milik.items():
            total = info.get("total", 0)
            pembayaran = info.get("pembayaran", "BELUM LUNAS")
            if pembayaran.upper() != "LUNAS":
                total_belum_lunas += total

            tabel.add_row(
                kode, 
                info["kamar"], 
                info["checkin"], 
                info["checkout"],
                rupiah(total),
                pembayaran,
                info.get("status", "MENUNGGU KONFIRMASI")
            )

        console.print(tabel)
        console.print(f"\nTotal belum dibayar: {rupiah(total_belum_lunas)}")

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
                str(i), 
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

    while True:
        reset()
        print(baris)
        print("RESERVASI KAMAR".center(60))
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


            tabel = table_util("Kamar Yang Tersedia")
            tabel.add_column("No", justify="center")
            tabel.add_column("No. Kamar", justify="center")
            tabel.add_column("Tipe")
            tabel.add_column("Harga/Malam", justify="right")

            for no, (nomor, info) in enumerate(tersedia.items(), start=1):
                tabel.add_row(
                    str(no),
                    nomor,
                    info["tipe"],
                    rupiah(info["harga"])
                )

            console.print(tabel)
            console.print(f"\nTotal Kamar Tersedia: {len(tersedia)}")
            print(f"Total     : {rupiah(total)}")

            print(baris)

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
            kamar["status"] = "DIPESAN"
            simpan()

            print(f"\nKamar     : {nomor} ({kamar['tipe']})")
            print(f"Lama Inap : {malam} malam")
            print(f"Total     : Rp {total:,}".replace(",", "."))
            print(f"\n>> Reservasi berhasil! Kode reservasi: {kode}")
            input("\nTekan Enter untuk kembali...")
            return


        except KeyError:
            print("\n>> Nomor kamar tidak ditemukan.")
        except LookupError as e:
            print(f"\n>> {e}")
            input("\nTekan Enter untuk kembali...")
            return
        except PermissionError:
            print("\n>> Kamar sedang tidak tersedia.")
        except ArithmeticError:
            print("\n>> Tanggal check-out harus setelah tanggal check-in.")
        except ValueError:
            print("\n>> Format tanggal harus DD-MM-YYYY, contoh 20-11-2026.")

        ulang = input("\nCoba lagi? (y/n): ").strip().lower()
        if ulang != "y":
            return

def ubah_profil(username):
    
    while True:
        reset()
        print(baris)
        print("UBAH DATA DIRI".center(60))
        print(baris)
        print(f"Username saat ini : {username}")
        try:
                    
            print("\nKosongkan jika tidak diubah")
            user_baru = input("Username baru        : ").strip()
            pass_lama = pwinput("Password lama        : ")
            pass_baru = pwinput("Password baru        : ")

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
            input("\nTekan Enter untuk kembali...")
            return username

        except (LookupError, PermissionError, ValueError) as e:
            console.print(f"\n>> {e}")
        except Exception as e:
            console.print(f"\n>> Terjadi kesalahan: {e}")

        ulang = input("\nCoba lagi? (y/n): ").strip().lower()
        if ulang != "y":
            return username