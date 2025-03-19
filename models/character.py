from flask import Flask
from models import db
from models.items import Item, Weapon, Shield, Armor, Accessory, Consumable, Scroll
from models.skill_enchantment import Skill, Enchantment, WeaponEnchantment, ShieldEnchantment

character_items = db.Table('character_items',
                           db.Column('character_id', db.Integer, db.ForeignKey('characters.id'), primary_key=True),
                           db.Column('item_id', db.Integer, db.ForeignKey('items.id'), primary_key=True)
                           )


class Character(db.Model):
    __tablename__ = 'characters'

    skill_point = 2

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    classification = db.Column(db.String(50))
    level = db.Column(db.Integer)
    experience = db.Column(db.Integer)
    mexperience = db.Column(db.Integer)
    health = db.Column(db.Integer)
    mhealth = db.Column(db.Integer)
    mana = db.Column(db.Integer)
    mmana = db.Column(db.Integer)
    damage = db.Column(db.Integer)
    defense = db.Column(db.Integer)
    accuracy = db.Column(db.Integer)
    speed = db.Column(db.Integer)
    luck = db.Column(db.Integer)

    dungeon_level = db.Column(db.Integer)

    # skill = db.Column(db.Text)
    gold = db.Column(db.Integer)
    inventory = db.relationship('Item', secondary=character_items, backref=db.backref('owners', lazy=True))

    def __init__(self, name, classification, mhealth, mmana, damage, defense, accuracy, speed, luck,
                 inventory=None, skill=None):

        # Base Stats
        self.name = name
        self.classification = classification
        self.level = 1
        self.experience = 0
        self.mexperience = 10
        self.health = mhealth
        self.mhealth = mhealth
        self.mana = mmana
        self.mmana = mmana
        self.damage = damage
        self.defense = defense
        self.accuracy = accuracy
        self.speed = speed
        self.luck = luck

        self.dungeon_level = 1

        # Skills
        if skill is None:
            self.skill = []
        else:
            self.skill = skill

        # Inventory
        self.gold = 0
        if inventory is None:
            self.inventory = []
        else:
            self.inventory = inventory

        # Equipment
        self.eqp_weapon = None
        self.eqp_shield = None
        self.eqp_helmet = None
        self.eqp_plate = None
        self.eqp_leggings = None
        self.eqp_boots = None
        self.eqp_accessory = None

    def display_stats(self):
        text = []
        text.append("Name: " + self.name)
        text.append("Class: " + self.classification)
        text.append("Level: " + str(self.level))
        text.append("Experience: " + str(self.experience) + "/" + str(self.mexperience))
        text.append("Health: " + str(self.health) + "/" + str(self.mhealth))
        text.append("Mana: " + str(self.mana) + "/" + str(self.mmana))
        text.append("Damage: " + str(self.damage))
        text.append("Defense: " + str(self.defense))
        text.append("Accuracy: " + str(self.accuracy))
        text.append("Speed: " + str(self.speed))
        text.append("Luck: " + str(self.luck))
        return text

    def stat_up(self, command):
        if command == 'health':
            self.mhealth += 1
            self.health = self.mhealth
            response = "You increased your max health by 1."
        elif command == 'damage':
            self.damage += 1
            response = "You increased your max attack by 1."
        elif command == 'defense':
            self.defense += 1
            response = "You increased your max defense by 1."
        elif command == 'mana':
            self.mmana += 1
            self.mana = self.mmana
            response = "You increased your max mana by 1."
        elif command == 'accuracy':
            self.accuracy += 1
            response = "You increased your max accuracy by 1."
        elif command == 'speed':
            self.speed += 1
            response = "You increased your max speed by 1."
        elif command == 'luck':
            self.luck += 1
            response = "You increased your max luck by 1."
        else:
            response = "Invalid command"
        db.session.commit()
        return response

    def level_up(self):
        if self.experience < self.mexperience:
            return
        if self.level % 10 == 0:
            self.skill_point += 1
        self.level += 1
        self.experience -= self.mexperience
        self.mexperience = 10 * self.level

    def add_inventory(self, item):
        self.inventory.append(item)

    def remove_inventory(self, item_id):
        self.inventory = [item for item in self.inventory if item.id != item_id]

    def add_stat(self, item):
        """Adds an item's stat bonuses to the character's stats."""
        stats = ['health', 'mhealth', 'mana', 'mmana', 'damage', 'defense', 'accuracy', 'speed', 'luck']

        for stat in stats:
            # Check if the item has the stat and add it to the character's corresponding stat
            item_value = getattr(item, stat, 0)  # Default to 0 if the item does not have this attribute
            if item_value:
                current_value = getattr(self, stat)
                setattr(self, stat, current_value + item_value)
        if self.health > self.mhealth:
            self.health = self.mhealth
        if self.mana > self.mmana:
            self.mana = self.mmana
        db.session.commit()

    def subtract_stat(self, item):
        """Subtracts an item's stat bonuses from the character's stats."""
        stats = ['health', 'mhealth', 'mana', 'mmana', 'damage', 'defense', 'accuracy', 'speed', 'luck']

        for stat in stats:
            item_value = getattr(item, stat, 0)  # Default to 0 if the item does not have this attribute
            if item_value:
                current_value = getattr(self, stat)
                setattr(self, stat, current_value - item_value)
        db.session.commit()

    def equip(self, item):
        if item not in self.inventory:
            print(f"{item.name} is not in inventory!")
            return

        self.inventory.remove(item)

        if item.classification == "Weapon":
            if self.eqp_weapon:
                self.subtract_stat(self.eqp_weapon)  # Subtract old weapon stats
            self.eqp_weapon = item

        elif item.classification == "Shield":
            if self.eqp_shield:
                self.subtract_stat(self.eqp_shield)  # Subtract old shield stats
            self.eqp_shield = item

        elif item.classification == "Helmet":
            if self.eqp_helmet:
                self.subtract_stat(self.eqp_helmet)  # Subtract old helmet stats
            self.eqp_helmet = item

        elif item.classification == "Plate":
            if self.eqp_plate:
                self.subtract_stat(self.eqp_plate)  # Subtract old plate stats
            self.eqp_plate = item

        elif item.classification == "Leggings":
            if self.eqp_leggings:
                self.subtract_stat(self.eqp_leggings)  # Subtract old leggings stats
            self.eqp_leggings = item

        elif item.classification == "Boots":
            if self.eqp_boots:
                self.subtract_stat(self.eqp_boots)  # Subtract old boots stats
            self.eqp_boots = item

        elif item.classification == "Accessory":
            if self.eqp_accessory:
                self.subtract_stat(self.eqp_accessory)  # Subtract old accessory stats
            self.eqp_accessory = item

        else:
            print(f"Item {item.name} does not have a valid classification and cannot be equipped.")
            self.inventory.append(item)  # Return item to inventory
            return

        # Add the new item's stats to the character
        self.add_stat(item)


def select_character(name, classification):
    if classification == 'Swordsman':
        new_character = Character(name, classification, 10, 1, 1, 1, 70, 10, 1)

    elif classification == 'Mage':
        new_character = Character(name, classification, 8, 5, 2, 1, 75, 10, 1)

    elif classification == 'Knight':
        new_character = Character(name, classification, 12, 1, 2, 1, 65, 7, 1)

    else:
        new_character = Character(name, classification, 10, 1, 1, 1, 70, 10, 1)
    return new_character



