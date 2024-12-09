import random
from blessed import Terminal

# Initialize the terminal
term = Terminal()

# Character and enemy classes
class Character:
    def __init__(self, name, level, health, attack, defense, xp=0):
        self.name = name
        self.level = level
        self.health = health
        self.attack = attack
        self.defense = defense
        self.xp = xp
        self.inventory = []
        self.equipped_armor = None

    def attack_target(self, target):
        # Calculate damage dealt to the target
        damage = self.attack - target.defense
        damage = max(damage, 0)  # Prevent negative damage
        target.health -= damage
        return damage

    def is_alive(self):
        return self.health > 0

    def add_item(self, item):
        if len(self.inventory) < 5:  # Inventory capacity of 5
            self.inventory.append(item)
        else:
            print("Inventory full. Cannot add more items.")

# Enemy class inherits from Character
class Enemy(Character):
    def __init__(self, name, health, attack, defense):
        super().__init__(name, level=1, health=health, attack=attack, defense=defense)

# Item class for loot
class Item:
    def __init__(self, name, effect):
        self.name = name
        self.effect = effect

# Generate random loot
def generate_loot():
    loot_types = [
        Item("Health Potion", "Restores 50 health."),
        Item("Mana Potion", "Restores 30 mana."),
        Item("Iron Armor", "Increases defense by 5."),
        Item("Silver Sword", "Increases attack by 5.")
    ]
    return random.choice(loot_types)

# Chance encounter for trap
def trigger_trap():
    traps = ["You fall into quicksand! You take 20 damage.", "A bear trap snaps shut on your leg! You take 10 damage."]
    return random.choice(traps)

# ASCII art for character classes and enemies
warrior_art = """
     O
    /|\\
    / \\
"""

mage_art = """
    /\\
   /__\\
    || 
"""

archer_art = """
    /\\
   /__\\
  /\\ || /\\
"""

goblin_art = """
   ,      ,
  /(.-""-.)\\
 |/       \\|
 ||       ||
"""

# Display character ASCII art based on class
def display_character_art(character_class):
    if character_class == "warrior":
        print(term.move_xy(0, 10) + warrior_art)
    elif character_class == "mage":
        print(term.move_xy(0, 10) + mage_art)
    elif character_class == "archer":
        print(term.move_xy(0, 10) + archer_art)

# Function to create a character
def create_character():
    name = input("Enter your character's name: ")
    class_choice = input("Choose your class (Warrior, Mage, Archer): ").lower()
    
    if class_choice == "warrior":
        print(term.clear())
        display_character_art("warrior")
        return Character(name, 1, 100, 15, 5)
    elif class_choice == "mage":
        print(term.clear())
        display_character_art("mage")
        return Character(name, 1, 80, 12, 3)
    elif class_choice == "archer":
        print(term.clear())
        display_character_art("archer")
        return Character(name, 1, 90, 10, 4)
    else:
        print("Invalid class choice. Defaulting to Warrior.")
        display_character_art("warrior")
        return Character(name, 1, 100, 15, 5)

# Random enemy generator
def random_enemy():
    enemy_type = random.choice(["Goblin", "Orc", "Skeleton", "Troll"])
    if enemy_type == "Goblin":
        print(term.move_xy(0, 12) + goblin_art)
        return Enemy("Goblin", 50, 10, 2)
    elif enemy_type == "Orc":
        return Enemy("Orc", 80, 15, 5)
    elif enemy_type == "Skeleton":
        return Enemy("Skeleton", 60, 12, 3)
    else:
        return Enemy("Troll", 100, 20, 8)

# Chance encounter logic
def chance_encounter():
    return random.random() < 0.7  # 70% chance of encountering an enemy

# Main game loop with chance encounters and combat
def main():
    # Create a character
    player = create_character()

    while True:
        print(term.clear())
        print(term.move_xy(0, 0) + "1. Wander (Chance of encounter)")
        print(term.move_xy(0, 1) + "2. Rest and recover health")
        print(term.move_xy(0, 2) + "3. View character stats")
        print(term.move_xy(0, 3) + "4. Exit game")

        action = input(term.move_xy(0, 5) + "Choose an action: ")

        if action == '1':
            encounter_result = random.choice(['enemy', 'loot', 'trap', 'nothing'])

            if encounter_result == 'enemy':
                if chance_encounter():
                    enemy = random_enemy()
                    print(term.move_xy(0, 6) + f"A wild {enemy.name} appears!")
                    input(term.move_xy(0, 7) + "Press Enter to continue to combat...")
                    combat(player, enemy)
                else:
                    print(term.move_xy(0, 6) + "You wander for a while but encounter nothing.")
                    input(term.move_xy(0, 7) + "Press Enter to continue...")

            elif encounter_result == 'loot':
                loot_item = generate_loot()
                print(term.move_xy(0, 6) + f"You found a {loot_item.name}!")
                player.add_item(loot_item)
                input(term.move_xy(0, 7) + "Press Enter to continue...")

            elif encounter_result == 'trap':
                trap_result = trigger_trap()
                print(term.move_xy(0, 6) + trap_result)
                input(term.move_xy(0, 7) + "Press Enter to continue...")

        elif action == '2':
            player.health = 100
            print(term.move_xy(0, 6) + f"{player.name} rests and recovers health.")
            input(term.move_xy(0, 7) + "Press Enter to continue...")

        elif action == '3':
            print(term.move_xy(0, 6) + f"Level: {player.level}")
            print(term.move_xy(0, 7) + f"Health: {player.health}")
            print(term.move_xy(0, 8) + f"Attack: {player.attack}")
            print(term.move_xy(0, 9) + f"Defense: {player.defense}")
            print(term.move_xy(0, 10) + f"XP: {player.xp}")
            print(term.move_xy(0, 11) + f"Inventory: {', '.join([item.name for item in player.inventory])}")
            if player.equipped_armor:
                print(term.move_xy(0, 12) + f"Equipped Armor: {player.equipped_armor.name}")
            input(term.move_xy(0, 13) + "Press Enter to continue...")

        elif action == '4':
            print(term.move_xy(0, 6) + "Exiting game. Goodbye!")
            break
        else:
            print(term.move_xy(0, 6) + "Invalid choice. Please try again.")
            input(term.move_xy(0, 7) + "Press Enter to continue...")

# Combat function with player and enemy
def combat(player, enemy):
    print(term.clear())
    print(term.move_xy(0, 0) + "Battle Start!")
    print(term.move_xy(0, 2) + f"{player.name} (Player) vs. {enemy.name} (Enemy)")

    while player.is_alive() and enemy.is_alive():
        damage = player.attack_target(enemy)
        if damage == 0:
            print(term.move_xy(0, 4) + f"{player.name} missed the attack!")
        else:
            print(term.move_xy(0, 4) + f"{player.name} dealt {damage} damage to {enemy.name}.")

        if not enemy.is_alive():
            print(term.move_xy(0, 5) + f"{player.name} has defeated {enemy.name}!")
            break

        damage = enemy.attack_target(player)
        if damage == 0:
            print(term.move_xy(0, 6) + f"{enemy.name} missed the attack!")
        else:
            print(term.move_xy(0, 6) + f"{enemy.name} dealt {damage} damage to {player.name}.")

        input(term.move_xy(0, 7) + "Press Enter to continue to the next turn...")

    if player.is_alive():
        print(term.move_xy(0, 8) + f"{player.name} wins the battle!")
    else:
        print(term.move_xy(0, 8) + f"{enemy.name} wins the battle!")
    input(term.move_xy(0, 9) + "Press Enter to continue...")

# Start the game
if __name__ == "__main__":
    main()
