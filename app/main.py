
from flask import Flask, request, jsonify, render_template
import json
import os
from urllib.parse import urlparse

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(BASE_DIR, "submissions.json")


def valid_url(url):
    if not isinstance(url, str):
        return False

    try:
        parsed = urlparse(url.strip())
        return (
            parsed.scheme in ("http", "https")
            and bool(parsed.netloc)
            and "." in parsed.netloc
            and " " not in parsed.netloc
        )
    except ValueError:
        return False


def read_submissions():
    if not os.path.exists(FILE):
        return []

    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_submissions(submissions):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(submissions, f, indent=4)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json(silent=True) if request.is_json else request.form

    if not data:
        return jsonify({"message": "Submission data required"}), 400

    required_fields = ["name", "registration", "title", "url"]

    for field in required_fields:
        if not data.get(field) or not data.get(field).strip():
            return jsonify({
                "message": f"{field} required"
            }), 400

    if not valid_url(data["url"].strip()):
        return jsonify({"message": "Invalid URL"}), 400

    submission = {
        "name": data["name"].strip(),
        "registration": data["registration"].strip(),
        "title": data["title"].strip(),
        "url": data["url"].strip()
    }

    submissions = read_submissions()
    submissions.append(submission)
    save_submissions(submissions)

    if request.is_json:
        return jsonify({
            "message": "Submission saved",
            "submission": submission
        }), 201

    return (
        '<p>Submission saved successfully!</p>'
        '<a href="/">Submit another assignment</a> | '
        '<a href="/submissions">View submissions</a>'
    )


@app.route("/submissions")
def show_submissions():
    return jsonify(read_submissions())


if __name__ == "__main__":
    app.run(debug=True)
