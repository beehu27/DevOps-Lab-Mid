from flask import Flask, request, jsonify
import json
import os
import re


app = Flask(__name__)


# File where submissions will be stored
FILE = "app/submissions.json"


# Create empty file if it does not exist
if not os.path.exists(FILE):
    with open(FILE, "w") as f:
        json.dump([], f)



# Function to check URL format
def valid_url(url):

    pattern = r'^https?://'

    return re.match(pattern, url)



# Home page
@app.route("/")
def home():

    return "Assignment Submission Portal"



# Submit assignment
@app.route("/submit", methods=["POST"])
def submit():


    data = request.json


    required_fields = [
        "name",
        "registration",
        "title",
        "url"
    ]


    # Check empty fields
    for field in required_fields:

        if not data.get(field):

            return jsonify(
                {
                    "message": f"{field} required"
                }
            ),400



    # Check URL
    if not valid_url(data["url"]):

        return jsonify(
            {
                "message":"Invalid URL"
            }
        ),400



    # Read old submissions
    with open(FILE,"r") as f:

        submissions=json.load(f)



    # Add new submission
    submissions.append(data)



    # Save submissions
    with open(FILE,"w") as f:

        json.dump(
            submissions,
            f,
            indent=4
        )



    return jsonify(
        {
            "message":"Submission saved"
        }
    )



# Show all submissions
@app.route("/submissions")
def show_submissions():


    with open(FILE,"r") as f:

        submissions=json.load(f)


    return jsonify(submissions)



# Run application
if __name__=="__main__":

    app.run(debug=True)