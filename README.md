# Athletics jobs scraper

# Features: 
* Scraps https://ncaamarket.ncaa.org/jobs/ to get job listings and store them into Google Spreadsheet. 
* All jobs are added to the sheet in the first load. During the delta loads, only new job listings are inserted into the sheet.
* Sends an alert email if scraper stops working for some reason. 

# Tools and libraries used: 
1. Scrapy
2. MongoDB
3. Google Sheets API v4
4. Docker

## To setup this scrapy parser

### Create a virtual environment and install all needed libraries
1. Create virtual environment with this command: `python -m venv venv`
2. Activate your virtual environment with these command:
* for linux: `source venv/bin/activate`
* for windows: `venv\Scripts\activate`
3. Install all needed libraries with this this command: `pip install -r requirements.txt`
### Create .env file for sensitive credentials
You should copy .env.example file and rename it to .env. In .env file you have to fill in the following variables:
```
* MONGO_INITDB_ROOT_USERNAME=root
* MONGO_INITDB_ROOT_PASSWORD=example

* ME_CONFIG_MONGODB_ADMINUSERNAME=root
* ME_CONFIG_MONGODB_ADMINPASSWORD=example

* GOOGLE_TOKEN_FILE_NAME='token.pickle'
* GOOGLE_SPREADSHEET_ID='example-exampleIDUBBt0KDiOLQ'

* GMAIL_USER='example@gmail.com'
* GMAIL_PASSWORD='password'
```
You have to change GOOGLE_SPREADSHEET_ID to your google spread sheet id.

### Create token.pickle file
You have to create google credentials with this link: https://developers.google.com/sheets/api/quickstart/python And save credentials.json into root folder of project. After that you have to use quickstart_google_sheet.py file to create token. You can use this command: `python quickstart_google_sheet.py`

### Create and run mongodb service in docker container
You have to use this command: `docker-compose up --build`

### Start parser
You can use this command: `scrapy crawl ncaamarket-jobs`
