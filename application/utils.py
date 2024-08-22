import json 
from pandas import DataFrame
import os
from pandera import DataFrameSchema

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


def empty_dataframe_like(schema : DataFrameSchema) -> DataFrame:
    """
        Construct empty dataframe from schema , ensures passing schema validation on init.
    """
    column_names = list(schema.columns.keys())
    data_types = {column_name: column_type.dtype.type.name for column_name, column_type in schema.columns.items()}
    return DataFrame(columns=column_names).astype(data_types)