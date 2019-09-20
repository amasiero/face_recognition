from flask import Flask, render_template
import json
import socket

app = Flask(__name__)

@app.route("/")
def output():
    return render_template("index.html", name = "Andrey Masiero")

@app.route("/get_faces", methods=['GET'])
def worker():
    data, addr = client.recvfrom(1024)
    return data

if __name__ == '__main__':
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    client.bind(("", 37020))
    app.run()
