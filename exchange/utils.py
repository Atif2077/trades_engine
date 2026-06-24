import os
import json
import yfinance as yf
from dotenv import load_dotenv
from groq import Groq
from .models import Asset, Signal

load_dotenv() 
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def generate_ai_signal(tkr):
    try:
        t = yf.Ticker(tkr)
        hist = t.history(period="1mo")
        if hist.empty:
            return
            
        closes = [round(price, 2) for price in hist['Close'].tolist()]
        
        prompt = (
            f"Analyze these 30 daily closing prices for {tkr}: {closes}. "
            "Return ONLY a valid JSON object with two keys: "
            "'vol' (an integer from 1 to 10 representing price volatility) and "
            "'rec' (a string: exactly 'BUY', 'SELL', or 'HOLD')."
        )
        
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
            response_format={"type": "json_object"}
        )
        
        result = json.loads(chat_completion.choices[0].message.content)
        ast = Asset.objects.get(tkr=tkr)
        
        Signal.objects.update_or_create(
            ast=ast,
            defaults={
                'vol': result.get('vol', 5), 
                'rec': result.get('rec', 'HOLD')
            }
        )
        print(f"Successfully generated AI signal for {tkr}")
        
    except Exception as e:
        print(f"AI Engine Failed for {tkr}: {e}")

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