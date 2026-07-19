import "./CoinDetailPage.css"
import { useNavigate } from "react-router-dom"


function CoinDetailPage() {

    const navigate = useNavigate()

    function handleBack() {
        navigate(-1)
    }

    function handleRefresh() {
        console.log("새로고침")
    }

    function handleSellPreview(tradeId: number) {
        navigate(`/coins/BTC/trades/${tradeId}/sell`)
    }

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
                    BTC 비트코인
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
                                ₿
                            </div>

                            <div className="coin-summary-name">
                                <h2>비트코인 (BTC)</h2>
                            </div>

                        </div>

                        <div className="coin-summary-price">

                            <span>현재가</span>

                            <strong>162,000,000원</strong>

                            <p>+2.15%</p>

                        </div>

                    </div>

                    {/* coin-summary-card-body */}
                    <div className="coin-summary-card__body">

                        <div className="summary-item">
                            <span>전체 보유수량</span>
                            <strong>0.052 BTC</strong>
                        </div>

                        <div className="summary-item">
                            <span>평균 매수가</span>
                            <strong>136,800,000원</strong>
                        </div>

                        <div className="summary-item">
                            <span>전체 매수원금</span>
                            <strong>7,113,600원</strong>
                        </div>

                        <div className="summary-item">
                            <span>평가금액</span>
                            <strong>8,424,000원</strong>
                        </div>

                        <div className="summary-item">
                            <span>평가손익</span>
                            <strong className="profit">+1,310,400원</strong>
                        </div>

                        <div className="summary-item">
                            <span>수익률</span>
                            <strong className="profit">+18.42%</strong>
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
                <article className="trade-card">

                    <div className="trade-card__header">
                        <time dateTime="2025-06-01T14:32:15">
                            2025-06-01 14:32:15
                        </time>

                        <span className="trade-card__id">
                            거래 ID 1
                        </span>
                    </div>

                    <div className="trade-card__body">

                        <div className="trade-item">
                            <span>매수가</span>
                            <strong>130,000,000원</strong>
                        </div>

                        <div className="trade-item">
                            <span>남은 수량</span>
                            <strong>0.020 BTC</strong>
                        </div>

                        <div className="trade-item">
                            <span>매수원금</span>
                            <strong>2,600,000원</strong>
                        </div>

                        <div className="trade-item">
                            <span>평가금액</span>
                            <strong>3,240,000원</strong>
                        </div>

                        <div className="trade-item">
                            <span>평가손익</span>
                            <strong className="profit">+640,000원</strong>
                        </div>

                        <div className="trade-item">
                            <span>수익률</span>
                            <strong className="profit">+24.62%</strong>
                        </div>

                    </div>

                    <button
                        className="trade-card__sell-button"
                        type="button"
                        onClick={() => handleSellPreview(1)}
                    >
                        매도 계산하기
                    </button>

                </article>

                {/* 개별 매수 거래 목록 메인 */}
                <article className="trade-card">

                    <div className="trade-card__header">
                        <time dateTime="2025-06-01T14:32:15">
                            2025-06-01 14:32:15
                        </time>

                        <span className="trade-card__id">
                            거래 ID 2
                        </span>
                    </div>

                    <div className="trade-card__body">

                        <div className="trade-item">
                            <span>매수가</span>
                            <strong>130,000,000원</strong>
                        </div>

                        <div className="trade-item">
                            <span>남은 수량</span>
                            <strong>0.020 BTC</strong>
                        </div>

                        <div className="trade-item">
                            <span>매수원금</span>
                            <strong>2,600,000원</strong>
                        </div>

                        <div className="trade-item">
                            <span>평가금액</span>
                            <strong>3,240,000원</strong>
                        </div>

                        <div className="trade-item">
                            <span>평가손익</span>
                            <strong className="profit">+640,000원</strong>
                        </div>

                        <div className="trade-item">
                            <span>수익률</span>
                            <strong className="profit">+24.62%</strong>
                        </div>

                    </div>

                    <button
                        className="trade-card__sell-button"
                        type="button"
                        onClick={() => handleSellPreview(2)}
                    >
                        매도 계산하기
                    </button>

                </article>

            </section>

            </section>

        </main>
    )
}

export default CoinDetailPage