import requests
from requests.exceptions import HTTPError
from decorator import decorator
from retry import retry

from cryptoTracker.application.utils import get_secret



"""
    see :
     - for pricing limitations https://getblock.io/pricing/
     - for node docs https://getblock.io/docs/
    
     

     Using JSON-RPC for most crytpo nodes with request library
"""
@decorator
def api_request(*args):
    """
        Simple wrapper for all api requests using retry options upon error , may extend for custom error handling
    """
    @retry(exceptions=(HTTPError),tries=3,delay=0,jitter=3,backoff=2)
    def wrapper(func , *args):
        resp = func(*args)
        return resp
    
    return wrapper
    

# region -------------- CLASSES ----------------------


class API():

    """
        Generic init class for getting api object
    """
    def __init__(self) -> None:
        self.secret = get_secret(['api','getBlock'])
    

def get_api() -> API:
    return API()
    
# endregion.
