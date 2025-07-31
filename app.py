import numpy as np
import pandas as pd
import yfinance as yf
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import streamlit as st
import matplotlib.pyplot as plt
import datetime  # If not already imported
from ta.momentum import RSIIndicator
from ta.trend import MACD

st.set_page_config(page_title="Stock Market Predictor", layout="wide")



import os
if not os.path.exists("Stock Predictions Model.keras"):
    raise FileNotFoundError("Model file not found.")
model = load_model("Stock Predictions Model.keras", compile=False)



st.markdown("""
    <div style="background-color:#0E1117;padding:20px;border-radius:10px">
        <h1 style="color:#FAFAFA;text-align:center;">📈 Stock Market Predictor</h1>
        <h5 style="color:#BBBBBB;text-align:center;">Powered by Deep Learning & Technical Indicators</h5>
    </div>
    """, unsafe_allow_html=True)


st.sidebar.title("📊 Navigation")
stock = st.sidebar.text_input("Enter Stock Symbol", "MSFT")
start = st.sidebar.date_input("Start Date", value=datetime.date(2015, 1, 1))
end = st.sidebar.date_input("End Date", value=datetime.date.today())

data = yf.download(stock, start, end)

if data.empty:
    st.error("Invalid stock symbol or no data available.")
    st.stop()

latest_close = data['Close'].iloc[-1].item()
latest_high = data['High'].iloc[-1].item()
latest_low = data['Low'].iloc[-1].item()

col1, col2, col3 = st.columns(3)
col1.metric("📌 Current Price", f"${latest_close:.2f}")
col2.metric("📈 Day High", f"${latest_high:.2f}")
col3.metric("📉 Day Low", f"${latest_low:.2f}")



st.subheader('Stock Data')
st.write(data)

data_train = pd.DataFrame(data.Close[0:int(len(data)*0.80)])
data_test = pd.DataFrame(data.Close[int(len(data)*0.80):])

scaler = MinMaxScaler(feature_range=(0, 1))
pas_100_days = data_train.tail(100)
data_test = pd.concat([pas_100_days, data_test], ignore_index=True)
data_test_scale = scaler.fit_transform(data_test)

# Add indicators
data['MA50'] = data['Close'].rolling(50).mean()
data['MA100'] = data['Close'].rolling(100).mean()
data['MA200'] = data['Close'].rolling(200).mean()
close_series = pd.Series(data['Close'].values.flatten(), index=data.index)
data['RSI'] = RSIIndicator(close=close_series, window=14).rsi()

macd = MACD(close=close_series, window_slow=26, window_fast=12, window_sign=9)
data['MACD'] = macd.macd()
data['MACD_Signal'] = macd.macd_signal()


# Tabs for sections
tab1, tab2, tab3 = st.tabs(["📉 Charts", "📈 Indicators", "🤖 Prediction"])

# Tab 1: Moving Average Charts
with tab1:
    if st.checkbox("Show Price vs MA50 Chart"):
        st.subheader('Price vs MA50')
        fig1 = plt.figure(figsize=(8, 6))
        plt.plot(data['Close'], label='Close Price', color='green')
        plt.plot(data['MA50'], label='MA50', color='red')
        plt.legend()
        st.pyplot(fig1)

    if st.checkbox("Show Price vs MA50 vs MA100 Chart"):
        st.subheader('Price vs MA50 vs MA100')
        fig2 = plt.figure(figsize=(8, 6))
        plt.plot(data['Close'], label='Close Price', color='green')
        plt.plot(data['MA50'], label='MA50', color='red')
        plt.plot(data['MA100'], label='MA100', color='blue')
        plt.legend()
        st.pyplot(fig2)

    if st.checkbox("Show Price vs MA100 vs MA200 Chart"):
        st.subheader('Price vs MA100 vs MA200')
        fig3 = plt.figure(figsize=(8, 6))
        plt.plot(data['Close'], label='Close Price', color='green')
        plt.plot(data['MA100'], label='MA100', color='red')
        plt.plot(data['MA200'], label='MA200', color='blue')
        plt.legend()
        st.pyplot(fig3)

# Tab 2: Technical Indicators (RSI and MACD)
with tab2:
    if st.checkbox("Show RSI Chart (14-day)"):
        st.subheader('RSI - Relative Strength Index')
        fig_rsi = plt.figure(figsize=(8, 4))
        plt.plot(data.index, data['RSI'], color='purple')
        plt.axhline(70, color='red', linestyle='--')  # Overbought
        plt.axhline(30, color='green', linestyle='--')  # Oversold
        plt.title('RSI over Time')
        plt.xlabel('Date')
        plt.ylabel('RSI Value')
        st.pyplot(fig_rsi)

    if st.checkbox("Show MACD Chart"):
        st.subheader('MACD - Moving Average Convergence Divergence')
        fig_macd = plt.figure(figsize=(8, 4))
        plt.plot(data.index, data['MACD'], label='MACD', color='#4E79A7', linewidth=2)
        plt.plot(data.index, data['MACD_Signal'], label='Signal Line', color='orange')
        plt.legend()
        plt.title('MACD over Time')
        st.pyplot(fig_macd)

# Tab 3: Predictions
with tab3:
    x = []
    y = []

    for i in range(100, data_test_scale.shape[0]):
        x.append(data_test_scale[i-100:i])
        y.append(data_test_scale[i, 0])

    x = np.array(x)
    y = np.array(y)

    predict = model.predict(x)

    # ✅ Inverse transform to original price range
   predict = scaler.inverse_transform(predict)
    y = np.array(y).reshape(-1, 1)
    y = scaler.inverse_transform(y)

    next_day_prediction = predict[-1][0]
    st.success(f"Predicted closing price for next day: ${next_day_prediction:.2f}")

    st.subheader('Original Price vs Predicted Price')
    fig4 = plt.figure(figsize=(10, 6))

    # 🗓 Match predictions with actual dates
    prediction_dates = data.index[-len(y):]

    plt.plot(prediction_dates, y, 'g', label='Original Price')
    plt.plot(prediction_dates, predict, 'r', label='Predicted Price')

    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Original vs Predicted Price')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig4)

