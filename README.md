# PythonLibrary
Скрипт
-- Таблица книг
CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    year INTEGER,
    total_copies INTEGER DEFAULT 1
);

-- Таблица читателей
CREATE TABLE readers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT
);

-- Таблица выдач
CREATE TABLE loans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER,
    reader_id INTEGER,
    date_out TEXT NOT NULL,
    date_return TEXT,
    FOREIGN KEY (book_id) REFERENCES books(id),
    FOREIGN KEY (reader_id) REFERENCES readers(id)
);

тестовые данные для заполнения
-- Книги
INSERT INTO books (title, author, year, total_copies) VALUES
('Война и мир', 'Толстой Л.Н.', 1869, 3),
('Преступление и наказание', 'Достоевский Ф.М.', 1866, 2),
('Мастер и Маргарита', 'Булгаков М.А.', 1967, 1),
('Евгений Онегин', 'Пушкин А.С.', 1833, 2);

-- Читатели
INSERT INTO readers (name, phone) VALUES
('Иванов Иван Иванович', '89111234567'),
('Петрова Мария Сергеевна', '89217654321'),
('Сидоров Алексей Петрович', '89319876543');

-- Выдачи
INSERT INTO loans (book_id, reader_id, date_out, date_return) VALUES
(1, 1, '2024-04-01', '2024-04-15'),
(3, 1, '2025-05-10', NULL),
(1, 2, '2025-05-01', NULL),
(4, 3, '2025-05-12', NULL);
