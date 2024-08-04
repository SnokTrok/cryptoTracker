import requests
from datetime import datetime
from requests.exceptions import HTTPError
from cryptoTracker.application.utils import get_secret
from cryptoTracker.application.etherscan.models import EthereumHistoricalPriceRequest
from retry import retry

"""
    For limitations on pricing plans for etherscan see : https://etherscan.io/apis

    Using the free plan gives us :
        - MAX 5 req per second
        - MAX 100,000 req per day

"""

class API():

    def __init__(self) -> None:
        self.secret = get_secret(["api","etherscan"])


    # TODO : retry wrap this request
    def get_eth_historical_price(self, start_date : datetime, end_date : datetime) -> dict:
        """
            Get eth historical pricing within input range
        """
        endpoint = self.secret['endpoint']
        key  = self.secret['key']

        req = EthereumHistoricalPriceRequest(
            startdate=start_date,enddate=end_date,
            sort='asc',apikey=key
        )
        print(req)
        resp = requests.get(endpoint,params=req.__dict__)
        assert resp.status_code == 200

        return resp.json()

