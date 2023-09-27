import random
import enemies
import items
import time
import sys


#The game works on a grid plane with x and y referring to the coordinates of each cell in the grid.
#Domain specific language is used make a string in the shape of a grid with each gridcells location defined by an x and y coordinate after
#the DSL is compiled into the games map.
#Each subclass in the MapTile superclass refers to a gridcell which triggers narrative, combat etc when moved into.

class MapTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def intro_text(self):
        text = self.alive_text
        if self.enemy.is_alive():
            text = self.alive_text
        else:
            text = self.dead_text
        return text

    def story_tile_end_text(self):
        return self.dead_text

    #indicates whether or not combat will take place in this tile for the action_adder function
    def battle_tile(self):
        return False

    def modify_player(self, player):
        pass

    def room_id(self):
        return "0"


#Provides the player with a randomised amount of supply/currency when entered
class FindSuppliesTwo(MapTile):
    def __init__(self, x, y):
        self.supply = random.randint(1, 50)
        self.gold_claimed = False
        super().__init__(x, y)

    def modify_player(self, player):
        if not self.gold_claimed:
            self.gold_claimed = True
            player.supply = player.supply + self.supply
            print("+{} supplies added.".format(self.supply))

    def intro_text(self):
        if self.gold_claimed:
            return """\n\n\n\n\n\n\n\n\n\n
    You stumble across a small hamlet in the forest. It is silent and forlorn, the small huts blackened by fire
    and empty of the life that once animated them. There is nothing here for us, we must carry on.
            \n"""
        else:
            return """\n\n\n\n\n\n\n\n\n\n
    The thick forest parts to reveal the warm glow of a hearth fire in a villagers window. Chickens and pigs
    sleep soundly in pens around the small village. It appears that neither animal or person is aware that
    there is even a war on in this peaceful place. Before you can speak a single word the hungry men under
    your command begin rushing towards the village.
            \n"""


class FindSuppliesOne(MapTile):
    def __init__(self, x, y):
        self.supply = random.randint(1, 50)
        self.gold_claimed = False
        super().__init__(x, y) #calls the init method of the parent class

    def modify_player(self, player):
        if not self.gold_claimed:
            self.gold_claimed = True
            player.supply = player.supply + self.supply
            print("+{} supplies added.".format(self.supply))

    def intro_text(self):
        if self.gold_claimed:
            return """\n\n\n\n\n\n\n\n\n\n
    You stumble across a small hamlet in the forest. It is silent and forlorn, the small huts blackened by fire
    and empty of the life that once animated them. There is nothing here for us, we must carry on.
            \n"""

        else:

            return """\n\n\n\n\n\n\n\n\n\n
    Napoleans plans to supply the army broke down disastrously once the border of the Russian Empire was crossed.
    The countryside was so poor that methods of foraging that once kept the army fed on campaign fell apart.
    Soon desperate men were pillaging everything they could, driving the local population to ruin.
            
    Napolean is furious upon finding out, ordering firing squads, but to no avail. Tens of thousands of men 
    desert and begin to pillage the countryside, sometimes even joining up with rebellious bands of local
    peasants. There is nothing to be done now, we must accept the stolen supplies or we will starve with the 
    unfortunate peasantry.
            
    "The path of Atilla in the age of barbarism cannot have been strewn with more horrible testimonies" -
    spoken by a polish officer upon discovering a man begging for bread was actually a local prince he once knew.
            \n"""


#Tile that allows the player to buy and sell items with supply.
class TraderTile(MapTile):
    def __init__(self, x, y):
        self.trader = items.Trader()
        self.enemy = enemies.NoEnemy()
        super().__init__(x, y)

    def trade(self, buyer, seller):
        for i, item in enumerate(seller.inventory, 1):
            print("{}. {} - {} Supply".format(i, item.name, item.value))
        while True:
            user_input = input("Choose an item or press Q to exit: ")
            if user_input in ['Q', 'q']:
                return
            else:
                try:
                    choice = int(user_input)
                    to_swap = seller.inventory[choice - 1]
                    self.swap(seller, buyer, to_swap)
                except ValueError:
                    print("Invalid choice!")

