# Django complete e-commerce app
This is a complete e-commerce app we developped during a Django course.
We show to learner how he can create a nice clean e-commerce app with many interesting and commun features using Symfony step by step.

## Design
The disign is based on the `MultiShop - Online Shop Website Template` available at [https://htmlcodex.com/online-shop-website-template](https://htmlcodex.com/online-shop-website-template)
![Preview](/static/img/design.jpg)

## Features
The covered features are:
- authentification (sign in, sign out, sign up, account settings)
- products exploration (display, details, search, filter)
- products promotions (discounts, arrival products, ...)
- like/review products and suggestions
- cart options (add, inscrease, decrease, remove, checkout)
- order options (confirm, delivery information, payement)
- alerts/faqs options
- contacts/newsletters options
- status pages (400, 404, 500, ...)
- administration panel

## Course organisation
- Part 1: project creaction with requiered packages/apps and configuration
- Part 2: making of front template base on the above one and add of admin panel
- Part 3: making the models base on the following one (available [here](https://dbdiagram.io/d/63a304ed99cb1f3b55a2c3fb))
![Model](/static/img/models.png)
Models are added to the admin panel (basically)
- Part 4: making of the features announced above
- Part 5: admin panel structuration with more design and dashboard
- Part 6: production

## App installation and configuration
Make sur you have Django developpment environment and proceed as follow:
1) Use the git clone command
    ```
    git clone https://github.com/HKassogue/django_eshop_dec_22.git
    ```
    One can clone a specific branch and proceed to setup.
2) Install the requiered packages
    ```
    pip install -r requirements.txt
    ```
3) Configure the `settings.py` file (specially data base)
4) Make the migrations
    ```
    python manage.py migrate
    ```
    If you want, you can delete the migrations files and proceed to your own migrations files
    ```
    python manage.py makemigrations
    python manage.py migrate
    ```
5) Add some data (categories, products, images) to your database<br>
6) Add a admin user account
    ```
    python manage.py createsuperuser
    ```
7) Run your server, go to the site and enjoy
    ```
    python manage.py runserver
    ```

## App galeries
- The header that contains:
![Header](/static/img/header.png)
  - the authentification options as logged in or not logged in on the top bar
  ![Not logged in options](/static/img/not_logged_in_options.png)
  ![Logged in options](/static/img/logged_in_options.png)
  - the search button options on the top bar
  ![Search button](/static/img/navbar_search.png)
  - the nav bar with display for categories, cart access and like survey
  ![Categories menue](/static/img/navbar2.png)
- The footer that contains basic informations/links:
![Footer](/static/img/footer.png)
- The loging and registration pages:
![Login page](/static/img/login.png)
![Registration page](/static/img/registration.png)
- The home page that contains:
  - the products promotion
  ![Products promotion](/static/img/home_promo.png)
  - the categories display
  ![Home categories](/static/img/home_cat_block.png)
  - the recent product display
  ![Recent products](/static/img/home_recent_prod.png)
  - the arrival product display
  ![Arrival products](/static/img/home_arrival_prod.png)
  - the vendors
  ![Vendors](/static/img/home_vendor.png)
- The shop page that contains the filter/sort options, products display with pagination
  ![Shop](/static/img/shop.png)
  ![Pagination](/static/img/shop_paginator.png)
- The cart page that contains related products with their information and edit options (add/remove, inscrease/decrease, reduction, proceed to checkout)
![Cart](/static/img/cart.png)
- The checkout page that contains the recap of the cart, delivery (shipping) details and the proceed to payment
![Checkout](/static/img/checkout.png)
- The payment page 
![Payment](/static/img/payment.png)
