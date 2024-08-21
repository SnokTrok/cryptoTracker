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