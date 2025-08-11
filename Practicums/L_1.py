from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/user/<name>')
def user(name):
    return f'Hello, {name}!'

@app.route('/calculate/<int:x>')
def calculate(x):
    return f'{x} * 2 = {x*2}'

@app.route('/squares/<float:y>')
def squares(y):
    return f'{y} * {y} = {y*y}'

@app.route('/reverse/<text>')
def reverse(text):
    splitext = text.split("/")
    return '/'.join(splitext[::-1])

if __name__ == '__main__':
    app.run(debug=True, port=8080)