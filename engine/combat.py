from models import db
import random
from flask import Flask, render_template, request, redirect, url_for, session
from models.character import Character, select_character
from models.enemy import Enemy, print_stats
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
            text.append("<span class='yellow-text'>Critical Hit!")
            damage = damage * 1.5
            return damage
        return damage
    diff *= -1
    if chance(diff):
        text.append("<span class='yellow-text'>Attack Dodged!")
        damage = damage * 0.5
        return damage
    return damage


def defense_calc(def_def, damage, block=False):
    if block:
        def_def *= 2
    if def_def > 100:
        def_def = 100
    if def_def < 100:
        damage = damage - damage * (def_def / 100)
        return damage
    damage = random.randint(0, 1)
    return damage


def character_atk(command, character):
    if command == '1':  # Normal Attack
        text = []

        """Calculates the damage from player to enemy"""
        damage = character.damage
        damage = accuracy_calc(character.accuracy, session['enemy']['speed'], damage, text)
        damage = defense_calc(session['enemy']['defense'], damage, session['enemy']['block'])

        """Checks for enemy flight and player range, does no damage if is flying and player has no ranged weapons"""
        if session['enemy']['flying']:
            if character.eqp_weapon.weapon_type != 'Ranged' or character.eqp_weapon.weapon_type != 'Magic':
                text.append(f"The {session['enemy']['name']} flew over your attack.")
                return text

        """Inflicts damage to enemy health points"""
        session['enemy']['health'] = session['enemy']['health'] - round(damage)
        text.append(f"You attacked {session['enemy']['name']} for <span class='hp-text'>{round(damage)} DMG")

    elif command == '2':  # Blocking Attack TODO FIX PLAYER BLOCKING
        text = [f"{session['enemy']['name']} blocks."]
        session['enemy']['block'] = True

    elif command == '3':  # Special Attack TODO MAKE SPECIAL ATTACK
        text = [f"You used your special."]

    else:
        text = ["character_atk error"]

    return text


def enemy_atk(character):
    session['enemy']['block'] = False

    choice = ['attack', 'block']
    if session['enemy']['flight']:
        choice.append('toggle flight')
    if session['enemy']['element']:
        choice.append('special')
    move = random.choice(choice)

    if move == 'attack':
        text = []
        damage = session['enemy']['damage']
        damage = accuracy_calc(session['enemy']['accuracy'], character.defense, damage, text)
        damage = defense_calc(character.defense, damage)
        character.health = round(character.health - damage)
        text.append(f"{session['enemy']['name']} attacked you for <span class='hp-text'>{round(damage)} DMG")

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


def battle_win(character):
    text = [f'You have defeated {session['enemy']['name']}.']
    character.gold += session['enemy']['drop_gold']
    text.append(f"You got <span class='gold-text'>{session['enemy']['gold']} GOLD")
    character.experience += session['enemy']['drop_experience']
    text.append(f"You got <span class='exp-text'>{session['enemy']['experience']} EXP")

    session['dungeon_room'] = "Cleared"
    session['enemy'] = False

    text.append("How do you proceed?")
    text.append("<span class='gray-text'>Next Room [1], Exit Dungeon [2]")
    return text


def battle_loss(character):
    text = [f"<span class='yellow-text'>You have been defeated by {session['enemy']['name']}."]
    session['enemy'] = False
    character.dungeon_level -= 1
    return text


def battle_sequence(command, character):
    text = ['']
    if command == '4':
        text = print_stats(session['enemy'])
        text.append("<span class='gray-text'>Attack [1], Block [2], Special [3]")
        text.append("<span class='gray-text'>Enemy Stats [4], Character Stats [5]")
        text.append("· · ─────────────────── · · ")
        return text

    elif command == '5':
        text = Character.display_stats(character)
        text.append("<span class='gray-text'>Attack [1], Block [2], Special [3]")
        text.append("<span class='gray-text'>Enemy Stats [4], Character Stats [5]")
        text.append("· · ─────────────────── · · ")
        return text

    if character.speed >= session['enemy']['speed']:
        text.extend(character_atk(command, character))
        if session['enemy']['health'] <= 0:
            text.extend(battle_win(character))
            return text

        text.extend(enemy_atk(character))
        if character.health <= 0:
            text.extend(battle_loss(character))
            return text

        text.append("<span class='gray-text'>Attack [1], Block [2], Special [3]")
        text.append("<span class='gray-text'>Enemy Stats [4], Character Stats [5]")
        text.append("· · ─────────────────── · · ")
        return text

    text.extend(enemy_atk(character))
    if character.health <= 0:
        text.extend(battle_loss(character))
        return text

    text.extend(character_atk(command, character))
    if session['enemy']['health'] <= 0:
        text.extend(battle_win(character))
        return text

    text.append("<span class='gray-text'>Attack [1], Block [2], Special [3]")
    text.append("<span class='gray-text'>Enemy Stats [4], Character Stats [5]")
    text.append("· · ─────────────────── · · ")
    return text
