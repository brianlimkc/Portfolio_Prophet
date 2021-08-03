# Project 4 - Portfolio Prophet

## Description

A fully responsive stock portfolio tracking and forecast app, which leverages Facebook Prophet to provide basic forecasts of whether you should hold, buy or sell a stock.

Try it out here - https://portfolio-prophet.herokuapp.com/

### Tech Used

- React
- Material UI
- Bootstrap
- Axios
- Django
- Python
- Facebook Prophet
- Django Rest Framework
- PostgresSQL
- Cron job

## Wireframes

<img src="https://i.imgur.com/m7CpRYJ.png">

<img src="https://i.imgur.com/q9ZhiyG.png">

<img src="https://i.imgur.com/AmxB5nd.png">


## User Stories

A user will be able to:
- View information on all stocks on the NASDAQ 100
- View historical stock data and forecasted future price of individual stocks
- View a shortlist of stocks with the highest projected price increases
- Create a watchlist of stocks 
- Create a portfolio of stocks 

## Planning and Development Process

- The project was chosen as we wanted to challenge ourselves by building an app which not only can be used view and track stock information, but is able to add value by providing a forecast of the projected stock price.
- We made use of yahoo finance API to obtain stock data, and Facebook Prophet as a fast and easy to use forecasting tool in order to generate our stock forecasts

## Problem Solving Strategy

- Our team realised early on that due to the large amount of data which needs to be pulled from yfinance and the time taken to generate the forecast (about 10-15seconds per stock), that there was a need to pre-generate all the forecast data and store it on a database on a daily basis, so that loading times when viewing individual stocks can be greatly reduced. 
- We limited our list of stocks to the NASDAQ 100 in order to make it more manageable.
- We refined our database models to streamline the amount of information to be stored, and rewrote our functions so that it would run more quickly. We also finetuned the frontend modules so that it would load more quickly. 
- We used Cron Job to run a batch process which runs at 2am every night to pull the required stock data from yahoo finance, run the forecast algorithm and write the results into a PostgresSQL on Supabase.io. 
- As a result of this, we managed to get individual load times down to 1-2s per stock. 

### Database

![ERD](https://i.imgur.com/LU7M3Q3.png)

We used a relational database model for our application which was built via Django. 

Starting from the left, we have a table for our Users, these will store their credentials such as username, email and password which ties to a uuid (generated automatically on user registration). Password is hashed when it is stored.

For every User, we intend to allow them to store multiple Portfolios. Portfolios allow segregation of User's Stocks by their Portfolios and is meant to track Stocks that the User owns and how much growth it has.

Each User will also be able to track certain Stocks in their Watchlist. Watchlists are meant to display Stocks that User wants to monitor but not yet buy/sell.

To allow identical info for stock data, across the different table, we store Stock info pulled from the api into the Stock table. The Stock table is linked to the Portfolio_Stock, Watchlist, Stocks_Tracked, Historical_Stock_Data and Recommendation tables

Due to the Prophet algorithm requiring historical data to run forecasts, we will store the data in Historical_Stock_Data for the algorithm to run on. Each time the app is loaded, only the new stock data is pulled to reduce loading time. 

Once the forecast is made from Prophet, we store the recommendation into the Recommendation table, as the algorithm requires time to process, we only schedule it to run daily and update this table. When displaying the Recommendation to the user, we will simply pull the data from this table which will increase the speed of loading.

## Acknowledgement

### Team Members

- Brian Lim
- Tan Kai Lin
- Chua Kai Ming

### Credits

I would like to thank Ebere and Isaac for their support and encouragement for this project!
![Screenshot 2021-07-29 at 1 31 20 PM](https://user-images.githubusercontent.com/76930093/127991734-8372a1ee-ce34-48dc-b638-84235745fae1.png)


