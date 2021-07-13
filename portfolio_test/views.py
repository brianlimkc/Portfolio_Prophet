from django.shortcuts import render
import yfinance as yf
from prophet import Prophet
from datetime import date, timedelta
import datetime
from portfolio_test.models import *

# Create your views here.
def show_stock(request):

    stock = request.GET.get("stock")

    if stock==None:
        stock="GOOG"
<<<<<<< HEAD
        
    START = "2015-01-01"
    TODAY = date.today().strftime("%Y-%m-%d")
    stock_name = stock

    ticker = yf.Ticker(stock_name)
    stock_info = ticker.info

    period = 1 * 365

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
=======
>>>>>>> 5fdd985ed28ff346d02e174287954da22f1c6946

    stock_record = Stock.objects.get(symbol=stock)
    
    stock_result = {
        "name" : stock_record.name,
        "symbol" : stock_record.symbol,
        "currentPrice" : stock_record.current_price,
        "industry" : stock_record.industry,
        "marketCap" : stock_record.market_cap,
        "high" : stock_record.prev_high,
        "low" : stock_record.prev_low,
        "volume" : stock_record.volume,
        "price_change" : stock_record.price_change
    }  

    historical_record = Historical_Stock_Data.objects.filter(stock_id = stock_record.id)

    chart_data = []

    for record in historical_record:            
        chart_data.append(float(record.price_close))

    print(chart_data)

    return render(
        request, 
        "portfolio_test/index.html", 
        {"stock_result":stock_result,
        "chart_data": chart_data,
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


def populate_history(stock):

    START = "2021-01-01"
    TODAY = date.today().strftime("%Y-%m-%d")
    period = 1 * 365

    # data = yf.download(stock.symbol, START, TODAY)
    data = yf.download(stock.symbol, START, TODAY)
  
    start_date = date(2021, 1, 1)
    end_date = date(2021, 7, 12)
    delta = timedelta(days=1)
    

    while start_date <= end_date:
        data_row = data[data.index==str(start_date)]                       
        close = data_row["Close"].values.tolist()
        for close_price in close:  
            record = Historical_Stock_Data(
                stock_id = stock,
                date_recorded = start_date,
                price_close = close_price
            )
            record.save()

        start_date += delta

    data.reset_index(inplace=True)  
    df_train = data[['Date','Close']]    

    df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

    m = Prophet()
    m.fit(df_train)
    future = m.make_future_dataframe(periods=period)
    forecast = m.predict(future)
    forecast_length = forecast.shape[0]

    for index in range(forecast_length):
        data_row = forecast[forecast.index == index]        
        fdate = data_row["ds"].values.tolist()
        yhat = data_row["yhat"].values.tolist()
        yhat_upper = data_row["yhat_upper"].values.tolist()
        yhat_lower = data_row["yhat_lower"].values.tolist()

        forecast_record = Forecast_Record(
            stock_id = stock,
            date = datetime.datetime.fromtimestamp(fdate[0]/1000000000),    
            yhat = yhat[0],
            yhat_upper = yhat_upper[0],
            yhat_lower = yhat_lower[0]
        )

        forecast_record.save()
         
  
def populate_stock_history(request):
    stocks = Stock.objects.all()
    for stock in stocks:        
        # populate_stock(stock)
        populate_history(stock)
    # populate_history(stock)



    

    



