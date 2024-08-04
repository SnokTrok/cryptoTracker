# **DISCLAIMER**

This project has been devised / scoped purely for my own learning purposes and as such there has been no financial gain, should anyone be interested in discussing taking this POC, or ideas / concept from it, further then I am open to the idea though this will require carefull budgeting consideration as many of the API's being used have seperate requirements for commercial use.

Many thanks for the free API plans provded by the following sources for making this possible:
- [getblock](https://getblock.io/) Used to get transactional information for the etherium block chain
- [OHLCscan](https://syve.readme.io/reference/price_historical_ohlc) found through [reddit](https://www.reddit.com/r/ethereum/comments/17h8f1d/i_built_a_free_full_historical_ohlc_crypto_price/) Used to get historical information for the Etherium block chain


# Initial Project Goals:

- To build a stock exchange storage database for later data analysis , Using pyhthon with pandas and sqlalchemy for ETL processes
- Use local postgres hosted database to store transformed data for later populating charts
- Live power charts showcasing market analysis for various stocks , for example crypto
- build local webapp for accessing / querying data from db realtime
- Build a prediction ML model from market data and grade it against historical data
- Build a comprehensive and user friendly way of viewing market information as a proof of concept web application

# Stretch goals
- scrape articles from the internet for stock news (can use an existing api for comparison)
- create auto trading logic and test against historical market states
- Build docker container for setting up project on any machine
- Build exmaple web deployment into AWS EC2 ?? (I want to get a deeper understanding of this and scalability factors)

## Initalisation :

The first roadblock I managed to encounter was related to my specific machine / VM setup , since I am using a windows computer with a VM Ubuntu image through WSL2 on limited internal SSD space I wanted to begin by creating my postgres data directory on a 2TB external harddrive , initially I tried to set this up through the postgres installation within WSL2, though due to the nature of the HDD (windows ntfs) and it containing data I didnt want to lose , I encountered issues trying to adjust file permission to allow WSL to rwx, meaning that the WSL postgres commands failed to initalize a db on the mounted drive, it took quite some time to find a solution to this and there was seemingly endless issues with using linux based commands to adjust permissions , changing owners , creating usergroups none of it worked!

The reason for this is mainly due to the drive / host machine itself rather than the VM, since the drive was formatted to ntfs (a windows friendly file system that thanksfully linux can also read) it wouldnt allow linux permission to overwrite/relax the windows ones meaning even files/dir created through the VM would follow default windows user perms, It seemed to me that the only way to allow this was to format the drive to GPT/exFAT of which would mean loosing that data as I had no way to back it up , alternatively I could try to relax the overall windows perms such that WSL2 can write to that HDD though again it would mean that changing permissions through WSL required to be more restrictive than windows level permissions.

I eventually came to a solution that worked , using windows level postgres installation to create / manage the db, though it wasn't without more headache , after downloading the windows installation , setting it up , creating the database , setting the storage to the external drive I was finally feeling like I was getting somewhere , after adjusting user credentials and susequently trying to connect to the created database through dbeaver showing a successfull connection I was excited to start making headway!

It was only after trying to access the db through WSL2 VM had I realized that more setup was required, specifically since the VM is recognized as a virtual system with its own runtime generated ip / port handling I wasnt sure how to get it to communicate with windows. After stumbling my way through stackexchange I came accross [the top comment](https://stackoverflow.com/questions/56824788/how-to-connect-to-windows-postgres-database-from-wsl) by `/u/xlm` which went into great detail the steps required to get this to work, after following along that comment , setting up my inbound rule (though severly limiting the allowed ports as that range is quite large and not without its risks) and some updates later due to using postgres  version 16+ I still couldnt connect.

It turns out the issue I was encountering was with the suggested route to find the windows accessable IP from within WSL , `/u/xlm` suggested using `"$(grep nameserver /etc/resolv.conf | awk '{print $2, "   winhost"}')"`  as a way of populating the runtime generated WSL2 windows IP into a handy to use host configuration which in my case was incorrect, instead using `dig +short "$(hostname).local" | head -n1` would yield the correct result, then all I had to do to connect was from within WSL2 command line : `psql -h winhost -U username` and press enter.

I then later verified that I could connect to this db through python using sqlalchemy and psycopg2.

I could finally begin devloping my RDB tables.

I decided to 'simulate' my own secret storage using internal files for runtime access of api keys / profile info , I have experience working with AWS Secrets Manager but since this project is designed for my use only I didnt want to start firing up an AWS Stack, Though a production implementation of this I would move from postgres to using redshift due to its columnar storage and incredibly fast read/write speeds.

## Next on the agenda :
- Create relation db tables for etherium market
- Pull historical etherium price information for later charting using [`etherscan`](https://docs.etherscan.io/api-endpoints/stats-1) api
- using websocket endpoints from binance we cna pull real time prices for many crypto see : https://www.youtube.com/watch?v=P_SIZDsI3Ro&ab_channel=NicholasRenotte


## Pulling historical ETH value :

Originally I was hoping to use the widely used etherscan api to get this, unfortunately it is locke dbehind a heft $199/mo paywall for the pro endpoints that includes historical information see : https://etherscan.io/apis though the code for accessing this has been included for anyone curious.

After some research I cam across [this reddit thread](https://www.reddit.com/r/ethereum/comments/17h8f1d/i_built_a_free_full_historical_ohlc_crypto_price/) in which `/u/112129` talks about a free to use OHLC historical endpoint they have created...
