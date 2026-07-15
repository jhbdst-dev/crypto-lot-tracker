import hashlib
import os
import uuid
from urllib.parse import urlencode, unquote

import jwt
import requests
from dotenv import load_dotenv


load_dotenv()

ACCESS_KEY = os.getenv("UPBIT_ACCESS_KEY")
SECRET_KEY = os.getenv("UPBIT_SECRET_KEY")

BASE_URL = "https://api.upbit.com"
PATH = "/v1/orders/closed"

START_DATE = "2025-01-01T00:00:00+09:00"
END_DATE = "2025-01-08T00:00:00+09:00"

params = {
    "state": "done",
    "start_time": START_DATE,
    "end_time": END_DATE,
    "limit": 100,
}

query_string = unquote(urlencode(params))

query_hash = hashlib.sha512(
    query_string.encode("utf-8")
).hexdigest()

payload = {
    "access_key": ACCESS_KEY,
    "nonce": str(uuid.uuid4()),
    "query_hash": query_hash,
    "query_hash_alg": "SHA512",
}

jwt_token = jwt.encode(payload, SECRET_KEY)
headers = {
    "Authorization": f"Bearer {jwt_token}",
}

response = requests.get(
    BASE_URL + PATH,
    params=params,
    headers=headers,
    timeout=10,
)

print("상태 코드:", response.status_code)
print("응답 내용:", response.json())