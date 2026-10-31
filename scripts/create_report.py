
import json
import os
import subprocess
from pathlib import Path
from datetime import datetime, timezone

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = PROJECT_ROOT / "reports" / "pytest-report.json"
OUTPUT_FILE = PROJECT_ROOT / "reports" / "testreport.json"


def git_command(command):
    try:
        result = subprocess.run(
            command,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception:
        return "Not available"


def get_repository():
    repository = os.getenv("GITHUB_REPOSITORY")

    if repository:
        return repository

    remote = git_command(["git", "config", "--get", "remote.origin.url"])

    if remote != "Not available":
        remote = remote.replace(".git", "")
        return remote.split(":")[-1].split("github.com/")[-1]

    return "Local project"


def create_report():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            "Pytest report not found. Run pytest with --json-report first."
        )

    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        pytest_data = json.load(file)

    summary = pytest_data.get("summary", {})
    test_results = []

    for test in pytest_data.get("tests", []):
        outcome = test.get("outcome", "unknown")
        failure_message = None

        for phase in ("setup", "call", "teardown"):
            phase_data = test.get(phase, {})
            crash = phase_data.get("crash")

            if crash:
                failure_message = crash.get("message")
                break

        test_results.append({
            "test_name": test.get("nodeid", "Unknown test"),
            "result": outcome,
            "failure_message": failure_message
        })

    total = summary.get("total", len(test_results))
    passed = summary.get("passed", 0)
    failed = summary.get("failed", 0)
    errors = summary.get("error", 0)

    overall_status = (
        "passed" if failed == 0 and errors == 0 else "failed"
    )

    report = {
        "repository": get_repository(),
        "branch": os.getenv(
            "GITHUB_REF_NAME",
            git_command(["git", "branch", "--show-current"])
        ),
        "commit_sha": os.getenv(
            "GITHUB_SHA",
            git_command(["git", "rev-parse", "HEAD"])
        ),
        "pipeline_run_id": os.getenv("GITHUB_RUN_ID", "Local run"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tests": test_results,
        "summary": {
            "total": total,
            "passed": passed,
            "failed": failed,
            "errors": errors
        },
        "overall_status": overall_status
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    print(f"Report created successfully: {OUTPUT_FILE}")
    print(f"Overall status: {overall_status}")


if __name__ == "__main__":
    create_report()
