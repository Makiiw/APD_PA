import os
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from kelola import tampilan_kelola_kamar, tambah_kamar, tampilkan_kamar
from kelola_tamu import tampilan_kelola_tamu
baris = ("=" * 60)


def menu_admin():
        while True:
                print (baris)
                print ("SELAMAT DATANG DI MENU ADMIN".center(60))
                print (baris)
                pilihan = inquirer.select(
                message= "PILIHAN YANG TERSEDIA: ",
                choices= [Choice(value = 1, name = "- Kelola Data Kamar"),
                        Choice(value = 2, name = "- Kelola Data Tamu"),
                        Choice(value = 3, name = "- Kelola Reservasi"),
                        Choice(value = 4, name = "- Kelola Pembayaran"),
                        Choice(value = 5, name = "- Rekaputulasi"),
                        Choice(value = 6, name = "- Kelola Pengumuman"),
                        Choice(value = 7, name = "- Balik Ke Menu Utama"),
                        Separator(baris)
                        ]
                ).execute()


                if pilihan == 1:
                        tampilan_kelola_kamar()
                elif pilihan == 2:
                        tampilan_kelola_tamu()
                elif pilihan == 3:
                        print (baris)
                        print ("Kelola Reservasi")
                elif pilihan == 4:
                        print (baris)
                        print ("Kelola Pembayaran")
                elif pilihan == 5:
                        print (baris)
                        print ("Rekaputulasi")
                elif pilihan == 6:
                        print ("Kelola Pengumuman")
                elif pilihan == 7:
                        return
                
