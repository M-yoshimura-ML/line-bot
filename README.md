# Line Bot Dev
## framework
- Flask 3.0.3
## MongoDB
- Using MongoDB Atlas
## Package install
- `pip install Flask`
- `pip install requests`
- `pip install pytz`
- `pip install pymongo`  
## Scheduler job
if you want to run job in local, you need to install APScheduler
- `pip install APScheduler`
- uncomment some block of lines in `main.py` 

so that you can check time notify function in local or Line bot

## Hosting Server 
- Vercel: https://vercel.com/
- Cron job setting: see file `vercel.json`
- After deploying modules to vercel, get endpoint url something like: https://xxxxx.vercel.app/
-  you need to set up the endpoint at LINE DEVELOPER webhook
https://developers.line.biz/console/
## Get API Credentials 
- LINE MESSAGING API TOKEN 
- LINE USER ID (This is used internally in your LINE app)
- WEATHER API KEY
- RAKUTEN APP ID
- GOOGLE CUSTOM SEARCH ENGINE ID
- GOOGLE CUSTOM SEARCH API KEY
- HOT PEPPER API KEY
- MongoDB URL with USER and PASSWORD 