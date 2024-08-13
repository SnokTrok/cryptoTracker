import requests
from requests.exceptions import HTTPError
from cryptoTracker.application.utils import get_secret
from cryptoTracker.application.OHLCscan.models.api import OHLCPricesRequest
from retry import retry

"""
    see : https://syve.readme.io/reference/welcome-to-syve
"""

@retry(HTTPError,tries=3,delay=0,backoff=3,jitter=1)
def get_OHLC_price_history(req : OHLCPricesRequest):
    """
        Get coin price history from OHLC endpoint
    """
    endpoint = get_secret(['api','OHLCscan'])['endpoint']

    params = req.__dict__
    resp  = requests.get(endpoint,params=params)
    
    if resp.status_code != 200:
        raise HTTPError('An error occured trying to reach OHLC endpoint')
    
    return resp.json()