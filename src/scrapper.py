import re
import json
import requests
from bs4 import BeautifulSoup
from constants import BASE_URL, PRODUCT_CATEGORY_URL, PRODUCT_PRICE_CHART_BASE_URL


class BaseScrapper:
    """
    The class contains methods to get data from the web.
    """

    def get_soup(self, url=None, html_doc=None, parser="html.parser"):
        """
        Get HTML source url or HTML document(as a text) and return beautifulsoup object
        raise requests.exceptions.RequestException
        """
        if url is not None:
            html_doc = requests.get(url).text
            # To prevent this error : UnicodeEncodeError: 'charmap' codec can't encode character '\u011f'
            # if show the error use below line
            html_doc = html_doc.encode("UTF-8")

        return BeautifulSoup(html_doc, parser)

    def fetch_json_data_as_object(self, url):
        """
        fetch_json_data_as_object method fetch json data from url and
        return dictionary object
        raise requests.exceptions.RequestException
        """

        # try :
        html_doc = requests.get(url).text
        html_doc = html_doc.encode("UTF-8")
        return json.loads(str(html_doc))
        # except requests.exceptions.RequestException:
        #     ras = requests.exceptions.RequestException

    def testme(self):
        print("test me!")


class ProductScraper(BaseScrapper):
    """
    This class handle a product scrapping proccess
    """

    def __init__(
        self, base_url, category_url, product_base_url, price_history_base_url,
        product_rating_base_url
    ):
        self.base_url = base_url
        self.category_url = base_url + category_url
        self.product_base_url = base_url + product_base_url
        self.price_history_base_url = base_url + price_history_base_url
        self.product_rating_base_url = base_url + product_rating_base_url
        self.product_list = []
        self.products_price_history = {}

    def fetch_category_page_product_list(self):
        """
        Get all products list in the category page from the category_url
        return self.product_list as a list object
        """
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

    def fetch_all_products_price_history(self):

        for product in self.product_list:

            if self.exist_any_product_price_history():
                # add current price to the Product history table
                pass
            else:
                product_price_history = self.fetch_product_price_history(product["id"])
                self.products_price_history[product["id"]] = product_price_history
            pass

    def fetch_product_rating(self, product_id):
        url = self.product_rating_base_url + str(product_id) + "/"
        print(url)
        rating_object = {}
        rating_soup = self.get_soup(url)
        rating_participants_element = rating_soup.find(
            "div",
            {"class": "c-comments__side-rating-all"},
        )
        rating_elements = rating_soup.find(
            "ul",
            {"class": "c-content-expert__rating"},
        ).find_all(
            "li"
        )
        # TODO: fetch farsi number and convert to number
        rating_participants_number = rating_participants_element.contents[0]

        ratings_sum = 0
        for element in rating_elements:
            title = element.find('div',attrs={'class':"c-content-expert__rating-title"}).contents
            rating = element.find('div',attrs={'class':"c-rating__rate js-rating-value"})["data-rate-value"]
            rating = int(rating.strip('%'))/20
            ratings_sum +=rating
            rating_object[str(title)] = rating

        rating_object['avg_rate'] = ratings_sum / len(rating_elements)
        rating_object['total_participants'] = rating_participants_number

        return rating_object

    def fetch_product_price_history(self, product_id):
        # Fetch Product price list
        url = self.price_history_base_url + str(product_id) + "/"
        print(url)
        price_list_soup = self.get_soup(url)
        return json.loads(str(price_list_soup))

    def exist_any_product_price_history(self, product_id):
        """
        The method check product history database,
        If exist any price history for the product, return true
        if dose not exist any price history for the product, return false
        """

        return False
