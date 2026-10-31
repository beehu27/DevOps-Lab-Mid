from flask import Flask, request, jsonify
import json
import os
from datetime import datetime


app = Flask(__name__)


REPORT_FOLDER = "reports"


if not os.path.exists(REPORT_FOLDER):
    os.makedirs(REPORT_FOLDER)



@app.route("/report", methods=["POST"])
def receive_report():

    data = request.json


    filename = f"{REPORT_FOLDER}/report.json"


    report = {
        "time": str(datetime.now()),
        "data": data
    }


    with open(filename, "w") as f:
        json.dump(report, f, indent=4)


    return jsonify(
        {
            "message": "Report received"
        }
    )



@app.route("/")
def home():

    return "Receiver Service Running"



if __name__ == "__main__":

    app.run(port=5001, debug=True)