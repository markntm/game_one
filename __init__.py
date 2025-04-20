from flask_sqlalchemy import SQLAlchemy
from game.models.npc import NPC
from game.models.shops import GuideShop, ArmoryShop, ConsumableShop, Inn

db = SQLAlchemy()

guide_npc = NPC("Eloria the Wise", "Ask me anything about this land...", chat_enabled=True)
armory_npc = NPC("Grenda", "Steel to keep you alive.")
consumable_npc = NPC("Fizz", "Potions for all your needs!")
inn_npc = NPC("Mara", "A warm place to rest.")

guide_shop = GuideShop(guide_npc)
armory_shop = ArmoryShop(armory_npc)
consumable_shop = ConsumableShop(consumable_npc)
inn_shop = Inn(inn_npc)

# Keep them in a dictionary for access
village_shops = {
    "guide": guide_shop,
    "armory": armory_shop,
    "consumable": consumable_shop,
    "inn": inn_shop
}
