import { Link } from "react-router-dom"

function HomePage() {
    return (
        <main>
            <h1>내 보유 자산</h1>

            <Link to="/coins/BTC">
                BTC 상세로 이동
            </Link>
        </main>
    )
}

export default HomePage