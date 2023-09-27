import items

class NonPlayableCharacter():
    def __init__(self):
        raise NotImplementedError("Do not create raw NPC objects.")

    def __str__(self):
        self.name


class Trader(NonPlayableCharacter):
    def __init__(self):
        self.name = "Requisition Officer"
        self.supply = 100
        self.inventory = [items.Skirmisher(),
                          items.LineTroops(),
                          items.CrustyBread(),
                          items.BattlefieldTriageKit(),
                          items.BattlefieldTriageKit()]
