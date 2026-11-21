import os
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from kelola import tampilan_kelola_kamar
from kelola_tamu import tampilan_kelola_tamu
from kelola_reservasi import tampilan_kelola_reservasi
from kelola_pembayaran import tampilan_kelola_pembayaran
from rekaputulasi import rekaputulasi
from kelola_pengumuman import tampilan_kelola_pengumuman
baris = ("=" * 60)


def menu_admin():
        while True:
                os.system("cls")
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
                        break
                elif pilihan == 3:
                        tampilan_kelola_reservasi()
                elif pilihan == 4:
                        tampilan_kelola_pembayaran()
                elif pilihan == 5:
                        rekaputulasi()
                elif pilihan == 6:
                        tampilan_kelola_pengumuman()
                elif pilihan == 7:
                        break
                
