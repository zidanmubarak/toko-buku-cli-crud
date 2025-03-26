"""
Toko Buku CLI CRUD Application
A command-line interface application for managing bookstore data with MySQL database.
Features:
- CRUD operations for books and employees
- Terminal-based login system with animation
- Purchase transactions with receipt generation
- Colored stock display
- Transaction reporting
"""

import MySQLdb as db
import os
from tabulate import tabulate
from termcolor import colored
from rich.panel import Panel
from rich.console import Console
from datetime import datetime
from colorama import Fore, Style, init
from pyfiglet import Figlet
from time import sleep

# Initialize console for rich text formatting
console = Console()

# Initialize colorama
init(autoreset=True)

# Database configuration
DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'passwd': '',
    'db': 'toko_buku'
}

# ================= HELPER FUNCTIONS =================

def create_connection():
    """Create and return a database connection."""
    try:
        return db.connect(**DB_CONFIG)
    except Exception as e:
        console.print(f"[bold red]Database connection error: {e}")
        exit(1)

def execute_query(connection, query, params=None, fetch=False):
    """Execute a SQL query with optional parameters."""
    cursor = connection.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if fetch:
            result = cursor.fetchall()
            # Check if no results were found when fetching
            if not result and 'SELECT' in query.upper():
                return None
            return result
        
        # For UPDATE and DELETE operations, check affected rows
        if query.strip().upper().startswith(("UPDATE", "DELETE")):
            affected_rows = cursor.rowcount
            if affected_rows == 0:
                connection.commit()
                return False  # No rows affected
            
        connection.commit()
        return cursor.lastrowid if query.strip().upper().startswith("INSERT") else True
    except Exception as e:
        console.print(f"[bold red]Query execution error: {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()

def get_table_columns(connection, table_name):
    """Get column names from a table."""
    query = f"DESCRIBE {table_name}"
    cursor = connection.cursor()
    cursor.execute(query)
    columns = [column[0] for column in cursor.fetchall()]
    cursor.close()
    return columns

def display_progress(message, duration=2):
    """Display a progress animation."""
    with console.status(f"[cyan bold]{message}"):
        for i in range(100):
            console.print(f"[progress({i + 1}/100)]", end='\r')
            sleep(duration / 100)

# ================= LOGIN FUNCTION =================

def animate_login():
    """Display login animation and establish database connection."""
    with console.status("[cyan bold]Sedang LOGIN....."):
        connection = None
        try:
            for i in range(100):
                connection = create_connection()
                console.print(f"[progress({i + 1}/100)]", end='\r')
                sleep(0.02)
                
            # Verify database connection by executing a simple query
            cursor = connection.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            
            return connection
        except Exception as e:
            console.print(f"[bold red]Login gagal: {e}")
            console.print("[bold yellow]Pastikan server database MySQL berjalan dan database 'toko_buku' telah dibuat.")
            exit(1)

# ================= DISPLAY FUNCTIONS =================

def display_ascii_banner(text="toko buku tengah malam", font='graffiti', color=Fore.RED):
    """Create and display a colored ASCII art banner."""
    figlet = Figlet(font=font)
    ascii_art = figlet.renderText(text)
    colored_ascii_art = f"{Style.BRIGHT}{color}" + ascii_art + Style.RESET_ALL
    print(f"\n{colored_ascii_art}")

def display_menu(title, menu_items, width=30):
    """Display a formatted menu."""
    panel_obj = Panel(menu_items, width=width, style="bold white", title=f"[bold green]{title}")
    console.print(panel_obj)

# ================= DATA OPERATIONS =================

def insert_data(connection, table_name):
    """Generic function to insert data into a table."""
    columns = get_table_columns(connection, table_name)
    
    while True:
        data_values = []
        for column in columns:
            value = console.input(f"[bold white]Masukkan nilai untuk kolom[bold white] [bold green]{column}[bold green] "
                                 f"[bold white](ketik[bold white] [bold red]n[bold red] [bold white]jika selesai): [bold white]")
            if value.lower() == 'n':
                break
                
            # Validate input for specific columns (could be expanded)
            if (column.lower().endswith('_id') or column.lower().startswith('id')) and not value.isdigit() and value:
                console.print(f"[bold red]Error: Kolom {column} seharusnya berisi angka.")
                # Reset and start over
                data_values = []
                break
                
            # For number fields like stok_buku and harga
            if column in ['stok_buku', 'harga'] and value:
                try:
                    float(value)  # Try converting to validate it's a number
                except ValueError:
                    console.print(f"[bold red]Error: Kolom {column} seharusnya berisi angka.")
                    # Reset and start over
                    data_values = []
                    break
                    
            data_values.append(value)

        if not data_values:
            continue  # Start over if values were reset due to validation errors

        try:
            if data_values:
                # Check length to make sure we're not inserting too many or too few values
                if len(data_values) != len(columns):
                    placeholders = ', '.join(['%s'] * len(data_values))
                    column_subset = columns[:len(data_values)]
                    insert_query = f"INSERT INTO {table_name} ({', '.join(column_subset)}) VALUES ({placeholders})"
                else:
                    placeholders = ', '.join(['%s'] * len(data_values))
                    insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
                
                result = execute_query(connection, insert_query, tuple(data_values))
                
                if result:
                    console.print("[bold blue]Data berhasil ditambahkan.")
                else:
                    console.print("[bold red]Gagal menambahkan data. Silakan periksa nilai yang dimasukkan.")
            else:
                console.print("[bold blue]Penambahan data dibatalkan.")
        except Exception as e:
            console.print(f"[bold red]Terjadi kesalahan: {e}")
            connection.rollback()

        if not data_values or value.lower() == 'n':
            break

def update_data(connection, table_name, id_column):
    """Generic function to update data in a table."""
    columns = get_table_columns(connection, table_name)

    record_id = console.input("[bold white]Masukkan ID yang ingin diupdate: ")
    
    # Check if record exists
    check_query = f"SELECT COUNT(*) FROM {table_name} WHERE {id_column} = %s"
    cursor = connection.cursor()
    cursor.execute(check_query, (record_id,))
    count = cursor.fetchone()[0]
    cursor.close()
    
    if count == 0:
        console.print(f"[bold red]Error: Data dengan {id_column} = {record_id} tidak ditemukan dalam database.")
        return
    
    update_values = {}
    for column in columns:
        value = console.input(f"[bold white]Masukkan nilai baru untuk kolom[bold white] [bold green]{column}[bold green] "
                             f"[bold white](tekan[bold white] [bold red]Enter[bold red] [bold white]jika tidak ingin mengubah): [bold white]")
        if value:
            update_values[column] = value

    try:
        if update_values:
            set_clause = ', '.join([f'{column} = %s' for column in update_values.keys()])
            update_query = f"UPDATE {table_name} SET {set_clause} WHERE {id_column} = %s"
            result = execute_query(connection, update_query, tuple(update_values.values()) + (record_id,))
            
            if result is False:
                console.print(f"[bold red]Gagal mengupdate data. Data dengan {id_column} = {record_id} mungkin sudah tidak ada.")
            else:
                console.print("[bold blue]Data berhasil diupdate.")
        else:
            console.print("[bold blue]Tidak ada perubahan dilakukan.")
    except Exception as e:
        console.print(f"[bold white]Terjadi kesalahan: [bold red]{e}")
        connection.rollback()

def delete_data(connection, table_name):
    """Generic function to delete data from a table."""
    columns = get_table_columns(connection, table_name)

    console.print("[bold white]Pilih kolom untuk dihapus:")
    for i, column in enumerate(columns, 1):
        print(f"{i}. {column}")

    try:
        selected_index = int(console.input("[bold white]Masukkan nomor kolom: ")) - 1
        if selected_index < 0 or selected_index >= len(columns):
            console.print("[bold blue]Nomor kolom tidak valid.")
            return
    except ValueError:
        console.print("[bold blue]Masukkan nomor yang valid.")
        return

    selected_column = columns[selected_index]
    target_value = console.input(f"[bold white]Masukkan nilai kolom[bold white] [bold green]{selected_column}[bold green] "
                               f"[bold white]yang ingin dihapus: [bold white]")

    # First check if the data exists
    check_query = f"SELECT COUNT(*) FROM {table_name} WHERE {selected_column} = %s"
    cursor = connection.cursor()
    cursor.execute(check_query, (target_value,))
    count = cursor.fetchone()[0]
    cursor.close()
    
    if count == 0:
        console.print(f"[bold red]Error: Data dengan {selected_column} = {target_value} tidak ditemukan dalam database.")
        return

    try:
        delete_query = f"DELETE FROM {table_name} WHERE {selected_column} = %s"
        result = execute_query(connection, delete_query, (target_value,))
        
        if result is False:
            console.print(f"[bold red]Tidak ada data yang dihapus. Data dengan {selected_column} = {target_value} tidak ditemukan.")
        else:
            console.print("[bold blue]Data berhasil dihapus.")
    except Exception as e:
        console.print(f"[bold white]Terjadi kesalahan: [bold red]{e}")
        connection.rollback()

# ================= MODULE FUNCTIONS =================

def manage_books(connection):
    """Display and manage book inventory."""
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM barang")
    stock_data = cursor.fetchall()
    stock_header = ["Buku ID", "Nama Buku", "Type Buku", "Stok Barang", "Harga"]
    
    # Color-code stock levels
    colored_stock_data = []
    for row in stock_data:
        colored_row = []
        for i, value in enumerate(row):
            if i == 3:  # Stock column
                if value == 0:
                    colored_row.append(colored(value, 'red'))  # Out of stock
                elif 0 < value <= 5:
                    colored_row.append(colored(value, 'yellow'))  # Low stock
                else:
                    colored_row.append(colored(value, 'green'))  # Good stock
            else:
                colored_row.append(value)
        colored_stock_data.append(colored_row)

    print(tabulate(colored_stock_data, headers=stock_header, tablefmt="rounded_outline"))

    # Book management menu
    menu_items = """
[bold white][[bold cyan]1[/][bold white]][/] [bold green]Insert Data[bold white] [/]
[bold white][[bold cyan]2[/][bold white]][/] [bold green]Update Data[bold white] [/]
[bold white][[bold cyan]3[/][bold white]][/] [bold green]Delete Data[bold white] [/]
[bold white][[bold cyan]0[/][bold white]][/] [bold green]Kembali ke Menu Utama[bold white]
"""
    display_menu("Menu Stok", menu_items)

    choice = console.input(f' [bold white][[bold cyan]+[/][bold white]][/] [bold white]Masukkan pilihan : ')

    if choice == "1":
        insert_data(connection, "barang")
    elif choice == "2":
        update_data(connection, "barang", "buku_id")
    elif choice == "3":
        delete_data(connection, "barang")
    elif choice == "0":
        display_main_menu(connection)
    else:
        console.print("[bold blue]Pilihan tidak valid")
    
    display_main_menu(connection)

def manage_employees(connection):
    """Display and manage employee data."""
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM pegawai")
    employee_data = cursor.fetchall()
    employee_headers = ["Pegawai ID", "Nama Pegawai", "Alamat", "No.Hp"]
    
    print(tabulate(employee_data, headers=employee_headers, tablefmt="rounded_outline"))

    # Employee management menu
    menu_items = """
[bold white][[bold cyan]1[/][bold white]][/] [bold green]Insert Data[bold white] [/]
[bold white][[bold cyan]2[/][bold white]][/] [bold green]Update Data[bold white] [/]
[bold white][[bold cyan]3[/][bold white]][/] [bold green]Delete Data[bold white] [/]
[bold white][[bold cyan]0[/][bold white]][/] [bold green]Kembali ke Menu Utama[bold white]
"""
    display_menu("Menu Pegawai", menu_items)

    choice = console.input(f' [bold white][[bold cyan]+[/][bold white]][/] [bold white]Masukkan pilihan : ')

    if choice == "1":
        insert_data(connection, "pegawai")
    elif choice == "2":
        update_data(connection, "pegawai", "pegawai_id")
    elif choice == "3":
        delete_data(connection, "pegawai")
    elif choice == "0":
        display_main_menu(connection)
    else:
        console.print("[bold blue]Pilihan tidak valid")
    
    display_main_menu(connection)

def process_purchase(connection):
    """Process book purchases and generate receipts."""
    cursor = connection.cursor()

    # Check if there are any books in stock
    cursor.execute("SELECT COUNT(*) FROM barang WHERE stok_buku > 0")
    book_count = cursor.fetchone()[0]
    
    if book_count == 0:
        console.print("[bold red]Error: Tidak ada buku yang tersedia di stok.")
        return

    # Get available book types
    cursor.execute("SELECT DISTINCT type_buku FROM barang WHERE stok_buku > 0")
    book_types_result = cursor.fetchall()
    
    if not book_types_result:
        console.print("[bold red]Error: Tidak ada tipe buku yang tersedia dengan stok positif.")
        return
        
    book_types = [row[0] for row in book_types_result]

    # Display available book types
    console.print("[bold white]Pilih Type Buku:")
    for i, book_type in enumerate(book_types, 1):
        console.print(f"[bold blue]{i}. [bold green]{book_type}")

    # Select book types
    try:
        selected_types_input = console.input("[bold white]Masukkan nomor type buku (pisahkan dengan koma): ")
        if not selected_types_input.strip():
            console.print("[bold red]Error: Input tidak boleh kosong.")
            return
            
        selected_type_indices = [int(index.strip()) - 1 for index in selected_types_input.split(',')]
        
        # Validate indices
        invalid_indices = [index for index in selected_type_indices if index < 0 or index >= len(book_types)]
        if invalid_indices:
            console.print("[bold red]Error: Nomor type buku tidak valid.")
            return
    except ValueError:
        console.print("[bold red]Error: Masukkan nomor yang valid.")
        return

    selected_types = [book_types[index] for index in selected_type_indices]

    # Get books with stock for selected types
    placeholders = ', '.join(['%s'] * len(selected_types))
    query = f"SELECT * FROM barang WHERE type_buku IN ({placeholders}) AND stok_buku > 0"
    cursor.execute(query, tuple(selected_types))
    available_books = cursor.fetchall()
    book_headers = ["Buku ID", "Nama Buku", "Type Buku", "Stok Barang", "Harga"]

    if not available_books:
        console.print("[bold red]Error: Stok buku untuk tipe yang dipilih kosong. Silakan pilih tipe buku lain.")
        return

    # Display available books with color-coded stock
    colored_books = []
    for row in available_books:
        colored_row = []
        for i, value in enumerate(row):
            if i == 3:  # Stock column
                if value == 0:
                    colored_row.append(colored(value, 'red'))
                elif 0 < value <= 5:
                    colored_row.append(colored(value, 'yellow'))
                else:
                    colored_row.append(colored(value, 'green'))
            else:
                colored_row.append(value)
        colored_books.append(colored_row)

    print(tabulate(colored_books, headers=book_headers, tablefmt="rounded_outline"))

    # Collect customer information
    purchase_items = []
    customer_name = console.input("[bold white]Masukkan nama pembeli: ")
    customer_address = console.input("[bold white]Masukkan alamat pembeli: ")

    # Insert customer data
    cursor.execute("INSERT INTO pembeli (nama_pembeli, alamat) VALUES (%s, %s)", 
                  (customer_name, customer_address))
    customer_id = cursor.lastrowid

    # Process book purchases
    while True:
        book_name = console.input("[bold white]Masukkan nama buku yang dibeli : ")

        # Check if book exists at all
        cursor.execute("SELECT buku_id, stok_buku, harga FROM barang WHERE nama_buku = %s LIMIT 1", 
                      (book_name,))
        book_exists = cursor.fetchone()
        
        if not book_exists:
            console.print(f"[bold red]Error: Buku dengan nama [bold green]{book_name}[/bold green] tidak ditemukan dalam database.")
            continue
            
        book_id, stock, price_per_book = book_exists
        
        # Check if book has stock
        if stock <= 0:
            console.print(f"[bold red]Error: Buku dengan nama [bold green]{book_name}[/bold green] sedang kosong stok.")
            continue

        # Get quantity
        try:
            quantity = int(console.input("[bold white]Masukkan jumlah buku yang dibeli: "))
            if quantity <= 0:
                console.print(f"[bold red]Error: Jumlah pembelian harus lebih dari 0.")
                continue
        except ValueError:
            console.print(f"[bold red]Error: Masukkan angka yang valid untuk jumlah buku.")
            continue

        if quantity > stock:
            console.print(f"[bold red]Error: Stok buku tidak mencukupi. Stok tersedia: [bold green]{stock}[/bold green]")
            continue

        # Calculate total price
        total_price = quantity * price_per_book

        # Get quantity
        quantity = int(console.input("[bold white]Masukkan jumlah buku yang dibeli: "))

        if quantity > stock:
            console.print(f"[bold blue]Maaf, stok buku tidak mencukupi untuk jumlah yang diminta.")
            continue

        # Calculate total price
        total_price = quantity * price_per_book

        # Add purchase to list
        purchase_items.append({
            "book_id": book_id,
            "book_name": book_name,
            "quantity": quantity,
            "price_per_book": price_per_book,
            "total_price": total_price
        })

        continue_shopping = console.input("[bold white]Ingin beli buku lagi? [bold green](y/n): ")
        if continue_shopping.lower() != 'y':
            break

    # Record transaction time
    current_datetime = datetime.now()
    current_date = current_datetime.strftime("%Y-%m-%d")
    current_time = current_datetime.strftime("%H:%M:%S")

    # Insert transaction records and update stock
    for item in purchase_items:
        # Insert transaction
        cursor.execute(
            "INSERT INTO transaksi (id_pembeli, buku_id, jumlah_buku, harga_per_buku, total_harga, tanggal, waktu) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (customer_id, item["book_id"], item["quantity"], item["price_per_book"], 
             item["total_price"], current_date, current_time)
        )
        
        # Update stock
        cursor.execute("UPDATE barang SET stok_buku = stok_buku - %s WHERE buku_id = %s",
                     (item["quantity"], item["book_id"]))

    connection.commit()

    # Format receipt data
    receipt_data = []
    for item in purchase_items:
        receipt_data.append({
            "Nama Buku": item["book_name"],
            "Jumlah Buku": item["quantity"],
            "Harga per Buku": item["price_per_book"],
            "Total Harga": item["total_price"]
        })

    # Generate receipt
    print_receipt(customer_name, customer_address, receipt_data, current_datetime)
    
    display_main_menu(connection)

