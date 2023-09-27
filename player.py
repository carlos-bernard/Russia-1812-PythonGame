import time

import enemies
import items
import world
import random


class Player:
    def __init__(self):
        self.inventory = [items.CrustyBread(), items.BattlefieldTriageKit()]
        self.x = world.start_tile_location[0]
        self.y = world.start_tile_location[1]
        self.supply = 5
        self.victory = False
        self.army = [items.Cavalry(), items.LineTroops(), items.Skirmisher()]

    #def is_alive(self): ##
       # return self.hp > 0

    def army_gone(self):
        return self.army == []

    def print_inventory(self):
        print("Supply: {}\nInventory:".format(self.supply))
        for item in self.inventory:
            print('- ' + str(item))
        print("Army:")
        for i, unit in enumerate(self.army, 1):
            print("{}: {}(Unit Pop:{} - Damage:{} - Unit Type:{} - Level: {}".format(i, unit, unit.unit_population,
                                                                                     unit.damage, unit.unit_type,
                                                                                     unit.unit_level))
        choice = input("Select a units number for more information or enter any other key to exit:")
        try:
            unit_choice = self.army[int(choice) - 1]
            print(unit_choice.information)
        except ValueError:
            print("\n")
            print(world.tile_at(self.x, self.y).intro_text())

    def test(self):
        room = world.tile_at(self.x, self.y)
        if room.check() == 1:
            print("yes")

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        room = world.tile_at(self.x, self.y)
        world.typing_print(room.intro_text())
        if room.room_id() == "1":
            army_choice = world.typing_input("choose army 1, 2 or 3: ")
            if army_choice == "1":
                self.army = room.mixed_army()
            elif army_choice == "2":
                self.army = room.inf_army()
            elif army_choice == "3":
                self.army = room.cav_army()

    def move_east(self):
        self.move(dx=0, dy=-1)

    def move_west(self):
        self.move(dx=0, dy=1)

    def move_south(self):
        self.move(dx=1, dy=0)

    def move_north(self):
        self.move(dx=-1, dy=0)




    def heal(self):
        consumables = [item for item in self.inventory
                       if isinstance(item, items.Consumable)]
        if not consumables:
            print("You dont have any items to heal you!")
            return

        damaged_units = [unit for unit in self.army
                         if unit.unit_population < unit.unit_start_population]

        print("Choose an item to use tp heal: ")
        for i, item in enumerate(consumables, 1):
            print("{}, {}".format(i, item))

        valid = False
        while not valid:
            choice = input("")
            print("Choose unit to heal: ")
            for u, unit in enumerate(damaged_units, 1):
                print("{}, {} - {}/{} soldiers left.".format(u, unit, unit.unit_population, unit.unit_start_population))
            unit_choice = input("")
            try:
                healed_unit = damaged_units[int(unit_choice) - 1]
                to_eat = consumables[int(choice) - 1]
                healed_unit.unit_population = min(healed_unit.unit_start_population,
                                                  healed_unit.unit_population + to_eat.healing_value)
                self.inventory.remove(to_eat)
                print("{} has been healed and now contains {} healthy soldiers.".format(healed_unit,
                                                                                        healed_unit.unit_population))
                valid = True
            except (ValueError, IndexError):
                print("Invalid choice, try again")

    def trade(self):
        room = world.tile_at(self.x, self.y)
        room.check_if_trade(self)


    def level_up(self):
        veterans = [unit for unit in self.army
                    if unit.experience >= 2]
        for unit in veterans:
            print("Choose a veterancy perk for {}".format(unit.name))
            print("1: Assign additional recruits (unit population + 10)"
                  "\n2: Improved weapon skills (damage + 10)")
            if not unit.armour:
                print("3: Issue high quality armour (20% chance to avoid damage)")
            if not unit.elite_weapons:
                print("4: Issue high quality weapons (20% chance to deal double damage)")
            if not unit.surgeon:
                print("5: Assign dedicated surgeon to unit (10% of casualties returned to unit after battle)")
            perk_choice = input("Enter perk choice number:")
            try:
                if perk_choice == "1":
                    unit.unit_population = unit.unit_population + 10
                elif perk_choice == "2":
                    unit.damage = unit.damage + 10
                    print(unit.damage)
                elif perk_choice == "3" and not unit.armour:
                    unit.armour = True
                    print("armour")
                    unit.armour = True
                elif perk_choice == "4" and not unit.elite_weapons:
                    print("weapons")
                    unit.elite_weapons = True
                elif perk_choice == "5" and not unit.surgeon:
                    print("surgeon")
                    unit.surgeon = True
                else:
                    print("Invalid entry please enter a valid perk number.")
                unit.experience = 0
                unit.unit_level += 1
            except (ValueError):
                "Invalid input please select a valid number and try again."


