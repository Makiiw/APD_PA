import json
FILE = "data_user_dan_kamar.json"

with open(FILE, "r") as f:
    data = json.load(f)

admin = data["admin"]
user = data["user"]
data_kamar = data["data_kamar"]
data_tamu = data["data_tamu"]
data_reservasi = data["data_reservasi"]
data_pengumuman = data["data_pengumuman"]

def simpan():
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)
        
