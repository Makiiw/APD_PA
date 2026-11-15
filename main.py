
import os
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from autentikasi import admin,user, register
from admin import menu_admin
from colorama import Fore
from menu_user import menu_user


while True:
    os.system("cls")
    baris = ("=" * 60)
    print (baris)
    print ("HotelManage - Reservasi Hotel".center(60))
    print (baris)
    def menu_utama():
            pilihan = inquirer.select(
                message= "PILIHAN MENU: ",
                choices=[
                        Choice(value=1, name="- Admin"),
                        Choice(value=2, name="- Pengguna"),
                        Choice(value=3, name="- Registrasi"),
                        Choice(value=4, name ="- Exit"),
                        Separator(baris),
                    ],
            ).execute()
            print (baris)

            if pilihan == 1:
                os.system("cls")
                nama = input("Masukkan Username: ").strip()
                sandi = input("Masukkan Password: ").strip()
                try:
                    akun = admin(nama, sandi)   
                    print(f"Login berhasil! Selamat datang".center(60))
                    menu_admin()
                except ValueError as e:
                            print(e)

            elif pilihan == 2:
                os.system("cls")
                nama = input("Masukkan Username: ").strip()
                sandi = input("Masukkan Password: ").strip()
                try:
                    akun = user(nama, sandi)
                    print(f"Login berhasil! Selamat datang".center(60))
                    menu_user()
                except ValueError as e:
                    print(e)

            elif pilihan == 3:
                    os.system("cls")
                    register()
                    menu_utama()

            elif pilihan == 4:
                exit()

            else:
                print("Pilihan tidak valid. Silakan coba lagi.")
                    
    menu_utama()
