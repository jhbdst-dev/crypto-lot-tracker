import { Route, Routes } from "react-router-dom"

import "./App.css"
import CoinDetailPage from "./pages/CoinDetailPage"
import HomePage from "./pages/HomePage"
import SellPreviewPage from "./pages/SellPreviewPage"

function App() {
    return (
        <div className="app">
            <Routes>
                <Route path="/" element={<HomePage />} />

                <Route
                    path="/coins/:market"
                    element={<CoinDetailPage />}
                />

                <Route
                    path="/coins/:market/trades/:tradeId/sell"
                    element={<SellPreviewPage />}
                />
            </Routes>
        </div>
    )
}

export default App