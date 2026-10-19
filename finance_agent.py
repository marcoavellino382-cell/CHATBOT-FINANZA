import yfinance as yf

def get_stock_info(ticker: str) -> dict:
    """Estrae i dati finanziari principali di un ticker."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        return {
            "Nome": info.get("longName", ticker),
            "Prezzo Attuale": f"${info.get('currentPrice', 'N/D')}",
            "P/E Ratio": info.get("trailingPE", "N/D"),
            "Market Cap": f"${info.get('marketCap', 0):,}",
            "Fatturato Totale": f"${info.get('totalRevenue', 0):,}",
            "Margine di Profitto": f"{info.get('profitMargins', 0) * 100:.2f}%" if info.get('profitMargins') else "N/D"
        }
    except Exception as e:
        return {"Errore": f"Impossibile recuperare i dati per {ticker}."}
