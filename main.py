import re
import json
import requests
from bs4 import BeautifulSoup
from constants import BASE_URL, PRODUCT_CATEGORY_URL, PRODUCT_PRICE_CHART_BASE_URL


def get_soup(url=None, html_doc=None, parser="html.parser"):
    """
    Get HTML source url or HTML document(as a text) and return beautifulsoup object
    """
    if url is not None:
        html_doc = requests.get(url).text

        # To prevent this error : UnicodeEncodeError: 'charmap' codec can't encode character '\u011f'
        # if show the error use below line
        # html_doc = html_doc.encode("UTF-8")

    return BeautifulSoup(html_doc, parser)

def write_to_file(name,data):
    fo = open(name, "w")
    # print ("Name of the file: ", fo.name)
    # print ("Closed or not : ", fo.closed)
    # print ("Opening mode : ", fo.mode)
    fo.write( str(data))
    fo.close()

# Get main page
url = BASE_URL + PRODUCT_CATEGORY_URL
soup = get_soup(url).find_all(
    "div",
    attrs={"class": "c-product-box c-promotion-box js-product-box has-more is-plp"},
)

product_list = []


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

    # get json data of 'data-enhanced-ecommerce' attribute
    element_data_object = json.loads(element["data-enhanced-ecommerce"])
    element_data_object["short_url"] = BASE_URL + product_short_url
    element_data_object["url"] = BASE_URL + product_url
    element_data_object["img_url"] = product_img_url
    product_list.append(element_data_object)


print("----------------")
# print(product_list[0])


# Fetch Product price list
def fetch_product_price_history( product_id):
    # Fetch Product price list
    url = BASE_URL + PRODUCT_PRICE_CHART_BASE_URL + str(product_id) + "/"
    print(url)
    price_list_soup = get_soup(url)
    return json.loads(str(price_list_soup))

for product in product_list[:2]:
            product_price_history = fetch_product_price_history(product['id'])
            product['price_history'] = product_price_history

# print(product_list)
print(json.dumps(product_list))
write_to_file("jlist.js", json.dumps(product_list))




# Get product page
# product = product_list[0]
# product_url = product['url']
# print(product_url)
# # "https://www.digikala.com/product/dkp-4958276/"
# product_soup = get_soup("https://www.digikala.com/product/dkp-4958276/")
# rating_elements = product_soup.find(
#     "div",
#     {"class": "c-comments__side-bar"},
# )

# script_element = product_soup.find(
#     "script",
#     attrs = { "type":"application/ld+json"},
# )

# print(script_element.contents)
# # Open a file
# fo = open("foo.html", "w")
# print ("Name of the file: ", fo.name)
# print ("Closed or not : ", fo.closed)
# print ("Opening mode : ", fo.mode)
# fo.write( str(product_soup))
# fo.close()
