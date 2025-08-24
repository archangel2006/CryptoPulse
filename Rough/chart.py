import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
from dataclasses import dataclass
from typing import Final
from typing import List



BASE_URL: Final[str]="https://api.coingecko.com/api/v3/coins/markets"
HISTORY_URL: Final[str]= "https://api.coingecko.com/api/v3/coins/{id}/market_chart"

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
def get_coins(vs_currency: str='usd') -> List["Coin"]:
    payload = {
            'vs_currency':vs_currency,
        'order':'market_cap_desc',
        'per_page':25,
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
def get_price_history(coin_id:str, vs_currency:str ='usd', days:int =7) -> pd.DataFrame:
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

theme = st.radio("Choose Theme", ["Light", "Dark"])

if theme == "Dark":
    primary = "#72C77D"
    bg = "#0e1117"
    secondary_bg = "#262730"
    text_color = "#FAFAFA"
else:
    primary = "#007acc"
    bg = "#ffffff"
    secondary_bg = "#f0f2f6"
    text_color = "#000000"

custom_css = f"""
    <style>
        body {{
            background-color: {bg};
            color: {text_color};
        }}
        .stApp {{
            background-color: {bg};
        }}
    </style>
"""

st.markdown(custom_css, unsafe_allow_html=True)
st.markdown(f"<h1 style='color:{primary}'>Themed Heading</h1>", unsafe_allow_html=True)


st.title("Real Time Cryptocurrency Tracker")

currency = st.sidebar.selectbox("Select Currency", ['inr','usd'])
coins = get_coins(currency)

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
    df_history = get_price_history(coin_obj.id, vs_currency=currency)

    

    if not df_history.empty:
        import matplotlib.dates as mdates

        # Create figure and axis
        fig, ax = plt.subplots(figsize=(10, 5))

        # Plot price history
        ax.plot(df_history['timestamp'], df_history['price'], color='green' if coin_obj.price_change_24h >= 0 else 'red', linewidth=2)

        # Title and labels
        ax.set_title(f"{coin_obj.name} Price Trend", fontsize=16, color=text_color)
        ax.set_xlabel("Time", color=text_color)
        ax.set_ylabel(f"Price ({currency.upper()})", color=text_color)

        # Format x-axis for better date readability
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d\n%H:%M'))

        # Set background and grid
        fig.patch.set_facecolor(bg_color)
        ax.set_facecolor(bg_color)
        ax.tick_params(colors=text_color)
        ax.grid(True, linestyle='--', alpha=0.3)

        # Show plot
        st.pyplot(fig)

    else:
        st.info("No Historical Data Available")
else:
    st.error("No Coins Data Available")
