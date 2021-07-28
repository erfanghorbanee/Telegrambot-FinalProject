import requests
import sqlite3
import logging
import re
from woocommerce import API

# Initializing logs
log = logging.getLogger(__name__)

log.debug("Trying to connect to database.db or create new if not exist")
conn = sqlite3.connect("database.db", check_same_thread=False)

with conn:
    log.debug("Initializing cursor")
    cursor = conn.cursor()

    # Creating user table if not exists
    cursor.executescript("""CREATE TABLE IF NOT EXISTS users
        (
             chat_id INTEGER not null
                primary key,
            first_name VARCHAR not null,
            username VARCHAR,
            phone_number VARCHAR,
            cart TEXT,
            is_making_order BOOLEAN,
            is_operator BOOLEAN,
            is_administrator BOOLEAN
        );
        """)

        # Creating operator table if not exists
    cursor.executescript("""CREATE TABLE IF NOT EXISTS operator
        (
             chat_id INTEGER not null
            primary key,
            first_name VARCHAR not null,
            username VARCHAR,
            phone_number VARCHAR,
            cart TEXT,
            is_making_order BOOLEAN,
            is_operator BOOLEAN,
            is_administrator BOOLEAN
        );
        """)

    # Creating category table if not exists
    cursor.executescript("""CREATE TABLE IF NOT EXISTS categories
        (
             category_id INTEGER not null
                primary key autoincrement,
            title VARCHAR
        );
        """)

    # Creating products table if not exists
    cursor.executescript("""CREATE TABLE IF NOT EXISTS products
        (
             id INTEGER not null
                primary key autoincrement,
            title VARCHAR,
            description TEXT,
            price INTEGER,
            image BLOB,
            category_id INTEGER,
            bot_shows BOOLEAN
        );
        """)

    # Creating orders table if not exists
    cursor.executescript("""CREATE TABLE IF NOT EXISTS orders
        (
             order_id INTEGER not null
                primary key autoincrement,
            chat_id INTEGER,
            contacts TEXT,
            order_items TEXT,
            order_date DATE,
            status INTEGER,
            note TEXT
        );
        """)
    conn.commit()


def if_user_exists(chat_id):
    try:
        cursor.execute("SELECT * FROM users WHERE chat_id LIKE ?", [chat_id])
        g_user = cursor.fetchall()
        log.debug(g_user[0][1] + " was checked on existing")
        return True
    except IndexError:
        return False


def new_user(chat_id, first_name, username, phone_number):
    cursor.execute("""INSERT INTO users (chat_id, first_name, username, phone_number, is_making_order, is_operator,
     is_administrator) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (chat_id, first_name, username, phone_number, 0, 0, 0))
    conn.commit()

def new_user_operator(chat_id, first_name, username, phone_number,is_operator):
    cursor.execute("""INSERT INTO operator (chat_id, first_name, username, phone_number, is_making_order, is_operator,
     is_administrator) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (chat_id, first_name, username, phone_number, 0, 1, 0))
    conn.commit()


def new_order(chat_id, contacts, order_items, order_date, status, note):
    cursor.execute("""
    INSERT INTO orders (chat_id, contacts, order_items, order_date, status, note) 
    VALUES (?, ?, ?, ?, ?, ?)
    """, (chat_id, contacts, order_items, order_date, status, note))
    conn.commit()


def add_category(title):
    cursor.execute("INSERT INTO category (title) VALUES (?)",
                   [title])
    conn.commit()
    log.debug(f"Added category: {title}")


def add_product(title, description, price, image, category_id):
    cursor.execute("""INSERT INTO products (title, description, price, image, category_id, bot_shows) 
    VALUES (?, ?, ?, ?, ?, ?)""", (title, description, price, image, category_id, 1))
    conn.commit()


def get_categories():
    cursor.execute("SELECT * FROM categories")
    return cursor.fetchall()


def get_products():
    cursor.execute("SELECT * FROM products")
    return cursor.fetchall()


def get_product_ids():
    cursor.execute("SELECT id FROM products")
    return cursor.fetchall()


def get_product_by_id(prod_id):
    cursor.execute("SELECT * FROM products WHERE id LIKE ?", [prod_id])
    product = cursor.fetchall()
    return product[0]


def get_user_by_id(user_id):
    cursor.execute("SELECT * FROM users WHERE chat_id LIKE ?", [user_id])
    g_user = cursor.fetchall()
    try:
        return g_user[0]
    except IndexError:
        return None


def get_cart_by_id(user_id):
    cursor.execute("SELECT cart FROM users WHERE chat_id LIKE ?", [user_id])
    user_cart = cursor.fetchall()
    return user_cart[0][0]


def get_orders_by_id(user_id):
    cursor.execute("SELECT * FROM orders WHERE chat_id LIKE ?", [user_id])
    user_cart = cursor.fetchall()
    return user_cart


def get_orders_ids_by_id(user_id):
    cursor.execute("SELECT order_id FROM orders WHERE chat_id LIKE ?", [user_id])
    order_ids = cursor.fetchall()
    return order_ids


def get_making_order_by_id(user_id):
    cursor.execute("SELECT is_making_order FROM users WHERE chat_id LIKE ?", [user_id])
    making_orders = cursor.fetchall()
    # print(making_orders)
    return making_orders[0][0]


def get_operators():
    cursor.execute("SELECT chat_id FROM operator WHERE is_operator LIKE ?", [1])
    operators = cursor.fetchall()
    try:
        return operators[0]
    except IndexError:
        return None


def set_cart_to_user(user_id, cart):
    cursor.executemany("""UPDATE users 
    SET cart = ? WHERE chat_id = ?""", ((cart, user_id), ))
    conn.commit()


def set_making_order_status_to_user(user_id, status):
    cursor.executemany("""UPDATE users 
    SET is_making_order = ? WHERE chat_id = ?""", ((status, user_id), ))
    conn.commit()


def set_phone_number_to_user(user_id, phone):
    cursor.executemany("""UPDATE users 
    SET phone_number = ? WHERE chat_id = ?""", ((phone, user_id), ))
    conn.commit()
# ============================================================================

# creating operator
new_user_operator("98948374", "Alireza", "@Bookworm98", "None",1)

# Connecting to Woocommerce
wcapi = API(
    url="http://localhost/wordpress/", # Your store URL
    consumer_key="ck_0fc9b7b3a719f64e44bff8bc41dfd0aba71f0cc7", # Your consumer key
    consumer_secret="cs_bacf34af6a5f7fc0051be013b357f9f1fe640117", # Your consumer secret
    wp_api=True, # Enable the WP REST API integration
    version="wc/v3" # WooCommerce WP REST API version
)

# Removes html tags from description we got out of woocommerce
def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext
  

# Get products from woocommerce
def get_woocommerce_products():
    count = 0
    for i in wcapi.get("products").json():
    
        img_data = requests.get(i["images"][0]["src"]).content
        with open("images/item_"+str(count)+".png", 'wb') as handler:
            handler.write(img_data)
            
        add_product(i["name"], cleanhtml(i["description"]), i["price"],
                    ("images/item_"+str(count)+".png"), i["id"])
        
        count += 1
        
get_woocommerce_products()
