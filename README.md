
# 📈 StockX AI – Smart Stock Market Price Predictor 🔮

**StockX AI** is an intelligent stock market forecasting web application that leverages deep learning (LSTM) and technical indicators (RSI, MACD, Moving Averages) to predict stock prices with interactive charts and real-time updates. Built with Streamlit, it’s designed for investors, analysts, and data enthusiasts who want meaningful price insights at their fingertips.


## 🎥 Demo Preview
MA--> https://drive.google.com/file/d/1vP5HFN8jBzvP8HYQmBMEwgEOtaTo_ex6/view?usp=sharing

Indicators --> https://drive.google.com/file/d/1rTtuGLmlbDFcfPfpXqcl3rtkVTqvFdjf/view?usp=sharing

Prediction --> https://drive.google.com/file/d/1IoznqKGHkYxytWyPPnJMQRpGvXASTiHp/view?usp=sharing

🖥️ **screen recording** 
📂 https://drive.google.com/file/d/1-I_LfmYrw9-WQHm5734QHSIFEoUVcXf7/view?usp=sharing

---

## 🚀 Key Features

- ✅ Real-time **stock data fetching** using Yahoo Finance
- 📉 Live **price prediction** with an LSTM model
- 📊 Interactive visualizations:
  - Moving Averages (MA50, MA100, MA200)
  - RSI (Relative Strength Index)
  - MACD (Moving Average Convergence Divergence)
- 🧠 Shows **next-day closing price prediction**
- 📈 Model evaluation with MAE, RMSE, and R² Score
- ⚡ Deployed with **Streamlit** (fast, responsive UI)

---

## 📌 Example Output

| Metric | Value |
|--------|-------|
| **Mean Absolute Error (MAE)** | `$11.36` |
| **Root Mean Squared Error (RMSE)** | `$14.30` |
| **R² Score** | `0.9109` → ✅ Excellent Accuracy |

🧪 **Predicted Closing Price Example:** `$508.30`  
📅 **Tested on:** `MSFT`, 2015–2025

---

## 🧠 How It Works

1. **User inputs stock symbol and date range**
2. **Data is fetched** from Yahoo Finance using `yfinance`
3. **Technical indicators** are calculated using `ta`
4. Data is scaled and passed into a pre-trained **LSTM model**
5. Model predicts next closing prices and renders comparison chart
6. **Model performance metrics** are calculated and shown

---

## 📂 Project Structure
StockX-AI/
│
├── app.py # Streamlit web app
├── Stock Predictions Model.keras # Pre-trained LSTM model
├── Screen Recording ... .mp4 # Walkthrough video
├── indicators.pdf, ma.pdf, ... # Visuals/screenshots
├── requirements.txt # Python dependencies
└── README.md # Project documentation


---

## 📦 Tech Stack

| Layer         | Tools Used                            |
|---------------|----------------------------------------|
| **Frontend**  | Streamlit                              |
| **Backend**   | Python, TensorFlow (Keras), NumPy, Pandas |
| **Data Source** | Yahoo Finance via `yfinance`         |
| **Indicators**| `ta` (Technical Analysis Library)      |
| **Visualization** | Matplotlib                         |

---

## 🔧 Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/your-username/StockX-AI.git
cd StockX-AI

2. Install dependencies::
pip install -r requirements.txt

3.Run the app locally:
streamlit run app.py


