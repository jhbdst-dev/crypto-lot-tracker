import { Link } from "react-router-dom"

function SellPreviewPage() {
    return (
        <main>
            <h1>예상 매도 계산</h1>

            <Link to="/coins/BTC">
                코인 상세로 이동
            </Link>
        </main>
    )
}

export default SellPreviewPage