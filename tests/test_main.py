import json
import os

import requests

BASE_URL = "http://localhost:8000"


def test_read_root():
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_is_mutant_valid_mutant_dna():
    response = requests.post(
        f"{BASE_URL}/mutant/",
        json={
            "dna": ["ATGCGA", "CAGTGC", "TTATGT", "AGAAGG", "CCCCTA", "TCACTG"]
        },
    )
    assert response.status_code == 200
    assert response.text == "Mutant detected"


def test_is_mutant_valid_human_dna():
    response = requests.post(
        f"{BASE_URL}/mutant/",
        json={
            "dna": ["ATGCCA", "CTGTGC", "TTATGT", "AGAAGG", "CACCTA", "TCACTG"]
        },
    )
    assert response.status_code == 403
    assert response.text == "Human detected"


def test_is_mutant_invalid_length():
    response = requests.post(
        f"{BASE_URL}/mutant/",
        json={"dna": ["ATGCGA", "CAGTGC", "TTATGT", "AGAAGG", "CCCCTA"]},
    )
    assert response.status_code == 400
    assert (
        response.text
        == "Validation error: All DNA sequences must be of the same length."
    )


def test_is_mutant_invalid_characters():
    response = requests.post(
        f"{BASE_URL}/mutant/",
        json={
            "dna": ["ATGCGA", "CAGTGC", "TTATGT", "AGAAGG", "CCCCTA", "TCACTZ"]
        },
    )
    assert response.status_code == 400
    assert response.text == (
        "Validation error: DNA sequences should contain valid characters "
        "(ACGT)"
    )


def test_get_stats():
    response = requests.get(f"{BASE_URL}/stats/")
    assert response.status_code == 200
    data = response.json()
    assert "count_mutant_dna" in data
    assert "count_human_dna" in data
    assert "ratio" in data


def test_read_db():
    response = requests.get(f"{BASE_URL}/db/")
    assert response.status_code == 200
    data = response.json()
    assert "sequences" in data


def test_cleanup():
    file_path = "app/db/sequences.json"
    if os.path.exists(file_path):
        with open(file_path, "r+") as file:
            data = json.load(file)
            if "sequences" in data and len(data["sequences"]) > 1:
                data["sequences"] = data["sequences"][:-2]
                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()