#checks if the player can afford the chosen item, if so adds it to player inventory and removes it from traders inventory
    def swap(self, seller, buyer, item):
        if item.value > buyer.supply:
            print("That's too expensive")
            return
        try:
            if isinstance(item, items.Unit):
                buyer.army.append(item)
            else:
                buyer.inventory.append(item)
            seller.inventory.remove(item)
            seller.supply = seller.supply + item.value
            buyer.supply = buyer.supply - item.value
            print("Trade complete!")
        except IndexError:
            "Error please try again"

#creates the menu and inputs to navigate the trade. Assigns the buyer and seller role to the right object.
    def check_if_trade(self, player):
        while True:
            print("Would you like to (B)uy, (S)ell, or (Q)uit? you have {} supply.".format(player.supply))
            user_input = input()
            if user_input in ['Q', 'q']:
                return
            elif user_input in ['B', 'b']:
                print("Here's whats available to buy: ")
                self.trade(buyer=player, seller=self.trader)
            elif user_input in ['S', 's']:
                try:
                    print("Here's whats available to sell: ")
                    self.trade(buyer=self.trader, seller=player)
                except IndexError:
                    print("error selection does not exist please try again")
            else:
                print("Invalid choice!")

    def intro_text(self):
        return """\n\n\n\n\n\n\n\n\n\n
    As you camp down for the night the long train of men stretching through the forests and planes begin to bunch
    up and gather around fires to rest. This is a good opportunity to trade for food or enlist men who have been
    seperated from their officers, if you have the supplies to support them.
           \n"""

#finishes the game when this map tile is reached.
class VictoryTile(MapTile):
    def modify_player(self, player):
        player.victory = True

    def intro_text(self):
        return """\n\n\n\n\n\n\n\n\n\n
    At last you limp back across the Nieman river with the husk that was once an army. It is hard to imagine a 
    greater military catastrophe than the 1812 campaign. It took Napolean and the men who followed him from a
    position of strength scarcely witnessed in history to utter ruin. 
    
    Half a million men are dead. 
    For every 12 that marched into Russia one was killed in battle, one was captured and died, 
    one was captured and survived, seven died from disease or the elements.
    Just two returned alive.
        \n"""


class CavalryTile(MapTile):
    def __init__(self, x, y):
        self.enemy = enemies.Cavalry()
        self.alive_text = "\n\n\n\n\n\n\n\n\n\nCavalry charges forward at your army!\n"
        self.dead_text = "\nA grim sight of ruined men and horses lays before you\n"

        super().__init__(x, y)

    def battle_tile(self):
        return True


class CossackTile(MapTile):
    def __init__(self, x, y):
        self.enemy = enemies.Cossacks()
        self.alive_text = "\n\n\n\n\n\n\n\n\n\nEnemy Cossacks begin to skirmish with your vanguard!\n"
        self.dead_text = "\nYou have managed to defeat the Cossacks and they have fled for good.\n"

        super().__init__(x, y)

    def battle_tile(self):
        return True


class GrenadierTile(MapTile):
    def __init__(self, x, y):
        self.enemy = enemies.Grenadiers()
        self.alive_text = "\n\n\n\n\n\n\n\n\n\nA unit of enemy Grenadiers attacks!\n"
        self.dead_text = "\nThe enemy grenadiers lay fallen before you\n"

        super().__init__(x, y)

    def battle_tile(self):
        return True


class SkirmishTile(MapTile):
    def __init__(self, x, y):
        self.enemy = enemies.Skirmisher()
        self.alive_text = "\n\n\n\n\n\n\n\n\n\nSkirmishers appear in the distance, sniping shots and falling back" \
                          " repeatedly\n"
        self.dead_text = "\nThe run down skirmishers lay fallen wherever they were caught\n"

        super().__init__(x, y)

    def battle_tile(self):
        return True


