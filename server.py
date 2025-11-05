import http.server
import socketserver
from urllib.parse import parse_qs  # Мы будем использовать только этот модуль

# Определяем порт, на котором будет работать сервер
PORT = 8000
CONTACTS_PAGE = 'contacts.html'


class MyHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        """
        Обработчик GET-запросов.
        Задание 2: На любой GET-запрос возвращать страницу «Контакты».
        """
        print(f"Получен GET-запрос для: {self.path}")

        try:
            # Пытаемся открыть и прочитать файл 'contacts.html'
            with open(CONTACTS_PAGE, 'rb') as file:
                content = file.read()

            # Отправляем код ответа 200 (ОК)
            self.send_response(200)
            # Отправляем заголовок Content-type, указывая, что это HTML
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()

            # Отправляем содержимое файла в теле ответа
            self.wfile.write(content)

        except FileNotFoundError:
            # Если файл не найден, отправляем ошибку 404
            print(f"Ошибка: Файл {CONTACTS_PAGE} не найден.")
            self.send_error(404, "Файл не найден")
        except Exception as e:
            # Обработка других возможных ошибок
            print(f"Произошла ошибка: {e}")
            self.send_error(500, "Внутренняя ошибка сервера")

    def do_POST(self):
        """
        Обработчик POST-запросов.
        Дополнительное задание: принять POST-запрос и напечатать
        в консоль все данные, которые были приняты.
        """
        print(f"\nПолучен POST-запрос для: {self.path}")

        try:
            # Получаем длину содержимого
            content_length = int(self.headers['Content-Length'])

            # Читаем тело запроса
            post_data_bytes = self.rfile.read(content_length)

            # Декодируем байты в строку
            post_data_str = post_data_bytes.decode('utf-8')

            # --- Печать данных в консоль ---
            print("--- НАЧАЛО ДАННЫХ POST-ЗАПРОСА ---")
            print(f"Сырые данные (raw): {post_data_str}")

            # Парсим данные формы (они приходят в формате 'key1=value1&key2=value2')
            # Используем urllib.parse.parse_qs - он встроен и работает отлично
            parsed_data = parse_qs(post_data_str)
            print("Разобранные данные (parsed):")
            for key, value in parsed_data.items():
                print(f"  {key}: {value[0]}")  # value[0] т.к. parse_qs возвращает список
            print("--- КОНЕЦ ДАННЫХ POST-ЗАПРОСА ---\n")

            # --- Отправляем простой ответ клиенту ---
            # (чтобы браузер не "завис" в ожидании)
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()

            response_message = f"""
            <html>
                <head><title>Спасибо!</title></head>
                <body>
                    <h1>Данные получены!</h1>
                    <p>Мы получили от вас следующие данные:</p>
                    <pre>{post_data_str}</pre>
                    <p><a href="/">Вернуться назад</a></p>
                </body>
            </html>
            """
            self.wfile.write(response_message.encode('utf-8'))

        except Exception as e:
            print(f"Ошибка при обработке POST-запроса: {e}")
            self.send_error(500, "Ошибка обработки POST-запроса")


# --- Запуск сервера ---
if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print(f"Сервер запущен и слушает порт {PORT}")
        print(f"Перейдите по адресу: http://localhost:{PORT}")
        httpd.serve_forever()