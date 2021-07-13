from django.shortcuts import render
import yfinance as yf
from prophet import Prophet
import datetime
from portfolio_test.models import *

# Create your views here.
def show_stock(request):

    stock = request.GET.get("stock")

    if stock==None:
        stock="GOOG"

    try: 
        stock_record = Stock.objects.get(symbol=stock)
    except Stock.DoesNotExist:
        new_stock = Stock(
            symbol = stock
        )
        populate_stock(new_stock)
        populate_history(new_stock)
        stock_record = new_stock
    
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
   
    return render(
        request, 
        "portfolio_test/index.html", 
        {"stock_result":stock_result,
        "chart_data": chart_data,
        }
        )
        


    # START = "2018-01-01"
    # TODAY = date.today().strftime("%Y-%m-%d")
    # stock_name = stock

    # ticker = yf.Ticker(stock_name)
    # stock_info = ticker.info

    # period = 1 * 365

    # data = yf.download(stock_name, START, TODAY)
    # data.reset_index(inplace=True)    

    # stock_history = data
    
    # results_length = stock_history.shape[0]
  
    # stock_result = {
    #     "name" : stock_info["shortName"],
    #     "symbol" : stock_info["symbol"],
    #     "quoteType" : stock_info["quoteType"],
    #     "currentPrice" : stock_info["currentPrice"],
    #     "industry" : stock_info["industry"],
    #     "marketCap" : stock_info["marketCap"],
    #     "close" : round(stock_history["Close"][results_length-1],2),
    #     "high" : round(stock_history["High"][results_length-1],2),
    #     "low" : round(stock_history["Low"][results_length-1],2),
    #     "volume" : stock_history["Volume"][results_length-1],
    #     "price_change" : round(stock_history["Close"][results_length-2] - stock_history["Close"][results_length-1],2),
    #     "percent_change" : round((stock_history["Close"][results_length-2] - stock_history["Close"][results_length-1])/100,2)
    # }  

    # df_train = data[['Date','Close']]
    # chart_data = data[['Close']].values.tolist()
    # flat_chart_data = [item for sublist in chart_data for item in sublist]
    
    # df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

    # m = Prophet()
    # m.fit(df_train)
    # future = m.make_future_dataframe(periods=period)
    # forecast = m.predict(future)
    # forecast_length = forecast.shape[0]
      
    # forecast_results = {
    #     "30_days_yhat" : round(forecast["yhat"][forecast_length-335],2),
    #     "30_days_yhat_lower" : round(forecast["yhat_lower"][forecast_length-335],2),
    #     "30_days_yhat_upper" : round(forecast["yhat_upper"][forecast_length-335],2),
    #     "180_days_yhat" : round(forecast["yhat"][forecast_length-185],2),
    #     "180_days_yhat_lower" : round(forecast["yhat_lower"][forecast_length-185],2),
    #     "180_days_yhat_upper" : round(forecast["yhat_upper"][forecast_length-185],2),
    #     "365_days_yhat" : round(forecast["yhat"][forecast_length-1],2),
    #     "365_days_yhat_lower" : round(forecast["yhat_lower"][forecast_length-1],2),
    #     "365_days_yhat_upper" : round(forecast["yhat_upper"][forecast_length-1],2),
    # }

    # print(forecast_results)

    # return render(
    #     request, 
    #     "portfolio_test/index.html", 
    #     {"stock_result":stock_result,
    #      "forecast_result" : forecast_results,
    #      "chart_data": flat_chart_data,
    #      "forecast" : forecast
    #     }
    #     )

def populate_stock(stock):

    ticker = yf.Ticker(stock.symbol).info    

    print(ticker["shortName"])

    stock.name = ticker["shortName"]
    stock.symbol = ticker["symbol"]
    stock.industry = ticker["industry"]
    stock.market_cap = round(ticker["marketCap"],2)
    stock.current_price = round(ticker["currentPrice"],2)
    stock.volume = round(ticker["volume"],2)
    stock.prev_high = round(ticker["regularMarketDayHigh"],2)
    stock.prev_low = round(ticker["regularMarketDayLow"],2)
    stock.price_change = round((ticker["previousClose"] - ticker["currentPrice"]),2)
    stock.percent_change = round(((ticker["previousClose"] - ticker["currentPrice"]) / ticker["currentPrice"]),2)
    stock.date_updated = datetime.datetime.now().date()
    stock.save()

def populate_history(stock):

    end_date = datetime.datetime.now().date()
    start_date = end_date - datetime.timedelta(days=5*365)
    delta = datetime.timedelta(days=1)
    period = 1 * 365
      
    data = yf.download(stock.symbol, start_date, end_date)
  
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

    stock.yhat_30 = round(forecast["yhat"][forecast_length-335],2)
    stock.yhat_30_upper = round(forecast["yhat_upper"][forecast_length-335],2)
    stock.yhat_30_lower = round(forecast["yhat_lower"][forecast_length-335],2)
    stock.yhat_30_advice = recommendation(stock.current_price,stock.yhat_30,stock.yhat_30_upper,stock.yhat_30_lower)
    stock.yhat_180 = round(forecast["yhat"][forecast_length-185],2)
    stock.yhat_180_upper = round(forecast["yhat_upper"][forecast_length-185],2)
    stock.yhat_180_lower = round(forecast["yhat_lower"][forecast_length-185],2)
    stock.yhat_180_advice = recommendation(stock.current_price,stock.yhat_30,stock.yhat_30_upper,stock.yhat_30_lower)
    stock.yhat_365 = round(forecast["yhat"][forecast_length-1],2)
    stock.yhat_365_upper = round(forecast["yhat_upper"][forecast_length-1],2)
    stock.yhat_365_lower = round(forecast["yhat_lower"][forecast_length-1],2)
    stock.yhat_365_advice = recommendation(stock.current_price,stock.yhat_30,stock.yhat_30_upper,stock.yhat_30_lower)
    stock.save()


    
def recommendation(price,yhat,yhat_upper,yhat_lower):
    if price < yhat_lower:
        return "BUY"
    elif price > yhat_upper:
        return "SELL"
    else:
        return "HOLD"



  
def populate_stock_history(request):

    Historical_Stock_Data.objects.all().delete()
    Forecast_Record.objects.all().delete()

    stocks = Stock.objects.all()
    for stock in stocks:        
        populate_stock(stock)
        populate_history(stock)
    



    

    



