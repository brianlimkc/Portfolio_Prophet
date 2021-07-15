from django.shortcuts import render
import yfinance as yf
from prophet import Prophet
import datetime
from stocks.models import *
from accounts.models import *
from django.http.response import JsonResponse
from stocks.serializers import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
def show_stock(request):

    stock = request.GET.get("stock")

    if stock==None:
        stock="GOOG"

    try:
        stock_record = Stock.objects.get(symbol=stock)
    except Stock.DoesNotExist:
        new_stock = Stock(symbol = stock)
        populate_stock(new_stock)
        populate_history(new_stock)
        stock_record = new_stock

    stock_record = Stock.objects.get(symbol=stock)
    stock_record_json = stock_record.serialize()
    # historical_record = Historical_Stock_Data.objects.filter(stock_id = stock_record.id)
    # historical_record_all = [r.serialize() for r in historical_record]
    forecast_record = Forecast_Record.objects.filter(stock_id = stock_record.id)
    forecast_record_all = [r.serialize() for r in forecast_record]

    return JsonResponse({
        "stock_record": stock_record_json,
        "historical_record" : historical_record_all,
        "forecast_record" : forecast_record_all
        })


def show_all(request):
    stock_record = Stock.objects.all()
    stock_record_all = [s.serialize() for s in stock_record]

    return JsonResponse({
        "stock_record_all": stock_record_all,
        })


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
    start_date = end_date - datetime.timedelta(days=2*365)
    delta = datetime.timedelta(days=1)
    period = 1 * 365

    data = yf.download(stock.symbol, start_date, end_date)

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

        date = datetime.datetime.fromtimestamp(fdate[0]/1000000000)
        data_row = data[data.index==index]["Close"]

        try:
            priceR = float(data_row)
        except:
            priceR = 0

        print(priceR)

        forecast_record = Forecast_Record(
            stock_id = stock,
            date = date,
            yhat = yhat[0],
            yhat_upper = yhat_upper[0],
            yhat_lower = yhat_lower[0],
            price = priceR,
        )

        forecast_record.save()

    stock.yhat_30 = round(forecast["yhat"][forecast_length-335],2)
    stock.yhat_30_upper = round(forecast["yhat_upper"][forecast_length-335],2)
    stock.yhat_30_lower = round(forecast["yhat_lower"][forecast_length-335],2)
    stock.yhat_30_advice = recommendation(stock.current_price,stock.yhat_30_upper,stock.yhat_30_lower)
    stock.yhat_180 = round(forecast["yhat"][forecast_length-185],2)
    stock.yhat_180_upper = round(forecast["yhat_upper"][forecast_length-185],2)
    stock.yhat_180_lower = round(forecast["yhat_lower"][forecast_length-185],2)
    stock.yhat_180_advice = recommendation(stock.current_price,stock.yhat_180_upper,stock.yhat_180_lower)
    stock.yhat_365 = round(forecast["yhat"][forecast_length-1],2)
    stock.yhat_365_upper = round(forecast["yhat_upper"][forecast_length-1],2)
    stock.yhat_365_lower = round(forecast["yhat_lower"][forecast_length-1],2)
    stock.yhat_365_advice = recommendation(stock.current_price,stock.yhat_365_upper,stock.yhat_365_lower)
    stock.save()


def recommendation(price,yhat_upper,yhat_lower):
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

    return Response({"message" : "Stock info fetched and populated"}, status=status.HTTP_200_OK)


