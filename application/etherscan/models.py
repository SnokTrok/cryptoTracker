from datetime import datetime
from pydantic import BaseModel , model_validator

"""
    Pydantic validated models for etherscan requests , ensures we are ONLY using known params

    see : https://docs.etherscan.io/api-endpoints
"""

class EthereumHistoricalPriceRequest(BaseModel):
    module : str = "stats"
    action : str = "ethdailyprice"

    startdate : datetime
    enddate : datetime
    sort : str
    apikey : str


    @model_validator(mode='after')
    def validate_interval(self):
        """
            Validate our interavl start < interval end, AND interval start < now()
            ALSO validate format matches yyyy-MM-dd EG 2019-02-01
        """
        if self.enddate < self.startdate:
            raise ValueError('end_date must be greater than start_date -> closer to today')
        if self.startdate >= datetime.now():
            raise ValueError('start_date must be before today (datetime.now())')
        try:
            self.startdate = self.startdate.strftime(r'%Y-%m-%d')
            self.enddate = self.enddate.strftime(r'%Y-%m-%d')
        except:
            raise ValueError('Both start_date and end_date must be dattime in the format yyyy-MM-DD')
        return self
