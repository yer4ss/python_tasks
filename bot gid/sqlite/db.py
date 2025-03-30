import sqlite3


# Подключение к базе и создание таблицы, если её нет
def create_table():
   conn = sqlite3.connect('cities.db')
   cursor = conn.cursor()
   cursor.execute('''
      CREATE TABLE IF NOT EXISTS cities (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         name TEXT UNIQUE,
         description TEXT,
         image_url TEXT,
         map_url TEXT
      )
   ''')

   print("База данных успешно создана!")

   conn.commit()
   conn.close()


# Функция для добавления города
def add_city(name, description, image_url):
   conn = sqlite3.connect('cities.db')
   cursor = conn.cursor()

   cursor.execute('INSERT OR IGNORE INTO cities (name, description, image_url) VALUES (?, ?, ?)',       #REPLACE - заменяет, если они уже существуют, IGNORE - игнорирует дубликат
                  (name, description, image_url))

   conn.commit()
   conn.close()


# Функция для получения информации о городе
def get_city_info(name):
   conn = sqlite3.connect('cities.db')
   cursor = conn.cursor()
   cursor.execute('SELECT description, image_url FROM cities WHERE name = ?', (name,))
   result = cursor.fetchone()
   conn.close()
   return result

# Функция для удаления города
def delete_city(name):
   try:
      conn = sqlite3.connect('cities.db')
      cursor = conn.cursor()

      # Выполняем запрос на удаление города по названию
      cursor.execute('DELETE FROM cities WHERE name = ?', (name,))
      conn.commit()

      # Проверяем, удалился ли город
      if cursor.rowcount > 0:
         print(f"🗑️ Город '{name}' успешно удалён!")
      else:
         print(f"❗ Город '{name}' не найден в базе.")
   except Exception as e:
      print(f"❌ Ошибка при удалении города '{name}': {e}")
   finally:
      conn.close()



def update_city(name, new_description, new_image_url):
   try:
      conn = sqlite3.connect('cities.db')
      cursor = conn.cursor()

      # Обновляем описание и изображение города по названию
      cursor.execute(
            'UPDATE cities SET description = ?, image_url = ? WHERE name = ?',
            (new_description, new_image_url, name)
      )

      conn.commit()

      # Проверяем, обновились ли данные
      if cursor.rowcount > 0:
            print(f"✅ Город '{name}' успешно обновлён!")
      else:
            print(f"❗ Город '{name}' не найден в базе.")

   except Exception as e:
      print(f"❌ Ошибка при обновлении города '{name}': {e}")

   finally:
      conn.close()


# Функция для просмотра всех городов
def get_all_cities():
   conn = sqlite3.connect('cities.db')
   cursor = conn.cursor()
   cursor.execute('SELECT * FROM cities')
   result = cursor.fetchall()
   conn.close()
   return result


print("✅")