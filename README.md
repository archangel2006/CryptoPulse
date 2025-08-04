# 🪙 CryptoPulse – Real-Time Cryptocurrency Tracker

![CryptoPulse](https://img.shields.io/badge/Built%20with-Python%20%7C%20Streamlit-blue.svg)  


**🔥 Built with Streamlit | 100% Python-Powered Web Dashboard**

> A blazing-fast, responsive **Real-Time Cryptocurrency Tracker** built entirely with **Streamlit**. This app tracks live crypto prices, trends, and top market movers across multiple fiat currencies and user-defined duration.

---

## 🧠 What is CryptoPulse?

**CryptoPulse** is a simple yet powerful web app to **track real-time cryptocurrency prices** using the CoinGecko API. It includes:

- Real-time price tracking for top cryptocurrencies
-  Dynamic price history chart over any **selected duration** 
- Supports **over 100 currencies**
- Visualizes **real-time** price history
- Choose and **display top coins**
- **Interactive** charts of price history
- Clean and minimal UI built with Streamlit
- Fast performance

---

## 📸 App Preview

> This app is hosted on Streamlit

Access it here: https://crypto-pulse.streamlit.app/

<img width="1869" height="770" alt="image" src="https://github.com/user-attachments/assets/5e979baf-a334-417b-8c5a-5ce6d9bda95b" />

<img width="1555" height="538" alt="image" src="https://github.com/user-attachments/assets/8e01f11d-4689-4a46-9c7e-b6932aaa9f80" />


---

## ✨ Features

| Feature                     |                                                                        |
| ---------------------------| ----------------------------------------------------------------------------------- |
| 🔄 Live Crypto Data         | Fetches real-time prices from the [CoinGecko API](https://www.coingecko.com/en/api) |
| 🌐 Multi-Currency Support   | Dynamically loads all supported fiat currencies                                     |
| ⏳ Adjustable Duration       | View 1 day, 7 days, 30 days, or more of price history                               |
| 🏆 Top Coins Slider         | Customize number of top cryptocurrencies displayed (5–50)                           |
| 📊 Interactive Line Charts  | View historical price data per coin                                                 |
| 🚀 100% Python — No HTML/JS | Pure Streamlit UI, matplotlib for charts                                            |
| ✅ Responsive UX             | Designed with minimal layout friction                                                |


---
## 🛠️ Tech Stack

| Layer      | Tool                                 |
| ---------- | ------------------------------------ |
| UI         | Streamlit                            |
| Backend    | Python                               |
| API Source | CoinGecko                            |
| Plotting   | Matplotlib / Streamlit native charts |
| Styling    | Streamlit Theme                      |
---

## 📂 File Structure

```
📁 CryptoPulse/
│
├── assets/             # demo screenshots
├── crypto_tracker.py   # Main Streamlit app
├── requirements.txt    # Required Python packages
└── README.md           # documentation
```
---

## 📦 Installation

```bash
# Step 1. Clone the repository

git clone https://github.com/archangel2006/CryptoPulse.git
cd CryptoPulse


# Step2. Create virtual environment

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


# Step3. install dependencies

pip install -r requirements.txt


# Step4. Running the app
streamlit run crypto_tracker.py
```

---
## Author

- Hackathon: 🐍 PyWeb Creators
- Team Name: Sableye
- Name: Vaibhavi Srivastava
- Github: [archangel2006](https://github.com/archangel2006)
