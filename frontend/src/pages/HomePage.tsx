import "./HomePage.css"
import { Link } from "react-router-dom"

function HomePage() {
    return (
        <main className="home-page">


            <header className="home-header">
                <h1 className="home-header__title">
                    내 보유 자산
                </h1>

                <button
                    className="home-header__refresh-button"
                    type="button"
                >
                    ↻
                </button>
            </header>


            <section className="asset-summary">
                <p className="asset-summary__label">
                    총 평가금액
                </p>

                <h2 className="asset-summary__price">
                    12,450,000원
                </h2>

                <p className="asset-summary__profit">
                    +1,230,000원 │ +10.96%
                </p>

                <div className="asset-summary__bottom">
                    <div>
                        <span>총 매수금액</span>
                        <strong>11,220,000원</strong>
                    </div>

                    <div>
                        <span>보유 코인</span>
                        <strong>3개</strong>
                    </div>
                </div>
            </section>

            
            <section className="coin-list">
                <div className="coin-list__header">
                    <h2>보유 코인 목록</h2>

                    <button
                        className="coin-list__sort-button"
                        type="button"
                    >
                        시세 기준 ▼
                    </button>
                </div>
            </section>


            <Link className="coin-card"
                to="/coins/BTC">

                <div className="coin-card__header">

                    <div className="coin-info">

                        <div className="coin-icon">
                            ₿
                        </div>

                        <div className="coin-name">
                            <h3>BTC</h3>
                            <p>비트코인</p>
                        </div>

                    </div>

                    <div className="coin-current-price">
                        <span>현재가</span>
                        <strong>162,000,000원</strong>
                    </div>
                    
                </div>

                <div className="coin-card__body">

                    <div className="coin-card__item">
                        <span>보유수량</span>
                        <strong>0.052 BTC</strong>
                    </div>

                    <div className="coin-card__item">
                        <span>평균 매수가</span>
                        <strong>136,800,000원</strong>
                    </div>

                    <div className="coin-card__item">
                        <span>평가금액</span>
                        <strong>8,420,000원</strong>
                    </div>

                    <div className="coin-card__item">
                        <span>평가손익</span>
                        <strong>+1,260,000원</strong>
                    </div>

                    <div className="coin-card__item">
                        <span>수익률</span>
                        <strong>+18.42%</strong>
                    </div>

                </div>

            </Link>
            
            <Link className="coin-card"
                to="/coins/XRP">

                <div className="coin-card__header">

                    <div className="coin-info">

                        <div className="coin-icon">
                            XRP
                        </div>

                        <div className="coin-name">
                            <h3>XRP</h3>
                            <p>리플</p>
                        </div>

                    </div>

                    <div className="coin-current-price">
                        <span>현재가</span>
                        <strong>880원</strong>
                    </div>

                </div>

                <div className="coin-card__body">

                    <div className="coin-card__item">
                        <span>보유수량</span>
                        <strong>1,200 XRP</strong>
                    </div>

                    <div className="coin-card__item">
                        <span>평균 매수가</span>
                        <strong>720원</strong>
                    </div>

                    <div className="coin-card__item">
                        <span>평가금액</span>
                        <strong>1,056,000원</strong>
                    </div>

                    <div className="coin-card__item">
                        <span>평가손익</span>
                        <strong>+192,000원</strong>
                    </div>

                    <div className="coin-card__item">
                        <span>수익률</span>
                        <strong>+22.22%</strong>
                    </div>

                </div>

            </Link>

            <Link className="coin-card"
                to="/coins/ETH">

                <div className="coin-card__header">

                    <div className="coin-info">

                        <div className="coin-icon">
                            Ξ
                        </div>

                        <div className="coin-name">
                            <h3>ETH</h3>
                            <p>이더리움</p>
                        </div>

                    </div>

                    <div className="coin-current-price">
                        <span>현재가</span>
                        <strong>3,420,000원</strong>
                    </div>

                </div>

                <div className="coin-card__body">

                    <div className="coin-card__item">
                        <span>보유수량</span>
                        <strong>0.63 ETH</strong>
                    </div>

                    <div className="coin-card__item">
                        <span>평균 매수가</span>
                        <strong>3,100,000원</strong>
                    </div>

                    <div className="coin-card__item">
                        <span>평가금액</span>
                        <strong>2,154,600원</strong>
                    </div>

                    <div className="coin-card__item">
                        <span>평가손익</span>
                        <strong>+201,600원</strong>
                    </div>

                    <div className="coin-card__item">
                        <span>수익률</span>
                        <strong>+10.32%</strong>
                    </div>

                </div>

            </Link>
        
        </main>
    )
}

export default HomePage