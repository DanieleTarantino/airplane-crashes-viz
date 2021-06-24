from flask import Flask, jsonify, request, send_file
from flask.templating import render_template
from flask.wrappers import Request
import wordcloudgen
import wordtreegen
import histogramgen
import nltk

app = Flask(__name__, template_folder="templates", static_folder="static")


"""
===============================================================================
Methods used to generate json files needed for visualizations
===============================================================================
"""


@app.route("/wt_data")
def wt_data():
    word = request.args.get("starting_word")
    return wordtreegen.generate_json("dataset.csv", word if word is not None else "crashed")


@ app.route("/dataset_enhanced.csv")
def get_ds():
    return send_file("dataset_enhanced.csv")


@ app.route("/countries.geojson")
def geojson():
    return send_file("countries.geojson")


@app.route("/wc_data")
def wc_data():
    words = wordcloudgen.wordcloud_from_cvs("dataset.csv", 25, (25, 75))
    return jsonify({"data": words})


@app.route("/hist.json")
def get_histogram():
    js = histogramgen.get_histogram_as_json()
    return jsonify(js)


# @app.route("/line_chart")
# def line_chart():
#     return send_file("dataset_enhanced.csv")
#     # return jsonify({1900: [10, 42], 2000: [42, 442]})
#     # return "<script>alert(1)</script>"

"""
===============================================================================
Methods used to render visualization pages inside iframes
===============================================================================
"""


@app.route("/world_map")
def world_map():
    return render_template("world_map.html")


@ app.route("/word_tree")
def word_tree():
    return render_template("word_tree.html")


@ app.route("/word_cloud")
def word_cloud():
    return render_template("word_cloud.html")


@ app.route("/line_chart")
def line_char():
    return render_template("line_chart.html")


@ app.route("/histogram")
def histogram():
    return render_template("histogram.html")


"""
===============================================================================
Root route
===============================================================================
"""


@ app.route("/")
def main():
    return render_template("index.html")


if __name__ == '__main__':

    # download ntlk required data
    nltk.download('punkt')
    nltk.download('wordnet')
    nltk.download('stopwords')

    app.run(host='0.0.0.0', port=31337, debug=True)
