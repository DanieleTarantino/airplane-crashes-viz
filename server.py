from flask import Flask, jsonify
from flask.templating import render_template
from pca_test import wordcloud_from_cvs
import random

app = Flask(__name__, template_folder="templates")


@app.route("/world_map")
def world_map():
    return render_template("world_map.html")


@app.route("/wc_data")
def wc_data():

    words = wordcloud_from_cvs("dataset.csv", 25, (25, 75))
    return jsonify({"data": words})


@ app.route("/word_cloud")
def word_cloud():
    # return Flask.send_static_file("/templates/world_map.html")
    return render_template("word_cloud.html")


@ app.route("/")
def main():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=31337, debug=True)
