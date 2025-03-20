from flask import Flask
from models import db
from models.character import character_items
from models.items import Item, Weapon, Shield, Armor, Accessory, Consumable, Scroll
from models.skill_enchantment import Skill, Enchantment, WeaponEnchantment, ShieldEnchantment


class Enemy(db.Model):
    __tablename__ = 'enemies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    classification = db.Column(db.String(50))
    element = db.Column(db.String(50))
    flight = db.Column(db.Boolean)
    drop_experience = db.Column(db.Integer)
    drop_gold = db.Column(db.Integer)
    drop_chance = db.Column(db.Integer)
    health = db.Column(db.Integer)
    damage = db.Column(db.Integer)
    defense = db.Column(db.Integer)
    accuracy = db.Column(db.Integer)
    speed = db.Column(db.Integer)
    exp_mod = db.Column(db.Integer)
    gld_mod = db.Column(db.Integer)
    chance_mod = db.Column(db.Integer)
    health_mod = db.Column(db.Integer)
    damage_mod = db.Column(db.Integer)
    defense_mod = db.Column(db.Integer)

    def __init__(self, name, classification, drop_experience, drop_gold, drop_chance,
                 health, damage, defense, accuracy, speed,
                 flight=False, element='Normal',
                 exp_mod=1, gld_mod=1, chance_mod=1, health_mod=1, damage_mod=1, defense_mod=1):

        self.name = name
        self.classification = classification
        self.element = element
        self.flight = flight
        self.drop_experience = drop_experience
        self.drop_gold = drop_gold
        self.drop_chance = drop_chance  # 0.00 to 1.00 percentage chance
        self.health = health
        self.damage = damage
        self.defense = defense
        self.accuracy = accuracy  # 0.00 to 1.00 percentage chance
        self.speed = speed
        self.exp_mod = exp_mod
        self.gld_mod = gld_mod
        self.chance_mod = chance_mod
        self.health_mod = health_mod
        self.damage_mod = damage_mod
        self.defense_mod = defense_mod

    def generate_stats(self, character_level):
        experience = self.drop_experience + (character_level * self.exp_mod)
        gold = self.drop_gold + (character_level * self.gld_mod)
        drop_chance = self.drop_chance + (character_level * self.chance_mod)
        if drop_chance > 1:
            drop_chance = 1
        health = self.health + (character_level * self.health_mod)
        damage = self.damage + (character_level * self.damage_mod)
        defense = self.defense + (character_level * self.defense_mod)
        return {"name": self.name, "classification": self.classification, "element": self.element,
                "flight": self.flight, "flying": False, "block": False, "experience": experience, "gold": gold,
                "drop_chance": drop_chance, "health": health, "damage": damage,
                "defense": defense, "accuracy": self.accuracy, "speed": self.speed}


def inst_enemies():  #
    new_enemy = Enemy('Cave Bat', 'Beast', 8, 3, 0.10, 5, 2, 1, 0.90, 5, flight=True)
    db.session.add(new_enemy)

    new_enemy = Enemy('Goblin', 'Beast', 7, 5, 0.15, 7, 3, 2, 0.65, 2)
    db.session.add(new_enemy)

    new_enemy = Enemy('Skeleton', 'Undead', 12, 8, 0.15, 10, 2, 3, 0.80, 2)
    db.session.add(new_enemy)

    new_enemy = Enemy('Zombie', 'Undead', 10, 3, 0.15, 15, 2, 2, 0.50, 1)
    db.session.add(new_enemy)

    new_enemy = Enemy('Wraith', 'Undead', 25, 20, 0.20, 20, 6, 5, 0.90, 4, flight=True, element='Dark')
    db.session.add(new_enemy)

    new_enemy = Enemy('Fire Imp', 'Beast', 18, 8, 0.20, 8, 6, 2, 0.75, 3, element='Fire')
    db.session.add(new_enemy)

    new_enemy = Enemy('Stone Golem', 'Construct', 50, 20, 0.25, 50, 5, 15, 0.60, 1, element='Earth')
    db.session.add(new_enemy)

    new_enemy = Enemy('Mimic', 'Construct', 30, 50, 0.15, 25, 7, 5, 0.70, 2)
    db.session.add(new_enemy)

    new_enemy = Enemy('Dire Wolf', 'Beast', 20, 12, 0.15, 15, 5, 3, 0.85, 4)
    db.session.add(new_enemy)

    new_enemy = Enemy('Venom Spider', 'Beast', 16, 6, 0.10, 9, 4, 2, 0.80, 5, element='Poison')
    db.session.add(new_enemy)

    new_enemy = Enemy('Undead Knight', 'Undead', 60, 40, 0.25, 50, 10, 8, 0.75, 2, element='Dark')
    db.session.add(new_enemy)

    new_enemy = Enemy('Cursed Armor', 'Construct', 45, 25, 0.25, 35, 8, 9, 0.65, 1, element='Dark')
    db.session.add(new_enemy)
    """
    new_enemy = Enemy('Lich', 'Undead', 100, 100, 0.05, 75, 12, 6, 0.85, 3, element='Dark')
    db.session.add(new_enemy)

    new_enemy = Enemy('Frost Wyrm', 'Beast', 120, 200, 0.05, 90, 15, 10, 0.70, 3, flight=True, element='Ice')
    db.session.add(new_enemy)
    
    new_enemy = Enemy('Phoenix', 'Beast', 150, 250, 0.02, 100, 20, 8, 0.90, 6, flight=True, element='Fire')
    db.session.add(new_enemy)

    new_enemy = Enemy('Kraken', 'Beast', 200, 500, 0.01, 150, 25, 12, 0.75, 2, element='Water')
    db.session.add(new_enemy)

    new_enemy = Enemy('Necromancer', 'Undead', 90, 150, 0.08, 55, 14, 5, 0.80, 3, element='Dark')
    db.session.add(new_enemy)
    """
    db.session.commit()


