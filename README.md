# Nearkart

NearKart is a role-based backend system built with Flask that demonstrates authentication, authorization, session management, and file handling in a multi-user environment.
The project focuses on understanding backend request flow and system structure without relying on heavy abstractions.

## Features:

### Seller Role
- Account registration and login
- Product creation with image uploads

### Buyer Role
- Account registration and login
- View products uploaded by sellers

## System Design Notes:
- Session-based authentication using Flask sessions
- Role-based access control for sellers and buyers
- Product images are stored on the local filesystem
- Only image paths are stored in the database
- Modular structure using Flask blueprints and utility layers

## Project Structure:
```text
project/
├── app.py
├── blueprints/
│   └── products.py
├── utility/
│   ├── database.py
│   └── services.py
├── static/
│   └── products/
├── templates/
│   ├── home.html
│   ├── seller_dash_board.html
│   ├── seller_login.html
│   ├── seller_signup.html
│   ├── customer_login.html
│   └── customer_signup.html
└── seller.db
```

## Running the Project

```bash
python app.py
```
## Scope & Limitations:
-No background processing or async tasks
-No order, payment, or inventory workflows implemented

