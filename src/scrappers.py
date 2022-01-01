import re
import json
import requests
import datetime
from bs4 import BeautifulSoup
from dataaccessobjects import (
    ProductPriceDataObject,
    ProductRatingDataObject,
    SimpeProductDataObject,
)

from utils import utils, jalali


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

    def get_json_data_as_object(self, url):
        """
        get_json_data_as_object method get json data from url and return data.

        raise requests.exceptions.RequestException
        """
        html_doc = requests.get(url).text
        html_doc = html_doc.encode("UTF-8")
        return json.loads(html_doc)


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

    def scrappe_category_page_products_list(self):
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
                    "has-more",
                    "is-plp",
                ]
            },
        )

        for element in product_boxes_soup:
            product_data_object = self.scrappe_product_data_object_from_html_element(
                element
            )
            if product_data_object is not None:
                self.product_list.append(product_data_object)

        return self.product_list

    def scrappe_product_data_object_from_html_element(
        self, element
    ) -> SimpeProductDataObject:
        try:

            # Get child elements
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
            rating_elements = element.find(
                "div", attrs={"class": "c-product-box__engagement-rating"}
            )

            # Get child element data
            # Get json data from 'data-enhanced-ecommerce' attribute of product <div> tag.
            product_object = json.loads(element["data-enhanced-ecommerce"])
            product_url = self.base_url + link_element["href"]
            product_short_url = (
                self.base_url + re.search("/product/dkp-[\d]*/", product_url)[0]
            )
            product_img_url = image_element["src"]
            price = price_element.find(
                "div", attrs={"class": "c-price__value-wrapper"}
            ).contents[0]
            price_before_discount = None
            total_rating = float(
                utils.convert_persian_str_number_to_number(
                    rating_elements.contents[0].strip()
                )
            )
            total_rating_participant = int(
                utils.convert_persian_str_number_to_number(
                    rating_elements.find("span")
                    .contents[0]
                    .strip()
                    .replace("(", "")
                    .replace(")", "")
                )
            )

            def exist_discount(element):
                if element != None and element.find("del"):
                    return True
                return False

            if exist_discount(price_element):
                persian_price = price_element.find("del").contents[0]
                price_before_discount = int(
                    utils.convert_persian_str_number_to_number(persian_price)
                )

            # Set product_object data
            simple_product_data_object = SimpeProductDataObject(
                id=product_object["id"],
                name=product_object["name"],
                url=product_url,
                short_url=product_short_url,
                img_url=product_img_url,
                price=int(utils.convert_persian_str_number_to_number(price)),
                price_before_discount=price_before_discount,
                total_rating=total_rating,
                total_rating_participant=total_rating_participant,
            )

            return simple_product_data_object

        except Exception as e:
            print("ERROR: in get_product_data_object_from_html_element()")
            print(e)

        return None

    def scrappe_product_rating(self, product_id):
        url = self.product_rating_base_url + str(product_id) + "/"

        rating_soup = self.get_soup(url)
        # Get html elements and data
        rating_participants_element = rating_soup.find(
            "div",
            attrs={"class": "c-comments__side-rating-all"},
        )
        rating_elements = rating_soup.find(
            "ul",
            attrs={"class": "c-content-expert__rating"},
        ).find_all("li")
        rating_participants_number = int(
            utils.convert_persian_str_number_to_number(
                re.findall(r"\d+", rating_participants_element.contents[0])[0]
            )
        )
        avg_rate = float(
            utils.convert_persian_str_number_to_number(
                rating_soup.find(
                    "div", attrs={"class": "c-comments__side-rating-main"}
                ).contents[0]
            )
        )

        # Create rating_details object
        rating_details = {}
        for element in rating_elements:

            title = element.find(
                "div", attrs={"class": "c-content-expert__rating-title"}
            ).contents
            rating = float(
                utils.convert_persian_str_number_to_number(
                    element.find(
                        "span", attrs={"class": "c-rating__overall-word"}
                    ).contents[0]
                )
            )

            rating_details[str(title)] = rating

        # Create ProductRatingDataObject instance
        product_rating_data_object = ProductRatingDataObject(
            total_rating=avg_rate,
            total_participants=rating_participants_number,
            rating_details=rating_details,
            time_stamp=datetime.datetime.now(),
        )

        return product_rating_data_object

    def scrappe_product_price_history(self, product_id):

        price_history_url = self.price_history_base_url + str(product_id) + "/"
        price_history_json = self.get_json_data_as_object(price_history_url)
        json_data = price_history_json["data"]

        # Create a list of ProductPriceHistory instances.
        product_price_history = []

        for idx, date in enumerate(json_data["Days"]):
            for serie in json_data["Series"]:
                try:
                    serie_data = serie["data"][idx]
                    product_price_data_object = ProductPriceDataObject(
                        price=int(serie_data["price"]),
                        color=serie["name"],
                        time_stamp=jalali.Persian(date).gregorian_datetime(),
                    )
                    product_price_history.append(product_price_data_object.data)
                except Exception:
                    pass

        return product_price_history
