'''神里绫华'''
from mailbox import NotEmptyError
from ....global_config import DISPLAY_LANGUAGE
from ....classes.character import Character, Skill
from ....classes.summon import Summon

class KamisatoAyaka(Character):
    '''神里绫华'''
    def __init__(self, player_id:int, position:int):
        if DISPLAY_LANGUAGE == "Chinese":
            super().__init__('神里绫华', player_id, position)
            self.SKILL_NAMES = ['神里流·倾', '神里流·冰华', '神里流·霜灭', '神里流·霰步']
        elif DISPLAY_LANGUAGE == "English":
            super().__init__('KamisatoAyaka', player_id, position)
            self.SKILL_NAMES = ['Kamisato Art: Kabuki', 'Kamisato Art: Hyouka', 'Kamisato Art: Soumetsu', 'Kamisato Art: Senho']
        self.NATIONALITY = 'Inazuma'
        self.WEAPON_TYPE = 'claymore'
        self.health_point = 10
        self.SKILLS_NUM = 4
        # Init skills
         
        normal_attack = Skill(name=self.SKILL_NAMES[0], cost={'Cryo':1, 'Arbitrary':2}, skill_type='Normal Attack')
        
        elemental_skill = Skill(name=self.SKILL_NAMES[1], cost={'Cryo':3}, skill_type='Elemental Skill')
        
        elemental_burst = Skill(name=self.SKILL_NAMES[2], cost={'Cryo':3, 'Power': 3}, skill_type='Elemental Burst')
        
        passive_skill = Skill(name=self.SKILL_NAMES[3], cost=None, skill_type='Passive Skill')
        

        
    