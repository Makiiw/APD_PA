import json
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


def cari_tamu(username):
    for id_tamu, t in data_tamu.items():
        if t.get("username") == username:
            return id_tamu, t
    return None, None

def buat_id_tamu():
    angka = [int(k) for k in data_tamu if k.isdigit()]
    return str(max(angka, default=0) + 1)

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
