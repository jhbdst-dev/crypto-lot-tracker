# crypto-lot-tracker

암호화폐 거래내역 기반
보유자산 / 투자손익 / 개별 매수 손익 계산 프로젝트

암호화폐 거래내역을 기반으로
보유자산과 손익을 계산하고,

전체 평균 손익뿐만 아니라
개별 매수 거래내역 기준의 손익 상태까지
추적하고 분석하기 위한 프로젝트이다.

---

## 프로젝트를 하게 된 이유

코인 거래를 하다 보면 같은 코인을 여러 번 나눠 매수하는 경우가 많다.
특히 가격이 하락할 때마다 추가 매수를 하게 되면 거래 횟수가 늘어나고,
매수 시점마다 투자 금액과 보유 수량도 모두 달라진다.

그래서 전체 평균 단가만 보면 손실처럼 보이더라도,
실제로는 특정 매수 물량은 현재 가격 기준으로 수익 상태일 수 있다.

나는 이런 거래 기록들을 기준으로
각 매수 물량의 수익률과 손익 상태를 정확하게 추적하고,
어떤 물량을 회전 매매에 활용할 수 있는지 분석하고 싶었다.

또한 나중에는 거래 기록을 기반으로 손익 및 세금 계산까지 할 수 있도록
이 프로젝트를 진행하게 되었다.

---

## 필드 설명

### trades (거래내역 데이터)

- id : 거래번호
- coin : 코인명
- market : 거래 마켓
- trade_type : 거래 종류 (BUY / SELL)
- price : 거래단가
- quantity : 거래수량
- fee : 수수료
- settlement_amount : 정산금액
- executed_at : 체결시간
- trade_amount : 거래금액

### 계산 결과 데이터

- total_quantity : 총 보유수량
- total_buy_amount : 총 매수금액
- average_buy_price : 평균 매수가
- current_value : 현재 평가금액
- profit_loss : 평가손익
- profit_rate : 수익률

### 거래별 데이터

- value : 거래별 평가금액
- transaction_profit_loss : 거래별 평가손익
- transaction_profit_rate : 거래별 수익률

### 매도 데이터

- sell_quantity : 매도 수량
- sell_price : 매도 가격
- sell_trade_amount : 매도 거래금액
- sell_fee_amount : 매도 수수료
- sell_settlement_amount : 매도 정산금액
- sold_buy_amount : 매도한 코인의 원가
- realized_profit_loss : 실현손익
- realized_profit_rate : 실현수익률
- remaining_quantity : 남은 보유수량
- remaining_buy_amount : 남은 총 매수금액
- remaining_average_buy_price : 남은 평균 매수가

---

## 거래 데이터 계산 흐름

입력 데이터

- price
- quantity
- fee_rate

↓

trade_amount 계산
(price × quantity)

↓

fee_amount 계산
(trade_amount × fee_rate)

↓

settlement_amount 계산
(trade_amount + fee_amount)

↓

보유자산 계산

- 총 매수금액
- 평균 매수가
- 평가손익
- 수익률

↓

거래별 손익 계산

- 거래별 평가금액
- 거래별 평가손익
- 거래별 수익률

↓

매도 및 실현손익 계산

- 매도 거래금액
- 매도 수수료
- 매도 정산금액
- 매도 원가
- 실현손익
- 실현수익률
- 남은 보유수량
- 남은 총 매수금액
- 남은 평균 매수가

---

## 파일 구조

### database.py : 거래내역 가져오는 파일

- PostgreSQL 연결
- 거래내역 조회

### calculator.py : 숫자 계산하는 파일

#### calculate_asset()

- 총 보유수량 계산
- 총 매수금액 계산
- 평균 매수가 계산
- 현재 평가금액 계산
- 평가손익 계산
- 수익률 계산

#### calculate_sell()

- 매도 거래금액 계산
- 매도 수수료 계산
- 매도 정산금액 계산
- 실현손익 계산
- 실현수익률 계산
- 남은 보유수량 계산
- 남은 총 매수금액 계산
- 남은 평균 매수가 계산

### main.py : 전체 실행 순서 조립하는 파일

- 거래내역 조회
- 현재가 입력
- 매도 수량, 매도 가격 입력
- calculate_asset() 요청
- calculate_sell() 요청
- 보유자산 및 매도 결과 화면 출력

### db_test.py : 테스트 파일

- 기능 테스트

---

## 프로젝트 진행 흐름

PHASE 1 - 매수 계산 엔진 ✅

