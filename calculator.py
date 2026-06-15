def calculate_asset(rows, current_prcie):
    
    print(f"현재가 = {current_prcie}")
    # 총 보유수량
    total_quantity = 0

    # 총 매수금액
    total_buy_amount = 0

    for row in rows:
        total_quantity += row[5]
        total_buy_amount += row[7]

    # 평균 매수가
    average_buy_price = total_buy_amount / total_quantity

    return total_quantity, total_buy_amount, average_buy_price