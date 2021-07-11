from django.shortcuts import render
import yfinance as yf
from datetime import date

# Create your views here.
def show_stock(request, stock):

    if stock==None:
        stock="GOOG"
        
    START = "2020-01-01"
    TODAY = date.today().strftime("%Y-%m-%d")
    stock_name = stock

    ticker = yf.Ticker(stock_name)
    stock_info = ticker.info

    # data = yf.download(stock, START, TODAY)
    # data.reset_index(inplace=True)
    # print(data)

    stock_history = ticker.history(start=START, end=TODAY)  
    stock_history.reset_index(inplace=True)
    results_length = stock_history.shape[0]
  
    stock_result = {
        "name" : stock_info["shortName"],
        "symbol" : stock_info["symbol"],
        "quoteType" : stock_info["quoteType"],
        "currentPrice" : stock_info["currentPrice"],
        "industry" : stock_info["industry"],
        "marketCap" : stock_info["marketCap"],
        "close" : round(stock_history["Close"][results_length-1],2),
        "high" : round(stock_history["High"][results_length-1],2),
        "low" : round(stock_history["Low"][results_length-1],2),
        "volume" : stock_history["Volume"][results_length-1],
        "price_change" : round(stock_history["Close"][results_length-2] - stock_history["Close"][results_length-1],2),
        "percent_change" : round((stock_history["Close"][results_length-2] - stock_history["Close"][results_length-1])/100,2)
    }

    return render(request, "portfolio_test/index.html", {"stock_result":stock_result})




    



