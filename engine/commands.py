from models import db
import random
from flask import Flask, render_template, request, redirect, url_for, session
from models.character import Character, select_character
from models.enemy import Enemy
from models.items import Item, Weapon, Shield, Armor, Accessory, Consumable, Scroll
from models.skill_enchantment import Skill, Enchantment, WeaponEnchantment, ShieldEnchantment, all_enchantments
from engine.combat import battle_sequence


def init_sessions(character_id):
    if 'messages' not in session:
        session['messages'] = []
    if 'action' not in session:
        session['action'] = 'default'
    if 'location' not in session:
        session['location'] = 'outside'
    if 'init' not in session:
        session['init'] = True
    if 'dungeon room' not in session:
        session['dungeon room'] = 'Enemy Room'


def outside(command, character):
    if session['init']:
        text = ['Where would you like to go?',
                "<span class='gray-text'>Dungeon [1], Shop [2], Inn [3]"]
        session['init'] = False
        return text

    if command == '1':
        session['location'] = 'dungeon'
        session['init'] = True
        text = ["──◇◆◇────◇◆◇────◇◆◇────◇◆◇──",
                '  You entered the Dungeon',
                "──◇◆◇────◇◆◇────◇◆◇────◇◆◇──"]
        text.extend(dungeon(command, character))

    elif command == '2':
        session['location'] = 'shop'
        session['init'] = True
        text = ["──◇◆◇────◇◆◇────◇◆◇────◇◆◇──",
                '    You entered the Shop',
                "──◇◆◇────◇◆◇────◇◆◇────◇◆◇──"]

    elif command == '3':
        session['location'] = 'inn'
        session['init'] = True
        text = ["──◇◆◇────◇◆◇────◇◆◇────◇◆◇──",
                '    You entered the Inn',
                "──◇◆◇────◇◆◇────◇◆◇────◇◆◇──"]
        text.extend(inn(command, character))

    else:
        text = ['Error outside']

    return text


def shop(command):
    pass


# find way to figure out when character is tired or not
def inn(command, character):
    if session['init']:
        text = ['Where would you like to sleep?', '1. Normal Bed', '2. Comfy Bed', '3. Back']
        session['init'] = False
        return text

    if command == '1':
        if character.gold < 10:
            session['init'] = True
            text = [f'Not enough gold, you need {10 - character.gold} more gold.']
            text.extend(inn(command, character))
            return text
        character.gold -= 10
        character.health += 5
        if character.health >= character.mhealth:
            character.health = character.mhealth
        session['init'] = True
        text = ['Slept in Normal Bed, Healed for 5 health.']
        session['location'] = 'outside'
        text.extend(outside(command, character))

    elif command == '2':
        if character.gold < 50:
            session['init'] = True
            text = [f'Not enough gold, you need {50 - character.gold} more gold.']
            text.extend(inn(command, character))
            return text
        character.gold -= 50
        character.health += 10
        if character.health >= character.mhealth:
            character.health = character.mhealth
        session['init'] = True
        text = ['Slept in Comfy Bed, Healed for 10 health.']
        session['location'] = 'outside'
        text.extend(outside(command, character))

    elif command == '3':
        session['location'] = 'outside'
        session['init'] = True
        text = ['Exited the inn.']
        text.extend(outside(command, character))

    else:
        text = ['Error inn']

    # db.session.commit()
    return text


def generate_enemy(character):
    all_enemies = Enemy.query.all()
    enemy = random.choice(all_enemies)
    return enemy.generate_stats(character.level)


def generate_dungeon(character):
    if character.dungeon_level % 10 == 0:
        room = "Boss Room"
    else:
        rooms = ["Enemy Room", "Empty Room", "Merchant Room", "Chest Room"]
        room = random.choices(rooms, weights=[0.40, 0.30, 0.20, 0.10], k=1)
    room = "Enemy Room"
    session['dungeon_room'] = room

    if room == "Enemy Room":
        session['enemy'] = generate_enemy(character)
        text = ["· · ─────────────────── ··『 ⚔ 』·· ─────────────────── · ·",
                f"<span class='yellow-text'>You encountered a {session['enemy']['name']}.",
                "<span class='gray-text'>Attack [1], Block [2], Special [3]",
                "<span class='gray-text'>Enemy Stats [4], Character Stats [5]",
                "· · ─────────────────── ··『 ⚔ 』·· ─────────────────── · ·"]

    elif room == "Empty Room":
        text = ["⌬══════════════════════⌬",
                f"<span class='yellow-text'>You entered an Empty Room, there is nothing here.",
                "⌬══════════════════════⌬"]

    elif room == "Merchant Room":
        text = ["⌬══════════════════════⌬",
                f"<span class='yellow-text'>You entered a Merchant Room, you can sell equipment or buy his trade.",
                "⌬══════════════════════⌬"]

    elif room == "Chest Room":
        text = ["⌬══════════════════════⌬",
                f"<span class='yellow-text'>You encountered a chest! Open to see what it holds.",
                "⌬══════════════════════⌬"]

    elif room == "Boss Room":
        text = ["· · ─────────────────── ··『 ⚔ 』·· ─────────────────── · ·",
                f"<span class='yellow-text'>You entered a Boss Room.",
                "· · ─────────────────── ··『 ⚔ 』·· ─────────────────── · ·"]

    else:
        text = ["generate dungeon error"]

    return text


def dungeon(command, character):
    if session['init']:
        text = [f'Dungeon floor: {character.dungeon_level}.']
        text.extend(generate_dungeon(character))
        session['init'] = False
        return text
    if session['dungeon_room'] == "Enemy Room":
        if session['enemy']:
            text = []
            text.extend(battle_sequence(command, character))
            return text
        return ['Enemy Error']
    return ['']


def process_command(command, character):
    text = ['---', 'Input: ' + str(command)]
    init_sessions(character.id)

    if session['location'] == 'outside':
        text.extend(outside(command, character))

    elif session['location'] == 'dungeon':
        text.extend(dungeon(command, character))

    elif session['location'] == 'shop':
        text.extend(shop(command))

    elif session['location'] == 'inn':
        text.extend(inn(command, character))

    if character.health <= 0:
        session['location'] = 'outside'
        session['init'] = True
        # text.append['You wake up in the fields.']
        text.extend(outside(command, character))

    return text
