import "./CoinDetailPage.css"
import { useEffect, useState } from "react"
import { useNavigate, useParams } from "react-router-dom"

type BuyTrade = {
    uuid: string
    created_at: string
    buy_price: number
    quantity: number
    buy_amount: number
    fee_amount: number
    total_buy_amount: number
    evaluation_amount: number
    evaluation_profit: number
    profit_rate: number
}

type CoinDetailData = {
    market: string
    coin_name: string
    current_price: number
    quantity: number
    average_buy_price: number
    total_buy_amount: number
    evaluation_amount: number
    evaluation_profit: number
    profit_rate: number
    buy_trades: BuyTrade[]
}

function CoinDetailPage() {

    const navigate = useNavigate()
    const { market } = useParams<{ market: string }>()

    const [coinData, setCoinData] =
        useState<CoinDetailData | null>(null)

    useEffect(() => {
        if (!market) {
            return
        }

        const apiMarket = market.startsWith("KRW-")
            ? market
            : `KRW-${market}`

        async function fetchCoinDetail() {
            try {
                const response = await fetch(
                    `http://127.0.0.1:8000/coins/${apiMarket}`
                )

                if (!response.ok) {
                    throw new Error(
                        "코인 상세 정보를 가져오지 못했습니다."
                    )
                }

                const data: CoinDetailData =
                    await response.json()

                setCoinData(data)
            } catch (error) {
                console.error(error)
            }
        }

        fetchCoinDetail()
    }, [market])


    function handleBack() {
        navigate(-1)
    }

    function handleRefresh() {
        console.log("새로고침")
    }

    function handleSellPreview(tradeId: string) {
        navigate(
            `/coins/${symbol}/trades/${tradeId}/sell`
        )
    }

    if (!coinData) {
        return <main>불러오는 중...</main>
    }

    const symbol = coinData.market.replace("KRW-", "")

    const coinIcon =
        symbol === "BTC"
            ? "₿"
            : symbol === "ETH"
            ? "Ξ"
            : "X"

    return (
        <main className="coin-detail-page">

            <header className="coin-detail-header">

                <button
                    className="back-button"
                    type="button"
                    onClick={handleBack}
                >
                    ←
                </button>

                <h1 className="page-title">
                    {symbol} {coinData.coin_name}
                </h1>

                <button
                    className="refresh-button"
                    type="button"
                    onClick={handleRefresh}
                >
                    ↻
                </button>

            </header>

            <section className="coin-detail-content">

                <section className="coin-summary-card">
                    
                    {/* coin-summary-card-top */}
                    <div className="coin-summary-card__top">

                        <div className="coin-summary-info">

                            <div className="coin-summary-icon">
                                {coinIcon}
                            </div>

                            <div className="coin-summary-name">
                                    <h2>
                                        {coinData.coin_name} ({symbol})
                                    </h2>
                            </div>

                        </div>

                        <div className="coin-summary-price">

                            <span>현재가</span>

                            <strong>
                                {Math.round(
                                    coinData.current_price
                                ).toLocaleString("ko-KR")}원
                            </strong>

                        </div>

                    </div>

                    {/* coin-summary-card-body */}
                    <div className="coin-summary-card__body">

                        <div className="summary-item">
                            <span>전체 보유수량</span>
                            <strong>
                                {coinData.quantity.toLocaleString(
                                    "ko-KR",
                                    {
                                        maximumFractionDigits: 8,
                                    }
                                )} {symbol}
                            </strong>
                        </div>

                        <div className="summary-item">
                            <span>평균 매수가</span>
                            <strong>
                                {Math.round(
                                    coinData.average_buy_price
                                ).toLocaleString("ko-KR")}원
                            </strong>
                        </div>

                        <div className="summary-item">
                            <span>전체 매수원금</span>
                            <strong>
                                {Math.round(
                                    coinData.total_buy_amount
                                ).toLocaleString("ko-KR")}원
                            </strong>
                        </div>

                        <div className="summary-item">
                            <span>평가금액</span>
                            <strong>
                                {Math.round(
                                    coinData.evaluation_amount
                                ).toLocaleString("ko-KR")}원
                            </strong>
                        </div>

                        <div className="summary-item">
                            <span>평가손익</span>
                            <strong
                                className={
                                    coinData.evaluation_profit >= 0
                                        ? "profit"
                                        : "loss"
                                }
                            >
                                {coinData.evaluation_profit >= 0 ? "+" : ""}
                                {Math.round(
                                    coinData.evaluation_profit
                                ).toLocaleString("ko-KR")}원
                            </strong>
                        </div>

                        <div className="summary-item">
                            <span>수익률</span>
                            <strong
                                className={
                                    coinData.profit_rate >= 0
                                        ? "profit"
                                        : "loss"
                                }
                            >
                                {coinData.profit_rate >= 0 ? "+" : ""}
                                {coinData.profit_rate.toFixed(2)}%
                            </strong>
                        </div>

                    </div>

                </section>

            {/* 개별 매수 거래 목록 */}
            <section className="trade-list">

                {/* 개별 매수 거래 목록 헤더 */}
                <div className="trade-list__header">

                    <h2>개별 매수 거래 목록</h2>

                    <button
                        className="trade-list__sort-button"
                        type="button"
                    >
                        최신순 ▼
                    </button>

                </div>

                {/* 개별 매수 거래 목록 메인 */}
                {coinData.buy_trades.map((trade) => (
                    <article
                        className="trade-card"
                        key={trade.uuid}
                    >
                        <div className="trade-card__header">
                            <time dateTime={trade.created_at}>
                                {trade.created_at}
                            </time>

                            <span className="trade-card__id">
                                거래 ID {trade.uuid.slice(0, 8)}
                            </span>
                        </div>

                        <div className="trade-card__body">

                            <div className="trade-item">
                                <span>매수가</span>
                                <strong>
                                    {Math.round(
                                        trade.buy_price
                                    ).toLocaleString("ko-KR")}원
                                </strong>
                            </div>

                            <div className="trade-item">
                                <span>남은 수량</span>
                                <strong>
                                    {trade.quantity.toLocaleString(
                                        "ko-KR",
                                        {
                                            maximumFractionDigits: 8,
                                        }
                                    )} {symbol}
                                </strong>
                            </div>

                            <div className="trade-item">
                                <span>매수원금</span>
                                <strong>
                                    {Math.round(
                                        trade.buy_amount
                                    ).toLocaleString("ko-KR")}원
                                </strong>
                            </div>

                            <div className="trade-item">
                                <span>평가금액</span>
                                <strong>
                                    {Math.round(
                                        trade.evaluation_amount
                                    ).toLocaleString("ko-KR")}원
                                </strong>
                            </div>

                            <div className="trade-item">
                                <span>평가손익</span>
                                <strong
                                    className={
                                        trade.evaluation_profit >= 0
                                            ? "profit"
                                            : "loss"
                                    }
                                >
                                    {trade.evaluation_profit >= 0 ? "+" : ""}
                                    {Math.round(
                                        trade.evaluation_profit
                                    ).toLocaleString("ko-KR")}원
                                </strong>
                            </div>

                            <div className="trade-item">
                                <span>수익률</span>
                                <strong
                                    className={
                                        trade.profit_rate >= 0
                                            ? "profit"
                                            : "loss"
                                    }
                                >
                                    {trade.profit_rate >= 0 ? "+" : ""}
                                    {trade.profit_rate.toFixed(2)}%
                                </strong>
                            </div>

                        </div>

                        <button
                            className="trade-card__sell-button"
                            type="button"
                            onClick={() =>
                                handleSellPreview(trade.uuid)
                            }
                        >
                            매도 계산하기
                        </button>
                    </article>
                ))}

            </section>

            </section>

        </main>
    )
}

export default CoinDetailPage