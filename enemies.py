class Enemy:
    def __init__(self):
        raise NotImplementedError("Do not create raw enemy objects")

    def __str__(self):
        return self.name


    def is_alive(self):
        return self.hp > 0


class LineTroops(Enemy):
    def __init__(self):
        self.name = "Musketeir"
        self.unit_type = "linetroop"
        self.damage = 15
        self.hp = 100
        self.charge_count = 0


class Bandits(Enemy):
    def __init__(self):
        self.name = "Bandits"
        self.unit_type = "infantry"
        self.damage = 10
        self.hp = 40
        self.charge_count = 0


class LithuaniaLifeGuard(Enemy):
    def __init__(self):
        self.name = "Lithuania Life Guard Infantry"
        self.unit_type = "linetroop"
        self.damage = 15
        self.hp = 150
        self.charge_count = 0


class Cavalry(Enemy):
    def __init__(self):
        self.name = "Russian Dragoons"
        self.unit_type = "cavalry"
        self.damage = 25
        self.hp = 65
        self.charge_count = 0


class Uhlans(Enemy):
    def __init__(self):
        self.name = "Uhlan Cavalry"
        self.unit_type = "cavalry"
        self.damage = 30
        self.hp = 75
        self.charge_count = 0


class Cossacks(Enemy):
    def __init__(self):
        self.name = "Cossacks"
        self.unit_type = "lancer"
        self.damage = 35
        self.hp = 50
        self.charge_count = 0


class CossackLifeGuard(Enemy):
    def __init__(self):
        self.name = "Cossack Life Guards"
        self.unit_type = "lancer"
        self.damage = 45
        self.hp = 60
        self.charge_count = 0


class Skirmisher(Enemy):
    def __init__(self):
        self.name = "Skirmisher"
        self.unit_type = "skirmish"
        self.damage = 10
        self.hp = 40
        self.charge_count = 0

class Jägers(Enemy):
    def __init__(self):
        self.name = "Jäger Skirmisher"
        self.unit_type = "skirmish"
        self.damage = 15
        self.hp = 50
        self.charge_count = 0



class Grenadiers(Enemy):
    def __init__(self):
        self.name = "Grenadiers"
        self.unit_type = "grenadier"
        self.damage = 17
        self.hp = 90
        self.charge_count = 0


class PavlovskGrenadiers(Enemy):
    def __init__(self):
        self.name = "Pavlovsk Elite Grenadiers"
        self.unit_type = "grenadier"
        self.damage = 22
        self.hp = 110
        self.charge_count = 0

class NoEnemy(Enemy):
    def __init__(self):
        self.name = None
        self.hp = 0
        self.damage = 0
        self.unit_type = None
        self.charge_count = 0


class GiantSpider(Enemy):
    def __init__(self):
        self.name = "Giant Spider"
        self.hp = 1
        self.damage = 1
        self.unit_type = "spear"
        self.charge_count = 0


class BatColony(Enemy):
    def __init__(self):
        self.name = "Colony of bats"
        self.hp = 100
        self.damage = 4
        self.unit_type = "not yet decided"
        self.charge_count = 0

class Ogre(Enemy):
    def __init__(self):
        self.name = "Ogre"
        self.hp = 100
        self.damage = 10
        self.unit_type = "infantry"
        self.charge_count = 0


class RockMonster(Enemy):
    def __init__(self):
        self.name = "Rock Monster"
        self.hp = 80
        self.damage = 15
        self.unit_type = "not yet decided"
        self.charge_count = 0


def skirmisher_vs_inf(enemy, unit):
    if enemy.unit_type == "skirmish":
        if (enemy.charge_count % 2) != 0:
            player_damage = 0
            return player_damage
        else:
            player_damage = unit.damage
            return player_damage
    else:
        player_damage = unit.damage
        return player_damage


def damage_vs_cav(enemy):
    if enemy.unit_type == "lancer":
        if enemy.charge_count == 1:
            percent = (140 * enemy.damage) / 100.0
            percent = int(percent)
            enemy_damage = percent
            return enemy_damage

        if enemy.charge_count >= 2:
            enemy_damage = enemy.damage
            return enemy_damage

    if enemy.unit_type == "spear":
        if enemy.charge_count == 1:
            enemy_percent = (35 * enemy.damage) / 100.0
            enemy_percent = int(enemy_percent)
            enemy_damage = enemy.damage + enemy_percent
            return enemy_damage

        if enemy.charge_count >= 2:
            enemy_percent = (25 * enemy.damage) / 100.0
            enemy_percent = int(enemy_percent)
            enemy_damage = enemy.damage + enemy_percent
            return enemy_damage
    else:
        enemy_damage = enemy.damage
        return enemy_damage


# calcuates what damage enemy should do against player units with the infantry unit type.
def damage_vs_infantry(enemy):
    if enemy.unit_type == "cavalry":
        if enemy.charge_count == 1:
            percent = (120 * enemy.damage) / 100.0
            percent = int(percent)
            enemy_damage = percent
            return enemy_damage

        if enemy.charge_count >= 2:
            enemy_damage = enemy.damage
            return enemy_damage

    if enemy.unit_type == "lancer":
        if enemy.charge_count == 1:
            percent = (140 * enemy.damage) / 100.0
            percent = int(percent)
            enemy_damage = percent
            return enemy_damage

        if enemy.charge_count >= 2:
            enemy_damage = enemy.damage
            return enemy_damage

    if enemy.unit_type == "grenadier":
        percent = (125 * enemy.damage) / 100.0
        percent = int(percent)
        enemy_damage = percent
        return enemy_damage
    else:
        enemy_damage = enemy.damage
        return enemy_damage

def damage_vs_lancer(enemy):
    if enemy.unit_type == "spear":
        if enemy.charge_count == 1:
            enemy_percent = (70 * enemy.damage) / 100.0
            enemy_percent = int(enemy_percent)
            enemy_damage = enemy.damage + enemy_percent
            return enemy_damage

        if enemy.charge_count >= 2:
            enemy_percent = (40 * enemy.damage) / 100.0
            enemy_percent = int(enemy_percent)
            enemy_damage = enemy.damage + enemy_percent
            return enemy_damage

    else:
        enemy_damage = enemy.damage
        return enemy_damage
