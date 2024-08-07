from datetime import datetime
from pydantic import BaseModel, Field, field_validator, ValidationInfo, model_validator


# see : https://syve.readme.io/reference/price_historical_ohlc
class OHLCPricesRequest(BaseModel):
    token_address : str = Field(...,title='Contract Address for token.')
    pool_address : str = Field('all', title='The address of the liquidity pool from which the OHLC prices will be fetched.')
    chain : str = Field('eth', title='Chain to pull price history from.')
    price_type : str = Field('price_token_usd_robust_tick_1' , title='This parameter determines what price to use to create OHLC with.')
    interval : str = Field('1d', title='Interval to return aggregate stats for , 1d = daily 1m = minuite')
    from_timestamp : int = Field(...,title='Return results whose timestamp_open are greater than or equal to the provided value.')
    until_timestamp : int = Field(...,title='Return results whose timestamp_open are less than or equal to the provided value.')
    max_size : int = Field(2500,title='Maximum number of records to return',gt=0,lt=2501)
    order : str = Field('asc',title='Return in asc or desc order')
    fill : bool = Field(False, title='flag to forward fill gaps in trade')
    with_volume : bool = Field(True , title='Return volume information with resp.')
    open_method : str = Field('first_trade', title='Determines how to calculate the open price.')

    @field_validator('price_type')
    def price_type_validator(cls, value : str, info: ValidationInfo):
        price_types = [
            'price_token_usd_tick_1',
            'price_token_usd_robust_tick_1',
            'price_token_usd_robust_total_{1h|24h}',
            'price_token_usd_robust_buy_{1h|24h}',
            'price_token_usd_robust_sell_{1h|24}',
            'price_token_usd_robust_mid_{1h|24h}'
        ]
        assert value in price_types, f'valid price types are : {price_types}'
        return value
    
    @field_validator('chain')
    def chain_validator(cls, value : str, info: ValidationInfo):
        chains = [
            'eth',
            'matic'
        ]
        assert value in chains, f'Valid chains are : {chains}'
        return value
    
    @field_validator('open_method')
    def open_method_validator(cls, value : str, info: ValidationInfo):
        open_methods = [
            'first_trade', 'prev_close'
        ]
        assert value in open_methods , f'Valid open_methods are : {open_methods}'
        return value
    
    @model_validator(mode='before')
    def validate_timestamps(cls , values) -> dict:
        """
            from_timestamp and until_timestamp are both integers Unix EPOCH times,
            this method is just to validate that the range is appropriately initilized

            in our case we will accept string in the format yyyy-mm-dd and explicitly convert them to datetime for 
            validation , then to unix Epoch.
        """
        dt_cols = ['from_timestamp' , 'until_timestamp']

        for col in dt_cols:
            try:
                values[col] = datetime.strptime(values[col],'%Y-%m-%d').timestamp()
            except Exception as e:
                print(e)
                raise ValueError(f'{col} must be supplied as a str in the yyyy-mm-dd format...')
        
        assert values['from_timestamp'] < values['until_timestamp'], 'from_timstamp must be before until_timestamp'
        return values