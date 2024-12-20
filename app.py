from flask import Flask, render_template_string
import sqlite3

app = Flask(__name__)

# Функция для создания базы данных и таблицы
def create_database():
    conn = sqlite3.connect('gifts.db')
    cursor = conn.cursor()

    # Создание таблицы gift_list
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gift_list (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            gift_name TEXT NOT NULL,
            price REAL NOT NULL,
            status TEXT NOT NULL
        )
    ''')

    # Проверка, существует ли уже таблица
    cursor.execute('SELECT COUNT(*) FROM gift_list')
    count = cursor.fetchone()[0]

    # Если таблица пустая, заполняем её данными
    if count == 0:
        gifts = [
            ('Иванов Иван Иванович', 'Книга', 500, 'не куплен'),
            ('Петрова Светлана Александровна', 'Чашка', 150, 'куплен'),
            ('Сидоров Сергей Петрович', 'Ноутбук', 50000, 'не куплен'),
            ('Коваленко Анна Вячеславовна', 'Косметика', 700, 'куплен'),
            ('Васильев Александр Николаевич', 'Подарочный сертификат', 2000, 'не куплен'),
            ('Семенова Дарья Игоревна', 'Игрушка', 300, 'не куплен'),
            ('Федоров Олег Владиславович', 'Наушники', 3500, 'куплен'),
            ('Романова Полина Васильевна', 'Плед', 1200, 'не куплен'),
            ('Лебедев Вячеслав Сергеевич', 'Настольная игра', 800, 'куплен'),
            ('Кузнецова Ольга Сергеевна', 'Билет на концерт', 4500, 'не куплен')
        ]

        # Вставка данных в таблицу
        cursor.executemany('''
            INSERT INTO gift_list (full_name, gift_name, price, status) VALUES (?, ?, ?, ?)
        ''', gifts)

        conn.commit()

    # Закрытие соединения
    conn.close()

# Функция для получения данных из базы данных
def get_gifts():
    conn = sqlite3.connect('gifts.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM gift_list')
    gifts = cursor.fetchall()
    conn.close()
    return gifts

@app.route('/')
def index():
    # Создаем базу данных и таблицу, если они ещё не существуют
    create_database()
    # Получаем подарки из базы данных
    gifts = get_gifts()

    # HTML-шаблон для отображения данных
    html_template = '''
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Список подарков</title>
      </head>
      <body>
        <h1>Список подарков на Новый Год</h1>
        <table border="1">
          <tr>
            <th>ID</th>
            <th>ФИО</th>
            <th>Название подарка</th>
            <th>Стоимость</th>
            <th>Статус</th>
          </tr>
          {% for gift in gifts %}
          <tr>
            <td>{{ gift[0] }}</td>
            <td>{{ gift[1] }}</td>
            <td>{{ gift[2] }}</td>
            <td>{{ gift[3] }}</td>
            <td>{{ gift[4] }}</td>
          </tr>
          {% endfor %}
        </table>
      </body>
    </html>
    '''

    return render_template_string(html_template, gifts=gifts)

if __name__ == '__main__':
    app.run(debug=True)