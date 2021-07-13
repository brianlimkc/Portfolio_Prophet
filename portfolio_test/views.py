from django.shortcuts import render
import yfinance as yf
from prophet import Prophet
from datetime import date
from portfolio_test.models import *

# Create your views here.
def show_stock(request):

    stock = request.GET.get("stock")


    if stock==None:
        stock="GOOG"
        
    START = "2015-01-01"
    TODAY = date.today().strftime("%Y-%m-%d")
    stock_name = stock

    ticker = yf.Ticker(stock_name)
    stock_info = ticker.info

    period = 1 * 365


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

    
    data = yf.download(stock_name, START, TODAY)
    data.reset_index(inplace=True)

    df_train = data[['Date','Close']]
    chart_data = data[['Close']].values.tolist()
    flat_chart_data = [item for sublist in chart_data for item in sublist]
    
    df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

    m = Prophet()
    m.fit(df_train)
    future = m.make_future_dataframe(periods=period)
    forecast = m.predict(future)
    forecast_length = forecast.shape[0]
      

    forecast_results = {
        "30_days_yhat" : round(forecast["yhat"][forecast_length-335],2),
        "30_days_yhat_lower" : round(forecast["yhat_lower"][forecast_length-335],2),
        "30_days_yhat_upper" : round(forecast["yhat_upper"][forecast_length-335],2),
        "180_days_yhat" : round(forecast["yhat"][forecast_length-185],2),
        "180_days_yhat_lower" : round(forecast["yhat_lower"][forecast_length-185],2),
        "180_days_yhat_upper" : round(forecast["yhat_upper"][forecast_length-185],2),
        "365_days_yhat" : round(forecast["yhat"][forecast_length-1],2),
        "365_days_yhat_lower" : round(forecast["yhat_lower"][forecast_length-1],2),
        "365_days_yhat_upper" : round(forecast["yhat_upper"][forecast_length-1],2),
    }

    print(forecast_results)

    return render(
        request, 
        "portfolio_test/index.html", 
        {"stock_result":stock_result,
         "forecast_result" : forecast_results,
         "chart_data": flat_chart_data,
         "forecast" : forecast
        }
        )



def populate_stock(stock):


    ticker = yf.Ticker(stock.symbol).info    

    print(ticker["shortName"])
    # print(stock)


    stock.name = ticker["shortName"]
    stock.symbol = ticker["symbol"]
    stock.industry = ticker["industry"]
    stock.market_cap = round(ticker["marketCap"],2)
    stock.current_price = round(ticker["currentPrice"],2)
    stock.volume = round(ticker["volume"],2)
    stock.prev_high = round(ticker["regularMarketDayHigh"],2)
    stock.prev_low = round(ticker["regularMarketDayLow"],2)
    stock.price_change = round((ticker["previousClose"] - ticker["currentPrice"]),2)
    # stock.date_updated = date.today().strftime("%Y-%m-%d")

    stock.save()
  
def populate_stock_history(request):
    stocks = Stock.objects.all()
    for stock in stocks:        
        populate_stock(stock)



    

    



