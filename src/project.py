import MySQLdb as db
import os
from tabulate import tabulate
from termcolor import colored
from rich.panel import Panel
from rich.console import Console
from datetime import datetime
from colorama import Fore, Back, Style, init
from pyfiglet import Figlet
from time import sleep
from rich import print as rprint

console = Console()

# =========================== LOGIN ============================================
def animasi_masuk():
    with console.status("[cyan bold]Sedang LOGIN....."):
        connection = None
        for i in range(100):
            connection = db.connect(host='127.0.0.1', user='root', passwd='', db='toko_buku')
            console.print(f"[progress({i + 1}/100)]", end='\r')
            sleep(0.02)

    return connection

# ======================= BANNER TOKO =========================================
def create_and_display_colored_ascii_art(text="toko buku tengah malam", font='graffiti', color=Fore.RED):
    figlet = Figlet(font=font)
    ascii_art = figlet.renderText(text)
    colored_ascii_art = f"{Style.BRIGHT}{color}" + ascii_art + Style.RESET_ALL
    print(f"\n{colored_ascii_art}")

    # colored_ascii_art = color + ascii_art
    # print(f"\n{colored_ascii_art}")

# ============================= INSERT DATA =====================================
def insert_data_barang(connection):
    cursor = connection.cursor()
    cursor.execute("DESCRIBE barang")
    columns = [column[0] for column in cursor.fetchall()]
    
    while True:
        data_values = []
        for column in columns:
            value = console.input(f"[bold white]masukkan nilai untuk kolom[bold white] [bold green]{column}[bold green] [bold white](ketik[bold white] [bold red]n[bold red] [bold white]jika selesai): [bold white]")
            if value.lower() == 'n':
                break
            data_values.append(value)

        try:
            if data_values:
                insert_data_query = f"INSERT INTO barang ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(data_values))})"
                cursor.execute(insert_data_query, tuple(data_values))
                connection.commit()
                console.print("[bold blue]Data berhasil ditambahkan.")
            else:
                console.print("[bold blue]Penambahan data dibatalkan.")
        except Exception as e:
            console.print(f"[bold white]Terjadi kesalahan: [bold red]{e}")
            connection.rollback()

        if not data_values or value.lower() == 'n':
            break

def insert_data_pegawai(connection):
    cursor = connection.cursor()
    cursor.execute("DESCRIBE pegawai")
    columns = [column[0] for column in cursor.fetchall()]
    
    while True:
        data_values = []
        for column in columns:
            value = console.input(f"[bold white]masukkan nilai untuk kolom[bold white] [bold green]{column}[bold green] [bold white](ketik[bold white] [bold red]n[bold red] [bold white]jika selesai): [bold white]")
            if value.lower() == 'n':
                break
            data_values.append(value)

        try:
            if data_values:
                insert_data_query = f"INSERT INTO pegawai ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(data_values))})"
                cursor.execute(insert_data_query, tuple(data_values))
                connection.commit()
                console.print("[bold blue]Data berhasil ditambahkan.")
            else:
                console.print("[bold blue]Penambahan data dibatalkan.")
        except Exception as e:
            console.print(f"[bold white]Terjadi kesalahan: [bold red]{e}")
            connection.rollback()

        if not data_values or value.lower() == 'n':
            break

# ======================================= UPDATE DATA ======================================
def update_data_barang(connection):
    cursor = connection.cursor()
    cursor.execute("DESCRIBE barang")
    columns = [column[0] for column in cursor.fetchall()]

    tujuan = console.input("[bold white]Masukkan ID yang ingin diupdate: ")
    
    update_values = {}
    for column in columns:
        value = console.input(f"[bold white]Masukkan nilai baru untuk kolom[bold white] [bold green]{column}[bold green] [bold white](tekan[bold white] [bold red]Enter[bold red] [bold white]jika tidak ingin mengubah): [bold white]")
        if value:
            update_values[column] = value

    try:
        if update_values:
            update_query = f"UPDATE barang SET {', '.join([f'{column} = %s' for column in update_values.keys()])} WHERE buku_id = %s"
            cursor.execute(update_query, tuple(update_values.values()) + (tujuan,))
            connection.commit()
            console.print("[bold blue]Data berhasil diupdate.")
        else:
            console.print("[bold blue]Tidak ada perubahan dilakukan.")
    except Exception as e:
        console.print(f"[bold white]Terjadi kesalahan: [bold red]{e}")
        connection.rollback()

