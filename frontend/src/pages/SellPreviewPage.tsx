import "./SellPreviewPage.css"
import { useEffect, useState } from "react"
import { useNavigate, useParams } from "react-router-dom"

type BuyTrade = {
    uuid: string
    created_at: string
    buy_price: number
    quantity: number
    buy_amount: number
}

type CoinDetailData = {
    market: string
    coin_name: string
    buy_trades: BuyTrade[]
}

function SellPreviewPage() {

    const navigate = useNavigate()

    const { market, tradeId } = useParams<{
        market: string
        tradeId: string
    }>()

    const [coinData, setCoinData] =
        useState<CoinDetailData | null>(null)

    const [selectedTrade, setSelectedTrade] =
        useState<BuyTrade | null>(null)

    const [sellPrice, setSellPrice] = useState("")

    const [sellQuantity, setSellQuantity] = useState("")

    useEffect(() => {
        if (!market || !tradeId) {
            return
        }

        const apiMarket = market.startsWith("KRW-")
            ? market
            : `KRW-${market}`

        async function fetchSelectedTrade() {
            try {
                const response = await fetch(
                    `http://127.0.0.1:8000/coins/${apiMarket}`
                )

                if (!response.ok) {
                    throw new Error(
                        "거래 정보를 가져오지 못했습니다."
                    )
                }

                const data: CoinDetailData =
                    await response.json()

                const trade = data.buy_trades.find(
                    (item) => item.uuid === tradeId
                )

                setCoinData(data)
                setSelectedTrade(trade ?? null)
            } catch (error) {
                console.error(error)
            }
        }

        fetchSelectedTrade()
    }, [market, tradeId])

    function handleBack() {
        navigate(-1)
    }

    function handleRefresh() {
        console.log("새로고침")
    }

    useEffect(() => {
        console.log(sellPrice)
    }, [sellPrice])

    function formatDate(dateString: string) {
        const date = new Date(dateString)

        return date.toLocaleString("ko-KR", {
            year: "numeric",
            month: "2-digit",
            day: "2-digit",
            hour: "2-digit",
            minute: "2-digit",
            hour12: false,
        })
    }


    if (!coinData || !selectedTrade) {
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
        <main className="sell-preview-page">


            <header className="sell-preview-header">
                <button
                    className="back-button"
                    type="button"
                    onClick={handleBack}
                >
                    ←
                </button>

                <h1 className="page-title">
                    예상 매도 계산
                </h1>

                <button
                    className="refresh-button"
                    type="button"
                    onClick={handleRefresh}
                >
                    ↻
                </button>
            </header>


            <section className="selected-trade-card">

                <div className="selected-trade-card__header">

                    <div className="selected-trade-coin">
                        <div className="selected-trade-icon">
                            {coinIcon}
                        </div>

                        <strong>{symbol} {coinData.coin_name}</strong>
                    </div>

                    <span className="selected-trade-id">
                        거래 ID {selectedTrade.uuid.slice(0, 8)}
                    </span>

                </div>

                <div className="selected-trade-card__body">

                    <div className="selected-trade-item">
                        <span>매수일시</span>
                        <strong>{formatDate(selectedTrade.created_at)}</strong>
                    </div>

                    <div className="selected-trade-item">
                        <span>매수가</span>
                        <strong>
                            {Math.round(
                                selectedTrade.buy_price
                            ).toLocaleString("ko-KR")}원
                        </strong>
                    </div>

                    <div className="selected-trade-item">
                        <span>남은 보유수량</span>
                        <strong>
                            {selectedTrade.quantity.toLocaleString(
                                "ko-KR",
                                {
                                    maximumFractionDigits: 8,
                                }
                            )} {symbol}
                        </strong>
                    </div>

                    <div className="selected-trade-item">
                        <span>실제 매수원가</span>
                        <strong>
                            {Math.round(
                                selectedTrade.buy_amount
                            ).toLocaleString("ko-KR")}원
                        </strong>
                    </div>

                </div>

            </section>


            <section className="sell-input-section">

                <h2 className="sell-input-section__title">
                    매도 정보 입력
                </h2>

                <div className="sell-input-group">

                    <label htmlFor="sell-price">
                        매도 예정가
                    </label>

                    <div className="sell-input-field">
                        <input
                            id="sell-price"
                            type="number"
                            value={sellPrice}
                            onChange={(e) => setSellPrice(e.target.value)}
                        />

                        <span>원</span>
                    </div>

                    <p className="sell-input-help">
                        현재가 162,000,000원
                        <strong> (+2.15%)</strong>
                    </p>

                </div>

                <div className="sell-input-group">

                    <label htmlFor="sell-quantity">
                        매도 예정수량
                    </label>

                    <div className="sell-input-field">
                        <input
                            type="number"
                            value={sellQuantity}
                            onChange={(e) => {
                                setSellQuantity(e.target.value)
                                console.log(e.target.value)
                            }}
                        />

                        <span>{coinData?.market.replace("KRW-", "")}</span>
                    </div>

                    <div className="sell-quantity-buttons">
                        
                        {/* 
                        <button type="button">25%</button>
                        <button type="button">50%</button>
                        <button type="button">75%</button>
                        */}
                        
                        <button
                            className="sell-quantity-buttons__all"
                            type="button"
                            onClick={() => {
                                if (selectedTrade) {
                                setSellQuantity(selectedTrade.quantity.toString())
                                }
                            }}
                        >
                            전량 ({selectedTrade?.quantity} {market?.replace("KRW-", "")})
                        </button>
                    </div>

                </div>

            </section>


            <section className="sell-result-section">

                <h2 className="sell-result-section__title">
                    예상 매도 결과
                </h2>

                <div className="sell-result-card">

                    <div className="sell-result-item">
                        <span>예상 매도금액</span>
                        <strong>3,240,000원</strong>
                    </div>

                    <div className="sell-result-item">
                        <span>예상 매도 수수료 (0.05%)</span>
                        <strong>1,620원</strong>
                    </div>

                    <div className="sell-result-item sell-result-item--settlement">
                        <span>예상 정산금액</span>
                        <strong>3,238,380원</strong>
                    </div>

                    <div className="sell-result-divider" />

                    <div className="sell-result-item">
                        <span>매도한 수량의 원가</span>
                        <strong>2,600,000원</strong>
                    </div>

                    <div className="sell-result-item">
                        <span>예상 실현손익</span>
                        <strong className="profit">+638,380원</strong>
                    </div>

                    <div className="sell-result-item">
                        <span>예상 실현수익률</span>
                        <strong className="profit">+24.55%</strong>
                    </div>

                    <div className="sell-result-divider" />

                    <div className="sell-result-item">
                        <span>매도 후 남은 수량</span>
                        <strong>0 BTC</strong>
                    </div>

                    <div className="sell-result-item">
                        <span>매도 후 남은 원가</span>
                        <strong>0원</strong>
                    </div>

                </div>

            </section>

            <button
                className="save-sell-plan-button"
                type="button"
            >
                매도 계획 저장
            </button>

        </main>
    )
}

export default SellPreviewPage