import re
import json
from persian_tools import digits
import requests
import datetime
from bs4 import BeautifulSoup

from utils import convert_persian_number_to_int


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

            # Use the following command.to prevent this error :
            # "UnicodeEncodeError: 'charmap' codec can't encode character '\u011f'"
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
    This class handle special product scrapping proccess
    """

    def __init__(
        self,
        base_url,
        category_url,
        price_history_base_url,
        product_rating_base_url,
    ):
        self.base_url = base_url
        self.category_url = base_url + category_url
        self.price_history_base_url = base_url + price_history_base_url
        self.product_rating_base_url = base_url + product_rating_base_url
        self.product_list = []
        self.products_price_history = []

    def fetch_category_page_products_list(self):
        """
        Get all products from the category page.
        Return self.product_list as a list object
        """
        product_boxes_soup = self.get_soup(self.category_url).find_all(
            "div",
            attrs={
                "class": [
                    "c-product-box",
                    "c-promotion-box",
                    "js-product-box",
                    # "has-more",
                    # "is-plp",
                ]
            },
        )

        for element in product_boxes_soup:
            try:
                # Get elements
                link_element = element.find(
                    "a",
                    attrs={
                        "class": [
                            "c-product-box__img",
                            "c-promotion-box__image",
                            "js-url",
                            "js-product-item",
                            "js-product-url",
                        ]
                    },
                )
                price_element = element.find(
                    "div",
                    attrs={"class": ["c-price__value", "c-price__value--plp"]},
                )
                image_element = link_element.find("img")

                # Get element data
                product_url = self.base_url + link_element["href"]
                product_short_url = (
                    self.base_url + re.search("/product/dkp-[\d]*/", product_url)[0]
                )
                product_img_url = image_element["src"]
                price = price_element.find(
                    "div", attrs={"class": "c-price__value-wrapper"}
                ).contents[0]

                # Set product_object data
                # Product <div> element has a 'data-enhanced-ecommerce' attribiute that contain product data as a json object.
                # Get json data of 'data-enhanced-ecommerce' attribute
                product_object = json.loads(element["data-enhanced-ecommerce"])
                product_object["url"] = product_url
                product_object["short_url"] = product_short_url
                product_object["img_url"] = product_img_url
                product_object["price"] = convert_persian_number_to_int(price)
                product_object["price_before_discount"] = None

                def exist_discount(element):
                    if element != None and element.find("del"):
                        return True
                    return False

                if exist_discount(price_element):
                    persian_price = price_element.find("del").contents[0]
                    price_before_discount = convert_persian_number_to_int(persian_price)
                    product_object["price_before_discount"] = price_before_discount
                    
                self.product_list.append(product_object)

            except Exception as e:
                # TODO: appropriate act
                pass
        return self.product_list

    def fetch_all_products_price_history(self):
        """
        If the product price history dose not exist fetch all products price history and inser into database,
        else just insert product price with a timestamp to database.
        """

        for product in self.product_list:

            if self.exist_any_product_price_history(product['id']):
                # add current price to the Product history table
                # TODO: Must save product price to database. this code is temporary!
                self.products_price_history[product["id"]].append(
                    [datetime.datetime.now(), product["price"]]
                )
                pass
            else:
                product_price_history = self.fetch_product_price_history(product["id"])
                price_history_object = {
                    product["id"]:product_price_history
                }
                self.products_price_history.append(price_history_object)
                return self.products_price_history
        
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
        ).find_all("li")
        # TODO: fetch farsi number and convert to number
        rating_participants_number = rating_participants_element.contents[0]

        ratings_sum = 0
        for element in rating_elements:
            title = element.find(
                "div", attrs={"class": "c-content-expert__rating-title"}
            ).contents
            rating = element.find(
                "div", attrs={"class": "c-rating__rate js-rating-value"}
            )["data-rate-value"]
            rating = int(rating.strip("%")) / 20
            ratings_sum += rating
            rating_object[str(title)] = rating

        rating_object["avg_rate"] = ratings_sum / len(rating_elements)
        rating_object["total_participants"] = rating_participants_number

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