def populate_stocksdb(requests):
    symbols = [
        "AAPL",
        "ADBE",
        "ADI",
        # "ADP",
        # "ADSK",
        # "AEP",
        # "ALGN",
        # "ALXN",
        # "AMAT",
        # "AMD",
        # "AMGN",
        # "AMZN",
        # "ANSS",
        # "ASML",
        # "ATVI",
        # "AVGO",
        # "BIDU",
        # "BIIB",
        # "BKNG",
        # "CDNS",
        # "CDW",
        # "CERN",
        # "CHKP",
        # "CHTR",
        # "CMCSA",
        # "COST",
        # "CPRT",
        # "CSCO",
        # "CSX",
        # "CTAS",
        # "CTSH",
        # "DLTR",
        # "DOCU",
        # "DXCM",
        # "EA",
        # "EBAY",
        # "EXC",
        # "FAST",
        # "FB",
        # "FISV",
        # "FOX",
        # "FOXA",
        # "GILD",
        # "GOOG",
        # "GOOGL",
        # "IDXX",
        # "ILMN",
        # "INCY",
        # "INTC",
        # "INTU",
        # "ISRG",
        # "JD",
        # "KDP",
        # "KHC",
        # "KLAC",
        # "LRCX",
        # "LULU",
        # "MAR",
        # "MCHP",
        # "MDLZ",
        # "MELI",
        # "MNST",
        # "MRNA",
        # "MRVL",
        # "MSFT",
        # "MTCH",
        # "MU",
        # "MXIM",
        # "NFLX",
        # "NTES",
        # "NVDA",
        # "NXPI",
        # "OKTA",
        # "ORLY",
        # "PAYX",
        # "PCAR",
        # "PDD",
        # "PEP",
        # "PTON",
        # "PYPL",
        # "QCOM",
        # "REGN",
        # "ROST",
        # "SBUX",
        # "SGEN",
        # "SIRI",
        # "SNPS",
        # "SPLK",
        # "SWKS",
        # "TCOM",
        # "TEAM",
        # "TMUS",
        # "TSLA",
        # "TXN",
        # "VRSK",
        # "VRSN",
        # "VRTX",
        # "WBA",
        # "WDAY",
        # "XEL",
        # "XLNX",
        # "ZM",
        ]

    for symbol in symbols:
        stock = Stock(
            symbol = symbol
        )
        stock.save()

    return Response({"message" : "Stocks inserted into DB"}, status=status.HTTP_200_OK)



@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def watchlist(request):
    user_id = request.user.id
    if request.method == "POST":
        stock_id = request.data["id"]
        try:
            user = User.objects.get(pk=user_id)
        except:
            print("user not found")
        try:
            stock = Stock.objects.get(pk=stock_id)
        except:
            print("stock not found")

        if len(Watchlist.objects.filter(user_id=user_id,stock_id=stock_id)) == 0:
            watchlist_record = Watchlist(
                user_id = user,
                stock_id = stock,
            )
            watchlist_record.save()
        return Response({"message" : "Stock saved into user watchlist"}, status=status.HTTP_201_CREATED)


    if request.method == "GET":
        watchlist = Watchlist.objects.filter(user_id=user_id)
        watchlist_stocks = []
        for w in watchlist:
            watchlist_record = w.serialize()
            watchlist_stock = Stock.objects.get(pk=watchlist_record["stock_id"].id).serialize()
            watchlist_stocks.append(watchlist_stock)
        return JsonResponse({"watchlist_stocks" : watchlist_stocks})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def watchlist_delete(request):
    user_id = request.user.id
    if request.method == "POST":
        stock_id = request.data["id"]
        try:
            user = User.objects.get(pk=user_id)
        except:
            print("user not found")
        try:
            watchlist = Watchlist.objects.filter(user_id=user_id, stock_id=stock_id)
        except:
            print("stock not found")
        for w in watchlist:
            w.delete()
        return Response({"message" : "Stock deleted from user watchlist"}, status=status.HTTP_200_OK)

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def portfolio(request):

    user_id = request.user.id

    if request.method == "POST":
        stock_id = request.data["id"]
        try:
            user = User.objects.get(pk=user_id)
        except:
            print("user not found")
        try:
            stock = Stock.objects.get(pk=stock_id)
        except:
            print("stock not found")
        portfolio_record = Portfolio(
            user_id = user,
            stock_id = stock,
            quantity = request.data['quantity'],
            price = request.data['price'],
            date = request.data['date'],
        )
        portfolio_record.save()
        return Response({"message" : "Stock saved into user portfolio"}, status=status.HTTP_201_CREATED)

    if request.method == "GET":
        portfolio = Portfolio.objects.filter(user_id=user_id)
        portfolio_stocks = []
        portfolio_records = []
        for p in portfolio:
            portfolio_record = p.serialize()
            portfolio_records.append(portfolio_record)
            portfolio_stock = Stock.objects.get(pk=portfolio_record["stock_id"].id).serialize()
            portfolio_stocks.append(portfolio_stock)

        return JsonResponse({"portfolio_stocks" : portfolio_stocks, "portfolio_records" : portfolio_records})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def portfolio_delete(request):

    user_id = request.user.id

    if request.method == "POST":
        stock_id = request.data["id"]
        try:
            user = User.objects.get(pk=user_id)
        except:
            print("user not found")
        try:
            portfolio_records = Portfolio.objects.filter(user_id=user_id, stock_id=stock_id)
        except:
            print("stock not found")
        for p in portfolio_records:
            p.delete()
        return Response({"message" : "Stock(s) deleted from user portfolio"}, status=status.HTTP_200_OK)
