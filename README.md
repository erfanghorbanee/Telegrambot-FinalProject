# Telegrambot-FinalProject

Telegram Book Store Bot 

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



