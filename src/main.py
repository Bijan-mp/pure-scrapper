"""
Entry point of application.
"""
import datetime
import time

from constants import (
    BASE_URL,
    FETCH_DELAY_MINUTES,
    MOBILE_CATEGORY_URL,
    PRODUCT_PRICE_HISTORY_BASE_URL,
    PRODUCT_RATING_BASE_URL,
)
from dataaccessobjects import (
    ProductDAO,
    ProductDataObject,
    ProductPriceDataObject,
)
from scrappers import ProductScraper
from multiprocessing.dummy import Pool

import os

MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_USERNAME = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")

url = "mongodb://{}:{}@{}:27017".format(MONGO_USERNAME, MONGO_PASSWORD, MONGO_HOST)
database = "scrapperdb"


def main():
    while True:
        product_scraper = ProductScraper(
            BASE_URL,
            MOBILE_CATEGORY_URL,
            PRODUCT_PRICE_HISTORY_BASE_URL,
            PRODUCT_RATING_BASE_URL,
        )
        product_objects_list = product_scraper.scrappe_category_page_products_list()

        product_dao = ProductDAO(url, database)
        time_stamp = datetime.datetime.now()

        function_arguments = list()

        for product in product_objects_list:
            function_arguments.append(
                (
                    product_scraper,
                    product_dao,
                    product,
                    time_stamp,
                )
            )

        n_threads = 8
        pool = Pool(n_threads)
        results = pool.starmap(scrape_and_insert_product, function_arguments)
        pool.close()
        pool.join()

        time.sleep(FETCH_DELAY_MINUTES * 60)


def scrape_and_insert_product(
    product_scraper: ProductScraper,
    product_dao: ProductDAO,
    product: ProductDataObject,
    time_stamp,
):
    product_rating_data_object = product_scraper.scrappe_product_rating(product.id)
    product_price_data_object = ProductPriceDataObject(
        price=product.data["price"],
        color="default",
        time_stamp=time_stamp,
        price_before_discount=product.data["price_before_discount"],
    )

    if product_dao.exist(product.id):

        product_data_object = ProductDataObject(
            id=product.id,
            name=product.data["name"],
            url=product.data["url"],
            short_url=product.data["short_url"],
            img_url=product.data["img_url"],
            rating_object=product_rating_data_object,
            price_object=product_price_data_object,
        )

    else:

        price_history = product_scraper.scrappe_product_price_history(product.id)
        product_data_object = ProductDataObject(
            id=product.id,
            name=product.data["name"],
            url=product.data["url"],
            short_url=product.data["short_url"],
            img_url=product.data["img_url"],
            rating_object=product_rating_data_object,
            price_object=product_price_data_object,
            price_history=price_history,
        )

    product_dao.create_or_update(
        product_data_object=product_data_object, time_stamp=time_stamp
    )


if __name__ == "__main__":
    main()
