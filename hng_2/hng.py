from fastapi import FastAPI, status, HTTPException
import httpx
from pydantic import BaseModel

class number(BaseModel):
    num : int
    
app = FastAPI()

def is_prime(num : int):
    if num < 2:
        return False
    for i in range (2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

def is_perfect(num : int):
    if num < 2:
        return False
    divisors = [1]
    for i in range(2, num // 2 + 1):
        if num % i == 0:
            divisors.append(i)
    return sum(divisors) == num

def is_armstrong(num):
    digits = [int(d) for d in str(num)]
    power = len(digits)
    armstrong_num = sum(i**power for i in digits)
    if (armstrong_num == num) and num % 2 == 1:
        return ['armstrong','odd']
    elif (armstrong_num == num) and num % 2 == 0:
        return ['armstrong', 'even']
    elif num % 2 == 0:
        return 'even'
    return 'odd'
def sum_number(num):
    sums = sum(int(i) for i in str(num))
    return sums

app = FastAPI()

@app.get("/math-fact/{number}", status_code=status.HTTP_200_OK)
async def get_math_fact(number: int):
    url = f"http://numbersapi.com/{number}/math?json=true"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    
    if response.status_code == 200:
        
        return {"number": number, "math_fact": response.json()["text"],
                "number" : number,
                "is_prime": is_prime(number),
                "is_perfect": is_perfect(number),
                "properties" : is_armstrong(number),
                "digit_sum" : sum_number(number)
                }
    else:
        raise HTTPException(status_code=404, detail="Math fact not found")

