import requests as re

def get_exchange_rates(to_currency: str, secrets: dict) -> float:
    """
        Finds the exchange rate to USD for a given currency.
        Params: 
            to_currency: The currency you want to convert into USD
        Returns:
            a float of the exchange rate
    """

    API_KEY = secrets["api_key"]

    # Get request
    url = "https://openexchangerates.org/api/latest.json"
    params = {
        "app_id":API_KEY,
        "base":"USD",
        "symbols": to_currency
    }

    response = re.get(url, params=params)
    json_response = response.json()
    exchange_rate_to_currency = json_response["rates"]["CAD"]
    exchange_rate_to_USD = round(1 / exchange_rate_to_currency, 4)

    return exchange_rate_to_USD