# Super simple to use and configure python ceneo scraper.

# Functionalities:
- checks current lowest product price on ceneo.pl
- configuration is made via Google sheets
- scraped data is collected  and stored in Google spreadsheet
- email notification sent on configured em-mail if product price achieves certain level 

# Requirements:
- python 3.6 or above
- run: pip install requirements.txt

# Setup:
1) Create new project in google developers console: https://console.developers.google.com.
2) Add two API interfaces to the project: Google Sheets API, Google Drive API.
3) Get service account credentials in json format (save it and add it to script folder with name changed to credentials.json)
4) Share the created sheets with application bot email (check this tutorial that explains a lot of topics: https://www.youtube.com/watch?v=T1vqS1NL89E)
5) Allow app to sign in to google account => generated password enter in file: e_mail.py in line 7 for email_app_pass (https://support.google.com/accounts/answer/185833?hl=en)
6) Configure gmail account to send and receive mail with price alert with same account in _mail.py in line 6.
7) In products.json file configure products to check for their prices at ceneo.pl. Set as many products as you need:
a) property productName = product name
b) property ceneoId = 96958323 => https://www.ceneo.pl/96958323
c) property alertPrice = floating point number (if product price achieves this value email notification will be send)
