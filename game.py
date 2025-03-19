from flask import Flask, render_template, request, redirect, url_for, session
from models import db
from engine.commands import process_command, init_sessions
from models.character import Character, select_character
from models.items import Item, Weapon, Shield, Armor, Accessory, Consumable, Scroll
from models.skill_enchantment import Skill, Enchantment, WeaponEnchantment, ShieldEnchantment, all_enchantments


app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game.db'
db.init_app(app)



@app.route('/')
@app.route('/start_screen', methods=['GET', 'POST'])
def start_screen():
    """Holds the start menu; listing pre-made characters, stats for pre-made characters,
    and option to create new character."""
    session['messages'] = {}
    session['character_id'] = None
    characters = Character.query.all()
    return render_template('start_screen.html', characters=characters)


# Route to handle character creation
@app.route('/create_character', methods=['POST'])
def create_character():
    # Get form data from the HTML form
    name = request.form.get('name')
    char_class = request.form.get('class')

    if name and char_class:
        new_character = select_character(name, char_class)
        db.session.add(new_character)
        db.session.commit()

        character_id = Character.query.filter_by(name=name).first().id
        init_sessions(character_id)

        print(f'Character Created: {name}, Class: {char_class}')

    return redirect(url_for('start_screen'))


@app.route('/game/<int:character_id>', methods=['GET'])
def continue_game(character_id):
    # Load the character from the database
    character = db.session.get(Character, character_id)
    session['character_id'] = character.id
    messages = ['Enter: Continue']
    session['init'] = True

    if character:
        return render_template('main.html', character=character, messages=messages)
    else:
        return redirect(url_for('start_screen'))


@app.route('/delete_character/<int:character_id>', methods=['POST'])
def delete_character(character_id):
    character = db.session.get(Character, character_id)

    if character:
        db.session.delete(character)
        db.session.commit()
        return redirect(url_for('start_screen'))
    else:
        return 'Character not found', 404


@app.route('/main', methods=['POST'])
def main():
    """renders the actual game allowing for back and forth feedback"""
    character_id = session['character_id']
    if not character_id:
        return redirect(url_for('start_screen'))
    character = Character.query.get(character_id)
    user_input = request.form['command'].lower()

    if 'messages' not in session or not isinstance(session['messages'], list):
        session['messages'] = []  # Initialize as an empty list

    if user_input == 'clear':
        session['messages'] = []

    output = process_command(user_input, character)
    session['messages'].extend(output)
    session.modified = True
    db.session.commit()

    return render_template('main.html', character=character, messages=session['messages'])


@app.route('/inventory/<int:character_id>', methods=['GET', 'POST'])
def inventory():
    """User can access inventory from /main, holds character stats and info and allows the
    equipping or un-equipping of items."""
    character_id = session.get('character_id')
    if not character_id:
        return redirect(url_for('start_screen'))

    character = Character.query.get(character_id)
    if request.method == 'POST':
        item = request.form.get('item')
        action = request.form.get('action')
        if action == 'add':
            character.add_item(item)
        elif action == 'remove':
            character.remove_item(item)
        db.session.commit()

    return render_template('inventory.html', character=character)


def debugging():
    character_id = 1
    character = db.session.get(Character, character_id)
    session['character_id'] = character.id

    while True:
        user_input = input("Input: ").lower()

        if 'messages' not in session:
            session['messages'] = []

        if user_input == 'clear':
            session['messages'] = []

        output = process_command(user_input, character)
        session['messages'].extend(output)
        session.modified = True
        print(session['messages'])


@app.route('/clear_session', methods=['GET'])
def clear_session():
    session.clear()
    return "Session cleared successfully", 200


def test():
    print("Running test mode...")
    with app.app_context():
        all_enchantments()
    return


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    testing = input("Mode: ")
    if testing == 'test':
        test()
    else:
        app.run(debug=True)





