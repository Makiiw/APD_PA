import os
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from autentikasi import admin,user, register
from admin import menu_admin
from colorama import Fore
from user import menu_user
import pwinput



def menu_utama():
    while True:
        os.system("cls")
        baris = ("=" * 60)
        print (baris)
        print ("H O T E L M A N A G E".center(60))
        print ("Sistem Reservasi Hotel".center(60))
        print (baris)
        pilihan = inquirer.select(
            message= "PILIHAN MENU: ",
            choices=[
                    Choice(value=1, name="[1] Masuk Sebagai Admin"),
                    Choice(value=2, name="[2] Masuk Sebagai Pengguna"),
                    Choice(value=3, name="[3] Registrasi Akun Baru"),
                    Choice(value=4, name ="[4] Keluar"),
                    Separator(baris),
                    ],
            qmark="",
            long_instruction="↑↓ pilih  •  Enter konfirmasi",
        ).execute()
        print (baris)
        
        if pilihan == 1:
                os.system("cls")
                nama = input("Masukkan Username: ").strip()
                sandi = pwinput.pwinput("Masukkan Password: ").strip()
                try:
                    akun = admin(nama, sandi)   
                    print(f"Login berhasil! Selamat datang".center(60))
                    menu_admin()
                except ValueError as e:
                    input(str(e) + "\nTekan Enter untuk melanjutkan...")
                    
        elif pilihan == 2:
                os.system("cls")
                nama = input("Masukkan Username: ").strip()
                sandi = pwinput.pwinput("Masukkan Password: ").strip()
                try:
                    username = user(nama, sandi)
                    print("Login berhasil".center(60))
                    menu_user(username)
                except ValueError as e:
                    input(str(e) + "\nTekan Enter untuk melanjutkan...")
                    
        elif pilihan == 3:
                os.system("cls")
                try:
                    register()
                except ValueError as e:
                    input(str(e) + "\nTekan Enter untuk melanjutkan...")
                    menu_utama()
                    
        elif pilihan == 4:
                exit()
        else:
                print("Pilihan tidak valid. Silakan coba lagi.")
                        

if __name__ == "__main__":
    menu_utama()
