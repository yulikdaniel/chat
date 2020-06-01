from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    with open('/home/yulikdaniel/mysite/history.txt', 'r') as f:
        a = f.readlines()
        if not len(a):
            return 'Sorry, nothing to show'
        return a[-1]


@app.route('/s/<name>')
def accept(name):
    with open('/home/yulikdaniel/mysite/history.txt', 'a') as f:
        f.write('\n' + name)
    return 'Succesful'


# if __name__ == '__main__':
#     app.run()