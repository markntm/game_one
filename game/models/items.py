from __init__ import db


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    classification = db.Column(db.String(50), nullable=False)  # Weapon, Shield, Armor, etc.
    image_url = db.Column(db.String(255))
    type = db.Column(db.String(50))  # Used for Single Table Inheritance (STI)

    # Common Fields for Weapons, Shields, Armor, etc.
    weapon_type = db.Column(db.String(50))
    damage = db.Column(db.Integer)
    accuracy = db.Column(db.Integer)
    defense = db.Column(db.Integer)
    deflect = db.Column(db.Float)  # For shields
    price = db.Column(db.Integer)
    rarity = db.Column(db.String(50))
    element = db.Column(db.String(50))
    req_mana = db.Column(db.Integer)
    enchantment = db.Column(db.String(50))
    mhealth = db.Column(db.Integer)
    mmana = db.Column(db.Integer)
    speed = db.Column(db.Integer)
    luck = db.Column(db.Integer)
    health = db.Column(db.Integer)
    mana = db.Column(db.Integer)
    duration = db.Column(db.Integer)
    skill = db.Column(db.String(50))  # For scrolls

    # Discriminator column for identifying the subclass
    __mapper_args__ = {
        'polymorphic_identity': 'item',
        'polymorphic_on': classification
    }

    def __init__(self, name, classification, image_url=None):
        self.name = name
        self.classification = classification
        self.image_url = image_url


class Weapon(Item):
    __mapper_args__ = {'polymorphic_identity': 'Weapon'}

    def __init__(self, name, classification, weapon_type, damage, accuracy, price, rarity, element=None, req_mana=0, image_url=None):
        super().__init__(name, classification, image_url)
        self.weapon_type = weapon_type
        self.damage = damage
        self.accuracy = accuracy
        self.price = price
        self.rarity = rarity
        self.req_mana = req_mana
        self.element = element
        self.enchantment = None


class Shield(Item):
    __mapper_args__ = {'polymorphic_identity': 'Shield'}

    def __init__(self, name, classification, defense, deflect, price, rarity, element=None, req_mana=0, image_url=None):
        super().__init__(name, classification, image_url)
        self.defense = defense
        self.deflect = deflect
        self.price = price
        self.rarity = rarity
        self.element = element
        self.req_mana = req_mana
        self.enchantment = None


class Armor(Item):
    __mapper_args__ = {'polymorphic_identity': 'Armor'}

    def __init__(self, name, classification, type, defense, price, rarity, mmana=0, accuracy=0, speed=0, image_url=None):
        super().__init__(name, classification, image_url)
        self.type = type
        self.defense = defense
        self.mmana = mmana
        self.accuracy = accuracy
        self.speed = speed
        self.price = price
        self.rarity = rarity


class Accessory(Item):
    __mapper_args__ = {'polymorphic_identity': 'Accessory'}

    def __init__(self, name, classification, type, mhealth, mmana, damage, defense, accuracy, speed, luck, rarity, image_url=None):
        super().__init__(name, classification, image_url)
        self.type = type
        self.mhealth = mhealth
        self.mmana = mmana
        self.damage = damage
        self.defense = defense
        self.accuracy = accuracy
        self.speed = speed
        self.luck = luck
        self.rarity = rarity


class Consumable(Item):
    __mapper_args__ = {'polymorphic_identity': 'Consumable'}

    def __init__(self, name, classification, type, health, mana, price, duration=0, image_url=None):
        super().__init__(name, classification, image_url)
        self.type = type
        self.health = health
        self.mana = mana
        self.duration = duration
        self.price = price


class Scroll(Item):
    __mapper_args__ = {'polymorphic_identity': 'Scroll'}

    def __init__(self, name, classification, skill, image_url=None):
        super().__init__(name, classification, image_url)
        self.skill = skill


rarities = ['Common', 'Uncommon', 'Rare', 'Epic', 'Mythic', 'Legendary', 'Divine']


