import json 
import os

def get_nested_key_value(keys : list[str], secret : dict) -> dict:
    """
        Traverse through nested keys in secrets for single value retrieval
    """
    if len(keys) > 1:
        return get_nested_key_value(keys=keys[1:], secret=secret[keys[0]])
    try:
        return secret[keys[0]]
    except:
        raise


def get_secret(keys : list[str]) -> dict:
    """
        Fetch key or nested key value as [key1 , subkey , subsubkey , ...] from input
    """
    this_path = os.path.abspath(__file__)
    secret_file = f'{"/".join(this_path.split(r"/")[:-3])}/private/keys.json'
    try:
        with open(secret_file,'r') as f:

            if isinstance(keys,str):
                secret = json.load(f)[keys]
                return secret
            secret = json.load(f)[keys[0]]
    except:
        raise
    
    return get_nested_key_value(keys=keys[1:],secret=secret)