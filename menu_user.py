import os
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
os.system("cls")

def menu_user():
    while True:
        os.system("cls")
        baris = ("=" * 60)
        print (baris)
        print ("SELAMAT DATANG DI MENU ADMIN")
        print (baris)

        pilihan = inquirer.select(
            message= "PILIHAN YANG TERSEDIA: ",
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
                os.system("cls")
                print (baris)
                print ("Informasi Dan Fasilitas Kamar".center(60))
                print (baris)
                os.system("pause")

        elif pilihan == 2:
            os.system("cls")
            print (baris)
            print ("Ketersediaan Kamar".center(60))
            print (baris)
            os.system("pause")

        elif pilihan == 3:
            os.system("cls")
            print (baris)
            print ("Detail Dan Status Reservasi".center(60))
            print (baris)
            os.system("pause")

        elif pilihan == 4:
            os.system("cls")
            print (baris)
            print ("Informasi Dan Riwayat Pembayaran".center(60))
            print (baris)
            os.system("pause")

        elif pilihan == 5:
            os.system("cls")
            print (baris)
            print ("Pengumuman Hotel".center(60))
            print (baris)
            os.system("pause")

        elif pilihan == 6:
            os.system("cls")
            print (baris)
            print ("Reservasi Kamar".center(60))
            print (baris)
            os.system("pause")

        elif pilihan == 7:
            return

        else:
            print ("Pilihan Tidak Valid. Masukkan Angka 1-7.".center(60))