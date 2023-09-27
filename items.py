

class NonPlayableCharacter():
    def __init__(self):
        raise NotImplementedError("Do not create raw NPC objects.")

    def __str__(self):
        self.name


class Trader(NonPlayableCharacter):
    def __init__(self):
        self.name = "Requisition Officer"
        self.supply = 100
        self.inventory = [Skirmisher(),
                          LineTroops(),
                          CrustyBread(),
                          BattlefieldTriageKit(),
                          BattlefieldTriageKit()]


class Unit:
    def __init__(self):
        self.experience = 0
        self.charge_count = 0
        self.unit_level = 0
        self.armour = False
        self.elite_weapons = False
        self.surgeon = False

#neccesarry so a string is returned instead of jibberish code when the class is called as a string. chooses which self. to return for the subclass
    def __str__(self):
        return self.name



class Cannon(Unit):
    def __init__(self):
        self.name = "randomized chance to hit but big damage. abandoned after the retreat. "


class Cavalry(Unit):
    def __init__(self):
        self.name = "Cuirassiers"
        self.unit_type = "cavalry"
        self.damage = 25
        self.unit_start_population = 65
        self.unit_population = 65
        self.value = 25
        self.attack_style = "charge with sabres held high"
        self.information = """Heavy cavalry resembling descendants of medieval knights. Despite being armed with a long
        straight sabre as well as a pistol or carbine, it is common for Cuirassiers to leave the fire arm or its ammo behind"""
        super().__init__()


class Carabiniers(Unit):
    def __init__(self):
        self.name = "Carabiniers-à-Cheval"
        self.unit_type = "cavalry"
        self.damage = 30
        self.unit_start_population = 75
        self.unit_population = 75
        self.value = 25
        self.attack_style = "fire off carbines and close to sabre range"
        self.information = """Elite horse troops armed with sabres and carbines made up of the strongest and tallest
         veterans from other regiments"""
        super().__init__()


class Lancers(Unit):
    def __init__(self):
        self.name = "Lighthorse-Lancers"
        self.unit_type = "lancer"
        self.damage = 35
        self.unit_start_population = 50
        self.unit_population = 50
        self.value = 25
        self.attack_style = "lower lances and charge"
        self.lance_charge_count = 0
        self.information = """stats and strengths and weaknesses\nLight horse armed with long lances for maximum damage
         on the charge. Polish lancers were considered the finest in europe and their men and tactics were adopted by
         both France and Russia"""
        super().__init__()


class Hussars(Unit):
    def __init__(self):
        self.name = "Lancer"
        self.unit_type = "Lighthorse-Lancers"
        self.damage = 45
        self.unit_start_population = 50
        self.unit_population = 50
        self.value = 25
        self.attack_style = "lower lances and charge"
        self.lance_charge_count = 0
        self.information = """stats and strengths and weaknesses\nLight horse known for their reckless courage in battle
        and an arrogance and military pride so fierce it often led them into duels and conflict with their allies."""
        super().__init__()


class Skirmisher(Unit):
    def __init__(self):
        self.name = "Skirmisher"
        self.unit_type = "skirmish"
        self.damage = 10
        self.unit_start_population = 40
        self.unit_population = 40
        self.value = 25
        self.attack_style = "spread out and begin to take sniping shots"
        self.value = 1
        self.information = "stats and strengths and weaknesses\nSkirmishers fight far differently than traditional" \
                           "infantry squares. using cover and concealment, advancing to fire and falling back as the" \
                           "situation calls for as opposed to acting as one unified block like the line infantry."
        super().__init__()


class Voltigeurs(Unit):
    def __init__(self):
        self.name = "Voltigeurs"
        self.unit_type = "skirmish"
        self.damage = 15
        self.unit_start_population = 50
        self.unit_population = 50
        self.value = 25
        self.attack_style = "spread out and begin to take sniping shots"
        self.value = 1
        self.information = "stats and strengths and weaknesses\n Shorter, more agile men trained to fight more" \
                           "independent than the average line troops. Often taken from highland regions due to a " \
                           "perceived advantage in fitness."
        super().__init__()

class LineTroops(Unit):
    def __init__(self):
        self.name = "Line Troops"
        self.unit_type = "linetroop"
        self.damage = 15
        self.unit_start_population = 100
        self.unit_population = 100
        self.value = 25
        self.attack_style = "form ranks and open fire"
        self.value = 10
        self.information = "stats and strengths and weaknesses\nThe most numerous and important element in the army."
        super().__init__()


class YoungGuard(Unit):
    def __init__(self):
        self.name = "Young Guard"
        self.unit_type = "linetroop"
        self.damage = 15
        self.unit_start_population = 150
        self.unit_population = 150
        self.value = 25
        self.attack_style = "form ranks and open fire"
        self.value = 10
        self.information = "stats and strengths and weaknesses\nConscripts chosen from the ranks for their good education" \
                           "or physical prowess and admitted into Napoleans personal guard. The young guard make up the" \
                           "bulk of this force and are afforded better pay and greater prestige than the average recruit."
        super().__init__()


