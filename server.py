import http.server
import socketserver
from urllib.parse import parse_qs

# Определяем порт, на котором будет работать сервер
PORT = 8000

# 1. СЛОВАРЬ МАРШРУТОВ (ОБНОВЛЕН)
# Сопоставляет URL-пути с именами файлов
ROUTES = {
    '/': 'index.html',              # Главная страница
    '/index': 'index.html',
    '/category': 'category.html',   # Страница категорий
    '/catalog': 'catalog.html',     # Страница каталога
    '/contacts': 'contacts.html',   # Страница контактов
    '/orders': 'orders.html',       # <<< ДОБАВЛЕН НОВЫЙ МАРШРУТ
}

class MyHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        """
        Обработчик GET-запросов с маршрутизацией.
        Теперь отдает разные HTML-файлы в зависимости от URL.
        """
        request_path = self.path
        print(f"Получен GET-запрос для: {request_path}")

        # 2. ОПРЕДЕЛЕНИЕ ИМЕНИ ФАЙЛА
        # Проверяем, есть ли запрошенный путь в нашем словаре маршрутов
        if request_path in ROUTES:
            file_to_serve = ROUTES[request_path]
        elif request_path.endswith('.html') and request_path[1:] in ROUTES.values():
            # Это позволяет также открывать файлы напрямую (например, /index.html)
            file_to_serve = request_path[1:]
        else:
            # Если маршрут не найден, отправляем 404
            self.send_error(404, "Страница не найдена")
            return

        try:
            # 3. ОТПРАВКА ФАЙЛА
            # Пытаемся открыть и прочитать соответствующий HTML-файл
            with open(file_to_serve, 'rb') as file:
                content = file.read()

            # Отправляем код ответа 200 (ОК)
            self.send_response(200)
            # Отправляем заголовок Content-type, указывая, что это HTML
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()

            # Отправляем содержимое файла в теле ответа
            self.wfile.write(content)

        except FileNotFoundError:
            # Если файл из словаря не найден на диске
            print(f"Ошибка: Файл {file_to_serve} не найден на диске.")
            self.send_error(404, f"Файл {file_to_serve} не найден")
        except Exception as e:
            # Обработка других возможных ошибок
            print(f"Произошла ошибка: {e}")
            self.send_error(500, "Внутренняя ошибка сервера")

    def do_POST(self):
        """
        Обработчик POST-запросов остается без изменений.
        Он по-прежнему печатает данные в консоль.
        """
        print(f"\nПолучен POST-запрос для: {self.path}")

        try:
            # Получаем длину содержимого
            content_length = int(self.headers['Content-Length'])

            # Читаем тело запроса
            post_data_bytes = self.rfile.read(content_length)
            post_data_str = post_data_bytes.decode('utf-8')

            # --- Печать данных в консоль ---
            print("--- НАЧАЛО ДАННЫХ POST-ЗАПРОСА ---")
            print(f"Сырые данные (raw): {post_data_str}")

            parsed_data = parse_qs(post_data_str)
            print("Разобранные данные (parsed):")
            for key, value in parsed_data.items():
                print(f"  {key}: {value[0]}")
            print("--- КОНЕЦ ДАННЫХ POST-ЗАПРОСА ---\n")

            # --- Отправляем ответ клиенту ---
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()

            response_message = f"""
            <html>
                <head><title>Спасибо!</title></head>
                <body>
                    <h1>Данные получены!</h1>
                    <p>Сообщение успешно отправлено. Проверьте консоль PyCharm.</p>
                    <p><a href="/">Вернуться на главную</a></p>
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
        print(f"Главная: http://localhost:{PORT}/")
        print(f"Контакты: http://localhost:{PORT}/contacts")
        httpd.serve_forever()