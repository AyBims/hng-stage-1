# Number Classification API

A REST API that analyzes numbers and returns their mathematical properties along with interesting facts.

## Features

- Determines if a number is prime
- Determines if a number is perfect
- Identifies Armstrong numbers
- Calculates digit sum
- Provides odd/even classification
- Fetches fun mathematical facts about numbers
- CORS enabled
- JSON response format
- Error handling for invalid inputs

## API Specification

### Endpoint

```
GET /api/classify-number?number={number}
```

### Success Response (200 OK)

```json
{
    "number": 371,
    "is_prime": false,
    "is_perfect": false,
    "properties": ["armstrong", "odd"],
    "digit_sum": 11,
    "fun_fact": "371 is an Armstrong number because 3^3 + 7^3 + 1^3 = 371"
}
```

### Error Response (400 Bad Request)

```json
{
    "number": "alphabet",
    "error": true
}
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/AyBims/hng-stage-1.git
cd nhng-stage-1
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running Locally

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## Dependencies

- Python 3.8+
- FastAPI
- Uvicorn
- Requests
- Pydantic

## Deployment

This API can be deployed to any platform that supports Python applications. Some recommended platforms:

- Heroku
- DigitalOcean
- AWS Elastic Beanstalk
- Google Cloud Platform

## Testing

Run the tests using pytest:

```bash
pytest
```

## API Documentation

Once the server is running, you can access the automatic interactive API documentation at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## License

MIT

## Author

[Ayomide Adeshina]
