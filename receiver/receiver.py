
import json
from pathlib import Path
from flask import Flask, request, jsonify

app = Flask(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORT_FILE = PROJECT_ROOT / "reports" / "testreport.json"


@app.route("/report", methods=["POST"])
def receive_report():
    report = request.get_json(silent=True)

    if not isinstance(report, dict):
        return jsonify({"error": "Invalid JSON report"}), 400

    required_fields = [
        "repository",
        "branch",
        "commit_sha",
        "pipeline_run_id",
        "timestamp",
        "tests",
        "summary",
        "overall_status"
    ]

    missing_fields = [
        field for field in required_fields if field not in report
    ]

    if missing_fields:
        return jsonify({
            "error": "Missing required fields",
            "missing": missing_fields
        }), 400

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(REPORT_FILE, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    return jsonify({
        "message": "Report received and saved successfully",
        "file": str(REPORT_FILE),
        "status": report["overall_status"]
    }), 200


@app.route("/", methods=["GET"])
def home():
    return "DevOps Test Report Receiver is running!"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=False)
