import datetime
import json
import re
import inscriptions
from classes.cart import Cart
from classes.catalog import Catalog
from classes.order import Order
from database import *
import logging

log = logging.getLogger("bot_functions")

# Creating new Catalog
catalog = Catalog(None)
catalog_group = dict()
# Creating new making_order
making_order_group = dict()


def handler(bot, types, message, call):
    creating_unique_catalog(message, call)
    if message and message.text:
        checking_messages(bot, message, types)
    elif call and call.message:
        checking_new_callback_data(bot, call, types)


def creating_unique_catalog(message, call):
    global catalog
    if message is not None or call is not None:
        if message:
            catalog = Catalog(message.chat.id)
        elif call.message.chat.id:
            catalog = Catalog(call.message.chat.id)
    if message is not None or call is not None:
        try:
            if catalog_group[catalog.chat_id] is None:
                log.debug(catalog_group)
        except KeyError:
            catalog_group[catalog.chat_id] = catalog
        if message and catalog_group[catalog.chat_id] is not None:
            catalog = catalog_group[message.chat.id]
        elif call and catalog_group[catalog.chat_id] is not None:
            catalog = catalog_group[call.message.chat.id]


def sending_start_message(bot, message, types):
    markup = creating_start_markup_buttons(types)
    bot.send_message(message.chat.id, 'Hi, {0.first_name}'.format(message.from_user) +
                      ' Glad to see you in our bot!\nThis is a <b>' +
                      'Book Store</b>.\n' +
                      'Select products in the catalog and then place an order in the basket :)'
                       , parse_mode='html', reply_markup=markup)


def start_func(message):
    if not if_user_exists(message.chat.id):
        new_user(message.chat.id, message.from_user.first_name, message.from_user.username, None)


def sending_help_message(bot, message):
    log.info(f"{message.from_user.username} sent a /help command")
    bot.send_message(message.chat.id, inscriptions.help_text, parse_mode='html')


def creating_start_markup_buttons(types):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item1 = types.KeyboardButton(inscriptions.catalog)
    item2 = types.KeyboardButton(inscriptions.cart)
    item3 = types.KeyboardButton(inscriptions.orders)
    item4 = types.KeyboardButton(inscriptions.contacts)
    item5 = types.KeyboardButton(inscriptions.faq)
    markup.add(item1, item2, item3, item4, item5)
    return markup


def checking_messages(bot, message, types):
    # Making order
    if get_making_order_by_id(message.chat.id):
        global making_order_group
        try:
            steps = making_order_group[message.chat.id][0]
            params = making_order_group[message.chat.id][1]
            checking_order_creating_steps(bot, message, types, steps, params)
        except KeyError:
            making_order_group[message.chat.id] = [
                {
                    "city": True,
                    "number_of_departament": False,
                    "full_name": False,
                    "number": False,
                    "payment_system": False
                },
                {
                    "city": None,
                    "number_of_departament": None,
                    "full_name": None,
                    "number": None,
                    "payment_system": None
                }
            ]
            steps = making_order_group[message.chat.id][0]
            params = making_order_group[message.chat.id][1]
            checking_order_creating_steps(bot, message, types, steps, params)
    else:
        # Main buttons
        if message.text == inscriptions.catalog:
            catalog_function(bot, message, types)
        elif message.text == inscriptions.cart:
            cart_function(bot, message, types)
        elif message.text == inscriptions.orders:
            orders_function(bot, types, message)
        elif message.text == inscriptions.faq:
            faq_function(bot, message)
        elif message.text == inscriptions.contacts:
            contacts_function(bot, message)
        else:
            bot.send_message(message.chat.id, inscriptions.unrecognized_message, parse_mode='html')


def checking_order_creating_steps(bot, message, types, steps, params):
    if not steps["number_of_departament"]:
        bot.send_message(message.chat.id, inscriptions.number_of_departament)
        params["city"] = message.text
        steps["number_of_departament"] = True
    elif not steps["full_name"]:
        bot.send_message(message.chat.id, inscriptions.full_name)
        params["number_of_departament"] = message.text
        steps["full_name"] = True
    elif not steps["number"]:
        bot.send_message(message.chat.id, inscriptions.number)
        params["full_name"] = message.text
        steps["number"] = True
    elif not steps["payment_system"]:
        bot.send_message(message.chat.id, inscriptions.payment_system, parse_mode='html')
        params["number"] = message.text
        steps["payment_system"] = True
    else:
        params["payment_system"] = message.text
        cart = Cart(message.chat.id)
        catalog.set_pre_order_params(params)
        markup = create_pre_order_markup(types)
        items_arr = make_items_array(message)
        items_text = items_arr[0]
        result_sum = items_arr[1]
        params_text = ""
        for k in params:
            params_text += "<b>{0}: </b>{1}\n".format(inscriptions.params_text[k], params[k])
        bot.send_message(message.chat.id, "{1}\n\n---\n{0}".format(items_text,
                                                                   inscriptions.is_everything_right) +
                         "---\n\n{1}<b>Total: </b>{0}".format(result_sum, params_text) +
                         inscriptions.currency, parse_mode='html', reply_markup=markup)
        cart.pre_order_params = params


