import unittest
from scrappers import ProductScraper

from utils.utils import read_file
from dataaccessobjects import ProductDataObject, SimpeProductDataObject

# TODO: Test connection test
# TODO: Test get true objects from a sample category html file
# TODO: Test get true object form a product page html file.
# TODO: Test get true object from a rating page html file.
# TODO: Test get true data from price histoy json file.


class ProductScrapperTestCase(unittest.TestCase):
    """
    To Test ProductScrapper methods Use some static files

    """

    def setUp(self):
        self.category_product_element_html_without_discount = read_file(
            "testmaterials/category-product-element.html"
        )
        self.category_product_element_html_with_discount = read_file(
            "testmaterials/category-product-element-with-discount.html"
        )

    def test_correction_of_scrappe_product_data_object_from_html_element_without_discount(
        self,
    ):
        """
        scrappe_product_data_object_from_html_element()
        Test method returned data whene element dose not have price discount.
        """
        predefined_simple_product_data_object = SimpeProductDataObject(
            id=4958276,
            name="product-test-fa-name",
            url="/product/dkp-4958276/گوشی-موبایل-شیائومی-مدل-poco-x3-pro-m2102j20sg-دو-سیم-کارت-ظرفیت-256-گیگابایت-و-8-گیگابایت-رم",
            short_url="/product/dkp-4958276/",
            img_url="https://dkstatics-public.digikala.com/digikala-products/77f6b5b39b58f0b81c7707e3626f55b74ee348aa_1623857594.jpg?x-oss-process=image/resize,m_lfit,h_600,w_600/quality,q_90",
            price=6666000,
            price_before_discount=None,
            total_rating=4.4,
            total_rating_participant=7481,
        )

        product_scraper = ProductScraper("", "", "", "")

        html_element = product_scraper.get_soup(
            html_doc=self.category_product_element_html_without_discount
        ).find(
            "div",
            attrs={
                "class": [
                    "c-product-box",
                    "c-promotion-box",
                    "js-product-box",
                ]
            },
        )

        simple_product_data_object = (
            product_scraper.scrappe_product_data_object_from_html_element(html_element)
        )

        self.assertEqual(
            simple_product_data_object.data["_id"],
            predefined_simple_product_data_object.data["_id"],
        )
        self.assertEqual(
            simple_product_data_object.data["name"],
            predefined_simple_product_data_object.data["name"],
        )
        self.assertEqual(
            simple_product_data_object.data["url"],
            predefined_simple_product_data_object.data["url"],
        )
        self.assertEqual(
            simple_product_data_object.data["short_url"],
            predefined_simple_product_data_object.data["short_url"],
        )
        self.assertEqual(
            simple_product_data_object.data["img_url"],
            predefined_simple_product_data_object.data["img_url"],
        )
        self.assertEqual(
            simple_product_data_object.data["price"],
            predefined_simple_product_data_object.data["price"],
        )
        self.assertEqual(
            simple_product_data_object.data["price_before_discount"],
            predefined_simple_product_data_object.data["price_before_discount"],
        )
        self.assertEqual(
            simple_product_data_object.data["total_rating"],
            predefined_simple_product_data_object.data["total_rating"],
        )
        self.assertEqual(
            simple_product_data_object.data["total_rating_participant"],
            predefined_simple_product_data_object.data["total_rating_participant"],
        )

    def test_correction_of_scrappe_product_data_object_from_html_element_with_discount(
        self,
    ):
        """
        scrappe_product_data_object_from_html_element()
        Test method returned data whene element dose not have price discount.
        """
        predefined_simple_product_data_object = SimpeProductDataObject(
            id=4958276,
            name="product-test-fa-name",
            url="/product/dkp-4958276/گوشی-موبایل-شیائومی-مدل-poco-x3-pro-m2102j20sg-دو-سیم-کارت-ظرفیت-256-گیگابایت-و-8-گیگابایت-رم",
            short_url="/product/dkp-4958276/",
            img_url="https://dkstatics-public.digikala.com/digikala-products/77f6b5b39b58f0b81c7707e3626f55b74ee348aa_1623857594.jpg?x-oss-process=image/resize,m_lfit,h_600,w_600/quality,q_90",
            price=2899000,
            price_before_discount=3087000,
            total_rating=4.4,
            total_rating_participant=7481,
        )

        product_scraper = ProductScraper("", "", "", "")

        html_element = product_scraper.get_soup(
            html_doc=self.category_product_element_html_with_discount
        ).find(
            "div",
            attrs={
                "class": [
                    "c-product-box",
                    "c-promotion-box",
                    "js-product-box",
                ]
            },
        )

        simple_product_data_object = (
            product_scraper.scrappe_product_data_object_from_html_element(html_element)
        )

        self.assertEqual(
            simple_product_data_object.data["_id"],
            predefined_simple_product_data_object.data["_id"],
        )
        self.assertEqual(
            simple_product_data_object.data["name"],
            predefined_simple_product_data_object.data["name"],
        )
        self.assertEqual(
            simple_product_data_object.data["url"],
            predefined_simple_product_data_object.data["url"],
        )
        self.assertEqual(
            simple_product_data_object.data["short_url"],
            predefined_simple_product_data_object.data["short_url"],
        )
        self.assertEqual(
            simple_product_data_object.data["img_url"],
            predefined_simple_product_data_object.data["img_url"],
        )
        self.assertEqual(
            simple_product_data_object.data["price"],
            predefined_simple_product_data_object.data["price"],
        )
        self.assertEqual(
            simple_product_data_object.data["price_before_discount"],
            predefined_simple_product_data_object.data["price_before_discount"],
        )
        self.assertEqual(
            simple_product_data_object.data["total_rating"],
            predefined_simple_product_data_object.data["total_rating"],
        )
        self.assertEqual(
            simple_product_data_object.data["total_rating_participant"],
            predefined_simple_product_data_object.data["total_rating_participant"],
        )
