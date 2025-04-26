from __init__ import db


class Shop(db.Model):
    __tablename__ = 'shops'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    npc = db.relationship('NPC', backref='shops', lazy=True)
    items = db.relationship('Item', backref='shop', lazy='dynamic')

    def __init__(self, name, npc):
        self.name = name
        self.npc = npc
        self.items = []

    def enter(self):  # override for every subclass
        return [f"You enter the {self.name}.\n {self.npc.speak()}",
                self.list()]

    def list_items(self):
        if not self.items:
            return "There's nothing here right now."
        return ["*Lists 4 items that are being sold.*", "<span class='gray-text'>Back [5]"]

    def buy_item(self, item_name):
        if item_name in self.items:
            return f"You bought {item_name}!"
        return f"{item_name} is not available here."

    def run(self, character, command, init):
        if init:
            return self.enter()
        else:
            if command == '1' and self.items[0]:
                pass
            elif command == '2' and self.items[1]:
                pass
            elif command == '3' and self.items[2]:
                pass
            elif command == '4' and self.items[3]:
                pass
            elif command == '5':
                return


class ArmoryShop(Shop):
    def __init__(self, npc):
        super().__init__("Weapon Shop", npc)
        self.items = ["Sword", "Bow", "Dagger"]


class ArmorShop(Shop):
    def __init__(self, npc):
        super().__init__("Armor Shop", npc)
        self.items = ["Helmet", "Chest-plate", "Shield"]


class ConsumableShop(Shop):
    def __init__(self, npc):
        super().__init__("Potion Shop", npc)
        self.items = ["Health Potion", "Mana Potion"]


class GuideShop(Shop):
    def __init__(self, npc):
        super().__init__("Guide Shop", npc)
        self.items = ["Map", "Monster Manual", "Town History"]


class Inn(Shop):
    def __init__(self, npc):
        super().__init__("The Cozy Inn", npc)

    def rest(self):
        return f"{self.npc.name} offers you a room. You rest and feel refreshed!"
