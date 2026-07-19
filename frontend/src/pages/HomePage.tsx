import "./HomePage.css"

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
                    aria-label="자산 정보 새로고침"
                >
                    ↻
                </button>
            </header>
        </main>
    )
}

export default HomePage