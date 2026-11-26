import os
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
import fitur_user as user

def menu_user(username):
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        baris = ("=" * 60)
        print (baris)
        print ("HotelManage - Reservasi Hotel".center(60))
        print (baris)

        pilihan = inquirer.select(
            message= "PILIHAN MENU: ",
            choices=[
                    Choice(value=1, name="- Informasi Dan Fasilitas Kamar"),
                    Choice(value=3, name="- Detail Dan Status Reservasi"),
                    Choice(value=4, name ="- Informasi Dan Riwayat Pembayaran"),
                    Choice(value=5, name ="- Pengumuman Hotel"),
                    Choice(value=6, name ="- Reservasi Kamar"),
                    Choice(value=7, name ="- ubah Data Diri"),
                    Choice(value=8, name ="- logout"),
                    Separator(baris),
                ],
        ).execute()
        print (baris)

        if pilihan == 1:
            user.tampilkan_kamar()
        elif pilihan == 3:
            user.reservasi_saya(username)
        elif pilihan == 4:
            user.riwayat_pembayaran(username)
        elif pilihan == 5:
           user.pengumuman_hotel()
        elif pilihan == 6:
          user.reservasi_kamar(username)
        elif pilihan == 7:
         user.ubah_profil(username)
        elif pilihan == 8:
            return
        else:
            print ("Pilihan Tidak Valid. Masukkan Angka 1-8.".center(60))

if __name__ == "__main__":
    menu_user("tes")