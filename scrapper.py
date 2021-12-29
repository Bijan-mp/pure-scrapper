import re
import json
import requests
from bs4 import BeautifulSoup


class ProductScraper:
    """
    This class handle a product scrapping proccess
    """

    def __init__(self, base_url, category_url, product_base_url, price_history_base_url):
        self.base_url = base_url
        self.category_url = base_url + category_url
        self.product_base_url = base_url + product_base_url
        self.price_history_base_url = base_url + price_history_base_url
        self.product_list = []

    def get_soup(url=None, html_doc=None, parser="html.parser"):
        """
        Get HTML source url or HTML document(as a text) and return beautifulsoup object
        """
        if url is not None:
            html_doc = requests.get(url).text
            # To prevent this error : UnicodeEncodeError: 'charmap' codec can't encode character '\u011f'
            # if show the error use below line
            html_doc = html_doc.encode("UTF-8")

        return BeautifulSoup(html_doc, parser)

    def fetch_category_page_product_list(self):
        '''
        Get all products list in the category page from the category_url
        return self.product_list as a list object
        '''
        soup = self.get_soup(self.category_url).find_all(
            "div",
            attrs={
                "class": "c-product-box c-promotion-box js-product-box has-more is-plp"
            },
        )

        # TODO: check if sort option of most-viewd selected

        for element in soup:

            link_element = element.find(
                "a",
                attrs={
                    "class": "c-product-box__img c-promotion-box__image js-url js-product-item js-product-url"
                },
            )
            image_element = link_element.find("img")

            product_url = link_element["href"]
            product_short_url = re.search("^/product/dkp-[\d]*/", product_url)[0]
            product_img_url = image_element["src"]

            # Fetch json data of 'data-enhanced-ecommerce' attribute and add urls to it.
            element_data_object = json.loads(element["data-enhanced-ecommerce"])
            element_data_object["short_url"] = self.base_url + product_short_url
            element_data_object["url"] = self.base_url + product_url
            element_data_object["img_url"] = product_img_url
            self.product_list.append(element_data_object)

        return self.product_list

    def fetch_products_price_history(self):

        for product in self.product_list:

            pass

    def fetch_product_price_history(self, product_id):
        # Fetch Product price list
        url = self.price_history_base_url + str(product_id) + "/"
        print(url)
        price_list_soup = self.get_soup(url)
        return json.loads(str(price_list_soup))