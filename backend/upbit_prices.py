from decimal import Decimal

import requests

# 업비트 API의 공통 기본 주소
BASE_URL = "https://api.upbit.com"

# 여러 코인의 현재 가격을 조회하는 함수
# markets: list[str] : 문자열로 이루어진 리스트를 매개변수로 받는다
# -> dict[str, Decimal] : 문자열을 키로하고 Decimal을 값으로 가지는 딕셔너리 반환
def get_current_prices(markets: list[str]) -> dict[str, Decimal]:

    # 업비트 현재가 조회 API에 요청을 보내고, 응답을 response 변수에 저장
    response = requests.get(

        # f-string을 이용해 업비트 현재가 조회 API 주소 생성
        f"{BASE_URL}/v1/ticker",

        # API에 전달할 조회 조건을 저장하는 딕셔너리
        params={

            # 리스트에 있는 여러 코인 이름을 쉼표(,)로 연결하여 하나의 문자열로 만듦
            "markets": ",".join(markets),
        },

        # 10초 안에 응답 없으면 요청 중단
        timeout=10,
    )

    # 응답 상태 코드가 200이 아니면 아래 코드 실행
    if response.status_code != 200:

        # RuntimeError 예외를 발생시키고 함수 실행 중단
        raise RuntimeError(response.json())

    # 현재 가격을 저장하기 위해 빈 딕셔너리 생성
    prices = {}

    # API에서 받은 현재가 정보를 하나씩 꺼내 ticker 변수에 저장하며 반복
    for ticker in response.json():

        # 현재 코인의 마켓이름을 꺼내 market 변수에 저장
        market = ticker["market"]

        # 현재 거래 가격을 문자열로 변환한 후, Decimal 자료형으로 반환하여 current_price에 저장
        current_price = Decimal(str(ticker["trade_price"]))

        # prices 딕셔너리에 코인 이름을 키로 하고 현재 가격을 값으로 저장
        prices[market] = current_price

    # 코인별 현재 가격이 저장된 딕셔너리를 반환한다
    return prices