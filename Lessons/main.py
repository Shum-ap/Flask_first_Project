from flask import Flask
import uuid as uuid_lib

app = Flask(__name__)

# Статический маршрут
@app.route('/')
def home():
    return 'Welcome to the homepage!'

@app.route('/about')
def about():
    return 'This is the about page.'

# Динамический маршрут (строка)
@app.route('/user/<username>')
def user_profile(username):
    return f'User: {username}'

# Динамический маршрут (int)
@app.route('/user/id/<int:user_id>')
def user_profile_by_id(user_id):
    return f'User with ID: {user_id}'

# Динамический маршрут (float)
@app.route('/price/<float:price>')
def show_price(price):
    return f'Price is {price:.2f} USD'

# Динамический маршрут (path)
@app.route('/files/<path:filepath>')
def show_file(filepath):
    return f'File path: {filepath}'

# Динамический маршрут (UUID)
@app.route('/uuid/<uuid:user_uuid>')
def show_user_by_uuid(user_uuid):
    return f'User UUID: {user_uuid}'

# Пример генерации UUID (не маршрут, просто утилита)
@app.route('/generate_uuid')
def generate_uuid():
    return f'Generated UUID: {uuid_lib.uuid4()}'

if __name__ == '__main__':
    app.run(debug=True)