def update_data_pegawai(connection):
    cursor = connection.cursor()
    cursor.execute("DESCRIBE pegawai")
    columns = [column[0] for column in cursor.fetchall()]

    tujuan = console.input("[bold white]Masukkan ID yang ingin diupdate: ")
    
    update_values = {}
    for column in columns:
        value = console.input(f"[bold white]Masukkan nilai baru untuk kolom[bold white] [bold green]{column}[bold green] [bold white](tekan[bold white] [bold red]Enter[bold red] [bold white]jika tidak ingin mengubah): [bold white]")
        if value:
            update_values[column] = value

    try:
        if update_values:
            update_query = f"UPDATE pegawai SET {', '.join([f'{column} = %s' for column in update_values.keys()])} WHERE pegawai_id = %s"
            cursor.execute(update_query, tuple(update_values.values()) + (tujuan,))
            connection.commit()
            console.print("[bold blue]Data berhasil diupdate.")
        else:
            console.print("[bold blue]Tidak ada perubahan dilakukan.")
    except Exception as e:
        console.print(f"[bold white]Terjadi kesalahan: [bold red]{e}")
        connection.rollback()
# =========================== DELETE DATA =======================================
def delete_data_barang(connection):
    cursor = connection.cursor()
    cursor.execute("DESCRIBE barang")
    columns = [column[0] for column in cursor.fetchall()]

    console.print("[bold white]Pilih kolom untuk dihapus:")
    for i, column in enumerate(columns, 1):
        print(f"{i}. {column}")

    # Memilih kolom untuk dihapus
    try:
        selected_index = int(console.input("[bold white]Masukkan nomor kolom: ")) - 1
        if selected_index < 0 or selected_index >= len(columns):
            console.print("[bold blue]Nomor kolom tidak valid.")
            return
    except ValueError:
        console.print("[bold blue]Masukkan nomor yang valid.")
        return

    selected_column = columns[selected_index]
    
    # Memasukkan nilai untuk kondisi penghapusan
    tujuan = console.input(f"[bold white]Masukkan nilai kolom[bold white] [bold green]{selected_column}[bold green] [bold white]yang ingin dihapus: [bold white]")

    try:
        delete_query = f"DELETE FROM barang WHERE {selected_column} = %s"
        cursor.execute(delete_query, (tujuan,))
        connection.commit()
        console.print("[bold blue]Data berhasil dihapus.")
    except Exception as e:
        console.print(f"[bold white]Terjadi kesalahan: [bold red]{e}")
        connection.rollback()

def delete_data_pegawai(connection):
    cursor = connection.cursor()
    cursor.execute("DESCRIBE pegawai")
    columns = [column[0] for column in cursor.fetchall()]

    console.print("[bold white]Pilih kolom untuk dihapus:")
    for i, column in enumerate(columns, 1):
        print(f"{i}. {column}")

    # Memilih kolom untuk dihapus
    try:
        selected_index = int(console.input("[bold white]Masukkan nomor kolom: ")) - 1
        if selected_index < 0 or selected_index >= len(columns):
            console.print("[bold blue]Nomor kolom tidak valid.")
            return
    except ValueError:
        console.print("[bold blue]Masukkan nomor yang valid.")
        return

    selected_column = columns[selected_index]
    
    # Memasukkan nilai untuk kondisi penghapusan
    tujuan = console.input(f"[bold white]Masukkan nilai kolom[bold white] [bold green]{selected_column}[bold green] [bold white]yang ingin dihapus: [bold white]")

    try:
        delete_query = f"DELETE FROM pegawai WHERE {selected_column} = %s"
        cursor.execute(delete_query, (tujuan,))
        connection.commit()
        console.print("[bold blue]Data berhasil dihapus.")
    except Exception as e:
        console.print(f"[bold white]Terjadi kesalahan: [bold red]{e}")
        connection.rollback()
