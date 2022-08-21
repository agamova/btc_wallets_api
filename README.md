## BTC wallets

Backend application that will allow users to register, create own BTC wallets and transfer BTC to other wallets inside the platform. Platform makes 1.5% profit from Transactions between users.
The following RESTful API endpoints implements:

**Users**
----
  

* **URL**

  `POST`/users

   Returns a token that will authenticate all other requests for this user.

* **Data Params**

  `{ "username" : "testname", "password" : "testpassword" }`

* **Success Response:**

    **Code:** 200 <br />
    **Content:** `{ token : 123456789ASDFGHJKIIGFTDRS }`

* **Error Response:**

    **Code:** 400 BAD REQUEST <br />
    **Content:** `{ error : "Wrong password" }`

  OR

   **Code:** 400 BAD REQUEST <br />
    **Content:** `{ "username": [
        "Enter a valid username. This value may contain only English letters, numbers, and @/./+/-/_ characters."
    ] }`

----

**Wallets**
----

* **URL**

  `POST`/wallets

  Create BTC wallet for the authenticated user. 1 BTC (or 100000000 satoshi) is automatically granted to the new wallet upon creation. User may register up to 10 wallets.
  Returns wallet address and current balance in BTC and USD.


* **Success Response:**

    **Code:** 201 Created <br />
    **Content:** 

   `{"address" : 123456789ASDFGHJKIIGFTDRS,
     "balance": [
        {
            "amount": 1.0,
            "currency": "BTC"
        },
        {
            "amount": 21276.59574468085,
            "currency": "USD"
        }
    ]}`

* **Error Response:**

    **Code:** 401 Anautorized <br />
    **Content:** `{ "detail": "Invalid token." }`

  OR

  **Code:** 400 BAD REQUEST <br />
    **Content:** `"error": "Wallets limit exceeded"`


  
* **URL**

  `GET`/wallets/:address

  Returns wallet address and current balance in BTC and USD.
* **URL Params**

   **Required:**

   `address=[str]`

* **Success Response:**

  **Code:** 200 OK <br />
    **Content:** `{"address" : 123456789ASDFGHJKIIGFTDRS,
     "balance": [
        {
            "amount": 1.0,
            "currency": "BTC"
        },
        {
            "amount": 21276.59574468085,
            "currency": "USD"
        }
    ]}`

* **Error Response:**

  **Code:** 401 Anautorized <br />
    **Content:** `{ "detail": "Invalid token." }`

  OR

  **Code:** 404 NOT FOUND <br />
    **Content:** ` "detail": "Not found."`


* **URL**

  `GET`/wallets/:address/transactions

  Returns transactions related to the wallet
* **URL Params**

   **Required:**

   `address=[str]`

* **Success Response:**

  **Code:** 200 OK <br />
    **Content:** `[
    {
        "from_wallet": "1rDlzmhSTVG12UblAP8Kw8jg8kjsYmc8mp",
        "to_wallet": "1hDG7SQh5S0GPAOHEgf5O9fHZqn0BUf2fy",
        "amount": "0.90000000",
        "commission": "0.00000000"
    }
]`

* **Error Response:**

  **Code:** 401 Anautorized <br />
    **Content:** `{ "detail": "Invalid token." }`

  OR

  **Code:** 404 NOT FOUND <br />
    **Content:** ` "detail": "Not found."`


 ----

**Transactions**
----

* **URL**

  `POST`/transactions

   Makes a transaction from one wallet to another
   Transaction is free if transferred to own wallet.
   Transaction costs 1.5% of the transferred amount (profit of the platform) if
transferred to a wallet of another user.

* **Data Params**

  ` {
        "from_wallet": "1rDlzmhSTVG12UblAP8Kw8jg8kjsYmc8mp",
        "to_wallet": "1hDG7SQh5S0GPAOHEgf5O9fHZqn0BUf2fy",
        "amount": "0.90000000"
    }`

* **Success Response:**

  **Code:** 201 Created <br />
    **Content:** 

   ` {
        "from_wallet": "1rDlzmhSTVG12UblAP8Kw8jg8kjsYmc8mp",
        "to_wallet": "1hDG7SQh5S0GPAOHEgf5O9fHZqn0BUf2fy",
        "amount": "0.90000000",
        "commission": "0.00000000"
    }`

* **Error Response:**

  **Code:** 401 Anautorized <br />
    **Content:** `{ "detail": "Invalid token." }`

  OR

  **Code:** 404 NOT FOUND <br />
    **Content:** ` "detail": "Not found."`
  
  OR
  **Code:** 403 FORBIDDEN <br />
  **Content:** ` 'error': 'Permission denied'`
  
  OR
   
   **Code:** 400 BAD REQUEST <br />
   **Content:** ` 'error': 'Insufficient funds'`
  

   * **URL**

   `GET` /transactions

   Returns user’s transactions
   
   * **Success Response:**

     **Code:** 200 OK <br />
       **Content:** `[ {
        "from_wallet": "1rDlzmhSTVG12UblAP8Kw8jg8kjsYmc8mp",
        "to_wallet": "1hDG7SQh5S0GPAOHEgf5O9fHZqn0BUf2fy",
        "amount": "0.90000000",
        "commission": "0.00000000"
    }]`

   * **Error Response:**

     **Code:** 401 Anautorized <br />
       **Content:** `{ "detail": "Invalid token." }`


______

**Statistics**
----


* **URL**

  `GET` /statistics

  Additional endpoint for administrator. Returns the total number of transactions and platform profit. ○ Authenticated with hardcoded token.

* **Success Response:**

  **Code:** 200 OK <br />
    **Content:** `[
    {
        "from_wallet": "1rDlzmhSTVG12UblAP8Kw8jg8kjsYmc8mp",
        "to_wallet": "1hDG7SQh5S0GPAOHEgf5O9fHZqn0BUf2fy",
        "amount": "0.90000000",
        "commission": "0.00000000"
    }
]`

* **Error Response:**

  **Code:** 401 Anautorized <br />
    **Content:** `{ "detail": "Invalid token." }`

  OR

  **Code:** 403 FORBIDDEN <br />
    **Content:** ` "detail": "You do not have permission to perform this action."`


-----

### Installation instructions

1. git clone https://github.com/agamova/btc_wallets_api.git
2. cd btc_wallets_api
3. cp .env.template .env
4. docker-compose up --build

Service will be available at 127.0.0.1:8000
