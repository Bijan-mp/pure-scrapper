# Digikala Mobile Products Scrapper

## TL;DR
## Run the project
#### Docker: To run the project use the docker-compose command:
```
docker-compose -f docker-compose.yml up -d
```

After all of the containers all live go to your ```localhost:8081``` to check the inserted data into the database. We use Mongo Express as an administrative interface for MongoDB.  

## Local: To run the project on your computer use the bellow commands:
Use the ```requirements.txt``` to install Python dependencies.
* After that use ```python3 -m unittest test``` to run test cases for the project.  
* To run the scrapper run ```python3 main.py```

# Technical Stack
## Python3
This scrapper is written in python. Python is an interpreted high-level general-purpose programming language. Its design philosophy emphasizes code readability with its use of significant indentation. 

## MongoDB
MongoDB is a source-available cross-platform document-oriented database program. Classified as a NoSQL database program, MongoDB uses JSON-like documents with optional schemas.
We use MongoDB to store scraped product data.
Each object in our program is something like this:

```
{
    _id: 6351381,
    name: 'product name',
    url: 'product url',
    short_url: 'short_url',
    img_url: 'image_url',
    price: 10499000,
    price_before_discount: null,
    total_rating: 4.2,
    total_rating_participant: 1145,
    rating_ditails: {
        '[\'کیفیت ساخت\']': 4.3,
        '[\'ارزش خرید به نسبت قیمت\']': 4.2,
        '[\'نوآوری\']': 4.2,
        '[\'امکانات و قابلیت ها\']': 4.3,
        '[\'سهولت استفاده\']': 4.3,
        '[\'طراحی و ظاهر\']': 4.2
    },
    rating_history: [
        {
            total_rating: 4.2,
            total_participants: 1145,
            rating_details: {
                '[\'کیفیت ساخت\']': 4.3,
                '[\'ارزش خرید به نسبت قیمت\']': 4.2,
                '[\'نوآوری\']': 4.2,
                '[\'امکانات و قابلیت ها\']': 4.3,
                '[\'سهولت استفاده\']': 4.3,
                '[\'طراحی و ظاهر\']': 4.2
            },
            time_stamp: ISODate('2022-01-01T19:49:14.012Z')
        },
          ...
    ],
    price_history: [
                 {
            price: 107490000,
            price_before_discount: null,
            color: 'مشکی',
            time_stamp: ISODate('2021-12-02T00:00:00.000Z')
        },
          ...
    ],
     create_timestamp: ISODate('2022-01-01T19:49:06.299Z'),
     update_timestamp: ISODate('2022-01-01T20:01:10.330Z')
}
```

## Mongo Express
Mongo Express is a lightweight web-based administrative interface deployed to manage MongoDB databases interactively.
We use Mongo Express as an administrative interface for MongoDB.

## Docker
We used Docker for deployment purposes. Use the docker-compose to deploy the scrapper on any server. Instructions are in the first section of the Readme.md