# ===================================== MENU STOK ===========================================
def barang(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM barang")
    stok_data = cursor.fetchall()
    stok_header = ["Buku ID", "Nama Buku", "Type Buku", "Stok Barang", "Harga"]
    
    colored_stok_data = []
    for row in stok_data:
        colored_row = []
        for i, value in enumerate(row):
            if i == 3 and value == 0:
                colored_row.append(colored(value, 'red'))
            elif i == 3 and 0 < value <= 5:
                colored_row.append(colored(value, 'yellow'))
            elif i == 3 and value > 5:
                colored_row.append(colored(value, 'green'))
            else:
                colored_row.append(value)
        colored_stok_data.append(colored_row)

    print(tabulate(colored_stok_data, headers=stok_header, tablefmt="rounded_outline"))

    while True:
        menu_items = """
[bold white][[bold cyan]1[/][bold white]][/] [bold green]Insert Data[bold white] [/]
[bold white][[bold cyan]2[/][bold white]][/] [bold green]Update Data[bold white] [/]
[bold white][[bold cyan]3[/][bold white]][/] [bold green]Delete Data[bold white] [/]
[bold white][[bold cyan]0[/][bold white]][/] [bold green]Kembali ke Menu Utama[bold white]
"""
        panel_obj = Panel(menu_items, width=30, style="bold white", title="[bold green]Menu Stok")
        console.print(panel_obj)

        pilihan = console.input(f' [bold white][[bold cyan]+[/][bold white]][/] [bold white]Masukkan pilihan : ')

        if pilihan == "1":
            insert_data_barang(connection)
        elif pilihan == "2":
            update_data_barang(connection)
        elif pilihan == "3":
            delete_data_barang(connection)
        elif pilihan == "0":
            daftar_menu(connection)
        else:
            console.print("[bold blue]Pilihan tidak valid")
        break
    daftar_menu(connection)

# ================================ MENU PEGAWAI ==============================================
def pegawai(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM pegawai")
    pegawai_data = cursor.fetchall()
    pegawai_headers = ["Pegawai ID", "Nama Pegawai", "Alamat", "No.Hp"]
    print(tabulate(pegawai_data, headers=pegawai_headers, tablefmt="rounded_outline"))

    while True:
        menu_items = """
[bold white][[bold cyan]1[/][bold white]][/] [bold green]Insert Data[bold white] [/]
[bold white][[bold cyan]2[/][bold white]][/] [bold green]Update Data[bold white] [/]
[bold white][[bold cyan]3[/][bold white]][/] [bold green]Delete Data[bold white] [/]
[bold white][[bold cyan]0[/][bold white]][/] [bold green]Kembali ke Menu Utama[bold white]
"""
        panel_obj = Panel(menu_items, width=30, style="bold white", title="[bold green]Menu Stok")
        console.print(panel_obj)

        pilihan = console.input(f' [bold white][[bold cyan]+[/][bold white]][/] [bold white]Masukkan pilihan : ')

        if pilihan == "1":
            insert_data_pegawai(connection)
        elif pilihan == "2":
            update_data_pegawai(connection)
        elif pilihan == "3":
            delete_data_pegawai(connection)
        elif pilihan == "0":
            daftar_menu(connection)
        else:
            console.print("[bold blue]Pilihan tidak valid")
        break
    daftar_menu(connection)

# ================================ MENU PEMBELI ========================================
def pembeli(connection):
    cursor = connection.cursor()

    # Fetch distinct book types
    cursor.execute("SELECT DISTINCT type_buku FROM barang")
    book_types = [row[0] for row in cursor.fetchall()]

    # Display available book types
    console.print("[bold white]Pilih Type Buku:")
    for i, book_type in enumerate(book_types, 1):
        console.print(f"[bold blue]{i}. [bold green]{book_type}")

    # Input book type choice
    try:
        selected_types_input = console.input("[bold white]Masukkan nomor type buku (pisahkan dengan koma): ")
        selected_type_indices = [int(index.strip()) - 1 for index in selected_types_input.split(',')]
        
        invalid_indices = [index for index in selected_type_indices if index < 0 or index >= len(book_types)]
        if invalid_indices:
            console.print("[bold blue]Nomor type buku tidak valid.")
            return
    except ValueError:
        console.print("[bold blue]Masukkan nomor yang valid.")
        return

    selected_types = [book_types[index] for index in selected_type_indices]


    # Fetch books with positive stock for selected types
    placeholders = ', '.join(['%s'] * len(selected_types))
    query = f"SELECT * FROM barang WHERE type_buku IN ({placeholders}) AND stok_buku > 0"
    cursor.execute(query, tuple(selected_types))
    stok_data = cursor.fetchall()
    stok_header = ["Buku ID", "Nama Buku", "Type Buku", "Stok Barang", "Harga"]

    if not stok_data:
        console.print("[bold blue]Stok buku kosong. Silakan pilih buku lain.")
        return

    colored_stok_data = []
    for row in stok_data:
        colored_row = []
        for i, value in enumerate(row):
            if i == 3 and value == 0:
                colored_row.append(colored(value, 'red'))
            elif i == 3 and 0 < value <= 5:
                colored_row.append(colored(value, 'yellow'))
            elif i == 3 and value > 5:
                colored_row.append(colored(value, 'green'))
            else:
                colored_row.append(value)
        colored_stok_data.append(colored_row)

    print(tabulate(colored_stok_data, headers=stok_header, tablefmt="rounded_outline"))

    struk_pembelian = []

    # Input data pembeli
    nama_pembeli = console.input("[bold white]Masukkan nama pembeli: ")
    alamat_pembeli = console.input("[bold white]Masukkan alamat pembeli: ")  # Add this line to get the address

    # Insert data into pembeli table
    cursor.execute("INSERT INTO pembeli (nama_pembeli, alamat) VALUES (%s, %s)", (nama_pembeli, alamat_pembeli))
    id_pembeli = cursor.lastrowid  # Get the last inserted ID

    while True:
        nama_buku = console.input("[bold white]Masukkan nama buku yang dibeli : ")

        # Fetch book with positive stock
        cursor.execute("SELECT stok_buku, harga FROM barang WHERE nama_buku = %s AND stok_buku > 0 LIMIT 1", (nama_buku,))
        book_info = cursor.fetchone()

        if not book_info:
            console.print(f"[bold white]Maaf, buku dengan nama[bold white] [bold green]{nama_buku}[bold green] [bold white]tidak ditemukan atau stok kosong.")
            return

        stok_buku, harga_per_buku = book_info

        jumlah_buku = int(console.input("[bold white]Masukkan jumlah buku yang dibeli: "))

        if jumlah_buku > stok_buku:
            console.print(f"[bold blue]Maaf, stok buku tidak mencukupi untuk jumlah yang diminta.")
            continue

        # Menghitung total harga
        total_harga = jumlah_buku * harga_per_buku

        # Menambah pembelian ke struk
        struk_pembelian.append({
            "Nama Pembeli": nama_pembeli,
            "Buku Dibeli": [{
                "Nama Buku": nama_buku,
                "Jumlah Buku": jumlah_buku,
                "Harga per Buku": harga_per_buku,
                "Total Harga": total_harga
            }],
        })

        lanjut_beli = console.input("[bold white]Ingin beli buku lagi? [bold green](y/n): ")
        if lanjut_beli.lower() != 'y':
            break

    # Menambahkan struk pembelian ke table pembeli
    current_datetime = datetime.now()
    current_date = current_datetime.strftime("%Y-%m-%d")
    current_time = current_datetime.strftime("%H:%M:%S")

    # Insert data into transaksi table
    for pembelian in struk_pembelian:
        for buku_dibeli in pembelian.get("Buku Dibeli", []):
            # Get buku_id for the purchased book
            cursor.execute("SELECT buku_id FROM barang WHERE nama_buku = %s LIMIT 1", (buku_dibeli["Nama Buku"],))
            buku_id = cursor.fetchone()
            if not buku_id:
                console.print(f"[bold white]Maaf, buku dengan nama[bold white] [bold green]{buku_dibeli['Nama Buku']}[bold green] [bold white]tidak ditemukan.")
                return
            buku_id = buku_id[0]

            # Insert data into transaksi with buku_id and id_pembeli
            cursor.execute(
                "INSERT INTO transaksi (id_pembeli, buku_id, jumlah_buku, harga_per_buku, total_harga, tanggal, waktu) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (id_pembeli, buku_id, buku_dibeli["Jumlah Buku"],
                buku_dibeli["Harga per Buku"], buku_dibeli["Total Harga"], current_date, current_time)
            )

        # Update stok buku
        for pembelian in struk_pembelian:
            for buku_dibeli in pembelian.get("Buku Dibeli", []):
                cursor.execute("UPDATE barang SET stok_buku = stok_buku - %s WHERE nama_buku = %s",
                                (buku_dibeli['Jumlah Buku'], buku_dibeli['Nama Buku']))

    connection.commit()
    cursor.close()

    # Menampilkan struk pembelian
    print_transaksi(struk_pembelian, current_datetime, alamat_pembeli, nama_toko="Toko Buku TENGAH MALAM")

    # Display the main menu
    daftar_menu(connection)

# ================================ MENU TRANSAKSI =======================================
def display_transaction_from_db(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM transaksi")
    pembeli_data = cursor.fetchall()

    headers = ["ID Transaksi","ID Pembeli", "ID Buku", "Jumlah Buku", "Harga per Buku", "Total Harga", "Tanggal", "Waktu"]
    rows = []

    for row in pembeli_data:
        id_transaksi, id_pembeli, buku_id, jumlah_buku, harga_per_buku, total_harga, tanggal, waktu = row
        rows.append([id_transaksi, id_pembeli, buku_id, jumlah_buku, harga_per_buku, total_harga, tanggal, waktu])

    table = tabulate(rows, headers=headers, tablefmt="rounded_outline")
    
    console.print("[bold white]Daftar Transaksi Pembeli:[/bold white]")
    print(table)

    daftar_menu(connection)


# ============================================ STRUK =====================================================
def print_transaksi(transaksi, current_datetime, alamat_pembeli="", nama_toko="Toko Buku TENGAH MALAM"):
    if not transaksi:
        console.print("[bold blue]Tidak ada transaksi yang tersedia.")
        return

    date_str = current_datetime.strftime("%Y-%m-%d")
    time_str = current_datetime.strftime("%H:%M:%S")

    headers = ["Nama", "Qty", "Harga", "Total"]
    rows = []

    for pembelian in transaksi:
        nama_pembeli = pembelian.get("Nama Pembeli", "")
        # alamat_pembeli = pembelian.get("Alamat Pembeli", "")
        buku_dibeli = pembelian.get("Buku Dibeli", [])

        for buku_info in buku_dibeli:
            nama_buku = buku_info.get("Nama Buku", "")
            jumlah_buku = buku_info.get("Jumlah Buku", "")
            harga_per_buku = buku_info.get("Harga per Buku", "")
            total_harga = buku_info.get("Total Harga", "")

            # Append a row with the information
            rows.append([nama_buku, f"{jumlah_buku}x", f"{harga_per_buku:,.2f}", f"{total_harga:,.2f}"])

    # Calculate total price
    total_price = sum(float(buku_info[-1].replace(",", "")) for buku_info in rows)

    # Determine column widths dynamically
    col_widths = [max(len(str(row[i])) for row in rows + [headers]) for i in range(len(headers))]

    # Create the panel content
    panel_content = f"{nama_toko}\n\n"
    panel_content += f"{'Tanggal':<{col_widths[0] + 10}} : {date_str}\n"
    panel_content += f"{'Waktu':<{col_widths[0] + 10}} : {time_str}\n"
    panel_content += f"{'Nama Pembeli':<{col_widths[0] + 10}} : {nama_pembeli}\n"
    panel_content += f"{'Alamat Pembeli':<{col_widths[0] + 10}} : {alamat_pembeli}\n"
    panel_content += "-" * sum(col_widths) + "\n"
    panel_content += " ".join(f"{headers[i]:<{col_widths[i]}}" for i in range(len(headers))) + "\n"
    panel_content += "-" * sum(col_widths) + "\n"

    for row in rows:
        panel_content += " ".join(f"{row[i]:<{col_widths[i]}}" for i in range(len(row))) + "\n"

    panel_content += "-" * sum(col_widths) + "\n"
    panel_content += f"{'Total Harga':<{col_widths[0] + 10}}: Rp. {total_price:,.2f}\n"
    panel_content += "\nTerima Kasih Sudah Belanja Di Toko Kami :)" 

    # Display the panel
    console.print(Panel(panel_content, title="", border_style="white"), justify="left")
    
# ================================ DAFTAR MENU ========================================
def daftar_menu(connection):
    print("\n")
    menu_items = """
    [bold white][[bold cyan]1[/][bold white]][/] [bold green]Barang[bold white] [/]
    [bold white][[bold cyan]2[/][bold white]][/] [bold green]Pegawai[bold white] [/]
    [bold white][[bold cyan]3[/][bold white]][/] [bold green]Pembeli[bold white] [/]
    [bold white][[bold cyan]4[/][bold white]][/] [bold green]Transaksi[bold white] [/]
    [bold white][[bold cyan]0[/][bold white]][/] [bold green]log out[bold white]
"""
    panel_obj = Panel(menu_items, width=30, style="bold white", title="[bold green]Daftar Menu")
    console.print(panel_obj)

    pilihan = console.input(f' [bold white][[bold cyan]+[/][bold white]][/] [bold white]Masukkan pilihan : ')

    if pilihan == "1":
        barang(connection)
    elif pilihan == "2":
        pegawai(connection)
    elif pilihan == "3":
        pembeli(connection)
    elif pilihan == "4":
        display_transaction_from_db(connection)
    elif pilihan == "0":
        print()
        with console.status("[cyan bold]Menuggu keluar..."):
            for i in range(100):
                console.print(f"[progress({i + 1}/100)]", end='\r')
                sleep(0.02)
        console.print("[bold red]Good Bye...[bold red]")
        exit()
    else:
        console.print("[bold blue]Pilihan tidak valid")

# ========================== MENJALANKAN ============================================
if __name__ == "__main__":
    os.system('clear')
    connection = animasi_masuk()
    if connection:
        create_and_display_colored_ascii_art()
        daftar_menu(connection)