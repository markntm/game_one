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

    def enter(self):
        return f"You enter the {self.name}.\n {self.npc.speak()}"

    def list_items(self):
        if not self.items:
            return "There's nothing here right now."
        return "\n".join(f"- {item}" for item in self.items)

    def buy_item(self, item_name):
        if item_name in self.items:
            return f"You bought {item_name}!"
        return f"{item_name} is not available here."


class WeaponShop(Shop):
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
