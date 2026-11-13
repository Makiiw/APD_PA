import os
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
baris = ("=" * 60)

def tampilan_kelola_kamar():
    os.system("cls")
    print (baris)
    pilihan = inquirer.select(
        message= "PILIHAN KELOLA KAMAR: ",
        choices = [
                   Choice(value= 1, name="Tambah Kamar"),
                   Choice(value=2, name="Tampil Data Kamar"),
                   Choice(value=3, name="Ubah Data Kamar"),
                   Choice(value=4, name="Hapus Data Kamar"),
                   Choice(value=5, name="Kembali Ke Menu Admin"),
                   Separator(baris)
                  ]
    ).execute()
    
    if pilihan == 1:
        tambah_kamar()

def tambah_kamar():
    os.system("cls")
    print (baris)
    print ("TAMBAH KAMAR".center(60))
    print (baris)
    nomor_kamar = input ("Nomor Kamar: ").upper()
    tipe_kamar = input ("Tipe Kamar: ").upper()
    fasilitas_kamar = input ("Fasilitas: ").upper()
    harga_kamar = input ("Harga per malam: ").upper()
    status_kamar = input ("Status :").upper().upper()

tampilan_kelola_kamar()