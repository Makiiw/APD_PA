
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
            Choice(value=1, name="- Admin"),
            Choice(value=2, name="- Pengguna"),
            Choice(value=3, name="- Registrasi"),
            Choice(value=4, name ="- Exit"),
            Separator(baris),
        ],
).execute()
print (baris)

if pilihan == 1:
        print ("Anda memilih login sebagai Admin".center(60))
        username = input("Masukan username: ")
        password = input("Masukan password: ")
    
elif pilihan == 2:
    print ("Anda memilih login sebagai Pengguna".center(60))
    username = input("Masukan username: ")
    password = input("Masukan password: ")

elif pilihan == 3:
    print ("Silahkan Registrasi Akun".center(60))


elif pilihan == 4:
    exit()


