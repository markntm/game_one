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

    def __init__(self, name, classification, drop_experience, drop_gold, drop_chance, health, damage, defense,
                 accuracy, speed, flight=False, element='Normal', exp_mod=1, gld_mod=1, chance_mod=1, health_mod=1, damage_mod=1, defense_mod=1):
        self.name = name
        self.classification = classification
        self.element = element
        self.flight = flight
        self.drop_experience = drop_experience
        self.drop_gold = drop_gold
        self.drop_chance = drop_chance
        self.health = health
        self.damage = damage
        self.defense = defense
        self.accuracy = accuracy
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
        health = self.drop_health + (character_level * self.health_mod)
        damage = self.drop_damage + (character_level * self.damage_mod)
        defense = self.drop_defense + (character_level * self.defense_mod)
        return {"name": self.name, "classification": self.classification, "element": self.element,
                "flight": self.flight, "flying": False, "block": False, "experience": experience, "gold": gold,
                "drop_chance": drop_chance, "health": health, "damage": damage,
                "defense": defense, "accuracy": self.accuracy, "speed": self.speed}


def inst_enemies():
    new_enemy = Enemy('Slime', 'Normal', 5, 1, 0.10, )
    return
