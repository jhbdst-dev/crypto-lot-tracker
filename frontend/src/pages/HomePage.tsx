import "./HomePage.css"
import { Link } from "react-router-dom"
import { useEffect, useState } from "react"

type Coin = {
    market: string
    quantity: number
    average_buy_price: number
    current_price: number
    total_buy_amount: number
    evaluation_amount: number
    evaluation_profit: number
    profit_rate: number
}

type Summary = {
        total_buy_amount: number
        total_evaluation_amount: number
        total_evaluation_profit: number
        total_profit_rate: number
        coin_count: number
    }

function HomePage() {

    const [coins, setCoins] = useState<Coin[]>([])

    const [summary, setSummary] = useState<Summary | null>(null)

    function fetchHomeData() {
        fetch("http://127.0.0.1:8000/home")
            .then((response) => response.json())
            .then((data) => {
                setSummary(data.summary)
                setCoins(data.coins)
            })
            .catch((error) => {
                console.error("API 오류:", error)
            })
    }

    useEffect(() => {
        fetchHomeData()
    }, [])

    return (
        <main className="home-page">

            {/* 헤더 */}
            <header className="home-header">
                <h1 className="home-header__title">
                    내 보유 자산
                </h1>

                <button
                    className="home-header__refresh-button"
                    type="button"
                    onClick={fetchHomeData}
                >
                    ↻
                </button>
            </header>

            {/* 전체 자산 요약 */}
            <section className="asset-summary">
                <p className="asset-summary__label">
                    총 평가금액
                </p>

                <h2 className="asset-summary__price">
                        {summary
                            ? `${summary.total_evaluation_amount.toLocaleString("ko-KR", {
                                maximumFractionDigits: 0,
                            })}원`
                            : "불러오는 중..."
                        }
                </h2>

                <p
                    className={
                        summary &&
                        summary.total_evaluation_profit >= 0
                            ? "asset-summary__profit profit"
                            : "asset-summary__profit loss"
                    }
                >
                        {summary
                            ? `${summary.total_evaluation_profit.toLocaleString("ko-KR", {
                                maximumFractionDigits: 0,
                            })}원 │ ${summary.total_profit_rate.toFixed(2)}%`
                            : "불러오는 중..."
                        }
                </p>

                <div className="asset-summary__bottom">
                    <div>
                        <span>총 매수금액</span>
                        <strong>
                            {summary
                                ? `${summary.total_buy_amount.toLocaleString("ko-KR", {
                                    maximumFractionDigits: 0,
                                })}원`
                                : "불러오는 중..."
                            }
                        </strong>
                    </div>

                    <div>
                        <span>보유 코인</span>
                        <strong>{summary ? summary.coin_count : 0}개</strong>
                    </div>
                </div>
            </section>

            {/* 실제 보유 코인 카드 */}
            {coins.map((coin) => {
                const symbol = coin.market.replace("KRW-", "")

            return (
                    <Link
                        className="coin-card"
                        to={`/coins/${symbol}`}
                        key={coin.market}
                    >
                        <div className="coin-card__header">
                            <div className="coin-info">
                                <div className="coin-icon">
                                    {symbol}
                                </div>

                                <div className="coin-name">
                                    <h3>{symbol}</h3>
                                    <p>{coin.market}</p>
                                </div>
                            </div>

                            <div className="coin-current-price">
                                <span>현재가</span>
                                <strong>
                                    {coin.current_price.toLocaleString("ko-KR", {
                                        maximumFractionDigits: 0,
                                    })}원
                                </strong>
                            </div>
                        </div>

                        <div className="coin-card__body">
                            <div className="coin-card__item">
                                <span>보유수량</span>
                                <strong>
                                    {coin.quantity} {symbol}
                                </strong>
                            </div>

                            <div className="coin-card__item">
                                <span>평균 매수가</span>
                                <strong>
                                    {coin.average_buy_price.toLocaleString("ko-KR", {
                                        maximumFractionDigits: 0,
                                    })}원
                                </strong>
                            </div>

                            <div className="coin-card__item">
                                <span>평가금액</span>
                                <strong>
                                    {coin.evaluation_amount.toLocaleString("ko-KR", {
                                        maximumFractionDigits: 0,
                                    })}원
                                </strong>
                            </div>

                            <div className="coin-card__item">
                                <span>평가손익</span>
                                <strong
                                    className={
                                        coin.evaluation_profit >= 0
                                            ? "profit"
                                            : "loss"
                                    }
                                >
                                    {coin.evaluation_profit >= 0 ? "+" : ""}
                                    {coin.evaluation_profit.toLocaleString("ko-KR", {
                                        maximumFractionDigits: 0,
                                    })}원
                                </strong>
                            </div>

                            <div className="coin-card__item">
                                <span>수익률</span>
                                <strong
                                    className={
                                        coin.profit_rate >= 0
                                            ? "profit"
                                            : "loss"
                                    }
                                >
                                    {coin.profit_rate >= 0 ? "+" : ""}
                                    {coin.profit_rate.toFixed(2)}%
                                </strong>
                            </div>

                            <div className="coin-card__item">
                                <span>총 매수금액</span>
                                <strong>
                                    {coin.total_buy_amount.toLocaleString("ko-KR", {
                                        maximumFractionDigits: 0,
                                    })}원
                                </strong>
                            </div>
                        </div>
                    </Link>
                )
            })}

        </main>
        
    )
}

export default HomePage