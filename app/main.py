import fastapi

from app import detector, validator
from app.db import db_gateway

app = fastapi.FastAPI()
db = db_gateway.DBGateway()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.post("/mutant/")
async def is_mutant(
    dna: dict[str, list[str]] = fastapi.Body(
        ...,
        example={
            "dna": ["ATGCGA", "CAGTGC", "TTATGT", "AGAAGG", "CCCCTA", "TCACTG"]
        },
    )
):
    """
    Detects whether a given DNA sequence belongs to a mutant or a human.
    Args:
        dna_list (list[str]): A list of strings representing the DNA sequence.
                              Example: ["ATGCGA", "CAGTGC", "TTATGT", "AGAAGG",
                              "CCCCTA", "TCACTG"]
    Returns:
        fastapi.Response:
            - 200 status code with "Mutant detected" if the DNA sequence
                belongs to a mutant.
            - 403 status code with "Human detected" if the DNA sequence
                belongs to a human.
            - 400 status code with "Invalid DNA sequence" if the DNA sequence
                is invalid.
    """
    try:
        dna_list = dna.get("dna", [])
        v = validator.Validator()
        is_valid = v.validate(dna_list)
    except Exception as e:
        return fastapi.Response(
            status_code=400, content=str(e), media_type="text/plain"
        )

    if not is_valid:
        return fastapi.Response(
            status_code=400,
            content="Invalid DNA sequence",
            media_type="text/plain",
        )

    d = detector.Detector()
    db.write_sequences(dna_list)

    if d.detect(dna_list):
        return fastapi.Response(
            status_code=200, content="Mutant detected", media_type="text/plain"
        )

    return fastapi.Response(
        status_code=403, content="Human detected", media_type="text/plain"
    )


@app.get("/stats/")
async def get_stats():
    """
    Returns statistics about the DNA sequences analyzed.
    Returns:
        dict: A dictionary containing the count of mutants and humans detected.
    """
    d = detector.Detector()
    data = db.read_detections()
    sequences = data.get("sequences", [])
    mutants = sum(1 for sequence in sequences if d.detect(sequence))
    humans = len(sequences) - mutants
    ratio = mutants / (humans or 1)

    return {
        "count_mutant_dna": mutants,
        "count_human_dna": humans,
        "ratio": ratio,
    }


@app.get("/db/")
async def read_db():
    """
    Returns the raw data from the database.
    Returns:
        dict: A dictionary containing the raw data from the database.
    """
    data = db.read_detections()
    return data
