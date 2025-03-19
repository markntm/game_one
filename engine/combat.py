from models import db
import random
from flask import Flask, render_template, request, redirect, url_for, session
from models.character import Character, select_character
from models.enemy import Enemy
from models.items import Item, Weapon, Shield, Armor, Accessory, Consumable, Scroll
from models.skill_enchantment import Skill, Enchantment, WeaponEnchantment, ShieldEnchantment, all_enchantments


def chance(acceptance):
    prob = random.randint(0, 100)
    if prob >= acceptance:
        return True
    return False


def accuracy_calc(atk_acc, def_spd, damage, text, wpn_acc=False):
    if wpn_acc:
        accuracy = int((atk_acc + wpn_acc) / 2)
    else:
        accuracy = atk_acc
    diff = accuracy - def_spd
    if diff >= 0:
        if chance(diff):
            text.append("Critical Hit!")
            damage = damage * 1.5
            return damage
        return damage
    diff *= -1
    if chance(diff):
        text.append("Attack Dodged!")
        damage = damage * 0.5
        return damage
    return damage


def defense_calc(def_def, damage, block=False):
    if block:
        def_def *= 2
    if def_def < 100:
        damage = damage - damage * (def_def / 100)
        return damage
    damage = random.randint(0, 1)
    return damage


def character_atk(command, character):
    if command == '1':
        text = []
        damage = character.damage
        damage = accuracy_calc(character.accuracy, session['enemy']['speed'], damage, text)
        damage = defense_calc(session['enemy']['defense'], damage, session['enemy']['block'])
        session['enemy']['health'] = round(session['enemy']['health'] - damage)
        text.append(f"You attacked {session['enemy']['name']} for {damage} dmg.")

    elif command == '2':
        text = [f"{session['enemy']['name']} blocks."]
        session['enemy']['block'] = True

    elif command == '3':
        text = [f"You used your special."]

    else:
        text = ["character_atk error"]

    return text


def enemy_atk(character):
    session['enemy']['block'] = False

    choice = ['attack', 'block']
    if session['enemy']['flight']:
        choice.append('toggle flight')
    # if session['enemy']['special']:
    #     choice.append('special')
    move = random.choice(choice)

    if move == 'attack':
        text = []
        damage = session['enemy']['damage']
        damage = accuracy_calc(session['enemy']['accuracy'], character.defense, damage, text)
        damage = defense_calc(character.defense, damage)
        character.health = round(character.health - damage)
        text.append(f"{session['enemy']['name']} attacked you for {damage} dmg.")

    elif move == 'block':
        text = [f"{session['enemy']['name']} blocks."]
        session['enemy']['block'] = True

    elif move == 'toggle flight':
        if session['enemy']['flying']:
            session['enemy']['flying'] = False
            text = [f"{session['enemy']['name']}, stops flying."]
        else:
            session['enemy']['flying'] = True
            text = [f"{session['enemy']['name']}, takes flight."]

    elif move == 'special':
        text = [f"{session['enemy']['name']}, uses special."]

    return text


def battle_sequence(command, character):
    text = ['']
    if character.speed >= session['enemy']['speed']:
        text.extend(character_atk(command, character))
        if session['enemy']['health'] <= 0:
            text.append(f'You have defeated {session['enemy']['name']}.')
            session['enemy'] = False
            return text

        text.extend(enemy_atk(character))
        if character.health <= 0:
            text.append(f'You have been defeated by {character.name}.')
            return text

        return text

    text.extend(enemy_atk(character))
    if character.health <= 0:
        text.append(f'You have been defeated by {character.name}.')
        return text

    text.extend(character_atk(command, character))
    if session['enemy']['health'] <= 0:
        text.append(f'You have defeated {session['enemy']['name']}.')
        session['enemy'] = False
        return text

    return text




