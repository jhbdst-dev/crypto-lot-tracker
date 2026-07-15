import os
import uuid

import jwt
import requests
from dotenv import load_dotenv


load_dotenv()

ACCESS_KEY = os.getenv("UPBIT_ACCESS_KEY")
SECRET_KEY = os.getenv("UPBIT_SECRET_KEY")

BASE_URL = "https://api.upbit.com"
PATH = "/v1/accounts"

payload = {
    "access_key": ACCESS_KEY,
    "nonce": str(uuid.uuid4()),
}

jwt_token = jwt.encode(payload, SECRET_KEY)

headers = {
    "Authorization": f"Bearer {jwt_token}",
}

response = requests.get(
    BASE_URL + PATH,
    headers=headers,
    timeout=10,
)

print("상태 코드:", response.status_code)
print(response.json())