class Grenadiers(Unit):
    def __init__(self):
        self.name = "grenadiers"
        self.unit_type = "grenadier"
        self.damage = 17
        self.unit_start_population = 90
        self.unit_population = 90
        self.value = 25
        self.attack_style = "fire rifles and lob grenades"
        self.information = "stats and strengths and weaknesses\nElite troops made up of the largest men, expected to " \
                           "present a fearsome sight. In some cases Grenadiers were even forbidden from laughing to add to" \
                           "this effect."
        super().__init__()


class OldGuard(Unit):
    def __init__(self):
        self.name = "Old Guard"
        self.unit_type = "grenadier"
        self.damage = 22
        self.value = 25
        self.unit_start_population = 110
        self.unit_population = 110
        self.attack_style = "fire rifles and lob grenades"
        self.information = "stats and strengths and weaknesses\nNapoleans Guard under his direct command. Both a" \
                           "fighting force as well as a personal guard for the emperor. The old guard is made up of the" \
                           "loyal men who have been with Napolean the longest, Veterans of scores of victories and " \
                           "diverse battlefields from Egypt to Prussia."
        super().__init__()


def cavalry_damage(unit_choice, enemy):
    if enemy.unit_type == "grenadier" or enemy.unit_type == "infantry" or enemy.unit_type == "skirmish":
        if unit_choice.charge_count == 1:
            percent = (125 * unit_choice.damage) / 100.0
            percent = int(percent)
            damage = percent
            return damage

        if unit_choice.charge_count >= 2:
            damage = unit_choice.damage
            return damage
    if enemy.unit_type == "spear":
        if unit_choice.charge_count == 1:
            percent = (70 * unit_choice.damage) / 100.0
            percent = int(percent)
            damage = percent
            return damage

        if unit_choice.charge_count >= 2:
            percent = (50 * unit_choice.damage) / 100.0
            percent = int(percent)
            damage = percent
            return damage
    else:
        if unit_choice.charge_count == 1:
            percent = (110 * unit_choice.damage) / 100.0
            percent = int(percent)
            damage = percent
            return damage

        if unit_choice.charge_count >= 2:
            damage = unit_choice.damage
            return damage


def grenadier_damage(unit_choice, enemy):
    if enemy.unit_type == "grenadier" or enemy.unit_type == "infantry":
        percent = (125 * unit_choice.damage) / 100.0
        percent = int(percent)
        damage = percent
        return damage
    if enemy.unit_type == "skirmish":
        if (enemy.charge_count % 2) != 0:
            damage = 0
            return damage
        else:
            percent = (125 * unit_choice.damage) / 100.0
            percent = int(percent)
            damage = percent
            return damage
    else:
        damage = unit_choice.damage
        return damage


def lancer_damage(unit_choice, enemy):
    if enemy.unit_type == "lancer":
        if unit_choice.charge_count == 1:
            percent = (115 * unit_choice.damage) / 100.0
            percent = int(percent)
            damage = percent
            return damage

        if unit_choice.charge_count >= 2:
            damage = unit_choice.damage
            return damage
    if enemy.unit_type == "spear":
        if unit_choice.charge_count == 1:
            percent = (60 * unit_choice.damage) / 100.0
            percent = int(percent)
            damage = percent
            return damage

        if unit_choice.charge_count >= 2:
            percent = (50 * unit_choice.damage) / 100.0
            percent = int(percent)
            damage = percent
            return damage
    if enemy.unit_type == "cavalry":
        if unit_choice.charge_count == 1:
            percent = (125 * unit_choice.damage) / 100.0
            percent = int(percent)
            damage = percent
            return damage

        if unit_choice.charge_count >= 2:
            damage = unit_choice.damage
            return damage

    else:
        if unit_choice.charge_count == 1:
            percent = (140 * unit_choice.damage) / 100.0
            percent = int(percent)
            damage = percent
            return damage

        if unit_choice.charge_count >= 2:
            damage = unit_choice.damage
            return damage

class Consumable:
    def __init__(self):
        raise NotImplementedError("Do not create raw Consumable objects outside of subclass")

    def __str__(self):
        return "{} (+{} HP)".format(self.name, self.healing_value)


class CrustyBread(Consumable):
    def __init__(self):
        self.name = "Crusty Bread"
        self.healing_value = 10
        self.value = 12

    def __str__(self):
        return self.name
        return str(self.healing_value)


class BattlefieldTriageKit(Consumable):
    def __init__(self):
        self.name = "Battlefield Triage Kit"
        self.healing_value = 45
        self.value = 25


