from database import get_products
# from WooCommerce import get_data

# id, name, info, price, img, category_id(1....10),  bot-show(1.....1)

# for i in get_products():
#     print(i[6])     #7
# print(get_products())

class Catalog:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.current_prod = 0
        self.products = get_products()
        self.prod_amount = len(self.products) - 1
        self.pre_order_params = None

    def set_pre_order_params(self, params):
        self.pre_order_params = params
