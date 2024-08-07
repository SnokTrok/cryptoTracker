# Plotting data using matplotlib and plotly


Now that I finally have some data stored I can begin to build visualisations from it, intitially I will be usign ployly with jupyter for prototyping this, but evetuallly I would like to look into live graphing tools for python web apps that I can deploy locally.

Plotly contains some easy to use candlestick charting functions :  https://plotly.com/python/candlestick-charts/

an interactive display can be found at: [TrackingHistoricalCoinPrices.ipynb](../../notebooks/TrackingHistoricalCoinPrices.ipynb)

To validate this data I will be cross referencing it to the previously linked eg. [(USDT))](https://coinranking.com/coin/HIVsRcGKkPFtW+tetherusd-usdt)

As you can see there is a clear correlation between the two shapes implying the data I am using is fairly accurate.

However from the generated charts we can clearly see some prety extreme reported price_low values especially for Tether (USDT) , this could be due to a number of things but in most cases implies some form of outlier
to remedy this we can ammed our logic to either bfill the price_low from previous records when we get either a null value or 0.
