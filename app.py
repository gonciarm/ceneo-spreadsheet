from ceneo_scraper import CeneoScraper

scraper = CeneoScraper()


def load_data():
    print(f'No products to search for! Products will be loaded from products.json file.')
    scraper.data_load()


def get_all_products():
    all_products = scraper.ceneo_products_list.get_all_values()
    return all_products


def scrape_products_prices():
    all_products = scraper.ceneo_products_list.get_all_values()
    for product in all_products:
        response = scraper.request_ceneo_product_page(product[1])
        product_lowest_price = scraper.find_product_lowest_price(response)
        scraper.save_products_lowest_price(product_name=product[0], lowest_price=product_lowest_price)
        scraper.price_alert_verification(product_name=product[0], lowest_price=product_lowest_price,
            alert_price=product[2])


def run():
    all_products = get_all_products()
    if all_products:
        scrape_products_prices()
    else:
        load_data()
        scrape_products_prices()


if __name__ == "__main__":
    run()
