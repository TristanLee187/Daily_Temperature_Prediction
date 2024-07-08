from KalshiClientsBaseV2 import ExchangeClient, HttpError
from kalshi_credentials import *
from predict import predict
import uuid

demo_api_base = "https://demo-api.kalshi.co/trade-api/v2"

exchange_client = ExchangeClient(exchange_api_base = demo_api_base, email = demo_email, password = demo_password)

tickers = {
    'austin': 'HIGHAUS',
    'chicago': 'HIGHCHI',
    'miami': 'HIGHMIA',
    'ny': 'HIGHNY'
}

# date string to append to the ticker, should be today!
date_string ='24MAR22'

# get predictions for the next day in the data, should be today! 
predictions = predict()
print(predictions)

for loc in tickers:
    prediction = round(predictions[loc])

    # get the ticker corresponding to the closest temperature range to the prediction
    prediction_ticker = ''
    ticker_found = False

    # if the predicted temperature is already in a ticker, use that one
    try:
        exchange_client.get_market(f'{tickers[loc]}-{date_string}-B{prediction + 0.5}')
        prediction_ticker = ticker
        ticker_found = True
        break
    except HttpError:
        try:
            exchange_client.get_market(f'{tickers[loc]}-{date_string}-B{prediction - 0.5}')
            prediction_ticker = ticker
            ticker_found = True
            break
        except HttpError:
            pass

    # if its the predicted temperature doesn't correspond to a ticker, we have to incrementally
    # search for the right one
    delta = 0

    while not ticker_found:
        attempt_tickers = [
            f'{tickers[loc]}-{date_string}-T{prediction + delta}',
            f'{tickers[loc]}-{date_string}-T{prediction - delta}',
        ]

        for ticker in attempt_tickers:
            try:
                exchange_client.get_market(ticker)
                prediction_ticker = ticker
                ticker_found = True
                break
            except HttpError:
                continue
        
        delta += 1

    print(loc, prediction_ticker)

    # complete the order
    order_params = {
        'ticker': prediction_ticker,
        'client_order_id': str(uuid.uuid4()),
        'type': 'limit',
        'action': 'buy',
        'side': 'yes',
        'count': 10,
        'yes_price': 50
    }

    exchange_client.create_order(**order_params)