def create_pre_order_markup(types):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton(inscriptions.order_true_btn, callback_data="order_true")
    item2 = types.InlineKeyboardButton(inscriptions.order_false_btn, callback_data="order_false")
    markup.add(item1, item2)
    return markup


def catalog_function(bot, message, types):
    catalog_first_prod(bot, message, types)


def catalog_first_prod(bot, message, types):
    try:
        with open(catalog.products[catalog.current_prod][4], 'rb') as photo:
            markup = catalog_markup_create(message.chat.id, catalog.products,
                                           catalog.current_prod, catalog.prod_amount, types)
            bot.send_photo(message.chat.id, photo,
                           "📚 <b>{0[1]}</b>\n{0[2]}".format(catalog.products[catalog.current_prod]),
                           reply_markup=markup, parse_mode='html')
    except IndexError as e:
        print(e)
        log.error("No products in catalog")
        bot.send_message(message.chat.id, inscriptions.no_prods_in_catalog)


def catalog_update(bot, call, types):
    markup = catalog_markup_create(call.message.chat.id, catalog.products,
                                   catalog.current_prod, catalog.prod_amount, types)
    bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                             caption="<b>{0[1]}</b>\n{0[2]}".format(catalog.products[catalog.current_prod]),
                             reply_markup=markup, parse_mode="html")


def catalog_markup_create(call, products, current_prod_catalog, last_prod, types):
    products_in_cart = how_many_in_cart(call, products, current_prod_catalog)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item = types.InlineKeyboardButton(products_in_cart + inscriptions.currency + " " +
                                      str(products[current_prod_catalog][3]) + " " +
                                      inscriptions.add_to_cart + " " +
                                      products[current_prod_catalog][1], callback_data="to_cart")
    markup.add(item)
    markup.row_width = 3
    item1 = types.InlineKeyboardButton("←", callback_data="prev")
    item2 = types.InlineKeyboardButton(f"{current_prod_catalog + 1} / {last_prod + 1}", callback_data="nothing")
    item3 = types.InlineKeyboardButton("→", callback_data="next")
    markup.add(item1, item2, item3)
    return markup


def how_many_in_cart(chat_id, products, current_prod_catalog):
    cart = Cart(chat_id)
    products_in_cart = cart.items
    try:
        cur_prod_amount = products_in_cart[str(products[current_prod_catalog][0])][7]["amount"]
        cur_prod_amount_string = f"({cur_prod_amount}) "
        return cur_prod_amount_string
    except TypeError:
        return ""
    except KeyError:
        return ""


def checking_new_callback_data(bot, call, types):
    if call.message:
        callback_data_catalog(bot, call, types)
        callback_data_cart(bot, call)
        callback_data_order(bot, call)
        if get_making_order_by_id(call.message.chat.id):
            callback_data_pre_order(bot, call)


def callback_data_catalog(bot, call, types):
    if call.data == "to_cart":
        callback_to_cart(call)
        catalog_update(bot, call, types)
    elif call.data == "next":
        callback_next_prod()
        catalog_update(bot, call, types)
    elif call.data == "prev":
        callback_prev_prod()
        catalog_update(bot, call, types)


def callback_to_cart(call):
    cart = Cart(call.message.chat.id)
    cart.add_item(catalog.products[catalog.current_prod])
    cart.set_cart_to_user()


def callback_next_prod():
    if catalog.current_prod == catalog.prod_amount:
        catalog.current_prod = 0
    else:
        catalog.current_prod += 1


def callback_prev_prod():
    if catalog.current_prod == 0:
        catalog.current_prod = catalog.prod_amount
    else:
        catalog.current_prod -= 1


def cart_function(bot, message, types):
    items_array = make_items_array(message)
    if items_array is not None:
        items_text = items_array[0]
        result_sum = items_array[1]
        markup = cart_markup_create(types)
        bot.send_message(message.chat.id, "<b>Basket</b>\n\n---\n{0}".format(items_text) +
                         "---\n\n<b>Total: </b>{0}".format(result_sum) +
                         inscriptions.currency, reply_markup=markup, parse_mode='html')
    elif items_array is None:
        bot.send_message(message.chat.id, inscriptions.cart_is_empty, parse_mode='html')


