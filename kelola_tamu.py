import os
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from data import simpan, data_tamu
from rich.console import Console
from rich.table import Table
console = Console()
baris = ("=" * 60)

def tampilan_kelola_tamu():
    while True:
        os.system("cls")
        print (baris)
        pilihan = inquirer.select(
            message= "PILIHAN KELOLA TAMU: ",
            choices = [
                    Choice(value= 1, name="Tambah Data Tamu"),
                    Choice(value=2, name="Tampil Data Tamu"),
                    Choice(value=3, name="Ubah Data Tamu"),
                    Choice(value=4, name="Hapus Data Tamu"),
                    Choice(value=5, name="Kembali Ke Menu Admin"),
                    Separator(baris)
                    ]
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
            id_tamu = input("Masukan Id Tamu: ").strip().upper()
            nama_tamu = input("Masukan Nama Tamu: ").strip().upper()
            no_hp = input("Masukan No HP: ").strip()
            alamat = input("Masukan Alamat: ").strip()
            
            if "" in (id_tamu, nama_tamu, no_hp, alamat):
                raise ValueError("Semua data wajib diisi.")
            if id_tamu in data_tamu:
                raise KeyError(f"ID tamu {id_tamu} sudah terdaftar.")
            if not no_hp.isdigit():
                raise ValueError("No. HP harus berupa angka.")
            data_tamu[id_tamu] = {
                "ID TAMU": id_tamu,
                "Nama": nama_tamu,
                "NO. HP": no_hp,
                "Alamat": alamat
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
        
        nomor = 0
        dilewati = 0
        for id_tamu, info in data_tamu.items():
            try:
                nama = info["Nama"]
                hp = str(info["NO. HP"])
                alamat = str(info["Alamat"])
            except (KeyError, TypeError):
                dilewati += 1
                continue
            nomor += 1
            tabel.add_row(str(nomor), id_tamu, nama, hp, alamat)
            
        console.print(tabel)
        console.print(f"\nTotal tamu: {nomor}")
        if dilewati:
            console.print(
                f">> {dilewati} data dilewati karena formatnya tidak lengkap.",
                markup=False,
            )
            
    except LookupError as e:
        console.print(f"\n>> {e}", markup=False)
    except Exception as e:
        console.print(f"\n>> Terjadi kesalahan: {e}", markup=False)
    finally:
        input("\nTekan Enter untuk kembali...")


def ubah_tamu():
    os.system("cls")
    print(baris)
    print("UBAH DATA TAMU".center(60))
    print(baris)
    try:
        id_tamu = input("Masukkan ID tamu yang diubah: ").strip().upper()
        tamu = data_tamu[id_tamu]  

        print("\nKosongkan jika tidak diubah")
        nama = input(f"Nama [{tamu['Nama']}]: ").strip().upper()
        hp = input(f"No. HP [{tamu['NO. HP']}]: ").strip()
        alamat = input(f"Alamat [{tamu['Alamat']}]: ").strip()

        if hp and not hp.isdigit():
            raise ValueError
        hp_baru = hp if hp else str(tamu["NO. HP"])

        tamu["Nama"] = nama or tamu["Nama"]
        tamu["NO. HP"] = hp_baru
        tamu["Alamat"] = alamat or tamu["Alamat"]
        simpan()

        print("\n>> Data tamu berhasil diubah!")

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
        tamu = data_tamu[id_tamu]  # KeyError jika ID tidak ada

        print(f"\nNama   : {tamu['Nama']}")
        print(f"No. HP : {tamu['NO. HP']}")
        print(f"Alamat : {tamu['Alamat']}")

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
