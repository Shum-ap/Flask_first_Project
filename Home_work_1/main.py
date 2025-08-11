from flask import Flask

# Создаём экземпляр приложения
app = Flask(__name__)

# Маршрут для корня сайта
@app.route("/")
def home():
    return "Hello, Flask!"

# Маршрут с параметром
@app.route("/user/<name>")
def user(name):
    return f"Hello, {name}!"

# Запуск приложения на порту 8080
if __name__ == "__main__":
    app.run(debug=True, port=8080)