class BanditTile(MapTile):
    def __init__(self, x, y):
        self.enemy = enemies.Bandits()
        self.alive_text ="""\n\n\n\n\n\n\n\n\n\n
    There we over 67 separate peasant rebellions during the course of Alexanders reign. The Russian Empire was the last 
    place in europe to abolish the brutal system of serfdom. At times brutalized or desperate peasants turned to 
    banditry to survive, with war brutalizing the land this situation has only become more common. As your army is 
    strung out in a thin line to pass through a thick forest, a band of these brigands launch an opportunistic attack 
    against you!
                         \n"""

        self.dead_text = "\n\n\n\n\n\n\n\n\n\nThe bandits morale broke quickly and they fled without much of a fight\n"


class StartTile(MapTile):
    def intro_text(self):
        return """\n\n\n\n\n\n\n\n\n\n
    The year is 1812. you sit overlooking the banks of the Nieman river in the midsummer heat. Before you the
    edge of Napoleanic europe runs into the cool waters of the Nieman river, its far currents lapping against the 
    vastness of Imperial Russia.

    All about you runs a tide of artillery and muskets, humanity and horses, banners and helmet crests above dusted air.
    The largest host yet witnessed by history, levelled like a lance before you, 
    glistening with marshal finery and gaudy colour, like jewels laid in its hilt.

    The friendship formed between Emperor Napolean and Tzar Alexander at Tilsit has cooled under the strain of France's
    anti British continental blockade and the pressure placed on the Tzar by Russian anger at defeat OF? and french
    influence in her affairs. 

    Press ada to continue:
        \n"""


class StoryTileOne(MapTile):
    def intro_text(self):
        return """\n\n\n\n\n\n\n\n\n\n
    You have been promoted to the rank of Général de Division and are required to take up command of a division/brigade?????
    in one of the corps of the Grande Armée. The posts available are:
    One: Combined arms brigade under the command of Marshal Davout
    Two: Infantry brigade under the command of Jérôme Bonaparte, King of Westphalia
    Three: Cavalry brigade under the command of Marshal Neye
                \n"""

    def room_id(self):
        return "1"
#populates the players army with the chosen set of units
    def cav_army(self):
        return [items.Cavalry(), items.Lancers(), items.Lancers()]

    def inf_army(self):
        return [items.LineTroops(), items.Skirmisher(), items.Grenadiers()]

    def mixed_army(self):
        return [items.LineTroops(), items.Cavalry(), items.Skirmisher()]

class StoryTileTwo(MapTile):

    def intro_text(self):
        return """\n\n\n\n\n\n\n\n\n\n
    The army crosses the nieman river expecting to join battle with the russian army, but finds it has fled
    east, leaving only a small rear guard of skirmishers behind to delay your advance
        \n"""


class StoryTileThree(MapTile):
    def __init__(self, x, y):
        self.enemy = enemies.Cossacks()
        self.alive_text = """\n\n\n\n\n\n\n\n\n\n
    Supporting a force as large as Napoleans grand army is a huge undertaking. As you move east deeper 
    into the Grand Duchy of Warsaw the question of supplying the army becomes more difficult as the land and its inhabitants grow poorer
    and the department created to deliver supplies from the west proves inefficient.
    It is vital that the Russian army is forced to stand and fight so the war can be concluded before winter.
    A russian Corps under Bagration has been caught in a trap, one corps is moving to block retreat while another
    moves up behind. Cossacks prepare to charge against the vanguard to allow for the rest of the army to escape.
        \n"""
        self.dead_text = "\nAfter fierce combat the remaining Cossacks fallback, but they may charge again.\n"

        super().__init__(x, y)

    def battle_tile(self):
        return True


