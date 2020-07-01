from flask import Flask
from bot import question, getQuestion

# home route
@app.route("/")
def home():
    return getQuestion()
