from gisim.status.base import CombatStatusEntity
from queue import PriorityQueue

class RainSword(CombatStatusEntity):
    """[Combat Status]When your active character receives at least 3 DMG: Decrease DMG taken by 1.Usage(s): 2"""
    name = "Rain Sword"
    description = """When your active character receives at least 3 DMG: Decrease DMG taken by 1.Usage(s): 2"""
    active = True
    value = 0

    def msg_handler(self, msg_queue: PriorityQueue) -> bool:
        """请编写处理函数"""
        print(f"Add Combat Status: {self.description}")
        return False

class RainbowBladework(CombatStatusEntity):
    """[Combat Status]After your character uses a Normal Attack: Deal 1 Hydro DMG.Usage(s): 3"""
    name = "Rainbow Bladework"
    description = "After your character uses a Normal Attack: Deal 1 Hydro DMG.Usage(s): 3"
    active = True
    value = 0

    def msg_handler(self, msg_queue: PriorityQueue) -> bool:
        """请编写处理函数"""
        print(f"Add Combat Status: {self.description}")
        return False