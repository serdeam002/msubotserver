import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello wlord"


if __name__ == '__main__':
    app.run(debug=True)
