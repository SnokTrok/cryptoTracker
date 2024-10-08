# Plotting data using matplotlib and plotly


Now that I finally have some data stored I can begin to build visualisations from it, intitially I will be usign ployly with jupyter for prototyping this, but evetuallly I would like to look into live graphing tools for python web apps that I can deploy locally.

Plotly contains some easy to use candlestick charting functions :  https://plotly.com/python/candlestick-charts/

an interactive display can be found at: [TrackingHistoricalCoinPrices.ipynb](../../notebooks/TrackingHistoricalCoinPrices.ipynb)

To validate this data I will be cross referencing it to the previously linked eg. [(USDT))](https://coinranking.com/coin/HIVsRcGKkPFtW+tetherusd-usdt)

As you can see there is a clear correlation between the two shapes implying the data I am using is fairly accurate.
<div>
<img src="img/Tether%20USDT%20validation.jpg" alt="drawing" width="200" style='inline'/>
<img src="img/Tether USDT example.jpg" alt="drawing" width="200" style='inline'/>
<img src="img/Wrapped BTC validation.jpg" alt="drawing" width="200" style='inline'/>
<img src="img/Wrapped BTC example.jpg" alt="drawing" width="200" style='inline'/>
<img src="img/Lido Staked Ether validatio.jpg" alt="drawing" width="200" style='inline'/>
<img src="img/Lido Staked Ether example.jpg" alt="drawing" width="200" style='inline'/>
</div>


However from the generated charts we can clearly see some prety extreme reported price_low values especially for Tether (USDT) , this could be due to a number of things but since the data is non 0 in most cases its hard to say wether it is an objective outlier or not, for the sake of our predictive model I will forward fill the open price from the previos candlestick if it is <= a certain threshold, another alternative we can use to identify ourliers would be using a standard deviation on the derivitive , in which we could apply a smoothing function to normalize our trends.



From here I wanted to look at creating a webapp portal for displaying the data / interacacting with it froma user perspective, it is good to abstract a lot of complexity and functionality from this as it will create a much more overall streamlined process, not to mention in most cases users wont want to be bombarded with complexity for them to achieve a relatively simple task.

I will be using Flask for v1 of this webapp although I do wnat to do a bit more research on Guvicorn applications and how they compare to the flask framework, from my preliminary search it seems that Flask uses the older Gunicorn solution which is limited on a single "threaded" approach (Note I use commas around threaded since it is actually refferencing a more Synchronos approach versus actual threading , the differences of which can get pretty difficult to track but it is mainly from multi-threaded running seperate process loops against specific CPU cores where as an asynchronous approach creates a task scheduling loop on a single thread similar to .nets coroutines)


To get started with this I decided to create a package from my project, this ensures consistant build information for installing the project fromfresh in the future , I also decided to create an __init__.py file containing my flask application instantiation , this means that I can develop my flask application and run it using  flask run after setting the correct environment variables as well as ensuring all my view files can import the same application instance.

Interestingly it seems the python community is movign away from the legacy installation config of using requirements.txt and setuptools and instead to solely using pyproject.toml to define project dependencies. At this point in the development of the project I had started using a requirements.txt file to house all of my package versions though this doesnt seeem neccesssary as I have no intention of downgrading my python version , in light of this I ammended the tomlfile to include package versions.

Anyway back to flask...

my entry point for the application is as follows : 
```python
@app.route('/')
def entry_point():
    template = r'main.html'
    # load the view on tokens into buttons etc... TODO
    return render_template(template)
```

The next task was to figure  out how to generate simple html at runtime and dependant on user input

from here I can modify the HTML script using plotly .to_html() to generate webapp renderable graphs.

This worked great to begin with , only it required refreshing the entire page everytime I wanted to switch the token view which isnt ideal, I decided to do some  more research into using dash with plotly figures.

A standard dash application actually launches a flask app itself that it then embedds the dash app onto , I could rewrite everything under this paradigm although it does mean using purely dash to do everything and makes it more cumbersome and means everything I add to this project would need to sit within this, I decided to take a different approach and override the dash initialisation to instead piggyback off of the existing flask app I had created, this required a bit of trial and error with setup but I got there in the end , with this I can now leverage all of dashs' feedback capabilities whilst also keeping any static pages / authentication within flask , best of both worlds.

After recreating my selector in dash and using its callback decorator I could now change token views whilst only refreshing the html elements that depend on it, resulting in a much better user experience. Next I want to link graphs together such that viewing data from one will automatically view linked data across charts for example see : https://dash.plotly.com/interactive-graphing

<div>
<img src="img/dash_setup.jpg" alt="drawing" width="400" style='inline'/>
</div>

I achieved a simple implementation of this using dash's callback decorator to output to 2 figures simultaneously , adding in a range slider to filter the data by date.


# Devlog
- [`entry4`](/devlog/entry4.md)