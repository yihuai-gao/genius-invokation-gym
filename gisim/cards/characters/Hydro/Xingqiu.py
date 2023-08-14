"""行秋"""
from queue import PriorityQueue
from typing import cast

from classes.message import AfterUsingSkillMsg, DealDamageMsg

from gisim.cards.characters.base import CharacterCard, CharacterSkill, GenericSkill
from gisim.classes.enums import (
    AttackType,
    CharPos,
    ElementType,
    EntityType,
    EquipmentType,
    Nation,
    PlayerID,
    SkillType,
    WeaponType,
)
from gisim.classes.status import CombatStatusEntity
from gisim.classes.summon import AttackSummon, Summon
from gisim.env import INF_INT
from gisim.get_game_info import get_game_info


class GuhuaStyle(GenericSkill):
    """
    古华剑法
    ~~~~~~~~
    造成2点`物理伤害`。
    """

    id: int = 12021
    name: str = "Guhua Style"
    text: str = """
    Deals 2 Physical DMG.
    """
    type: SkillType = SkillType.NORMAL_ATTACK
    costs: dict[ElementType, int] = {ElementType.HYDRO: 1, ElementType.ANY: 2}
    damage_element: ElementType = ElementType.NONE
    damage_value: int = 2


class FatalRainscreen(GenericSkill):
    """
    画雨笼山
    ~~~~~~~~
    造成2点`水元素伤害`，本角色`附着水元素`，生成`雨帘剑`。
    """

    id: int = 12022
    name: str = "Fatal Rainscreen"
    text: str = """
    Deals 2 Hydro DMG, grants this character Hydro Application, creates 1 Rain Sword.
    """
    type: SkillType = SkillType.ELEMENTAL_SKILL
    costs: dict[ElementType, int] = {ElementType.HYDRO: 3}
    damage_element: ElementType = ElementType.HYDRO
    damage_value: int = 2
    combat_status_name: str = "Rain Sword"
    combat_status_id: int = 112021
    combat_status_remaining_round: int = INF_INT
    combat_status_remaining_usage: int = 2
    self_element_attachment: ElementType = ElementType.HYDRO


class Raincutter(GenericSkill):
    """
    裁雨留虹
    ~~~~~~~~
    造成1点`水元素伤害`，本角色`附着水元素`，生成`虹剑势`。
    """

    id: int = 12023
    name: str = "Raincutter"
    text: str = """
    Deals 1 Hydro DMG, grants this character Hydro Application, creates 1 Rainbow Bladework.
    """
    type: SkillType = SkillType.ELEMENTAL_BURST
    costs: dict[ElementType, int] = {ElementType.HYDRO: 3, ElementType.POWER: 2}
    damage_element: ElementType = ElementType.HYDRO
    damage_value: int = 1
    combat_status_name: str = "Rainbow Bladework"
    combat_status_id: int = 112022

    combat_status_remaining_round: int = INF_INT
    combat_status_remaining_usage: int = 3
    self_element_attachment: ElementType = ElementType.HYDRO


class Xingqiu(CharacterCard):
    """行秋"""

    id: int = 1202
    name: str = "Xingqiu"
    element_type: ElementType = ElementType.HYDRO
    nations: list[Nation] = [Nation.Liyue]
    health_point: int = 10
    power: int = 0
    max_power: int = 2
    weapon_type: WeaponType = WeaponType.SWORD
    skills: list[CharacterSkill] = [
        GuhuaStyle(),
        FatalRainscreen(),
        Raincutter(),
    ]


class RainSwordStatus(CombatStatusEntity):
    """[Combat Status]When your active character receives at least 3 DMG:
    Decrease DMG taken by 1.
    Usage(s): 2
    """

    id: int = 112021
    name: str = "Rain Sword"
    description: str = """When your active character receives at least 3 DMG: Decrease DMG taken by 1.Usage(s): 2"""
    active: bool = True
    value: int = 0
    remaining_round: int = INF_INT
    remaining_usage: int = 2

    def msg_handler(self, msg_queue: PriorityQueue) -> bool:
        top_msg = msg_queue.queue[0]
        if isinstance(top_msg, DealDamageMsg):
            top_msg = cast(DealDamageMsg, top_msg)

            for idx, (target_id, target_pos, element_type, dmg_val) in enumerate(
                top_msg.targets
            ):
                if target_id == self.player_id and dmg_val >= 3:
                    print(
                        f"    Combat Status Effect By {self.player_id.name}:\n        {self.name}:{self.description}\n        Origin DMG: {element_type.name} -> {dmg_val} - {1}\n"
                    )

                    top_msg.targets[idx] = (
                        target_id,
                        target_pos,
                        element_type,
                        dmg_val - 1,
                    )
                    self.remaining_usage -= 1
                    # updated = True

        if self.remaining_usage == 0 or self.remaining_round == 0:
            self.active = False

        return False


class RainbowBladeworkStatus(CombatStatusEntity):
    """[Combat Status]After your character uses a Normal Attack:
    Deal 1 Hydro DMG.
    Usage(s): 3"""

    id: int = 112022
    name: str = "Rainbow Bladework"
    description = (
        "After your character uses a Normal Attack: Deal 1 Hydro DMG.Usage(s): 3"
    )
    active: bool = True
    value: int = 0
    remaining_round: int = INF_INT
    remaining_usage: int = 3

    def msg_handler(self, msg_queue: PriorityQueue) -> bool:
        top_msg = msg_queue.queue[0]
        updated = False
        if self._uuid in top_msg.responded_entities:
            return False

        if isinstance(top_msg, AfterUsingSkillMsg):
            top_msg = cast(AfterUsingSkillMsg, top_msg)
            for targets_player_id, targets_pos in top_msg.skill_targets:
                if (
                    top_msg.skill_type == SkillType.NORMAL_ATTACK
                    and top_msg.sender_id == self.player_id
                ):
                    print(
                        f"    Combat Status Effect By {self.player_id.name}:\n        {self.name}:{self.description}\n        PutDMG: HYDRO -> 1\n"
                    )

                    new_msg = DealDamageMsg(
                        sender_id=self.player_id,
                        attacker=(self.player_id, CharPos.NONE),
                        attack_type=AttackType.COMBAT_STATUS,
                        targets=[
                            (targets_player_id, CharPos.ACTIVE, ElementType.HYDRO, 1)
                        ],
                    )
                    msg_queue.put(new_msg)
                    self.remaining_usage -= 1
                    updated = True

        if self.remaining_usage == 0 or self.remaining_round == 0:
            self.active = False

        if updated:
            top_msg.responded_entities.append(self._uuid)

        return updated
