
from player import Player
from collections import OrderedDict
import world
import time



"Allows the player to start the game when ready and then prints out introductory narrative with pauses between paragraphs"
if world.typing_input("Press any key to start game: ") == "":
    print(world.clear_text())
    world.typing_print(str(world.Introduction()))
    time.sleep(1)
    world.typing_print(str(world.IntroPartTwo()))
    time.sleep(1)
    if world.typing_input(str(world.IntroPartThree())) == "":
        print(world.clear_text())
        world.typing_print("Move north, you are required for audience by the Imperial Headquarters.\n")


    def play():
        world.parse_world_dsl()  # code relies on world being parsed before creating the player object else start_tile_location is none when its called
        player = Player()
        while not player.army_gone() and not player.victory:  # This while loop keeps the game looping until the user wins,loses or quits
            # room = world.tile_location(player.x, player.y) #
            room = world.tile_at(player.x, player.y)
            # print(room.intro_text()) removed to stop intro text repeating after using inventory
            # room.modify_player(player)
            if not player.army_gone() and not player.victory:
                choose_action(room, player)
            elif player.army_gone():
                print("You died")


    # Considers conditions the player is currently in and provides available responses
    def get_available_actions(room, player):
        actions = OrderedDict()
        check_hp = True
        list_item_count = True
        print("Choose an action: ")
        action_adder(actions, 'I', player.print_inventory, "Unit and inventory information")

        for unit in player.army:
            if list_item_count:
                if unit.experience >= 2:
                    action_adder(actions, 'L', player.level_up, "Assign unit veterancy")
                    list_item_count = False

        if isinstance(room, world.TraderTile):
            action_adder(actions, 'T', player.trade, "Trade")

        for units in player.army:
            if units.unit_population < units.unit_start_population:
                while check_hp:
                    action_adder(actions, 'H', player.heal, "Heal")
                    check_hp = False

        if room.battle_tile() and room.enemy.is_alive():
            action_adder(actions, 'A', player.attack, "Attack")
        else:
            if world.tile_location(room.x, room.y - 1):
                action_adder(actions, 'E', player.move_east, "Go East")
            if world.tile_location(room.x, room.y + 1):
                action_adder(actions, 'W', player.move_west, "Go West")
            if world.tile_location(room.x + 1, room.y):
                action_adder(actions, 'S', player.move_south, "Go South")
            if world.tile_location(room.x - 1, room.y):
                action_adder(actions, 'N', player.move_north, "Go North")

        return actions


def action_adder(action_dict, hotkey, action, name):
    action_dict[hotkey.lower()] = action
    action_dict[hotkey.upper()] = action
    print("{}: {}".format(hotkey, name))


def choose_action(room, player):
    action = None
    while not action:
        available_actions = get_available_actions(room, player)
        action_input = input("Action: ")
        action = available_actions.get(action_input)
        if action:
            action()
        else:
            print("Invalid action!")


play()


