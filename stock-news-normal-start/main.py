import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = '' # Daily 25 limited
NEWS_API_KEY = ""

account_sid = ''
auth_token = ''

stock_parameters = {
    "function" : "TIME_SERIES_DAILY",
    "symbol" : STOCK_NAME,
    "apikey" : STOCK_API_KEY
}

response = requests.get(url=STOCK_ENDPOINT, params=stock_parameters)
response.raise_for_status()
stock_data = response.json()

## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

stock_price = [value for (key,value) in stock_data["Time Series (Daily)"].items()]
yesterday_data = stock_price[0]
yesterday_closing_price = stock_price[0]['4. close']

the_day_before_yesterday_data = stock_price[1]
the_day_before_yesterday_data_closing_price = stock_price[1]['4. close']

difference = abs(float(yesterday_closing_price) - float(the_day_before_yesterday_data_closing_price)) # 분모를 뭐로할지 세팅.

diff_percent = (difference / float(yesterday_closing_price)) * 100

## STEP 2: https://newsapi.org/
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.


if diff_percent > 0:
    news_parameters = {
        "qInTitle": COMPANY_NAME,
        "apiKey": NEWS_API_KEY
    }

    news_response = requests.get(url=NEWS_ENDPOINT, params=news_parameters)
    news_response.raise_for_status()
    articles = news_response.json()["articles"]
    three_articles = articles[:3]

    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number.

    formatted_articles = [f"Headlines : {article['title']}. \nBrief : {article['description']}" for article in three_articles]

    client = Client(account_sid, auth_token)

    for article in formatted_articles:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
        from_='+18884387182',
        body=article,
        to='+18777804236'
        )
        print(message.sid)

#Optional TODO: Format the message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

