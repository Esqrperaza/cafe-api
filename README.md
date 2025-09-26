Cafe & Wifi

This is a collection of cafes located in England, using data supplied by others. Throught this api, one is able to access different coffee shops, delete, update and add cafes (delete function with api key).

GET:
Get All Cafes
http://127.0.0.1:5000/all?
Will return every cafe in the database as JSON
all_cafes_postman.png

Get Random Cafe
http://127.0.0.1:5000/random?
Will return a random cafe from the database as a JSON
Example Response:
{
    "cafe": {
        "can_take_calls": false,
        "coffee_price": "£3.00",
        "has_sockets": true,
        "has_toilet": true,
        "has_wifi": true,
        "id": 7,
        "img_url": "https://lh3.googleusercontent.com/p/AF1QipP_NbZH7A1fIQyp5pRm1jOGwzKsDWewaxka6vDt=s0",
        "location": "Shoreditch",
        "map_url": "https://g.page/acehotellondon?share",
        "name": "Ace Hotel Shoreditch",
        "seats": "50+"
    }
}
Search by Location
Will return every cafe matching location.
Query Params
loc=Peckham
http://127.0.0.1:5000/search?loc=Peckham


DELETE
Delete Cafe
http://127.0.0.1:5000/report-close/99?api_key=Delete_key

Will remove and delete a cafe from the database. Replace "99" with valid entry. Must include api_key in parameters

PARAMS
api_key=Delete_key

Removes cafe from the database
Example Request
Delete Cafe
curl

curl --location --request DELETE 'http://127.0.0.1:5000/report-close/99?api_key=Delete_key'

Example Response

{
    "response": {
        "SUCCESS": "Cafe 4 has been deleted"
    }
}

PATCH
Update Price
http://127.0.0.1:5000/update-price/99?new_price=$1.00

Will set a new price from a given cafe, e.g. "99". Must include new_price parameter.

PARAMS
new_price=$1.00

Updates price with given paramater
Example Request
Update Price
curl

curl --location --request PATCH 'http://127.0.0.1:5000/update-price/99?new_price=%241.00'

Example Response

{
    "response": {
        "success": "Successfully updated price for Trade Commercial Road"
    }
}

POST
Add Cafe
http://127.0.0.1:5000/add?name=Larry&map_url=maps.goog.com&img_url=pic.jpg&location=Riverside&has_sockets=0&has_toilet=0&has_wifi=0&can_take_calls=0&seats=20-25&coffee_price=$3.75

Will use a form style body request to add new entry to cafe database.
PARAMS
name

Larry
map_url

maps.goog.com
img_url

pic.jpg
location

Riverside
has_sockets

0
has_toilet

0
has_wifi

0
can_take_calls

0
seats

20-25
coffee_price

$3.75
Bodyurlencoded
name

Larry
map_url

map
img_url

img
location

Riverside
has_sockets

1
has_toilet

1
has_wifi

1
can_take_calls

1
seats

20-25
coffee_price

$3.99
