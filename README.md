# Telegrambot-FinalProject

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

A Telegram Book Store Bot that is able to connect to any WordPress site (in this case our Book shop) using WooCommerce REST API and fetch all of its existing products in order to show it in the bot to our customers. \
Users will be able to see the price of products, add them to their cart, and get redirected to the payment page.

This was actually the final project of my bachelor's course at the University of Guilan.

## Requirements
- [Python 3.8 (or higher)](https://www.python.org/)
- install this package with `pip install pyTelegramBotApi` in your cmd(you can check this [link](https://github.com/eternnoir/pyTelegramBotAPI) for documents)
- install this package with `pip install WooCommerce` in your cmd(you can check this [link](http://woocommerce.github.io/woocommerce-rest-api-docs/#) for documents)
- get a token for your bot from https://t.me/BotFather and write it in core.py

## How to work with database
- for checking `database.db` file after it's been created, use : https://sqliteonline.com

### Generating API keys in the WordPress admin interface
To create or manage keys for a specific WordPress user, go to WooCommerce > Settings > Advanced > REST API.

![image](https://user-images.githubusercontent.com/49264993/127431296-968a9106-0c94-4e07-b93e-dc107f62123b.png)

Click the "Add Key" button. In the next screen, add a description and select the WordPress user you would like to generate the key for. Use of the REST API with the generated keys will conform to that user's WordPress roles and capabilities.

Choose the level of access for this REST API key, which can be Read access, Write access or Read/Write access. Then click the "Generate API Key" button and WooCommerce will generate REST API keys for the selected user.

![image](https://user-images.githubusercontent.com/49264993/127431327-490776a5-9319-4a0e-a7ca-1faade395ee8.png)


Now that keys have been generated, you should see two new keys, a QRCode, and a Revoke API Key button. These two keys are your Consumer Key and Consumer Secret.

![image](https://user-images.githubusercontent.com/49264993/127431351-06e34a39-c3f5-4bc1-a420-88f40bba798c.png)

And the final step! just put these keys in database.py at woocommerce function and we're ready to go :D



