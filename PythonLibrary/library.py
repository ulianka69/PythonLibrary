import sqlite3
from datetime import datetime, timedelta


def init_db():
    conn = sqlite3.connect('library.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER,
            total_copies INTEGER DEFAULT 1
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS readers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS loans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER,
            reader_id INTEGER,
            date_out TEXT NOT NULL,
            date_return TEXT,
            FOREIGN KEY (book_id) REFERENCES books(id),
            FOREIGN KEY (reader_id) REFERENCES readers(id)
        )
    ''')
    conn.commit()
    conn.close()


def add_book(title, author, year, copies=1):
    conn = sqlite3.connect('library.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO books (title, author, year, total_copies) VALUES (?, ?, ?, ?)",
                (title, author, year, copies))
    conn.commit()
    conn.close()
    print(f"Книга '{title}' добавлена.")

def add_reader(name, phone):
    conn = sqlite3.connect('library.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO readers (name, phone) VALUES (?, ?)", (name, phone))
    conn.commit()
    conn.close()
    print(f"Читатель '{name}' добавлен.")

def lend_book(book_id, reader_id):
    conn = sqlite3.connect('library.db')
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM loans WHERE book_id = ? AND date_return IS NULL", (book_id,))
    borrowed = cur.fetchone()[0]
    cur.execute("SELECT total_copies FROM books WHERE id = ?", (book_id,))
    total = cur.fetchone()[0]
    if borrowed >= total:
        print("Нет свободных экземпляров.")
    else:
        date_out = datetime.now().strftime("%Y-%m-%d")
        cur.execute("INSERT INTO loans (book_id, reader_id, date_out) VALUES (?, ?, ?)",
                    (book_id, reader_id, date_out))
        conn.commit()
        print(f"Книга выдана читателю {reader_id}")
    conn.close()

def return_book(loan_id):
    conn = sqlite3.connect('library.db')
    cur = conn.cursor()
    date_return = datetime.now().strftime("%Y-%m-%d")
    cur.execute("UPDATE loans SET date_return = ? WHERE id = ?", (date_return, loan_id))
    conn.commit()
    conn.close()
    print("Книга возвращена.")


def report_debtors():
    conn = sqlite3.connect('library.db')
    cur = conn.cursor()
    cur.execute('''
        SELECT readers.name, books.title, loans.date_out
        FROM loans
        JOIN readers ON loans.reader_id = readers.id
        JOIN books ON loans.book_id = books.id
        WHERE loans.date_return IS NULL
          AND julianday('now') - julianday(loans.date_out) > 14
    ''')
    rows = cur.fetchall()
    print("\n--- Должники (более 14 дней) ---")
    for row in rows:
        print(f"{row[0]} должен книгу '{row[1]}' от {row[2]}")
    conn.close()

def report_popular_books():
    conn = sqlite3.connect('library.db')
    cur = conn.cursor()
    cur.execute('''
        SELECT books.title, COUNT(*) as total
        FROM loans
        JOIN books ON loans.book_id = books.id
        GROUP BY books.id
        ORDER BY total DESC
        LIMIT 5
    ''')
    rows = cur.fetchall()
    print("\n--- ТОП-5 популярных книг ---")
    for row in rows:
        print(f"{row[0]} — выдана {row[1]} раз")
    conn.close()


def menu():
    while True:
        print("\n=== БИБЛИОТЕКА ===")
        print("1. Добавить книгу")
        print("2. Добавить читателя")
        print("3. Выдать книгу")
        print("4. Вернуть книгу")
        print("5. Отчёт: должники")
        print("6. Отчёт: популярные книги")
        print("0. Выход")
        choice = input("Выберите: ")
        if choice == '1':
            title = input("Название: ")
            author = input("Автор: ")
            year = int(input("Год: "))
            copies = int(input("Количество экземпляров: "))
            add_book(title, author, year, copies)
        elif choice == '2':
            name = input("ФИО читателя: ")
            phone = input("Телефон: ")
            add_reader(name, phone)
        elif choice == '3':
            book_id = int(input("ID книги: "))
            reader_id = int(input("ID читателя: "))
            lend_book(book_id, reader_id)
        elif choice == '4':
            loan_id = int(input("ID выдачи: "))
            return_book(loan_id)
        elif choice == '5':
            report_debtors()
        elif choice == '6':
            report_popular_books()
        elif choice == '0':
            break
        else:
            print("Неверная команда")


if __name__ == "__main__":
    init_db()
    try:
        add_book("Война и мир", "Толстой", 1869, 3)
        add_book("Преступление и наказание", "Достоевский", 1866, 2)
        add_reader("Иванов Иван", "123-456")
        add_reader("Петрова Мария", "789-012")
    except:
        pass
    menu()