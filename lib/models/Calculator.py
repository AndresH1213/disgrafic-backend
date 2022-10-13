"""
  prices
  HANDWORK :: design => troquelling => perfor => numbering => packaging_sent => binding => uv => plastification
  MATERIALS :: plates => ink => papper => machine
  plates => id | quantity
  papper => id | size | quantity
  machine => id | quantity
"""


from lib.models.Product import ProductModel


class Calculator:
    def __init__(self, plates, papper, machine, handwork, gain_percentage):
        self.plates = plates
        self.papper = papper
        self.machine = machine
        self.handwork = handwork
        self.gain_percentage = gain_percentage

    def get_papper_price(self):
        p = self.papper
        quantity = int(p['quantity'])
        u = quantity // int(p['size'])
        units = u if p['size'] and u > 0 else 1
        unit_price = self.get_price_by_id(self.papper['id'])
        return units * unit_price

    def get_machine_price(self):
        unit_price = self.get_price_by_id(self.machine['id'])
        return unit_price * int(self.machine['quantity'])

    def get_plates_price(self):
        unit_price = self.get_price_by_id(self.plates['id'])
        return unit_price * int(self.plates['quantity'])

    def get_price_by_id(self, item_id):
        item = dict(ProductModel.get(hash_key=item_id))
        return int(item['price'])

    def get_total_price(self):
        handwork_price = self.handwork
        papper_price = float(self.get_papper_price())
        plates_price = int(self.get_plates_price())
        machine_price = int(self.get_machine_price())

        print("plates: ", plates_price)
        print("papper: ", papper_price)
        print("machine: ", machine_price)

        partial_total = papper_price + plates_price + machine_price + handwork_price
        print("partial: ", partial_total)
        return partial_total + (partial_total*self.gain_percentage)
