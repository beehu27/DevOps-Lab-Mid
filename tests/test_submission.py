import sys
import json
import pytest
from pathlib import Path

# Add main project folder to Python import path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app import main

@pytest.fixture
def client(tmp_path, monkeypatch):
    # Create a separate temporary JSON file for each test
    test_file = tmp_path / "submissions.json"
    test_file.write_text("[]", encoding="utf-8")

    # Use the temporary file instead of the original submissions.json
    monkeypatch.setattr(main, "FILE", str(test_file))

    main.app.config["TESTING"] = True

    with main.app.test_client() as client:
        yield client


def test_valid_submission_saved_and_displayed(client):

    data = {
        "name": "Abeeha Asif",
        "registration": "FA23-BAI-016",
        "title": "DevOps Lab Mid",
        "url": "https://github.com/beehu27/DevOps-Lab-Mid"
    }

    # Submit valid assignment
    response = client.post("/submit", json=data)

    assert response.status_code in (200, 201)

    # Check submissions list
    saved_response = client.get("/submissions")

    assert saved_response.status_code == 200

    submissions = saved_response.get_json()

    assert len(submissions) == 1
    assert submissions[0]["name"] == "Abeeha Asif"
    assert submissions[0]["registration"] == "FA23-BAI-016"

    # Check JSON file
    with open(main.FILE, "r", encoding="utf-8") as file:
        saved_data = json.load(file)

    assert len(saved_data) == 1


def test_missing_registration_rejected(client):

    data = {
        "name": "Abeeha Asif",
        "registration": "",
        "title": "DevOps Lab Mid",
        "url": "https://github.com/beehu27/DevOps-Lab-Mid"
    }

    response = client.post("/submit", json=data)

    assert response.status_code == 400

    # Check that invalid submission was not saved
    submissions = client.get("/submissions").get_json()

    assert len(submissions) == 0


def test_invalid_url_rejected(client):

    data = {
        "name": "Abeeha Asif",
        "registration": "FA23-BAI-016",
        "title": "DevOps Lab Mid",
        "url": "not-a-valid-url"
    }

    response = client.post("/submit", json=data)

    assert response.status_code == 400

    # Check that invalid submission was not saved
    submissions = client.get("/submissions").get_json()

    assert len(submissions) == 0
