import json
from datetime import datetime
from pathlib import Path

FILE = Path(__file__).with_name("data_user_dan_kamar.json")

with FILE.open("r", encoding="utf-8") as f:
    data = json.load(f)

admin = data["admin"]
user = data["user"]
data_kamar = data["data_kamar"]
data_tamu = data["data_tamu"]
data_reservasi = data["data_reservasi"]
data_pengumuman = data["data_pengumuman"]

def simpan():
    with FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


FORMAT_TANGGAL = "%d-%m-%Y"

def cari_tamu(username):
    for id_tamu, t in data_tamu.items():
        if t.get("username") == username:
            return id_tamu, t
    return None, None

def buat_id_tamu():
    angka = [int(k) for k in data_tamu if k.isdigit()]
    nomor = max([data.get("id_tamu_terakhir", 0)] + angka) + 1
    data["id_tamu_terakhir"] = nomor
    return str(nomor)

def buat_profil_tamu(username):
    id_tamu, tamu = cari_tamu(username)
    if tamu:
        return id_tamu
    id_tamu = buat_id_tamu()
    data_tamu[id_tamu] = {
        "ID TAMU": id_tamu,
        "username": username,
        "Nama": username.upper(),
        "NO. HP": "",
        "Alamat": ""
    }
    return id_tamu

def profil_lengkap(tamu):
    return bool(str(tamu.get("NO. HP", "")).strip()) and bool(str(tamu.get("Alamat", "")).strip())

def kamar_bentrok(nomor, masuk, keluar):
    for r in data_reservasi.values():
        if r.get("kamar") != nomor or r.get("status", "MENUNGGU KONFIRMASI") in ("SELESAI", "DIBATALKAN"):
            continue
        r_masuk = datetime.strptime(r["checkin"], FORMAT_TANGGAL)
        r_keluar = datetime.strptime(r["checkout"], FORMAT_TANGGAL)
        if masuk < r_keluar and keluar > r_masuk:
            return True
    return False

def sinkron_status_kamar(nomor):
    kamar = data_kamar.get(nomor)
    if not kamar or kamar["status"] == "PERBAIKAN":
        return
    aktif = [
        r.get("status", "MENUNGGU KONFIRMASI") for r in data_reservasi.values()
        if r.get("kamar") == nomor and r.get("status", "MENUNGGU KONFIRMASI") not in ("SELESAI", "DIBATALKAN")
    ]
    if "CHECK-IN" in aktif:
        kamar["status"] = "TERISI"
    elif aktif:
        kamar["status"] = "DIPESAN"
    else:
        kamar["status"] = "TERSEDIA"
