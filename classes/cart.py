import json

from database import get_cart_by_id, set_cart_to_user


class Cart:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.items = self.get_items_by_id()
        # print(self.items)

    def add_item(self, item):
        item = list(item)
        item_id = str(item[0])
        try:
            if not self.items[item_id]:
                print("No items in cart")
            elif self.items[item_id]:
                self.items[item_id][7]["amount"] += 1
        except KeyError:
            self.items[item_id] = item
            self.items[item_id].append({"amount": 1})

    def return_cart_json(self):
        return json.dumps(self.items)

    def get_items_by_id(self):
        if (
            get_cart_by_id(self.chat_id) is not None
            and get_cart_by_id(self.chat_id) != "null"
        ):
            return json.loads(get_cart_by_id(self.chat_id))
        elif (
            get_cart_by_id(self.chat_id) is None
            or get_cart_by_id(self.chat_id) == "null"
        ):
            return dict()

    def set_cart_to_user(self):
        set_cart_to_user(self.chat_id, self.return_cart_json())

    def get_prod_by_id(self, prod_id):
        try:
            return self.items[str(prod_id)]
        except KeyError:
            return None
