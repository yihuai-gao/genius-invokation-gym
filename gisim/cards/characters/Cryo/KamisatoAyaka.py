'''神里绫华'''
from ..character import Character, Skill
from ..summon import Summon

class KamisatoAyaka(Character):
    '''神里绫华'''
    def __init__(self, player_id:int, position:int):
        super().__init__('神里绫华', 'KamisatoAyaka', player_id, position)
        self.NATIONALITY = 'Inazuma'
        self.WEAPON_TYPE = 'claymore'
        self.health_point = 10
        self.SKILLS_NUM = 4
        self.CHINESE_SKILL_NAMES = ['神里流·倾', '神里流·冰华', '神里流·霜灭', '神里流·霰步']
        self.English_SKILL_NAMES = ['Kamisato Art: Kabuki', 'Kamisato Art: Hyouka', 'Kamisato Art: Soumetsu', 'Kamisato Art: Senho']
        # Init skills
         
        normal_attack = Skill(Chinese_name='神里流·倾', English_name='Kamisato Art: Kabuki', cost={'Cryo':1, 'Arbitrary':2}, skill_type='Normal Attack')
        
        elemental_skill = Skill(Chinese_name='神里流·冰华', English_name='Kamisato Art: Hyouka', cost={'Cryo':3}, skill_type='Elemental Skill')
        
        elemental_burst = Skill(Chinese_name='神里流·霜灭', English_name='Kamisato Art: Soumetsu', cost={'Cryo':3, 'Power': 3}, skill_type='Elemental Burst')
        
        passive_skill = Skill(Chinese_name='神里流·霰步', English_name='Kamisato Art: Senho', cost=None, skill_type='Passive Skill')
        

        
    