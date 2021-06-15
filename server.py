from flask import Flask
from flask.templating import render_template

app = Flask(__name__, template_folder="templates")


@app.route("/")
def main():
    return render_template("index.html")
