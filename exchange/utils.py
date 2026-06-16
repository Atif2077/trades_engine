import yfinance as yf
from decimal import Decimal
from .models import Asset

def sync_market_prices():
    tkrs = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA"]
    
    try:
        for tkr in tkrs:
            t = yf.Ticker(tkr)
            prc = t.fast_info.get("lastPrice")
            
            if prc:
                Asset.objects.update_or_create(
                    tkr=tkr,
                    defaults={
                        "name": tkr,
                        "prc": Decimal(str(round(prc, 2)))
                    }
                )
        return
    except Exception as e:
        print(f"API Fetch Failed: {e}")
        
    mock_data = [
        ("AAPL", "Apple Inc.", 175.50),
        ("MSFT", "Microsoft Corp.", 402.10),
        ("GOOGL", "Alphabet Inc.", 144.20),
        ("AMZN", "Amazon.com Inc.", 178.30),
        ("TSLA", "Tesla Inc.", 190.50),
        ("NVDA", "NVIDIA Corp.", 850.20)
    ]
    
    for tkr, name, prc in mock_data:
        Asset.objects.update_or_create(
            tkr=tkr,
            defaults={
                "name": name,
                "prc": Decimal(str(prc))
            }
        )