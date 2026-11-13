import pwinput
from colorama import Fore
import Data

def login(user, pass):

def register():
    username_baru = input("Masukkan Username baru   : ").strip()
    password_baru = pwinput.pwinput("Masukkan Password baru   : ").strip()
    Data.users[username_baru] = password_baru
    print(Fore.GREEN + "Registrasi berhasil!" + Fore.RESET)