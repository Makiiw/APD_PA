import os
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from data import simpan, data_tamu
from rich.console import Console
from rich.table import Table

console = Console()
baris = "=" * 60


def tampilan_kelola_tamu():
    while True:
        os.system("cls")
        print(baris)
        pilihan = inquirer.select(
<<<<<<< HEAD
            message="PILIHAN KELOLA TAMU: ",
            choices=[
                Choice(value=1, name="Tambah Tamu"),
                Choice(value=2, name="Tampil Data Tamu"),
                Choice(value=3, name="Ubah Data Tamu"),
                Choice(value=4, name="Hapus Data Tamu"),
                Choice(value=5, name="Kembali Ke Menu Admin"),
                Separator(baris),
            ],
=======
            message= "PILIHAN KELOLA KAMAR: ",
            choices = [
                    Choice(value= 1, name="Tambah Data Tamu"),
                    Choice(value=2, name="Tampil Data Tamu"),
                    Choice(value=3, name="Ubah Data Tamu"),
                    Choice(value=4, name="Hapus Data Tamu"),
                    Choice(value=5, name="Kembali Ke Menu Admin"),
                    Separator(baris)
                    ]
>>>>>>> 85dd5c940c4833ec2cf5c3fa1d828ceecb5ed424
        ).execute()
        if pilihan == 1:
            tambah_tamu()
        elif pilihan == 2:
            tampilkan_tamu()
        elif pilihan == 3:
            ubah_tamu()
        elif pilihan == 4:
            hapus_tamu()
        elif pilihan == 5:
            break


def tambah_tamu():
    os.system("cls")
    print(baris)
    print("TAMBAH TAMU".center(60))
    print(baris)
    try:
        id_tamu = input("Masukkan ID Tamu: ").strip().upper()
        nama_tamu = input("Masukkan Nama Tamu: ").strip().upper()
        no_hp = input("Masukkan No HP: ").strip()
        alamat = input("Masukkan Alamat: ").strip()

        if "" in (id_tamu, nama_tamu, no_hp, alamat):
            raise ValueError("Semua data wajib diisi.")
        if id_tamu in data_tamu:
            raise KeyError("ID tamu sudah terdaftar.")
        if not no_hp.isdigit():
            raise ValueError("No. HP harus berupa angka.")

        data_tamu[id_tamu] = {
            "id": id_tamu,
            "nama": nama_tamu,
            "hp": no_hp,
            "alamat": alamat,
        }
        simpan()
        print("\n>> Data tamu berhasil ditambahkan!")
    except ValueError as e:
        print(f"\n>> Input tidak valid: {e}")
    except KeyError as e:
        print(f"\n>> Gagal! {e.args[0]}")
    except KeyboardInterrupt:
        print("\n\n>> Input dibatalkan.")
    except Exception as e:
        print(f"\n>> Terjadi kesalahan: {e}")
    finally:
        input("\nTekan Enter untuk kembali...")


def tampilkan_tamu():
    os.system("cls")
    print(baris)
    print("DAFTAR TAMU".center(60))
    print(baris)
    try:
        if not data_tamu:
            raise LookupError("Data tamu masih kosong.")

        tabel = Table(title="Data Tamu Hotel", show_lines=True)
        tabel.add_column("No", justify="center")
        tabel.add_column("ID Tamu", justify="center")
        tabel.add_column("Nama")
        tabel.add_column("No. HP")
        tabel.add_column("Alamat")

        for no, (id_tamu, info) in enumerate(data_tamu.items(), start=1):
<<<<<<< HEAD
            tabel.add_row(str(no), id_tamu, info["nama"], str(info["hp"]), info["alamat"])

        console.print(tabel)
        console.print(f"\nTotal tamu: {len(data_tamu)}")
=======
            tabel.add_row(str(no), id_tamu, info["Nama"], str(info["NO. HP"]), info["Alamat"])

        console.print(tabel)
        console.print(f"\nTotal tamu: {len(data_tamu)}")

>>>>>>> 85dd5c940c4833ec2cf5c3fa1d828ceecb5ed424
    except LookupError as e:
        console.print(f"\n>> {e}")
    except KeyError as e:
        console.print(f"\n>> Data tamu tidak lengkap, kolom {e} tidak ditemukan.")
    except Exception as e:
        console.print(f"\n>> Terjadi kesalahan: {e}")
    finally:
        input("\nTekan Enter untuk kembali...")


def ubah_tamu():
    os.system("cls")
    print(baris)
    print("UBAH DATA TAMU".center(60))
    print(baris)
    try:
        id_tamu = input("Masukkan ID tamu yang diubah: ").strip().upper()
<<<<<<< HEAD
        tamu = data_tamu[id_tamu]

        print("\nKosongkan jika tidak diubah")
        nama = input(f"Nama [{tamu['nama']}]: ").strip().upper()
        hp = input(f"No. HP [{tamu['hp']}]: ").strip()
        alamat = input(f"Alamat [{tamu['alamat']}]: ").strip()

        if hp and not hp.isdigit():
            raise ValueError

        tamu["nama"] = nama or tamu["nama"]
        tamu["hp"] = hp or tamu["hp"]
        tamu["alamat"] = alamat or tamu["alamat"]
        simpan()
        print("\n>> Data tamu berhasil diubah!")
=======
        tamu = data_tamu[id_tamu]  # KeyError jika ID tidak ada

        print("\nKosongkan jika tidak diubah")
        nama = input(f"Nama [{tamu['Nama']}]: ").strip().upper()
        hp = input(f"No. HP [{tamu['NO. HP']}]: ").strip()
        alamat = input(f"Alamat [{tamu['Alamat']}]: ").strip().upper()

        # validasi dulu, jika salah belum ada data yang berubah
        hp_baru = int(hp) if hp else tamu["NO. HP"]
        if hp_baru <= 0:
            raise ValueError

        tamu["Nama"] = nama or tamu["Nama"]
        tamu["NO. HP"] = hp_baru
        tamu["Alamat"] = alamat or tamu["Alamat"]
        simpan()

        print("\n>> Data tamu berhasil diubah!")

>>>>>>> 85dd5c940c4833ec2cf5c3fa1d828ceecb5ed424
    except KeyError:
        print("\n>> ID tamu tidak ditemukan.")
    except ValueError:
        print("\n>> No. HP harus berupa angka.")
    finally:
        input("\nTekan Enter untuk kembali...")


def hapus_tamu():
    os.system("cls")
    print(baris)
    print("HAPUS DATA TAMU".center(60))
    print(baris)
    try:
        id_tamu = input("Masukkan ID tamu yang dihapus: ").strip().upper()
<<<<<<< HEAD
        tamu = data_tamu[id_tamu]

        print(f"\nNama   : {tamu['nama']}")
        print(f"No. HP : {tamu['hp']}")
        print(f"Alamat : {tamu['alamat']}")
=======
        tamu = data_tamu[id_tamu]  # KeyError jika ID tidak ada

        print(f"\nNama   : {tamu['Nama']}")
        print(f"No. HP : {tamu['NO. HP']}")
        print(f"Alamat : {tamu['Alamat']}")
>>>>>>> 85dd5c940c4833ec2cf5c3fa1d828ceecb5ed424

        konfirmasi = input("\nYakin ingin menghapus? (y/n): ").strip().lower()
        if konfirmasi == "y":
            del data_tamu[id_tamu]
            simpan()
            print("\n>> Data tamu berhasil dihapus!")
        else:
            print("\n>> Penghapusan dibatalkan.")
    except KeyError:
        print("\n>> ID tamu tidak ditemukan.")
    finally:
        input("\nTekan Enter untuk kembali...")
