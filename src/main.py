"""
Entry point of application.
"""
import json
import time

from constants import (
    BASE_URL,
    FETCH_DELAY_MINUTES,
    MOBILE_CATEGORY_URL,
    PRODUCT_PRICE_HISTORY_BASE_URL,
    PRODUCT_RATING_BASE_URL,
)
from scrapper import ProductScraper


def main():
    while True:
        time.sleep(FETCH_DELAY_MINUTES)


if __name__ == "__main__":
    #     main()
    from persian_tools import digits



    product_scraper = ProductScraper(
        BASE_URL,
        MOBILE_CATEGORY_URL,
        PRODUCT_PRICE_HISTORY_BASE_URL,
        PRODUCT_RATING_BASE_URL,
    )

    product_list = product_scraper.fetch_category_page_products_list()

    for product in product_list:
        #  print(json.dumps(product))
        print("price ; ",product['price'])
        if product['price_before_discount'] is not None:
            print("befor discount ; ",product['price_before_discount'])

    products_price_history = product_scraper.fetch_all_products_price_history()
    print("----------")
    for price_history in products_price_history:
        print("price : ",price_history)
        print("----------------")