def display_transactions(connection):
    """Display transaction history."""
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM transaksi")
    transaction_data = cursor.fetchall()

    headers = ["ID Transaksi", "ID Pembeli", "ID Buku", "Jumlah Buku", 
              "Harga per Buku", "Total Harga", "Tanggal", "Waktu"]
    
    table = tabulate(transaction_data, headers=headers, tablefmt="rounded_outline")
    
    console.print("[bold white]Daftar Transaksi Pembeli:[/bold white]")
    print(table)

    display_main_menu(connection)

def print_receipt(customer_name, customer_address, items, timestamp, store_name="Toko Buku TENGAH MALAM"):
    """Generate and print a purchase receipt."""
    date_str = timestamp.strftime("%Y-%m-%d")
    time_str = timestamp.strftime("%H:%M:%S")

    headers = ["Nama", "Qty", "Harga", "Total"]
    rows = []

    # Prepare receipt rows
    for item in items:
        rows.append([
            item["Nama Buku"],
            f"{item['Jumlah Buku']}x",
            f"{item['Harga per Buku']:,.2f}",
            f"{item['Total Harga']:,.2f}"
        ])

    # Calculate total price
    total_price = sum(item["Total Harga"] for item in items)

    # Determine column widths
    col_widths = [max(len(str(row[i])) for row in rows + [headers]) for i in range(len(headers))]

    # Create receipt content
    panel_content = f"{store_name}\n\n"
    panel_content += f"{'Tanggal':<{col_widths[0] + 10}} : {date_str}\n"
    panel_content += f"{'Waktu':<{col_widths[0] + 10}} : {time_str}\n"
    panel_content += f"{'Nama Pembeli':<{col_widths[0] + 10}} : {customer_name}\n"
    panel_content += f"{'Alamat Pembeli':<{col_widths[0] + 10}} : {customer_address}\n"
    panel_content += "-" * sum(col_widths) + "\n"
    panel_content += " ".join(f"{headers[i]:<{col_widths[i]}}" for i in range(len(headers))) + "\n"
    panel_content += "-" * sum(col_widths) + "\n"

    for row in rows:
        panel_content += " ".join(f"{row[i]:<{col_widths[i]}}" for i in range(len(row))) + "\n"

    panel_content += "-" * sum(col_widths) + "\n"
    panel_content += f"{'Total Harga':<{col_widths[0] + 10}}: Rp. {total_price:,.2f}\n"
    panel_content += "\nTerima Kasih Sudah Belanja Di Toko Kami :)" 

    # Display the receipt
    console.print(Panel(panel_content, title="", border_style="white"), justify="left")

