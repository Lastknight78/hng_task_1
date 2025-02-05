from fastapi import FastAPI, status, HTTPException
import httpx
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

origins = ["*"]


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

def is_prime(num : int):
    if num < 0:
        return False
    if num < 2:
        return False
    for i in range (2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

def is_perfect(num : int):
    if num < 0:
        return False
    if num < 2:
        return False
    divisors = [1]
    for i in range(2, num // 2 + 1):
        if num % i == 0:
            divisors.append(i)
    return sum(divisors) == num

def is_armstrong(num):
    if num < 0:
        return 'even' if num % 2 == 0 else 'odd'

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
    if num < 0:
        num = abs(num)
        sums = -sum(int(i) for i in str(num))
    else:
        sums = sum(int(i) for i in str(abs(num)))
    return sums

app = FastAPI()

@app.get("/classify-number", status_code=status.HTTP_200_OK)
async def get_math_fact(number):
    url = f"http://numbersapi.com/{number}/math?json=true"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        
    if response.status_code == 200:
        number = int(number)
        return {
                "number" : number,
                "is_prime": is_prime(number),
                "is_perfect": is_perfect(number),
                "properties" : is_armstrong(number),
                "digit_sum" : sum_number(number),
                "number": number, "fun_fact": response.json()["text"]
                }
    else:
        return JSONResponse(content={"number":"alphabet","error": True},status_code=400)

