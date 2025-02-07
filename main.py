from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import math
import requests
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
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n: int) -> bool:
    """Check if a number is perfect."""
    if n <= 1:
        return False
    sum_divisors = sum(i for i in range(1, n) if n % i == 0)
    return sum_divisors == n

def is_armstrong(n: int) -> bool:
    """Check if a number is an Armstrong number."""
    num_str = str(n)
    power = len(num_str)
    return sum(int(digit) ** power for digit in num_str) == n

def get_digit_sum(n: int) -> int:
    """Calculate the sum of digits."""
    return sum(int(digit) for digit in str(n))

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

def get_fun_fact(n: int) -> str:
    """Get a fun fact about the number from the Numbers API."""
    try:
        response = requests.get(f"http://numbersapi.com/{n}/math")
        if response.status_code == 200:
            # Remove any special characters or formatting that might break JSON
            fact = response.text.strip().replace('\n', ' ').replace('\r', '')
            return fact
        else:
            # Fallback fun fact if API fails
            if is_armstrong(n):
                digits = list(str(n))
                power = len(digits)
                calculation = " + ".join([f"{d}^{power}" for d in digits])
                return f"{n} is an Armstrong number because {calculation} = {n}"
            return f"{n} is {'even' if n % 2 == 0 else 'odd'}"
    except:
        # Fallback for connection errors
        return f"Number {n}"

@app.get("/api/classify-number")
async def classify_number(number: str = None):
    """
    Classify a number and return its properties.
    """
    # Handle missing number parameter
    if number is None:
        return JSONResponse(
            status_code=400,
            content={"number": "", "error": True}
        )
    
    # Handle invalid number input
    try:
        num = int(number)
    except ValueError:
        return JSONResponse(
            status_code=400,
            content={"number": number, "error": True}
        )
    
    response = NumberResponse(
        number=num,
        is_prime=is_prime(num),
        is_perfect=is_perfect(num),
        properties=get_properties(num),
        digit_sum=get_digit_sum(num),
        fun_fact=get_fun_fact(num)
    )
    
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
