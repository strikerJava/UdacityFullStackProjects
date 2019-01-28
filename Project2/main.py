from flask import Flask
app = Flask(__name__)

@app.route('/')

def startPoint():
    return "Hello Flask"

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
