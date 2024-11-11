# MUTANT DETECTOR: MAGNETO'S CORP
![Magneto](assets/magneto.avif)

## Table of contents
- [MUTANT DETECTOR: MAGNETO'S CORP](#mutant-detector-magnetos-corp)
  - [Table of contents](#table-of-contents)
  - [Description](#description)
  - [Technologies](#technologies)
  - [Installation](#installation)
    - [Using Docker](#using-docker)
  - [Usage](#usage)
    - [Mutant Detection](#mutant-detection)
    - [Stats](#stats)
    - [Using CURL](#using-curl)
      - [Mutant Detection](#mutant-detection-1)
      - [Stats](#stats-1)
  - [Cloud Testing](#cloud-testing)
  - [Tests](#tests)

## Description
This project is a mutant detector, which is able to detect if a human is a mutant

## Technologies
- Python
- FastAPI
- Docker
- Docker Compose
- Terraform

## Installation
1. Clone the repository
2. Create a virtual environment with `python -m venv venv`
3. Activate the virtual environment with `source venv/bin/activate`
4. Install the dependencies with `pip install -r requirements.txt`
5. Create the `.env` file with the following variables:
    ```bash
    DB_SOURCE="json"
    ```
6. Run `fastapi run app/main.py --port 8000` to start the server

### Using Docker
1. Run `docker-compose up` to start the server

## Usage

### Mutant Detection
1. Open your browser and go to `http://localhost:8000/docs`
2. Click on the `POST /mutant/` button
3. Click on the `Try it out` button
4. Write the DNA sequence in the `dna` field or use the example provided
5. Click on the `Execute` button

### Stats
1. Open your browser and go to `http://localhost:8000/docs`
2. Click on the `GET /stats/` button
3. Click on the `Try it out` button
4. Click on the `Execute` button

### Using CURL

You can also use curl to test the API. You just have to remove the `/docs` from the URL and add the endpoint you want to test.

#### Mutant Detection
```bash
curl -X 'POST' \
  'http://localhost:8000/mutant/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "dna": [
    "ATGCGA",
    "CAGTGC",
    "TTATGT",
    "AGAAGG",
    "CCCCTA",
    "TCACTG"
  ]
}'
```

#### Stats
```bash
curl -X 'GET' \
  'http://localhost:8000/stats/' \
  -H 'accept: application/json'
```


## Cloud Testing

This project is deployed in ECS using AWS Fargate. The URL is: [http://mutant-alb-341917332.us-east-2.elb.amazonaws.com/docs](http://mutant-alb-341917332.us-east-2.elb.amazonaws.com/docs)

## Tests
To run the tests, run `pytest tests/` in the root directory
