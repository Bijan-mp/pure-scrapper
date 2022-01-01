import datetime
import pymongo


# Data Objects
class DataObject:
    def __init__(self, id):
        self.data = {}
        self.id = id


class ProductRatingDataObject(DataObject):
    def __init__(self, total_rating, total_participants, rating_details, time_stamp):
        self.data = {
            "total_rating": total_rating,
            "total_participants": total_participants,
            "rating_details": rating_details,
            "time_stamp": time_stamp,
        }


class ProductPriceDataObject(DataObject):
    def __init__(self, price, color, time_stamp, price_before_discount=None):
        self.data = {
            "price": price,
            "price_before_discount": price_before_discount,
            "color": color,
            "time_stamp": time_stamp,
        }


class SimpeProductDataObject(DataObject):
    def __init__(
        self,
        id,
        name,
        url,
        short_url,
        img_url,
        price,
        price_before_discount,
        total_rating,
        total_rating_participant,
    ):
        super(SimpeProductDataObject, self).__init__(id)
        self.data = {
            "_id": id,
            "name": name,
            "url": url,
            "short_url": short_url,
            "img_url": img_url,
            "price": price,
            "price_before_discount": price_before_discount,
            "total_rating": total_rating,
            "total_rating_participant": total_rating_participant,
        }


class ProductDataObject(SimpeProductDataObject):
    def __init__(
        self,
        id,
        name,
        url,
        short_url,
        img_url,
        rating_object: ProductRatingDataObject,
        price_object: ProductPriceDataObject,
        price_history=None,
    ):
        self.rating_object = rating_object
        self.price_object = price_object
        super(ProductDataObject, self).__init__(
            id=id,
            name=name,
            url=url,
            short_url=short_url,
            img_url=img_url,
            price=self.price_object.data["price"],
            price_before_discount=self.price_object.data["price_before_discount"],
            total_rating=self.rating_object.data["total_rating"],
            total_rating_participant=self.rating_object.data["total_participants"],
        )
        self.data["rating_ditails"] = self.rating_object.data["rating_details"]
        self.data["rating_history"] = [self.rating_object.data]
        if price_history is not None:
            self.data["price_history"] = price_history
        else:
            self.data["price_history"] = [self.price_object.data]

    def get_data(self):
        try:
            del self.data["rating_history"]
            del self.data["price_history"]
        except KeyError:
            pass
        return self.data


# Data Access Objects
class BaseDAO:
    """
    Data Access Object use to working with data over database for special collection(table)
    Methods :
    creat_or_update()
    """

    def __init__(self, client_url, db_name, collection_name):
        self.client = pymongo.MongoClient(client_url)
        self.database = self.client[db_name]
        self.collection = self.database[collection_name]

    def exist(self, id):
        if self.collection.count_documents({"_id": id}, limit=1):
            return True
        return False


class ProductDAO(BaseDAO):
    """
    Data Access Object is used to working with data over database for a given collection(table).
    """

    __collection_name = "product"

    def __init__(self, client_url, db_name):
        super(ProductDAO, self).__init__(client_url, db_name, self.__collection_name)

    def create_or_update(
        self,
        product_data_object: ProductDataObject,
        time_stamp=datetime.datetime.now(),
    ):

        try:

            result = self.create(product_data_object, time_stamp)
            print("Colection [{}] - A document created.".format(self.__collection_name))

        except pymongo.errors.DuplicateKeyError as e:
            # If document exists, then update it.
            del product_data_object.data["create_timestamp"]
            product_data_object.data["update_timestamp"] = time_stamp
            query = {"_id": product_data_object.id}
            newvalues = {
                "$push": {
                    "rating_history": product_data_object.rating_object.data,
                    "price_history": product_data_object.price_object.data,
                },
                "$set": product_data_object.get_data(),
            }

            result = self.collection.update_one(query, newvalues).upserted_id
            print("Colection [{}] - A document updated.".format(self.__collection_name))

        else:
            return result

    def create(
        self,
        product_data_object: ProductDataObject,
        time_stamp=datetime.datetime.now(),
    ):
        product_data_object.data["create_timestamp"] = time_stamp
        return self.collection.insert_one(product_data_object.data).inserted_id