class StoryTileFour(MapTile):
    def __init__(self, x, y):
        self.enemy = enemies.LithuaniaLifeGuard()
        self.alive_text = """\n\n\n\n\n\n\n\n\n\n
    An even larger force of Cossack's has returned. Jerome Bonaparte is supposed to be moving up behind us to support
    but he has not arrived. We may need to withdraw when possible.
        \n"""
        self.dead_text = """\n\n\n\n\n\n\n\n\n\n
    Despite your best efforts the battle of Mir has been the first defeat of the Russian campaign.
    Bagrations corps has slipped the noose and managed to fall back. Frustratingly the russians do not seem willing to
    join battle, so we must pursue them further and further east. The cause of the defeat has been lain at the feet of
    King Jerome Bonaparte and he has grown frustrated and left the campaign all together, leaving his corp in the hands of FINISH!!!!!!!1!!!
        \n"""

        super().__init__(x, y)

    def battle_tile(self):
        return True



class StoryTileFive(MapTile):
    def intro_text(self): return """\n\n\n\n\n\n\n\n\n\n 
    As we are about to bed down for the night near Vilhna a primeval storm falls upon us.Torrents of freezing water 
    pursue man and beast wherever they might try to seek shelter all through the long night. When dawn at last breaks 
    its way through the rain clouds a horrible sight is revealed. Abandoned wagons, dead and dying horses and freezing 
    men lay strewn all about in the mud.At least ten thousand war horses and fourty thousand supply horses are lost in 
    a single twenty four hour period. It is with dread that one must consider it is not yet even winter.
    \n"""


class StoryTileSix(MapTile):
    def intro_text(self): return """\n\n\n\n\n\n\n\n\n\n
    The army has split into two huge columns in an effort to encricle one of the Russian army corps. 
    Follow either the northern or southern column.
    \n\n"""


class StoryTileSeven(MapTile):
    def intro_text(self): return """\n\n\n\n\n\n\n\n\n\n
    We have arrived at the holy city of Smolensk, home of "Our Lady of Smolensk"
    a painting attributed to the biblical figure Luke.It is believed The Russians will sally forth in order to protect
    this holy relic and can then be finally trapped and defeated.
    
    In the hours before the battle the men of both armies mingle to trade items as if they were not soon to be at 
    eachothers throats, but with the roar of 200 cannon the battle commences. Our troops face the unenviable task of 
    assaulting the cities high walls without ladders or any climbing apparatus at all.
    \n"""


class StoryTileEight(MapTile):
    def intro_text(self): return """\n\n\n\n\n\n\n\n\n\n
    For hours men dashed themselves on the walls to no avail, while in our
    peripheries the very city itself ceased to exist.Consumed by a conflagration of cannon balls, until the fire of the
    battle gave way to the fire of dawn, Illuminating a section of the Polish contingent finally breaching the walls.
    But the Russians did not sally forth or stand and fight, for fifteen thousand casualties a dead city was won. Empty,
    with less than 300 structures still standing and an intact Russian army fled across the river.
    
    But the Russians struggle to stomach another retreat.Anger within the army forces the Tsar to replace its leader
    Barclay with Prince Kutuzov, despite Kutuzov's belief that retreat was the correct course of action.
    \n"""


class StoryTileNine(MapTile):
    def __init__(self, x, y):
        self.enemy = enemies.LithuaniaLifeGuard()
        self.alive_text = """\n\n\n\n\n\n\n\n\n\n
    We arrive outside the village of Borodino to find the Russians have turned and arrayed for battle, the holy icon
    "our lady of smolensk" rescued and held aloft amidst their banners by orthodox priests. Two systems of earthworks
    dominate the battlefield, named the flèches beaten back four times. We are ordered to join the fifth charge against it.
    
    "I could not escape the feeling that something huge and destructive was hanging all of us" 
    Captain Von Linsingen - 2nd Westphalian Light Battalion
        \n"""

        self.dead_text = """\n
    We have captured a part of the earthworks, but a fierce counter attack has again driven us out. 
    But in the mean time Polish troops are making progress on our right flank and a great melee ensues 
    on our left over the great redoubt.
        \n"""

        super().__init__(x, y)

    def battle_tile(self):
        return True


