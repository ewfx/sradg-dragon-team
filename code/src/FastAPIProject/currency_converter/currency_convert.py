import requests
import  os
from dotenv import load_dotenv

class CurrencyConverter:

    _to_currency = ""
    def __init__(self, to_currency="USD"):
        load_dotenv()
        self._to_currency = to_currency
        self.api_key = os.environ.get("API_KEY")


    def __get_conversion_rate(self,from_currency):
        url = f"https://api.currencyfreaks.com/v2.0/rates/latest?apikey={self.api_key}&symbols={from_currency}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data:
                exchange_rate = round(float(data["rates"][from_currency]),1)
                return exchange_rate
            else:
                print("Error: Invalid API response or currency not found.")
                return None

        except requests.exceptions.RequestException as e:
            print(f"Error fetching exchange rates: {e}")
            return None
        except KeyError as e:
            print(f"KeyError: {e}, check api response format or currency codes")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    def get_conversion_rates(self,from_currencies):
        currency_conversion_rates = {}
        try:
            for from_currency in from_currencies:
                currency_conversion_rates[from_currency] = self.__get_conversion_rate(from_currency)
            return currency_conversion_rates
        except Exception as e:
            print(f"Error fetching exchange rates: {e}")
            return None

