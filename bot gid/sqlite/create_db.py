import sqlite3


# Подключаемся к базе данных (создаст файл cities.db)
conn = sqlite3.connect('cities.db')
cursor = conn.cursor()


# Удаляем таблицу, если она уже существует
cursor.execute('DROP TABLE IF EXISTS cities')


# Создаем таблицу с колонками: id, name, description, image_url
cursor.execute('''
    CREATE TABLE IF NOT EXISTS cities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        description TEXT,
        image_url TEXT
    )
''')

print("База данных успешно создана!")


# Сохраняем и закрываем соединение
conn.commit()
conn.close()