class StoryTileTen(MapTile):
    def __init__(self, x, y):
        self.enemy = enemies.PavlovskGrenadiers()
        self.alive_text = """\n\n\n\n\n\n\n\n\n\n
    After countering a major Russian cavalry charge marshal Murat's cavalry corps has joined us for the sixth major
    attack on the flèches. General Bagration has been overseeing the defenses and hardening resolve here personally.
    He has just been gravely wounded by artillery and enemy morale is wavering. We must now take advantage of this
    oppurtunity.
        \n"""

        self.dead_text = """
    We have succeeded in capturing the flèches and the Russians are falling back in dissaray on this part of the front. 
    Yet Napolean refuses to commit his reserves, so we are required to reinforce the assault on the great redoubt.
        \n"""

        super().__init__(x, y)

    def battle_tile(self):
        return True


class StoryTileEleven(MapTile):
    def __init__(self, x, y):
        self.enemy = enemies.Uhlans()
        self.alive_text = """\n\n\n\n\n\n\n\n\n\n
    The Russians have been resisting doggedly about the great redoubt for the entire day, remaining in tight ranks
    even as cannon continously punch holes in their formations. Despite the overwhelming mass before it the redoubt
    holds until finally a unit of Saxon cavalry manages to outflank and enter it from the side in an astonighing feat of arms. The cavalry is 
    near to wiping out all the gunners inside, but we must reinforce them lest a counter attack retake the ground
    once again.
        \n"""

        self.dead_text = """
    As we stand amidst the carnage of the redoubt in exhaustion all the remaining cavalry are
    sent forth to exploit this victory, but they are countered by the last Russian cavalry on the field.
    With Napolean still refusing to commit his imperial guard, the rest of the army in utter exhuastion
    and dusk approaching the fighting must end for the day despite the bloodied Russian army still
    managing to stand across from us.
    I will not destroy my Guard. I am eight hundred leagues from France and i will not risk my
    last reserve. - Napolean on being asked to commit his reserves.
        \n"""

        super().__init__(x, y)

    def battle_tile(self):
        return True


class StoryTileTwelve(MapTile):
    def intro_text(self): return """\n\n\n\n\n\n\n\n\n\n
    We expected the fighting to continue on the next day. But upon dawn revealing the truly horrifying cost of the battle
    Kutuzov has ordered the Russian army to withdraw. Borodino would prove to be the bloodiest single day of the entire
    blood soaked years of the Napoleonic wars. With the french losing fourty nine generals and the Russian army losing the
    ability to fight at all. Despite the cost it would seem victory is close to hand and the gates of Moscow are even closer.
    \n"""


class StoryTileThirteen(MapTile):

    def intro_text(self): return """\n\n\n\n\n\n\n\n\n\n
    On the 14th of September Napolean enters Moscow behind a battered army. The city is desolate and empty, with small fires
    burning in the distance. Within fourty eight hours three quarters of the great city has burnt to the ground with
    precious few supplies left behind to find.
    
    For five weeks Napolean waits in the Kremlin expecting to negotiate and settle a peace with Tsar Alexander, but he refuses to even speak.
    Finally, with the supply situation dire Napolean decides to turn around. But with winter bearing down it is a late
    hour to leave.
    
    "What a terrible sight! And they did this themselves! So many palaces! What an incredible solution! 
    What kind of people! These are Scythians!" - Napolean on the Russian order to burn Moscow.
    \n"""

class StoryTileFourteen(MapTile):
    def __init__(self, x, y):
        self.enemy = enemies.CossackLifeGuard()
        self.alive_text = """\n\n\n\n\n\n\n\n\n\n
        The army heads back west the way it came.
        The long strung out columns on the smolensk road find no forage on the lands they already picked clean. 
        Every time men try to forage or are split off at all the Cossacks waiting in the wings pounce. The Grande Armée
        is no longer so grand and with Russian reinforcements we are now out numbered for the first time. The situation
        is dire.
        \n"""
        self.dead_text = "\n"

        super().__init__(x, y)

    def battle_tile(self):
        return True


