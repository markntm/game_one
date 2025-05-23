from flask import session
from shop_manager import village_shops


def rooms_main(command, character):
    if session['init'] and session['village'] == 'village':
        return ['Which shop would you like to visit?',
                '<span class="gray-text">Armory [1], Consumable [2], Guide [3], Inn [4], Back [5]']

    if not session['init'] and session['village'] == 'village':
        if command == '1':
            session['init'] = True
            session['village'] = 'armory'
            return ['You enter the Armory.']
        elif command == '2':
            session['init'] = True
            session['village'] = 'consumable'
            return ['You enter the Consumable Shop.']
        elif command == '3':
            session['init'] = True
            session['village'] = 'guide'
            return ['You enter the Guide Shop.']
        elif command == '4':
            session['init'] = True
            session['village'] = 'inn'
            return ['You enter the Inn.']
        elif command == '5':
            session['init'] = True
            session['village'] = 'village'
            session['location'] = 'outside'
            return ['You exit the village.']

    if session['village'] == 'armory':
        session['init'] = not session['init']
        return village_shops['armory'].run(character, command, not session['init'])

    elif session['village'] == 'consumable':
        session['init'] = not session['init']
        return village_shops['consumable'].run(character, command, not session['init'])

    elif session['village'] == 'guide':
        session['init'] = not session['init']
        return village_shops['guide'].run(character, command, not session['init'])

    elif session['village'] == 'inn':
        session['init'] = not session['init']
        return village_shops['inn'].run(character, command, not session['init'])

    else:
        return ['rooms error']
