# Live charting DEX data using Binance websockets

From here I wanted to start experimenting with streaming data to a live populated candlestick chart, from my preliminary research I found that Binance has free publicly available websocket subscriptions that allow exactly this at paramater driven intervals.

A quick search to deepen my understanding led me to [this article](https://www.pubnub.com/guides/websockets/) detailing what websockets are, their main differences including :
- allows the live back and forth communication between client and server 
- creates a continuous live connection between client and server
- negates the need to for consistent polling to achieve low latency communication

with some drawbacks including:
- vulnerability issues arising when TLS/SSL encryption is not setup on the live connection properly
- scalability considerations for large user base applications since the connection must stay open 
- backwards compatability limited since older browser systems may not support websockets

In my case these drawbacks are neglible for the following reasons :
1) I am only running local webapp deployments so security shouldnt be an issue , I have already limited the inbound rules port range to my specific machine as well as only to the postgres application itself
2) I have no intention of deploying this as a public application for others to subscribe to , I merely want to create some working examples
3) Most users nowadays use modern browser technology which by default supports websockets

Another interesting alternative for asynchronous communication is SEE (server sent events) of which does operate on the HTTP protocol though due to Binances implementation of websockets I wont be diving into this for now...

You can find an example of me using the binance websockets and formatting the data in [this notebook](../../notebooks/RealTimeCryptoPriceExtraction.ipynb)

For storing all of this data I decided to implement another database schema in postgres titles "exchange" , this is because unlike the OHLCscan endpoint that is givig me crypto -> USD (presumably using USDT conversion) the binance stream allows me to subscribe to various crypto -> crypto conversion rate data, meaning we could go from WBTC -> WETH for example rather than to USD. In light of this I wanted to seperate the data I was gathering from this process from the data being pulled from OHLCscan.

Following are the tables used for this:

```sql
create table exchange.token (
		id serial primary key,
		"name" VARCHAR(10)
);


create table exchange.price_history (
	token_id INTEGER,
	date_open TIMESTAMP without TIME zone not null,
	date_close TIMESTAMP without TIME zone not null,
	price_open Numeric(10,6),
	price_close Numeric(10,6),
	price_high numeric(10,6),
	price_low NUMERIC(10,6),
	volume NUMERIC(15,6),
	num_trades INTEGER,
	constraint fk_token_id foreign key (token_id) references exchange."token" (id) on update cascade on delete cascade,
	constraint token_id_date_open_pk primary key (token_id, date_open)
);
```

I am aware that the devloper(s) working on OHLCscan are implementing and actively developing DEX endpoints as part of their api and I will be looking at this at a later date.


from learning about websockets I would like to try to implement my own in the form of a realtime Unity multiplayer project, one to add to the list for sure!

From here all I needed to do was format the websocket response into a pandas dataframe , to do this I firslty defined the schema in pandera to ensure consistent data formatting
```python
binance_kline_message_schema = DataFrameSchema(
    columns={
    'symbol' : Column('string') ,
    'price_open' : Column('Float64' , nullable=False),
    'price_close' : Column('Float64' , nullable=False),
    'price_low' : Column('Float64' , nullable=False),
    'price_high'  : Column('Float64', nullable=False),
    'date_open' : Column('datetime64[ns]',nullable=False),
    'date_close' : Column('datetime64[ns]', nullable=False)
    },
    strict=True,
    coerce=False
)
```

This schema was also used to generate an empty dataframe for initializing the chart on application startup.

