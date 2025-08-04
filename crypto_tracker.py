import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
from dataclasses import dataclass
from typing import Final
from typing import List



BASE_URL: Final[str]="https://api.coingecko.com/api/v3/coins/markets"
HISTORY_URL: Final[str]= "https://api.coingecko.com/api/v3/coins/{id}/market_chart"
CURR_URL: Final[str]= "https://api.coingecko.com/api/v3/simple/supported_vs_currencies"

@dataclass()
class Coin:
    id:str
    name:str
    symbol:str
    current_price: float
    high_24h: float
    low_24h: float
    price_change_24h: float
    price_change_percentage_24h: float

@st.cache_data(show_spinner=False)
def get_coins(vs_currency: str='usd', top_n:int =20) -> List["Coin"]:
    payload = {
            'vs_currency':vs_currency,
        'order':'market_cap_desc',
        'per_page':top_n,
        'page':1
    }
    try:
        response = requests.get(BASE_URL, params=payload)
        response.raise_for_status()
        data = response.json()
        return[
            Coin(
                id = item['id'],
                name = item['name'],
                symbol = item['symbol'],
                current_price = item['current_price'],
                high_24h = item['high_24h'],
                low_24h = item['low_24h'],
                price_change_24h = item['price_change_24h'],
                price_change_percentage_24h = item['price_change_percentage_24h']
            ) for item in data
        ]
    except Exception as e:
        st.error(f"Error Fetching Coins: {e}")
        return []
    
@st.cache_data(show_spinner=False)
def get_supported_currencies():
    
    response = requests.get(CURR_URL)
    if response.status_code == 200:
        return sorted(response.json())
    else:
        return['inr'] # fallback
    
        
@st.cache_data(show_spinner=False)
def get_price_history(coin_id:str, vs_currency:str ='usd', days:str ='7') -> pd.DataFrame:
    url = HISTORY_URL.format(id=coin_id)
    params = {'vs_currency' : vs_currency, 'days' : days}

    try:
        response = requests.get(url, params = params)
        response.raise_for_status()
        prices = response.json()['prices']

        df = pd.DataFrame(prices, columns=['timestamp','price'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
        
    except Exception as e:
        st.warning(f"Error Fetching History: {e}")
        return pd.DataFrame()
        
    
st.set_page_config(page_title = "Crypto Tracker", layout="wide")

st.title("💰 Real Time Cryptocurrency Tracker")

#currency = st.sidebar.selectbox("Select Currency", ['inr','usd'])

# Currency dropdown
currency = st.sidebar.selectbox("Select Currency", get_supported_currencies())
# SLider for topcoins
top_n = st.sidebar.slider("Number of Top Coins",min_value=5,max_value=50,value=20)
# Selectbox for duration
duration = st.sidebar.selectbox("Time Duration (days)", ['1','7','30','90','180','365','max'])


coins = get_coins(currency, top_n)

if coins:
    coin_names = [f"{coin.name}({coin.symbol.upper()})" for coin in coins]
    selected_coin = st.sidebar.selectbox("Select Coin", coin_names)
    coin_obj = coins[coin_names.index(selected_coin)]

    st.subheader(f"{coin_obj.name} ({coin_obj.symbol.upper()})")
    st.metric("Current Price", f"{coin_obj.current_price:,.2f} {currency.upper()}")

    col1,col2,col3 = st.columns(3)
    col1.metric("24 High", f"{coin_obj.high_24h:,.2f}")
    col2.metric("24 Low", f"{coin_obj.low_24h:,.2f}")
    col3.metric("24 Change (24h)", f"{coin_obj.price_change_percentage_24h:,.2f}%")

# matplot
    df_history = get_price_history(coin_obj.id, vs_currency=currency, days=duration)

    if not df_history.empty:
        st.line_chart(df_history.set_index('timestamp')['price'])
    else:
        st.info("No Historical Data Available")

    # ---- Table Of Top Coins -----
    st.subheader(f"🏆Top {top_n} Coins by Market Cap ({currency.upper()})")

    coin_table = pd.DataFrame([{
        'Name' : coin.name,
        'Symbol': coin.symbol.upper(),
        'Price' :f"{coin.current_price:,.2f} {currency.upper()}",
        '24h Change (%)': f"{coin.price_change_percentage_24h:,.2f}",
        'Market Cap' : f"{coin.current_price*1_000_000:.0f}"
    } for coin in coins])   

    st.dataframe(coin_table, use_container_width=True)
else:
    st.error("No Coins Data Available")
