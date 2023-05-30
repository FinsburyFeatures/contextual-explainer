import os

import anthropic
from flask import Flask, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
anthropic_client = anthropic.Client(api_key=os.getenv("ANTHROPIC_API_KEY"))


@app.route("/", methods=("GET", "POST"))
def index():
    return jsonify({"hello": "world"})
