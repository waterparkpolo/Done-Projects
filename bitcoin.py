import sys
import json
import requests
import locale
locale.setlocale(locale.LC_ALL, '')

def main():
    try:
        one_coin=float(sys.argv[1])
        one_bit=requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
        j=one_bit.json()
        J=one_coin*j["bpi"]["USD"]["rate_float"]
        J=round(J,4)
        print(f'${J:,}')
    except requests.RequestException:
        sys.exit("Command-line argument is not a number")
    except ValueError:
        sys.exit("Command-line argument is not a number")
    except IndexError:
        sys.exit("Missing command-line")
main()
#{
#    'time': {
#        'updated': 'Sep 28, 2024 21:18:07 UTC',
#        'updatedISO': '2024-09-28T21:18:07+00:00',
#        'updateduk': 'Sep 28, 2024 at 22:18 BST'
#        },
#    'disclaimer': 'This data was produced from the CoinDesk Bitcoin Price Index (USD). Non-USD currency data converted using hourly conversion rate from openexchangerates.org',
#    'chartName': 'Bitcoin',
#    'bpi': {
#        'USD': {'code': 'USD', 'symbol': '&#36;', 'rate': '65,568.995', 'description': 'United States Dollar', 'rate_float': 65568.9953},
#        'GBP': {'code': 'GBP', 'symbol': '&pound;', 'rate': '49,038.199', 'description': 'British Pound Sterling', 'rate_float': 49038.1992},
#        'EUR': {'code': 'EUR', 'symbol': '&euro;', 'rate': '58,693.103', 'description': 'Euro', 'rate_float': 58693.1026}}}