class StoryTileFifteen(MapTile):
    def __init__(self, x, y):
        self.enemy = enemies.LineTroops()
        self.alive_text = """\n\n\n\n\n\n\n\n\n\n
    On November 15th as the vangaurd reaches Krasnoe, it is found that Kutuzov has advanced
    quickly and is threatening to block our retreat. We must drive through lest we be trapped!
        \n"""
        self.dead_text = """\n
    Kutuzov has failed to fully commit his forces and we have broken through. Unfortunately when
    Ney arrives with the read guard he finds the way blocked by sixty thousand enemies. In a feat bordering
    on miraculous the marshal manages to break through across a thinly frozen river and rejoin us,
    yet only a few hundred still accompany him where once there were thousands.
        \n"""

        super().__init__(x, y)

    def battle_tile(self):
        return True


class StoryTileSixteen(MapTile):
    def __init__(self, x, y):
        self.enemy = enemies.Jägers()
        self.alive_text = """\n\n\n\n\n\n\n\n\n\n
    The following week we reach the wide banks of the Berezina in Belarus only
    to find the bridge burning. A new bridge can be constructed but with the Russian's in pursuit we must launch a
    feint to the south and draw their attention away from the bridging operation.
        \n"""

        self.dead_text = """\n
        We have distracted them enough for two bridges to be completed. We must fall back and cross while we can.
        \n"""

        super().__init__(x, y)

    def battle_tile(self):
        return True


class StoryTileSeventeen(MapTile):
    def __init__(self, x, y):
        self.enemy = enemies.Cavalry()
        self.alive_text = """\n\n\n\n\n\n\n\n\n\n
    Moving so many men across such narrow bridges is taking too much time. We are compelled to join a desperate rear
    guard action to hold the Russians off while whats left of our army escapes.
        \n"""

        self.dead_text = """\n
    Time has been bought for our units to withdraw across the bridge. You look back to witness
    fire reflected on the Berezina. A decision to burn the bridges has condemned thousands to death
    on the frigid eastern bank.
        \n"""

        super().__init__(x, y)

    def battle_tile(self):
        return True


# def modify_player(self, player):
       # if self.enemy.is_alive():
        #    player.hp = player.hp - self.enemy.damage
         #   print("Enemy does {} damage. You have {} HP remaining.".format(self.enemy.damage, player.hp))


# We use a domain specific language to create the map and then use python to interpret it.
# VT = VictoryTile - EN = EnemyTile - ST = StartTile

#Domain specific language used to represent the games map. The space between two pipe characters represents a map tile.
#Each set of letters is an abbreviation for a type of map tile as defined in tile_type_dict

world_dsl = """
|    |ST13|SKR |ST14|
|    |ST12|    |ST15|
|    |ST11|    |ST16|
|    |ST10|    |ST17|
|    |ST9 |    |VT  |
|    |ST8 |    |    |
|SKR |ST7 |SKR |    |
|SKR |    |SKR |    |
|TT  |ST6 |FS1 |    |
|    |ST5 |    |    |
|    |ST4 |    |    |
|    |TT  |    |    |
|    |COS |    |    |
|    |ST3 |    |    |
|    |SKR |    |    |
|    |ST2 |    |    |
|    |FS1 |    |    |
|    |ST3 |ST  |TT  |
"""


# Python doesnt check for syntax errors in DSL code so we implement error checking for
# At least one victory tile, one start tile and each row needs to have the same number of cells.
# error checking for same number of cell in each row may need to be removed later on in the project.

#avoids syntax errors by ensuring the DSL has a start tile, victory tile and grid is layed out correctly.
def is_dsl_valid(dsl):
    if dsl.count("|ST  |") != 1:
        return False
    if dsl.count("|VT  |") == 0:
        return False
    # List comprehension meaning store the content of each line in a list, unless a line = [] / is empty
    lines = dsl.splitlines()
    lines = [l for l in lines if
             l]
    pipe_counts = [line.count("|") for line in
                   lines]
    for count in pipe_counts:
        if count != pipe_counts[0]:
            return False

    return True

