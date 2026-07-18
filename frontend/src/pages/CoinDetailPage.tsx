import { Link } from "react-router-dom"

function CoinDetailPage() {
    return (
        <main>
            <h1>코인별 개별 거래</h1>

            <Link to="/">
                Home으로 이동
            </Link>

            <br />

            <Link to="/coins/BTC/trades/1/sell">
                예상 매도 계산으로 이동
            </Link>
        </main>
    )
}

export default CoinDetailPage