from models import db
from flask import Flask


class Skill:
    def __init__(self, name, element, req_weapon, mult_damage, com_points, description):
        self.name = name
        self.element = element
        self.req_weapon = req_weapon
        self.mult_damage = mult_damage
        self.com_points = com_points
        self.description = description


class Enchantment(db.Model):
    __tablename__ = 'enchantments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    rarity = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __init__(self, name, rarity):
        self.name = name
        self.rarity = rarity
        self.description = ''


class WeaponEnchantment(Enchantment):
    __tablename__ = 'weapon_enchantments'

    id = db.Column(db.Integer, db.ForeignKey('enchantments.id'), primary_key=True)
    damage = db.Column(db.Integer, nullable=False, default=0)
    accuracy = db.Column(db.Integer, nullable=False, default=0)
    mana = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, name, rarity, damage=0, accuracy=0, mana=0):
        super().__init__(name, rarity)
        self.damage = damage
        self.accuracy = accuracy
        self.mana = mana


class ShieldEnchantment(Enchantment):
    __tablename__ = 'shield_enchantments'

    id = db.Column(db.Integer, db.ForeignKey('enchantments.id'), primary_key=True)
    defense = db.Column(db.Integer, nullable=False, default=0)
    deflect = db.Column(db.Float, nullable=False, default=0.0)
    mana = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, name, rarity, defense=0, deflect=0.0, mana=0):
        super().__init__(name, rarity)
        self.defense = defense
        self.deflect = deflect
        self.mana = mana


'''Enchantments'''


def all_enchantments():  # COMMITED !
    weapon_enchantments = [

            WeaponEnchantment('Sharp', 'Common', damage=2, accuracy=-1, mana=1),
            WeaponEnchantment('Jagged', 'Common', damage=3, accuracy=-2, mana=0),

            WeaponEnchantment('Venomous', 'Uncommon', damage=5, accuracy=-2, mana=2),
            WeaponEnchantment('Shocking', 'Uncommon', damage=6, accuracy=-3, mana=1),

            WeaponEnchantment('Blazing', 'Rare', damage=8, accuracy=-4, mana=3),
            WeaponEnchantment('Phantom', 'Rare', damage=9, accuracy=-5, mana=1),

            WeaponEnchantment('Infernal', 'Epic', damage=12, accuracy=-6, mana=4),
            WeaponEnchantment('Shadowed', 'Epic', damage=11, accuracy=-4, mana=2),

            WeaponEnchantment('Celestial', 'Mythic', damage=15, accuracy=-7, mana=5),
            WeaponEnchantment('Runed', 'Mythic', damage=14, accuracy=-5, mana=3),

            WeaponEnchantment('Cataclysmic', 'Legendary', damage=20, accuracy=-8, mana=6),
            WeaponEnchantment('Ethereal', 'Legendary', damage=18, accuracy=-6, mana=4),

            WeaponEnchantment('Omniscient', 'Divine', damage=25, accuracy=-10, mana=10),
            WeaponEnchantment('Transcendent', 'Divine', damage=22, accuracy=-7, mana=7)
    ]

    db.session.add_all(weapon_enchantments)

    shield_enchantments = [
            ShieldEnchantment('Sturdy', 'Common', defense=2, deflect=0.05, mana=1),
            ShieldEnchantment('Splintered', 'Common', defense=1, deflect=0.03, mana=0),

            ShieldEnchantment('Chilling', 'Uncommon', defense=4, deflect=0.1, mana=2),
            ShieldEnchantment('Toxic', 'Uncommon', defense=3, deflect=0.08, mana=1),

            ShieldEnchantment('Glacial', 'Rare', defense=7, deflect=0.2, mana=2),
            ShieldEnchantment('Blessed', 'Rare', defense=8, deflect=0.1, mana=0),

            ShieldEnchantment('Runed', 'Epic', defense=10, deflect=0.25, mana=3),
            ShieldEnchantment('Stormforged', 'Epic', defense=9, deflect=0.3, mana=4),

            ShieldEnchantment('Draconic', 'Mythic', defense=15, deflect=0.35, mana=4),
            ShieldEnchantment('Eclipsing', 'Mythic', defense=13, deflect=0.4, mana=5),

            ShieldEnchantment('Titanic', 'Legendary', defense=20, deflect=0.5, mana=6),
            ShieldEnchantment('Heavenly', 'Legendary', defense=18, deflect=0.45, mana=5),

            ShieldEnchantment('Transcendent', 'Divine', defense=25, deflect=0.7, mana=10),
            ShieldEnchantment('Omniscient', 'Divine', defense=22, deflect=0.6, mana=8)
    ]

    db.session.add_all(shield_enchantments)
    db.session.commit()