def make_items_array(message):
    cart = Cart(message.chat.id)
    items = cart.items
    items_arr = list()
    items_text = str()
    items_sum = 0
    try:
        for item in items:
            amount = items[item][7]['amount']
            price = items[item][3]
            local_sum = amount * price
            items_text += f"<b>{items[item][1]}</b>\n{amount} " \
                          f"{inscriptions.amount} x {price}{inscriptions.currency} = {local_sum}\n"
            items_sum += local_sum
        if items_text == "":
            return None
        else:
            items_arr.append(items_text)
            items_arr.append(items_sum)
            return items_arr
    except TypeError:
        return None


def cart_markup_create(types):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton(inscriptions.clear_basket, callback_data="clear_basket")
    item2 = types.InlineKeyboardButton(inscriptions.make_order, callback_data="make_order")
    markup.add(item1, item2)
    return markup


def callback_data_cart(bot, call):
    if call.data == "clear_basket":
        callback_clear_basket(call)
        cart_update(bot, call)
    elif call.data == "make_order":
        callback_make_order(bot, call)
        cart_update(bot, call)


def cart_update(bot, call):
    cart = Cart(call.message.chat.id)
    if cart.items == {}:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, inscriptions.cart_is_empty, parse_mode='html')


def callback_clear_basket(call):
    cart = Cart(call.message.chat.id)
    cart.items = None
    cart.set_cart_to_user()


def callback_make_order(bot, call):
    start_making_order(bot, call)


def start_making_order(bot, call):
    bot.send_message(call.message.chat.id, inscriptions.city_of_dislocation)
    set_making_order_status_to_user(call.message.chat.id, 1)


def callback_data_order(bot, call):
    orders = Order(call.message.chat.id)
    # If order in user`s order list
    for order in orders.orders:
        if call.data == order[0]:
            bot.send_message(call.message.chat.id, order.return_items_note_str())


def orders_function(bot, types, message):
    order = Order(message.chat.id)
    if not order.is_orders():
        bot.send_message(message.chat.id, inscriptions.no_orders_text)
    elif order.is_orders():
        markup = create_orders_markup(types, message)
        bot.send_message(message.chat.id, inscriptions.some_orders_here, reply_markup=markup)


def create_orders_markup(types, message):
    orders = Order(message.chat.id)
    markup = types.InlineKeyboardMarkup(row_width=2)
    for order in orders.orders:
        item = types.InlineKeyboardButton(order[0], callback_data=order[0])
        markup.add(item)
    return markup

def callback_data_pre_order(bot, call):
    if call.data == "order_true":
        user = get_user_by_id(call.message.chat.id)
        date = datetime.datetime.now()
        date_id = re.search(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", str(date))
        date_id = date_id.group()
        cart = Cart(call.message.chat.id)
        params = catalog.pre_order_params
        new_order(call.message.chat.id, json.dumps({
            "Chat ID": call.message.chat.id,
            "Phone": params["number"],
            "Name": user[1],
            "Username": user[2],
        }), cart.return_cart_json(), date_id, 0, json.dumps(params))
        set_phone_number_to_user(call.message.chat.id, params["number"])
        set_making_order_status_to_user(call.message.chat.id, 0) 
        send_to_operators(bot, call.message)
        bot.send_message(call.message.chat.id,
                         inscriptions.order_true)
        set_making_order_status_to_user(call.message.chat.id, 0)
        callback_clear_basket(call)
        
    elif call.data == "order_false":
        set_making_order_status_to_user(call.message.chat.id, 0)
        catalog.pre_order_params = None
        bot.send_message(call.message.chat.id, inscriptions.order_false)


def send_to_operators(bot, message):
    #try:
    user = get_user_by_id(message.chat.id)
    params = catalog.pre_order_params
    items_arr = make_items_array(message)
    items_text = items_arr[0]
    result_sum = items_arr[1]
    order = get_orders_by_id(message.chat.id)[len(get_orders_by_id(message.chat.id)) - 1]
    params_text = ""
    for k in params:
        params_text += "<b>{0}: </b>{1}\n".format(inscriptions.params_text[k], params[k])
    user_info_str = "------------------------\n" + f"<b>Name:</b> {user[1]}\n" + f"<b>Username:</b> {user[2]}\n" + \
                    f"<b>Phone number:</b> {user[3]}\n" + f"<b>Telegram order ID:</b> | {order[0]} |\n" + \
                    f"<b>date:</b> {order[4]}\n" + "-----\n" + \
                    f"Status: {inscriptions.status[order[5]]}\n" + "-----\n\n"
    for operator_id in get_operators():
        bot.send_message(operator_id, user_info_str + "<b>Basket</b>\n\n---\n{0}".format(items_text) +
                         "---\n\n{1}<b>Total: </b>{0}".format(result_sum, params_text) +
                         inscriptions.currency, parse_mode='html')


def faq_function(bot, message):
    bot.send_message(message.chat.id, inscriptions.faq_text, parse_mode='html')


def contacts_function(bot, message):
    bot.send_message(message.chat.id, inscriptions.contacts_text, parse_mode='html')
