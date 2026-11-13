import os
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
os.system("cls")
baris = ("=" * 60)
print (baris)
print ("HotelManage - Reservasi Hotel".center(60))
print (baris)

pilihan = inquirer.select(
    message= "PILIHAN MENU: ",
    choices=[
            Choice(value=1, name="- Informasi Dan Fasilitas Kamar"),
            Choice(value=2, name="- Ketersediaan Kamar"),
            Choice(value=3, name="- Detail Dan Status Reservasi"),
            Choice(value=4, name ="- Informasi Dan Riwayat Pembayaran"),
            Choice(value=5, name ="- Pengumuman Hotel"),
            Choice(value=6, name ="- Reservasi Kamar"),
            Choice(value=7, name ="- logout"),
            Separator(baris),
        ],
).execute()
print (baris)

if pilihan == 1:
        print ("Anda memilih Informasi Dan Fasilitas Kamar".center(60))

elif pilihan == 2:
    print ("Anda memilih Ketersediaan Kamar".center(60))

elif pilihan == 3:
    print ("Anda memilih Detail Dan Status Reservasi".center(60))

elif pilihan == 4:
    print ("Anda memilih Informasi Dan Riwayat Pembayaran".center(60))

elif pilihan == 5:
    print ("Anda memilih Pengumuman Hotel".center(60))

elif pilihan == 6:
    print ("Anda memilih Reservasi Kamar".center(60))

elif pilihan == 7:
    exit()

else:
    print ("Pilihan Tidak Valid. Masukkan Angka 1-7.".center(60))

# Part 1
