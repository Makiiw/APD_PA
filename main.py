
import os
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from autentikasi import login, register
from colorama import Fore

os.system("cls")
baris = ("=" * 60)
print (baris)
print ("HotelManage - Reservasi Hotel".center(60))
print (baris)

def menu_utama():
    while True:
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

        if pilihan == "1":
                    nama = input("Masukkan Username: ").strip()
                    sandi = input("Masukkan Password: ").strip()
                    try:
                        akun = admin(nama, sandi)   
                        print(f"Login berhasil! Selamat datang, {akun[2]}!")
                    except ValueError as e:
                        print(e)

            elif pilihan == "2":
                    nama = input("Masukkan Username: ").strip()
                    sandi = input("Masukkan Password: ").strip()
                    try:
                        akun = user(nama, sandi)
                        print(f"Login berhasil! Selamat datang, {akun[2]}!")
                    except ValueError as e:
                        print(e)

            elif pilihan == "3":
                    print("Terima kasih telah menggunakan program ini. Sampai jumpa!")
                    break

            else:
                print("Pilihan tidak valid. Silakan coba lagi.")
                

                elif pilihan == 3:
                    print ("Silahkan Registrasi Akun".center(60))
                    register()


                elif pilihan == 4:
                    exit()

menu_utama()
