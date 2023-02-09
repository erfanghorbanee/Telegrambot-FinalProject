import json

from database import get_orders_by_id, new_order


class Order:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.orders = get_orders_by_id(self.chat_id)

    def new_order_create(self, contacts, order_items, order_date, status, note):
        contacts = json.dumps(contacts)
        note = json.dumps(note)
        new_order(self.chat_id, contacts, order_items, order_date, status, note)

    def is_orders(self):
        print(self.orders)
        if self.orders and self.orders[0][6] != 4:
            return True
        elif not self.orders or self.orders[0][6] == 4:
            return False

    def return_items_note_str(self, order_id):
        order = self.orders[order_id]
        order_string = ""
        for k, v in json.loads(order[6]):
            order_string += f"\n<b>{k}</b>: {v}"
        string = f"<b>Order {order_id}</b>\n\n---\n{order[3]}---\n"
        return string
