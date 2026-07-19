import "./SellPreviewPage.css"
import { useNavigate } from "react-router-dom"

function SellPreviewPage() {

    const navigate = useNavigate()

    function handleBack() {
        navigate(-1)
    }

    function handleRefresh() {
        console.log("새로고침")
    }


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
                            ₿
                        </div>

                        <strong>BTC 비트코인</strong>
                    </div>

                    <span className="selected-trade-id">
                        거래 ID 1
                    </span>

                </div>

                <div className="selected-trade-card__body">

                    <div className="selected-trade-item">
                        <span>매수일시</span>
                        <strong>2025-06-01 14:32:15</strong>
                    </div>

                    <div className="selected-trade-item">
                        <span>매수가</span>
                        <strong>130,000,000원</strong>
                    </div>

                    <div className="selected-trade-item">
                        <span>남은 보유수량</span>
                        <strong>0.020 BTC</strong>
                    </div>

                    <div className="selected-trade-item">
                        <span>실제 매수원가</span>
                        <strong>2,600,000원</strong>
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
                            defaultValue="162000000"
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
                            id="sell-quantity"
                            type="number"
                            step="0.001"
                            defaultValue="0.020"
                        />

                        <span>BTC</span>
                    </div>

                    <div className="sell-quantity-buttons">
                        <button type="button">25%</button>
                        <button type="button">50%</button>
                        <button type="button">75%</button>

                        <button
                            className="sell-quantity-buttons__all"
                            type="button"
                        >
                            전량 (0.020 BTC)
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