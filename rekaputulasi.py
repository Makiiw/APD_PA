import os
from collections import Counter
from rich.console import Console
from data import data_kamar, data_tamu, data_reservasi
from util import table as table_util, rupiah

baris = ("=" * 60)
console = Console()

STATUS_KAMAR = ["TERSEDIA", "DIPESAN", "TERISI", "PERBAIKAN"]
STATUS_RESERVASI = ["MENUNGGU KONFIRMASI", "DIKONFIRMASI", "CHECK-IN", "SELESAI", "DIBATALKAN"]


def rekaputulasi():
    os.system("cls")
    print(baris)
    print("REKAPITULASI HOTEL".center(60))
    print(baris)
    try:
        hitung_kamar = Counter(k["status"].upper() for k in data_kamar.values())
        tabel_kamar = table_util("Rekap Kamar")
        tabel_kamar.add_column("Keterangan")
        tabel_kamar.add_column("Jumlah", justify="center")
        tabel_kamar.add_row("Total kamar", str(len(data_kamar)))
        for s in STATUS_KAMAR:
            tabel_kamar.add_row(s.capitalize(), str(hitung_kamar[s]))
        lainnya = len(data_kamar) - sum(hitung_kamar[s] for s in STATUS_KAMAR)
        if lainnya: 
            tabel_kamar.add_row("Lainnya", str(lainnya))

        
        hitung_reservasi = Counter(
            r.get("status", "MENUNGGU KONFIRMASI") for r in data_reservasi.values()
        )
        tabel_reservasi = table_util("Rekap Tamu & Reservasi")
        tabel_reservasi.add_column("Keterangan")
        tabel_reservasi.add_column("Jumlah", justify="center")
        tabel_reservasi.add_row("Total tamu terdaftar", str(len(data_tamu)))
        tabel_reservasi.add_row("Total reservasi", str(len(data_reservasi)))
        for s in STATUS_RESERVASI:
            tabel_reservasi.add_row(s.capitalize(), str(hitung_reservasi[s]))

        
        lunas = 0
        belum = 0
        for r in data_reservasi.values():
            if r.get("status", "MENUNGGU KONFIRMASI") == "DIBATALKAN":
                continue
            if r.get("pembayaran", "BELUM LUNAS") == "LUNAS":
                lunas += r["total"]
            else:
                belum += r["total"]

        tabel_uang = table_util("Rekap Pemasukan")
        tabel_uang.add_column("Keterangan")
        tabel_uang.add_column("Jumlah", justify="right")
        tabel_uang.add_row("Pemasukan (sudah lunas)", rupiah(lunas))
        tabel_uang.add_row("Belum dibayar", rupiah(belum))
        tabel_uang.add_row("Total nilai reservasi", rupiah(lunas + belum))

        console.print(tabel_kamar)
        console.print("")
        console.print(tabel_reservasi)
        console.print("")
        console.print(tabel_uang)

    except KeyError as e:
        console.print(f"\n>> Data tidak lengkap, kolom {e} tidak ditemukan.")
    except Exception as e:
        console.print(f"\n>> Terjadi kesalahan: {e}")
    finally:
        input("\nTekan Enter untuk kembali...")