import websocket

# WebSocket 연결 객체 생성
ws = websocket.WebSocket()

# 업비트 서버 연결
ws.connect("wss://api.upbit.com/websocket/v1")

# 구독 요청
ws.send('[{"ticket":"test"},{"type":"ticker","codes":["KRW-XRP"]}]')

# 현재가 수신
data = ws.recv()

print(data)