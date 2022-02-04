import requests, re, gspread, smtplib, json
from datetime import date
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from e_mail import Email


class CeneoScraper(Email):
    url = 'https://www.ceneo.pl/'

    def __init__(self):
        gc = gspread.service_account(filename='credentials.json')
        ceneo_database = self.setup(gc)
        self.ceneo_products_prices = ceneo_database.worksheet('Products Prices')
        self.ceneo_products_list = ceneo_database.worksheet('Products List')


    def setup(self, google_client):
        """
        Setup spreadsheet structure on google drive. Creates spreadsheet Ceneo Database if not exists and shares with
        defined user.
        :param google_client:  Initiated google client.
        :return: Spreadsheet object.
        """
        title = 'Ceneo Database'
        shared_for = 'enter user gmail adress here'
        if title not in [sh.title for sh in google_client.openall()]:
            # create spreadsheet
            ceneo_database = google_client.create(title)
            # give access to created spreadsheet
            ceneo_database.share(shared_for, perm_type='user', role='owner')
            # rename worksheet Sheet1 to Products List
            products_list = ceneo_database.get_worksheet_by_id(0)
            products_list.update_title('Products List')
            # create worksheet Product Prices
            ceneo_database.add_worksheet(title="Products Prices", rows="200", cols="3")
        # open Ceneo Database spreadsheet if exists
        ceneo_database = google_client.open('Ceneo Database')

        return ceneo_database

    def data_load(self):
        """
        Loads all products prom products.json file.
        """
        try:
            with open('product.json', 'r') as products_json:
                products = json.load(products_json)
                for product in products["allProducts"]:
                    self.ceneo_products_list.append_row([product["productName"], product["ceneoId"], product["alertPrice"]])
            print(f'{len(products["allProducts"])} product loaded.')
        except Exception as e:
            print(e)


    def request_ceneo_product_page(self, ceno_product_id):
        """
        Requests ceneo product page based on ceneo product id from spreadsheet ='Product list', col2.
        :param ceno_product_id: id of product in ceneo
        :return: ceneo product page
        """
        try:
            with requests.Session() as s:
                response = s.get(self.url + str(ceno_product_id), verify=False)
        except Exception as e:
            print(e)

        return response

    def find_product_lowest_price(self, response):
        """
        Search for product lowest price on ceneo product page.
        :param response: Ceneo product page.
        :return: Product lowest price.
        """
        soup = BeautifulSoup(response.text, 'html.parser')
        script_text = soup.find_all('script')
        text = str(script_text)
        lowest_price = float(re.search(r'"lowPrice":.+\d', text).group().split(' ')[1])
        return lowest_price

    def save_products_lowest_price(self, product_name, lowest_price):
        """
        Save product to google spread sheet: col1 = product name, col2 = product price, col3 = timestamp (YYYY-MM-DD).
        :param product_name: Product Name
        :param lowest_price: Product Lowest Proce
        """
        try:
            self.ceneo_products_prices.append_row([product_name, lowest_price, date.today().strftime('%Y-%m-%d')])
        except Exception as e:
            print(e)

    def price_alert_email(self, product_name, lowest_price):
        """
        Send email with price alert.
        Configured with emial on gmail.com
        :param product_name: Product Name
        :param lowest_price: Product Lowest Price
        """
        msg = MIMEMultipart()
        msg['To'] = self.email_address
        msg['From'] = self.email_address
        msg['Subject'] = self.email_subject(product_name)
        msg.attach(MIMEText(self.email_body(product_name, lowest_price), 'plain'))
        email_text = msg.as_string()
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)  # mail server configuration
            server.ehlo()
            server.login(self.email_address, self.email_app_pass)
            # send mail >> sent from, send to, email message
            server.sendmail(self.email_address, self.email_address, email_text)
            server.close()
        except Exception as e:
            print(e)

    def price_alert_verification(self, product_name, lowest_price, alert_price):
        """
        Check if found product price(lowest price) reaches alert price then triggers alert email.
        :param product_name: Product Name.
        :param lowest_price: Lowest price of product that has been found
        :param alert_price: Product price set as alert price.
        """
        if lowest_price <= float(alert_price):
            self.price_alert_email(product_name=product_name, lowest_price=lowest_price)
