import sys

sys.path.append(".")


from app.main import app


client = app.test_client()



# Test 1:
# Complete details + valid URL
def test_valid_submission():

    response = client.post(
        "/submit",
        json={
            "name": "Abeeha",
            "registration": "FA22-BCS-001",
            "title": "DevOps Lab Mid",
            "url": "https://github.com/test"
        }
    )


    assert response.status_code == 200

    assert response.json["message"] == "Submission saved"




# Test 2:
# Missing registration number
def test_missing_registration():

    response = client.post(
        "/submit",
        json={
            "name": "Abeeha",
            "title": "DevOps Lab Mid",
            "url": "https://github.com/test"
        }
    )


    assert response.status_code == 400

    assert "registration required" in response.json["message"]





# Test 3:
# Invalid URL
def test_invalid_url():

    response = client.post(
        "/submit",
        json={
            "name": "Abeeha",
            "registration": "FA22-BCS-001",
            "title": "DevOps Lab Mid",
            "url": "wrong-url"
        }
    )


    assert response.status_code == 400

    assert response.json["message"] == "Invalid URL"