One issue I encountered when integrating this into my webapplication was the websocket.run_orever() method caused the main thread to hang , this makes sense since that function opens up the data stream and constantly listens for a response, from this I knew I had 2 options , one modify my existing thread to use asynchronous methods (somewhat equivalent to c# coroutines) or to open a seperate thread, some considerations for both:

**Async:**
- An async method requires me to periodically yield from the websocket functions to continue the applciation execution, this could mean it gets in the way of important callback events from dash.
- 

**New Thread:**
- A new Thread means syncing clocks between websockets stream and my main applicaiton becomes tricky , in my case however since we are only populating the data from this websocket thread some desync shouldnt really matter , nothing will overwrite the data coming from websockets in my main thread , we are also retrieving a 1m interval stream of data 
- Using a new thread means handling every exception within this thread explicitly myself, since the thread itself will just hang with little obvious  trace If I can run into any fatal errors that SHOULD halt the entire application I need to hard enforce this using the threads on_error callback method.
- multi threading is complex and tends to require higher resource usage
- multi threading can introduce other issues including race conditions (multiple threads attempting to access the same data) locks (single thread controlled data , blocking other threads from modiying) and deadlocks (multiple threads waiting to acquire locks from one another , preventing the execution of both)

in most cases async/await is the better option due to scalability / mainatability concerns with multi threading.

I firstly tried the multi threaded approach , this worked great to begin with but as mentioned earlier made debugging slightly more cumbersome having to route the errors through to the main event via a callback : 


```python
def on_error(ws , err):
    print(f"[red]An exception occured in websocket thread! {err}[grey]")

async def open_websocket_thread():
    print("Opening websocket listening thread...")
    ws_thread = threading.Thread(target=open_binance_websockets)
    ws_thread.start()
    await asyncio.sleep(1)


async def open_binance_websockets():
    #global websockets
    global exchange_data
    #websocket.enableTrace(True)
    # currency websocket endpoints to subscribe to 
    subscribed_symbols = ['WBTCUSDT']#, 'WBTCETH']

    # kline_1m -> per min updated stream of data 
    subscribed = "/".join([coin.lower() + '@kline_1m' for coin in subscribed_symbols])
    socket = "wss://stream.binance.com:9443/stream?streams=" + subscribed
    ws = websocket.WebSocketApp(socket, on_message=on_binance_kline_message , on_open=on_websocket_start, on_error=on_error)
    websockets.append(ws)
    ws.run_forever()
```

after some time working with this I decided it would be good practice to try the asyncio approach as this is a programming paradigm in webapplications that can handle many more concurrent user requests simultaneously, I also was not looking forward to te increasing complexity this project is bound to face whilst managing multi threading with my lack of exposure to such methodologies.


I began by first trying to setup the asyncio event loop with my existing code, though quickly found myself faces with issues revelving around integrating the event loop with the defaultly syncronous loop Flask uses , and by extension Dash , after looking online for solutions I found [dash-extensions](https://www.dash-extensions.com/components/websocket) package that includes handling websocket connections via a custom component which allows me to stream the recv() from the bininace websocket through to a dash callback funciton , negating my previously expected need to use the Interval component to regularly look for updated live data.

After a short while I managed to implement a working live stream that didnt interrupt my main thread!

Before moving onto playing about with LSTM training, there were a few quality of life changes I wanted to make t my project:
- the RangeSlider feature could do with some TLC since it is hard to pick exact dates and it seems the interval shifting is off in code somewhere for this I want to move over to the [DatePickerRange](https://dash.plotly.com/dash-core-components/datepickerrange) dash component
- Storing the streamed websocket data to my local db for future use to complete the live cycle


solving the first issue is relatively straighforward , just changing out our layout.py and callbacks.py to accomodate the new component format : 
```python
#------------- FROM layout.py------------------------------

def load_dt_slider( date_min  : datetime, date_max : datetime) -> dcc.DatePickerRange:
    """
        Constructs a slider using EPOCH integer ranges , but display as datetime conversions?
    """
    # remove time from datetime components
    date_min = date_min.date()
    date_max = date_max.date()

    start_date =starting_data_filter[0].date()
    end_date = starting_data_filter[1].date()

    return dcc.DatePickerRange(
        min_date_allowed=date_min,
        max_date_allowed=date_max,
        initial_visible_month=start_date,
        start_date=start_date,
        end_date=end_date,
        id='drp-interval-filter'
    )

#--------- AND FROM callbacks.py-------------------------------

	    @dash_app.callback(
            Output('static-price-history-candle-graph' ,'figure'),
            Output('static-price-history-line-graph' ,'figure'),
            Input('dd-token-select', 'value'),
            Input("drp-interval-filter" , 'start_date'),
            Input("drp-interval-filter" , 'end_date')
        )
    def change_token(token_id , date_start , date_end):# , start_date , end_date):

        token_id = set_current_token_id(token_id)

        df_history = token_data[token_id]['price_history']

        print(f'{date_start} - {date_end}')
        date_mask = (
            df_history.date_open.ge(date_start) & df_history.date_close.le(date_end)
        )
        df_filtered = df_history.loc[date_mask]

        # build graphs
        candle_fig = generate_candlestick_price_history_graph(df_history=df_filtered,token_name=token_data[token_id]['token_name'],token_identifier='')
        line_fig = generate_line_price_history_graph(df_history=df_filtered,token_name=token_data[token_id]['token_name'],token_identifier='')
        return candle_fig , line_fig
```

whilst this is still not very good in terms of UX , it will do for now , long term though following an actual design page for styling would be ideal.



# DEVLOG : 
- [entry5](/devlog/entry5.md)   