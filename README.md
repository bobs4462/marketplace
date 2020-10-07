# marketplace
Implementation of a oversimplified marketplace application.

# Usage
## Test database
If test database does not exist in `data` directory, run:
```sh
python3 initdb.py
```
to create database schema and populate it with test data

## Running the server
In order to start the server run:
```sh
python3 main.py
```
this will start the server, and it's immediately ready to accept connections

## Available methods
### Get methods
*All parameters for get request should encoded in url*

**Methods:**
* /user/get
* /user/orders/get
* /shop/inventory/get

#### /user/get
**Parameters:**
    * id - id of desired user
**Example:**
```
curl -X GET http://localhost:8080/user/get?id=111
```

#### /user/orders/get
**Parameters:**
    * user\_id - id of desired user
```
curl -X GET http://localhost:8080/user/orders/get?user_id=111
```

#### /shop/inventory/get
**Parameters:**
    * shop\_id - id of desired shop
```
curl -X GET http://localhost:8080/shop/inventory/get?shop_id=999
```

**Example**

### Post methods
*All parameters for post request should be passed in body in json format*

**Methods:**
* /order/create

#### /order/create
**Parameters:**
    * book\_id - id of bought book
    * book\_quantity - the number of copies of book bought
    * user\_id - id of the user, who made the purchase
    * shop\_id - id of shop, where the purchase was made
```
curl -d '{"book_id": 2222, "user_id": 111, "shop_id": 999, "book_quantity": 2}' -X POST http://localhost:8080/order/create
```
