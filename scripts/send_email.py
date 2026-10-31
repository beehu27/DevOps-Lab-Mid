
import json
import os
import smtplib
from email.message import EmailMessage

# Read the generated test report
report_path = "reports/testreport.json"

with open(report_path, "r", encoding="utf-8") as file:
    report = json.load(file)

# Read credentials from GitHub Secrets (environment variables)
email_username = os.environ["MAIL_USERNAME"]
email_password = os.environ["MAIL_PASSWORD"]

# Send the email to the same Gmail address
receiver_email = email_username

status = report.get("overall_status", "unknown")
summary = report.get("summary", {})

# Create email
message = EmailMessage()
message["From"] = email_username
message["To"] = receiver_email
message["Subject"] = f"DevOps CI Test Report - {status.upper()}"

body = f"""
DevOps CI Pipeline Test Report

Repository: {report.get('repository')}
Branch: {report.get('branch')}
Commit SHA: {report.get('commit_sha')}
Pipeline Run ID: {report.get('pipeline_run_id')}
Timestamp: {report.get('timestamp')}

Overall Status: {status}

Total Tests: {summary.get('total')}
Passed Tests: {summary.get('passed')}
Failed Tests: {summary.get('failed')}
Errors: {summary.get('errors')}

Test Details:
"""

for test in report.get("tests", []):
    body += f"""
Test Name: {test.get('name')}
Result: {test.get('result')}
Failure Message: {test.get('failure_message')}
"""

message.set_content(body)

# Send email through Gmail SMTP
with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    server.login(email_username, email_password)
    server.send_message(message)

print("Test report email sent successfully!")
