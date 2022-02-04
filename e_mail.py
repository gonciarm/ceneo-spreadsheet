from dataclasses import dataclass


@dataclass
class Email:
    email_address: str = 'enter user email adress here'
    email_app_pass: str = 'enter app password here'

    def email_subject(self, product_name):
        """
        Create email subject.
        :param product_name: Product Name
        :return: Email subject with product name.
        """
        return f'Price alert for {product_name}!'

    def email_body(self, product_name, lowest_price):
        """
        Create email body/message.
        :param product_name: Product Name
        :param lowest_price: Product Lowest Price
        :return: Email message with product name and product lowest price.
        """
        return f"Hey, price of: {product_name} has dropped.\nCurrent lowest price is now: {lowest_price}.\nYour beloved scraper-bot."