def display_main_menu(connection):
    """Display the main menu and handle user choices."""
    print("\n")
    menu_items = """
    [bold white][[bold cyan]1[/][bold white]][/] [bold green]Barang[bold white] [/]
    [bold white][[bold cyan]2[/][bold white]][/] [bold green]Pegawai[bold white] [/]
    [bold white][[bold cyan]3[/][bold white]][/] [bold green]Pembeli[bold white] [/]
    [bold white][[bold cyan]4[/][bold white]][/] [bold green]Transaksi[bold white] [/]
    [bold white][[bold cyan]0[/][bold white]][/] [bold green]Log Out[bold white]
"""
    display_menu("Daftar Menu", menu_items)

    choice = console.input(f' [bold white][[bold cyan]+[/][bold white]][/] [bold white]Masukkan pilihan : ')

    if choice == "1":
        manage_books(connection)
    elif choice == "2":
        manage_employees(connection)
    elif choice == "3":
        process_purchase(connection)
    elif choice == "4":
        display_transactions(connection)
    elif choice == "0":
        display_progress("Menunggu keluar...", 2)
        console.print("[bold red]Good Bye...[bold red]")
        exit()
    else:
        console.print("[bold blue]Pilihan tidak valid")
        display_main_menu(connection)

# ================= MAIN FUNCTION =================

def main():
    """Main application function."""
    os.system('clear' if os.name == 'posix' else 'cls')  # Clear screen
    
    try:
        # Login and establish database connection
        connection = animate_login()
        
        if connection:
            # Display application banner
            display_ascii_banner()
            
            # Show main menu
            display_main_menu(connection)
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Program dihentikan oleh pengguna.")
    except Exception as e:
        console.print(f"\n[bold red]Terjadi kesalahan yang tidak terduga: {e}")
    finally:
        console.print("[bold blue]Terima kasih telah menggunakan aplikasi Toko Buku.")

# Entry point
if __name__ == "__main__":
    main()