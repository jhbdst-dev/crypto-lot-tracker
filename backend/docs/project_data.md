# 프로젝트 데이터 정리

---

## 주문내역 (upbit_api.py)

### API에서 사용하는 데이터

- market
- side
- price
- executed_volume
- executed_funds
- paid_fee
- created_at

### DB에 저장하는 데이터

- uuid
- market
- side
- ord_type
- state
- price
- volume
- executed_volume
- executed_funds
- paid_fee
- trades_count
- created_at

---

## 현재 보유자산 (upbit_accounts.py)

### API에서 사용하는 데이터

- currency
- balance
- locked
- avg_buy_price

### 프로젝트에서 사용하는 데이터

```python
assets = {
    "KRW-BTC": {
        "quantity": balance + locked,
        "average_buy_price": avg_buy_price,
    }
}
```

---

## 실시간 현재가 (upbit_ws.py)

### API에서 사용하는 데이터

- code
- trade_price

### 프로젝트에서 사용하는 데이터

```python
market = data["code"]
current_price = data["trade_price"]
```
