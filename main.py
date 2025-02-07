from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import math
import requests
import json
import re
from typing import List, Dict, Union
from pydantic import BaseModel

app = FastAPI(title="Number Classification API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ErrorResponse(BaseModel):
    number: str
    error: bool = True

class NumberResponse(BaseModel):
    number: int
    is_prime: bool
    is_perfect: bool
    properties: List[str]
    digit_sum: int
    fun_fact: str

def is_prime(n: int) -> bool:
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(abs(n))) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n: int) -> bool:
    """Check if a number is perfect."""
    if n <= 1:
        return False
    sum_divisors = sum(i for i in range(1, abs(n)) if n % i == 0)
    return sum_divisors == abs(n)

def is_armstrong(n: int) -> bool:
    """Check if a number is an Armstrong number."""
    num_str = str(abs(n))
    power = len(num_str)
    return sum(int(digit) ** power for digit in num_str) == abs(n)

def get_digit_sum(n: int) -> int:
    """Calculate the sum of digits."""
    return sum(int(digit) for digit in str(abs(n)))

def get_properties(n: int) -> List[str]:
    """Get the properties of a number (armstrong and odd/even)."""
    properties = []
    if is_armstrong(n):
        properties.append("armstrong")
    
    if n % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")
    
    return properties

def clean_fun_fact(text: str) -> str:
    """Clean and sanitize fun fact text to ensure valid JSON."""
    # Remove any non-ASCII characters
    text = text.encode('ascii', 'ignore').decode()
    
    # Remove new lines and extra whitespace
    text = ' '.join(text.split())
    
    # Remove any other characters that might break JSON
    text = re.sub(r'[^\x20-\x7E]', '', text)
    
    return text

def get_fun_fact(n: int) -> str:
    """Get a fun fact about the number from the Numbers API."""
    try:
        response = requests.get(f"http://numbersapi.com/{n}/math")
        if response.status_code == 200:
            # Clean and validate the fun fact
            fact = clean_fun_fact(response.text)
            # Verify it can be encoded as JSON
            json.dumps({"test": fact})
            return fact
        else:
            raise requests.RequestException
    except (requests.RequestException, json.JSONDecodeError):
        # Fallback fun fact if API fails or returns invalid JSON
        if is_armstrong(n):
            digits = list(str(abs(n)))
            power = len(digits)
            calculation = " + ".join([f"{d}^{power}" for d in digits])
            return clean_fun_fact(f"{n} is an Armstrong number because {calculation} = {abs(n)}")
        return f"{n} is {'even' if n % 2 == 0 else 'odd'}"

@app.get("/api/classify-number")
async def classify_number(number: str = None):
    """
    Classify a number and return its properties.
    """
    if number is None:
        return JSONResponse(
            status_code=400,
            content={"number": "", "error": True}
        )
    
    try:
        # First try to convert to float to accept decimal numbers
        float_num = float(number)
        # Then convert to int for the calculations
        num = int(float_num)
        
        response = NumberResponse(
            number=num,
            is_prime=is_prime(num),
            is_perfect=is_perfect(num),
            properties=get_properties(num),
            digit_sum=get_digit_sum(num),
            fun_fact=get_fun_fact(num)
        )
        
        # Validate the entire response can be serialized to JSON
        response_dict = response.dict()
        json.dumps(response_dict)
        
        return JSONResponse(content=response_dict)
    except ValueError:
        return JSONResponse(
            status_code=400,
            content={"number": number, "error": True}
        )
    except json.JSONDecodeError:
        # If JSON serialization fails, return with a safe fallback fun fact
        response = NumberResponse(
            number=num,
            is_prime=is_prime(num),
            is_perfect=is_perfect(num),
            properties=get_properties(num),
            digit_sum=get_digit_sum(num),
            fun_fact=f"{num} is {'even' if num % 2 == 0 else 'odd'}"
        )
        return JSONResponse(content=response.dict())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
