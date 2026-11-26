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
        