#Shortens the names of the map tiles placed in each cell of the DSL map grid.
tile_type_dict = {"VT  ": VictoryTile,
                  "ST  ": StartTile,
                  "FS1 ": FindSuppliesOne,
                  "FS2 ": FindSuppliesTwo,
                  "TT  ": TraderTile,
                  "CAV ": CavalryTile,
                  "SKR ": SkirmishTile,
                  "GRN ": GrenadierTile,
                  "COS ": CossackTile,
                  "ST1 ": StoryTileOne,
                  "ST2 ": StoryTileTwo,
                  "ST3 ": StoryTileThree,
                  "ST4 ": StoryTileFour,
                  "ST5 ": StoryTileFive,
                  "ST6 ": StoryTileSix,
                  "ST7 ": StoryTileSeven,
                  "ST8 ": StoryTileEight,
                  "ST9 ": StoryTileNine,
                  "ST10": StoryTileTen,
                  "ST11": StoryTileEleven,
                  "ST12": StoryTileTwelve,
                  "ST13": StoryTileThirteen,
                  "ST14": StoryTileFourteen,
                  "ST15": StoryTileFifteen,
                  "ST16": StoryTileSixteen,
                  "ST17": StoryTileSeventeen,
                  "    ": None}


world_map = []

start_tile_location = None

#checks the DSL is valid, looks up the mappings for the abbreviations, creates new map tiles and assigns them their coordinates
def parse_world_dsl():
    if not is_dsl_valid(world_dsl):
        raise SyntaxError("DSL is invalid!")

    dsl_lines = world_dsl.splitlines()
    dsl_lines = [x for x in dsl_lines if x]

    for y, dsl_row in enumerate(dsl_lines):
        row = []
        dsl_cells = dsl_row.split("|")
        dsl_cells = [c for c in dsl_cells if c]
        for x, dsl_cell in enumerate(dsl_cells):
            tile_type = tile_type_dict[dsl_cell]
            if tile_type == StartTile:
                global start_tile_location
                start_tile_location = x, y
            row.append(tile_type(x, y) if tile_type else None) #what is going on? error comming from here. partially fixed when indentation changed slightly??

        world_map.append(row)

#returns the coordinates of the starting tile as defined in the DSL grid
def tile_location(x, y):
    if x < 0 or y < 0:
        return None
    try:
        return world_map[y][x]
    except IndexError:
        return None

#returns the coordinates of the tile the player is currently at.
def tile_at(x, y):
    if x < 0 or y < 0:
        return None
    try:
        return world_map[y][x]
    except IndexError:
        return None


"""makes the print and input functions output text gradually"""
def typing_print(text):
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.001)


def typing_input(text):
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.01)
    value = input()
    return value


def clear_text():
    return "\n\n\n\n\n\n\n\n\n\n\n"


class Introduction:
    def __init__(self):
        self.message = """
    The year is 1812. you sit overlooking the banks of the Nieman river in the midsummer heat. Before you the
    edge of Napoleonic europe runs into the cool waters of the Nieman river, its far currents lapping against the 
    vastness of Imperial Russia."""

    def __str__(self):
        return self.message


class IntroPartTwo(Introduction):
    def __init__(self):
        self.message = """\n
    All about you runs a tide of artillery and muskets, humanity and horses, banners and helmet crests above dusted air.
    The largest host yet witnessed by history, levelled like a lance before you, glistening with marshal finery and 
    gaudy colour, like jewels laid in its hilt."""


class IntroPartThree(Introduction):
    def __init__(self):
        self.message = """\n
    The friendship formed between Emperor Napoleon and Tzar Alexander at Tilsit has fractured and the two empires are 
    once again at war. Any moment now you will cross the river and take your place at the head of your men.
    Press ada to continue: """