- 총 보유수량
- 총 매수금액
- 평균 매수가
- 평가손익
- 거래별 손익

PHASE 2 - 매도 및 실현손익

- 매도 처리
- 실현손익 계산
- 남은 보유자산 재계산

PHASE 3 - 데이터 구조 및 자동화

- 거래내역 구조 정리
- 업비트 API 연동

PHASE 4 - 서비스 확장

- UI 및 시각화
- 세금 계산
- 추가 분석 기능

---

## 개발 로그

### PHASE 1 - 보유자산 계산 MVP ✅

- [DB 구축] 2026-06-04 : PostgreSQL 설치 및 trades 테이블 생성 (터미널 PostgreSQL 사용법)
- [거래내역 조회] 2026-06-05 : Python 가상 환경 셋팅, Python과 PostgreSQL 연결, DB Test
- [자산 계산] 2026-06-08 : 총 보유수량, 총 매수금액, 평균 매수가 계산
- [ 보유자산 화면 출력] 2026-06-15 : 현재가 입력, 현재 평가금액 계산, 평가손익 계산, 수익률 계산, 출력 형식 개선

### PHASE 1.5 - 개별 거래내역 손익 확인 화면

- [거래별 손익 확인]2026-06-16 : 거래내역 출력, 각 거래에서 필요한 데이터 확인하기, 현재가와 매수가 비교, 거래별 현재 평가금액, 거래별 평가손익, 거래별 수익률 계산, 콘솔 출력
- [계산 기준 정리] 2026-06-17 : 수수료율 추가, 거래금액/수수료/정산금액 계산, settlement_amount 기준 총 매수금액·평균 매수가·평가손익 계산

### PHASE2 - 매도 및 실현손익 계산

- [매도 입력] 2026-06-21
  : sell_quantity, sell_price 추가,
  calculate_sell() 함수 생성

- [매도 정산] 2026-06-21
  : sell_trade_amount,
  sell_fee_amount,
  sell_settlement_amount 계산

- [실현손익] 2026-06-21
  : sold_buy_amount,
  realized_profit_loss,
  realized_profit_rate 계산

- [남은 자산 재계산] 2026-06-21
  : remaining_quantity,
  remaining_buy_amount,
  remaining_average_buy_price 계산

---

## PHASE1 - 보유자산 계산 엔진

1. PostgreSQL에서 거래내역 조회
2. 현재가(current_price) 입력
3. 총 보유수량(total_quantity) 계산
4. 총 매수금액(total_buy_amount) 계산
5. 평균 매수가(average_buy_price) 계산
6. 현재 평가금액(current_value) 계산
7. 평가손익(profit_loss) 계산
8. 수익률(profit_rate) 계산
9. 거래별 평가금액(value) 계산
10. 거래별 평가손익(transaction_profit_loss) 계산
11. 거래별 수익률(transaction_profit_rate) 계산
12. 보유자산 및 거래별 손익 화면 출력

## PHASE2 - 매도 및 실현손익 계산

1. 매도 수량(sell_quantity), 매도 가격(sell_price) 입력
2. calculate_sell() 함수 생성 및 입력값 전달
3. 매도 거래금액(sell_trade_amount) 계산
4. 매도 수수료(sell_fee_amount) 계산
5. 매도 정산금액(sell_settlement_amount) 계산
6. 평균 매수가 기준 매도 원가(sold_buy_amount) 계산
7. 실현손익(realized_profit_loss) 계산
8. 실현수익률(realized_profit_rate) 계산
9. 남은 보유수량(remaining_quantity) 계산
10. 남은 총 매수금액(remaining_buy_amount) 계산
11. 남은 평균 매수가(remaining_average_buy_price) 계산
12. 매도 결과 화면 출력

## PHASE2.5 - 매도 계산 정리

1. calculate_sell()은 print 없이 return만 하게 정리
2. main.py에서 매도 결과 화면 출력
3. README.md에 PHASE2 완료 내용 정리
4. 2026_06_21.md에 최종 계산 흐름 정리

## PHASE3 - 데이터 구조 정리

1. BUY / SELL 거래내역 구조 통일
2. DB trades 테이블에 sell 거래도 저장할지 정리
3. trade_type == "BUY" / "SELL" 기준으로 계산 분기
4. 지금 하드코딩한 sell_quantity, sell_price를 거래내역 데이터로 옮길 준비

## PHASE4 - Upbit API 연동

1. 현재가 API 가져오기
2. 보유자산 조회
3. 체결내역 조회
4. DB 저장 자동화
