import os
import data
import pwinput


def admin(nama, sandi):
    os.system("cls")
    user_ada = False
    pass_ada = False
    for akun in data.admin:
        if akun[0] == nama:
            user_ada = True
        if akun[1] == sandi:
            pass_ada = True
        if akun[0] == nama and akun[1] == sandi:
            return akun
    if nama == "" and sandi =="":
        raise ValueError("Username dan Password tidak boleh kosong!")
    elif nama == "":
        raise ValueError("Username tidak boleh kosong!")
    elif sandi == "":
        raise ValueError("Password tidak boleh kosong!")
    elif not user_ada and not pass_ada:
        raise ValueError("Username dan Password salah!")
    elif not user_ada:
        raise ValueError("Username salah!")
    raise ValueError("Password salah!")

def user(nama, sandi):
    os.system("cls")
    user_ada = False
    pass_ada = False
    for akun in data.user:
        if akun[0] == nama:
            user_ada = True
        if akun[1] == sandi:
            pass_ada = True
        if akun[0] == nama and akun[1] == sandi:
            return nama
    if nama == "" and sandi =="":
        raise ValueError("Username dan Password tidak boleh kosong!")
    elif nama == "":
        raise ValueError("Username tidak boleh kosong!")
    elif sandi == "":
        raise ValueError("Password tidak boleh kosong!")
    elif not user_ada and not pass_ada:
        raise ValueError("Username dan Password salah!")
    elif not user_ada:
        raise ValueError("Username salah!")
    raise ValueError("Password salah!")

def register():
    os.system("cls")
    username_baru = input("Masukkan Username Baru: ").strip()
    password_baru = pwinput.pwinput("Masukkan Password Baru: ").strip()
    for akun in data.admin + data.user:
        if akun[0] == username_baru:
            raise ValueError("Username sudah digunakan, Silahkan gunakan username lain!")
    data.user.append([username_baru, password_baru, "User"])
    data.simpan()
    print("Register berhasil!")