#handles units attacking eachother and adds penalties/bonuses depending on match up of unit types
    def attack(self):
        charge_count_list = []
        enemy_charge_count_list = []
        game_over = "Your army is decimated and you have been defeated.\n Game Over"
        print("Choose unit to attack with")
        army = [unit for unit in self.army]
        for i, unit in enumerate(army, 1):
            print("{}: {}(Unit Pop:{} - Damage:{} - Unit Type:{}".format(i, unit, unit.unit_population,
                                                                         unit.damage, unit.unit_type))
        valid = False
        while not valid:
            choice = input()
            try:
                unit_choice = army[int(choice) - 1]
                room = world.tile_at(self.x, self.y)
                enemy = room.enemy
                damage = 0
                enemy_damage = 0
                charge_count_list.append(unit_choice)
                enemy_charge_count_list.append(enemy)
                unit_choice.charge_count += 1
                enemy.charge_count += 1

                if unit_choice.unit_type == "linetroop":
                    # checks if the unit is fighting a skirmisher and adjusts its damage accordingly
                    damage = enemies.skirmisher_vs_inf(enemy, unit_choice)
                    # calculates the enemies damage according to its bonus against infantry
                    enemy_damage = enemies.damage_vs_infantry(enemy)

                if unit_choice.unit_type == "cavalry":
                    damage = items.cavalry_damage(unit_choice, enemy)
                    enemy_damage = enemies.damage_vs_cav(enemy)

                if unit_choice.unit_type == "lancer":
                    damage = items.lancer_damage(unit_choice, enemy)
                    enemy_damage = enemies.damage_vs_lancer(enemy)


# units with the type of skrimish only take return damage on every second attack/ uness fighting cav
                if unit_choice.unit_type == "skirmish":
                    if (unit_choice.charge_count % 2) != 0:
                        damage = enemies.skirmisher_vs_inf(enemy, unit_choice)
                        enemy_damage = 0
                        unit_choice.attack_style = "spread out and from a safe range take sniping shots"
                    else:
                        damage = enemies.skirmisher_vs_inf(enemy, unit_choice)
                        enemy_damage = enemies.damage_vs_infantry(enemy)
                        unit_choice.attack_style = "begin to fall back as the enemy closes the distance yet continue to fire"

                if unit_choice.unit_type == "grenadier":
                    damage = items.grenadier_damage(unit_choice, enemy)
                    enemy_damage = enemies.damage_vs_infantry(enemy)



                #checks if unit has armour trait then gives it a 20% chance to avoid damage from attack.
                if unit_choice.armour:
                    if random.random() < 0.20:
                        enemy_damage = 0
                        unit_choice.attack_style = "skilfully dodging incoming attacks" + unit_choice.attack_style
                #checks for elite weapons trait then gives a 20% chance to double attack damage
                if unit_choice.elite_weapons:
                    if random.random() < 0.90:
                        damage = damage + damage

                unit_choice.unit_population -= enemy_damage
                enemy.hp -= damage
                unit_choice.experience += 1

                if unit_choice.unit_population <= 0:
                    self.army.remove(unit_choice)
                    if not self.army:
                        world.typing_print("\nYour army is decimated and you have been defeated.\n")
                        time.sleep(0.7)
                        world.typing_print("Game Over")
                        return

                print("Your {} {} against the {}, dealing {} damage and taking {} casualties".
                      format(unit_choice.name, unit_choice.attack_style, enemy.name, damage, enemy_damage))


                # Wipes counts back to zero so units special abilities should behave properly in next fight
                # Provides correct information regarding the status of units and enemies.
                if not enemy.is_alive():
                    for i in charge_count_list:
                        i.charge_count = 0
                    for i in enemy_charge_count_list:
                        i.charge_count = 0
                    if unit_choice.unit_population <= 0:
                        print("You killed {} but your {} were destroyed".format(enemy.name, unit_choice.name))
                        world.typing_print(room.story_tile_end_text())
                    else:
                        print("You killed {}. {} {}'s survived the engagement unharmed".
                              format(enemy.name, unit_choice.unit_population, unit_choice.name))
                        world.typing_print(room.story_tile_end_text())

                    valid = True
                    # regenerates units with the surgeon trait after battle
                    for unit in self.army:
                        if unit.surgeon:
                            regen_amount = (10 * unit.unit_population) / 100
                            regen_amount = int(regen_amount)
                            unit.unit_population = min(unit.unit_start_population,unit.unit_population + regen_amount)
                else:
                    if unit_choice.unit_population <= 0:
                        print("{} has {} HP left.".format(enemy.name, enemy.hp))
                        print("{} has destroyed your {}".format(enemy.name, unit_choice.name))
                    else:
                        print("{} has {} HP left.".format(enemy.name, enemy.hp))
                        print("The {}'s attacks leave your {} with {} soldiers left".
                              format(enemy.name, unit_choice.name, unit_choice.unit_population))

            except (ValueError, IndexError):
                print("Your unit choice has been defeated, or your choice is invalid.\n"
                      "Select number from unit list.")
