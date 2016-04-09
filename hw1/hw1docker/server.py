from flask import Flask, request, redirect, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return 'Please head to /hello or /echobot'

@app.route("/hello",methods=['GET'])
def hello():
    if request.method== 'GET':
       return "Hello world!"

@app.route("/echo",methods=['GET'])
def echo():
    if request.method == 'GET':
        message = request.args.get('msg')
        return message  

if __name__ == "__main__":
    app.debug = True
    app.run(port=8080)