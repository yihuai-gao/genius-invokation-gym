from queue import PriorityQueue
from typing import cast, Dict

from gisim.cards.base import WeaponCard
from gisim.cards.characters import get_skill_type
from gisim.classes.enums import ElementType, EquipmentType, WeaponType
from gisim.classes.equipment import WeaponEntity
from gisim.classes.message import AfterUsingSkillMsg, DealDamageMsg, Message

from gisim.classes.enums import SkillType
from gisim.classes.message import ChangeDiceMsg


class MagicGuideCard(WeaponCard):
    id: int = 311101
    name: str = "Magic Guide"
    text: str = """The character deals +1 DMG.(Only Catalyst Characters can equip this. A character can equip a maximum of 1 Weapon)"""
    costs: Dict[ElementType, int] = {ElementType.SAME: 2}
    weapon_type: WeaponType = WeaponType.CATALYST


class MagicGuide(WeaponEntity):
    name: str = "Magic Guide"
    weapon_type: WeaponType = WeaponType.CATALYST


class SacrificialFragmentsCard(WeaponCard):
    id: int = 311102
    name: str = "Sacrificial Fragments"
    text: str = """The character deals +1 DMG.After the character uses an Elemental Skill: Create 1 Elemental Die of the same Elemental Type as this character. (Once per Round)(Only Catalyst Characters can equip this. A character can equip a maximum of 1 Weapon)"""
    costs: Dict[ElementType, int] = {ElementType.SAME: 3}
    weapon_type: WeaponType = WeaponType.CATALYST


class SacrificialFragments(WeaponEntity):
    name: str = "Sacrificial Fragments"
    weapon_type: WeaponType = WeaponType.CATALYST


class SkywardAtlasCard(WeaponCard):
    id: int = 311103
    name: str = "Skyward Atlas"
    text: str = """The character deals +1 DMG.Once per Round: This character's Normal Attacks deal +1 additional DMG.(Only Catalyst Characters can equip this. A character can equip a maximum of 1 Weapon)"""
    costs: Dict[ElementType, int] = {ElementType.SAME: 3}
    weapon_type: WeaponType = WeaponType.CATALYST


class SkywardAtlas(WeaponEntity):
    name: str = "Skyward Atlas"
    weapon_type: WeaponType = WeaponType.CATALYST


class RavenBowCard(WeaponCard):
    id: int = 311201
    name: str = "Raven Bow"
    text: str = """The character deals +1 DMG.(Only Bow Characters can equip this. A character can equip a maximum of 1 Weapon)"""
    costs: Dict[ElementType, int] = {ElementType.SAME: 2}
    weapon_type: WeaponType = WeaponType.BOW


class RavenBow(WeaponEntity):
    name: str = "Raven Bow"
    weapon_type: WeaponType = WeaponType.BOW


class SacrificialBowCard(WeaponCard):
    id: int = 311202
    name: str = "Sacrificial Bow"
    text: str = """The character deals +1 DMG.After the character uses an Elemental Skill: Create 1 Elemental Die of the same Elemental Type as this character. (Once per Round)(Only Bow Characters can equip this. A character can equip a maximum of 1 Weapon)"""
    costs: Dict[ElementType, int] = {ElementType.SAME: 3}
    weapon_type: WeaponType = WeaponType.BOW


class SacrificialBow(WeaponEntity):
    name: str = "Sacrificial Bow"
    weapon_type: WeaponType = WeaponType.BOW


class SkywardHarpCard(WeaponCard):
    id: int = 311203
    name: str = "Skyward Harp"
    text: str = """The character deals +1 DMG.Once per Round: This character's Normal Attacks deal +1 additional DMG.(Only Bow Characters can equip this. A character can equip a maximum of 1 Weapon)"""
    costs: Dict[ElementType, int] = {ElementType.SAME: 3}
    weapon_type: WeaponType = WeaponType.BOW


class SkywardHarp(WeaponEntity):
    name: str = "Skyward Harp"
    weapon_type: WeaponType = WeaponType.BOW


class WhiteIronGreatswordCard(WeaponCard):
    id: int = 311301
    name: str = "White Iron Greatsword"
    text: str = """The character deals +1 DMG.(Only Claymore Characters can equip this. A character can equip a maximum of 1 Weapon)"""
    costs: Dict[ElementType, int] = {ElementType.SAME: 2}
    weapon_type: WeaponType = WeaponType.CLAYMORE


class WhiteIronGreatsword(WeaponEntity):
    name: str = "White Iron Greatsword"
    weapon_type: WeaponType = WeaponType.CLAYMORE


class SacrificialGreatswordCard(WeaponCard):
    id: int = 311302
    name: str = "Sacrificial Greatsword"
    text: str = """The character deals +1 DMG.After the character uses an Elemental Skill: Create 1 Elemental Die of the same Elemental Type as this character. (Once per Round)(Only Claymore Characters can equip this. A character can equip a maximum of 1 Weapon)"""
    costs: Dict[ElementType, int] = {ElementType.SAME: 3}
    weapon_type: WeaponType = WeaponType.CLAYMORE


class SacrificialGreatsword(WeaponEntity):
    name: str = "Sacrificial Greatsword"
    weapon_type: WeaponType = WeaponType.CLAYMORE


