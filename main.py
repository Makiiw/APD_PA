from autentikasi import admin, user



print("Selamat datang di program login!")
while True:
    print("\nMenu:")
    print("1. admin")
    print("2. user")
    print("3. Keluar")
    pilihan = input("Pilih menu (1/2/3): ").strip()

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