class WolfsGravestoneCard(WeaponCard):
    id: int = 311303
    name: str = "Wolf's Gravestone"
    text: str = """The character deals +1 DMG.Deal +2 additional DMG if the target's remaining HP is equal to or less than 6.(Only Claymore Characters can equip this. A character can equip a maximum of 1 Weapon)"""
    costs: Dict[ElementType, int] = {ElementType.SAME: 3}
    weapon_type: WeaponType = WeaponType.CLAYMORE


class WolfsGravestone(WeaponEntity):
    name: str = "Wolf's Gravestone"
    weapon_type: WeaponType = WeaponType.CLAYMORE


class WhiteTasselCard(WeaponCard):
    id: int = 311401
    name: str = "White Tassel"
    text: str = """The character deals +1 DMG.(Only Polearm Characters can equip this. A character can equip a maximum of 1 Weapon)"""
    costs: Dict[ElementType, int] = {ElementType.SAME: 2}
    weapon_type: WeaponType = WeaponType.POLEARM


class WhiteTassel(WeaponEntity):
    name: str = "White Tassel"
    weapon_type: WeaponType = WeaponType.POLEARM


class LithicSpearCard(WeaponCard):
    id: int = 311402
    name: str = "Lithic Spear"
    text: str = """The character deals +1 DMG.When played: For each party member from Liyue, grant 1 Shield point to the character to which this is attached. (Max 3 points)(Only Polearm Characters can equip this. A character can equip a maximum of 1 Weapon)"""
    costs: Dict[ElementType, int] = {ElementType.SAME: 3}
    weapon_type: WeaponType = WeaponType.POLEARM


class LithicSpear(WeaponEntity):
    name: str = "Lithic Spear"
    weapon_type: WeaponType = WeaponType.POLEARM


class SkywardSpineCard(WeaponCard):
    id: int = 311403
    name: str = "Skyward Spine"
    text: str = """The character deals +1 DMG.Once per Round: This character's Normal Attacks deal +1 additional DMG.(Only Polearm Characters can equip this. A character can equip a maximum of 1 Weapon)"""
    costs: Dict[ElementType, int] = {ElementType.SAME: 3}
    weapon_type: WeaponType = WeaponType.POLEARM


class SkywardSpine(WeaponEntity):
    name: str = "Skyward Spine"
    weapon_type: WeaponType = WeaponType.POLEARM


class TravelersHandySwordCard(WeaponCard):
    id: int = 311501
    name: str = "Traveler's Handy Sword"
    text: str = """The character deals +1 DMG.(Only Sword Characters can equip this. A character can equip a maximum of 1 Weapon)"""
    costs: Dict[ElementType, int] = {ElementType.SAME: 2}
    weapon_type: WeaponType = WeaponType.SWORD


class TravelersHandySword(WeaponEntity):
    name: str = "Traveler's Handy Sword"
    weapon_type: WeaponType = WeaponType.SWORD


class SacrificialSwordCard(WeaponCard):
    id: int = 311502
    name: str = "Sacrificial Sword"
    text: str = """The character deals +1 DMG.After the character uses an Elemental Skill: Create 1 Elemental Die of the same Elemental Type as this character. (Once per Round)(Only Sword Characters can equip this. A character can equip a maximum of 1 Weapon)"""
    costs: Dict[ElementType, int] = {ElementType.SAME: 3}
    weapon_type: WeaponType = WeaponType.SWORD


class SacrificialSword(WeaponEntity):
    name: str = "Sacrificial Sword"
    weapon_type: WeaponType = WeaponType.SWORD

    def msg_handler(self, msg_queue: PriorityQueue):
        # Increase 1 dmg by default without any advanced effects
        top_msg = msg_queue.queue[0]
        updated = False
        if self._uuid in top_msg.responded_entities:
            return updated

        if isinstance(top_msg, DealDamageMsg):
            top_msg = cast(DealDamageMsg, top_msg)
            if top_msg.attacker == (self.player_id, self.char_pos):
                for idx, (player_id, char_pos, elem_type, dmg_val) in enumerate(
                    top_msg.targets
                ):
                    if elem_type is not ElementType.PIERCE:
                        top_msg.targets[idx] = (
                            player_id,
                            char_pos,
                            elem_type,
                            dmg_val + 1,
                        )
                        updated = True
        if isinstance(top_msg, AfterUsingSkillMsg):
            if self.active == True and self.triggered_in_a_round == 0:
                top_msg = cast(AfterUsingSkillMsg, top_msg)
                if get_skill_type(top_msg.skill_name) == SkillType.ELEMENTAL_SKILL:
                    # TODO: Get the element type of the current character (Essentially one need to get all the game information visible for all entities)
                    new_msg = ChangeDiceMsg(
                        sender_id=self.player_id,
                        remove_dice_idx=[],
                        new_target_element=[ElementType.OMNI],
                    )
                    msg_queue.put(new_msg)
                    updated = True
                    self.triggered_in_a_round += 1
                    self.active = False

        if updated:
            top_msg.responded_entities.append(self._uuid)
        return updated


class AquilaFavoniaCard(WeaponCard):
    id: int = 311503
    name: str = "Aquila Favonia"
    text: str = """The character deals +1 DMG.After the opposing character uses a Skill: If the character with this attached is the active character, heal this character for 1 HP. (Max twice per Round)(Only Sword Characters can equip this. A character can equip a maximum of 1 Weapon)"""
    costs: Dict[ElementType, int] = {ElementType.SAME: 3}
    weapon_type: WeaponType = WeaponType.SWORD


class AquilaFavonia(WeaponEntity):
    name: str = "Aquila Favonia"
    weapon_type: WeaponType = WeaponType.SWORD
