


from cards.base import WeaponCard
from classes.enums import ElementType, EquipmentType, WeaponType
from classes.equipment import WeaponEntity


class MagicGuideCard(WeaponCard):
    id: int = 311101
    name: str = 'Magic Guide'
    text: str = '''The character deals +1 DMG.(Only Catalyst Characters can equip this. A character can equip a maximum of 1 Weapon)'''
    costs: dict[ElementType, int] = {ElementType.SAME: 2}
    weapon_type: WeaponType = WeaponType.CATALYST
    
class MagicGuide(WeaponEntity):
    name = 'Magic Guide'
    
    
class SacrificialFragmentsCard(WeaponCard):
    id: int = 311102
    name: str = "Sacrificial Fragments"
    text: str = """The character deals +1 DMG.After the character uses an Elemental Skill: Create 1 Elemental Die of the same Elemental Type as this character. (Once per Round)(Only Catalyst Characters can equip this. A character can equip a maximum of 1 Weapon)"""
    costs: dict[ElementType, int] = {ElementType.SAME: 3}
    weapon_type: WeaponType = WeaponType.CATALYST

class SacrificialFragments(WeaponEntity):
    name: str = "Sacrificial Fragments"


class SkywardAtlasCard(WeaponCard):
    id: int = 311103
    name: str = "Skyward Atlas"
    text: str = """The character deals +1 DMG.Once per Round: This character's Normal Attacks deal +1 additional DMG.(Only Catalyst Characters can equip this. A character can equip a maximum of 1 Weapon)"""
    costs: dict[ElementType, int] = {ElementType.SAME: 3}
    weapon_type: WeaponType = WeaponType.CATALYST

class SkywardAtlas(WeaponEntity):
    name: str = "Skyward Atlas"


class RavenBowCard(WeaponCard):
    id: int = 311201
    name: str = "Raven Bow"
    text: str = """The character deals +1 DMG.(Only Bow Characters can equip this. A character can equip a maximum of 1 Weapon)"""
    costs: dict[ElementType, int] = {ElementType.SAME: 2}
    weapon_type: WeaponType = WeaponType.BOW

class RavenBow(WeaponEntity):
    name: str = "Raven Bow"


class SacrificialBowCard(WeaponCard):
    id: int = 311202
    name: str = "Sacrificial Bow"
    text: str = """The character deals +1 DMG.After the character uses an Elemental Skill: Create 1 Elemental Die of the same Elemental Type as this character. (Once per Round)(Only Bow Characters can equip this. A character can equip a maximum of 1 Weapon)"""
    costs: dict[ElementType, int] = {ElementType.SAME: 3}
    weapon_type: WeaponType = WeaponType.BOW

class SacrificialBow(WeaponEntity):
    name: str = "Sacrificial Bow"


class SkywardHarpCard(WeaponCard):
    id: int = 311203
    name: str = "Skyward Harp"
    text: str = """The character deals +1 DMG.Once per Round: This character's Normal Attacks deal +1 additional DMG.(Only Bow Characters can equip this. A character can equip a maximum of 1 Weapon)"""
    costs: dict[ElementType, int] = {ElementType.SAME: 3}
    weapon_type: WeaponType = WeaponType.BOW

class SkywardHarp(WeaponEntity):
    name: str = "Skyward Harp"


class WhiteIronGreatswordCard(WeaponCard):
    id: int = 311301
    name: str = "White Iron Greatsword"
    text: str = """The character deals +1 DMG.(Only Claymore Characters can equip this. A character can equip a maximum of 1 Weapon)"""
    costs: dict[ElementType, int] = {ElementType.SAME: 2}
    weapon_type: WeaponType = WeaponType.CLAYMORE

class WhiteIronGreatsword(WeaponEntity):
    name: str = "White Iron Greatsword"


class SacrificialGreatswordCard(WeaponCard):
    id: int = 311302
    name: str = "Sacrificial Greatsword"
    text: str = """The character deals +1 DMG.After the character uses an Elemental Skill: Create 1 Elemental Die of the same Elemental Type as this character. (Once per Round)(Only Claymore Characters can equip this. A character can equip a maximum of 1 Weapon)"""
    costs: dict[ElementType, int] = {ElementType.SAME: 3}
    weapon_type: WeaponType = WeaponType.CLAYMORE

class SacrificialGreatsword(WeaponEntity):
    name: str = "Sacrificial Greatsword"


class WolfsGravestoneCard(WeaponCard):
    id: int = 311303
    name: str = "Wolf's Gravestone"
    text: str = """The character deals +1 DMG.Deal +2 additional DMG if the target's remaining HP is equal to or less than 6.(Only Claymore Characters can equip this. A character can equip a maximum of 1 Weapon)"""
    costs: dict[ElementType, int] = {ElementType.SAME: 3}
    weapon_type: WeaponType = WeaponType.CLAYMORE

class WolfsGravestone(WeaponEntity):
    name: str = "Wolf's Gravestone"


class WhiteTasselCard(WeaponCard):
    id: int = 311401
    name: str = "White Tassel"
    text: str = """The character deals +1 DMG.(Only Polearm Characters can equip this. A character can equip a maximum of 1 Weapon)"""
    costs: dict[ElementType, int] = {ElementType.SAME: 2}
    weapon_type: WeaponType = WeaponType.POLEARM

class WhiteTassel(WeaponEntity):
    name: str = "White Tassel"


class LithicSpearCard(WeaponCard):
    id: int = 311402
    name: str = "Lithic Spear"
    text: str = """The character deals +1 DMG.When played: For each party member from Liyue, grant 1 Shield point to the character to which this is attached. (Max 3 points)(Only Polearm Characters can equip this. A character can equip a maximum of 1 Weapon)"""
    costs: dict[ElementType, int] = {ElementType.SAME: 3}
    weapon_type: WeaponType = WeaponType.POLEARM

class LithicSpear(WeaponEntity):
    name: str = "Lithic Spear"


class SkywardSpineCard(WeaponCard):
    id: int = 311403
    name: str = "Skyward Spine"
    text: str = """The character deals +1 DMG.Once per Round: This character's Normal Attacks deal +1 additional DMG.(Only Polearm Characters can equip this. A character can equip a maximum of 1 Weapon)"""
    costs: dict[ElementType, int] = {ElementType.SAME: 3}
    weapon_type: WeaponType = WeaponType.POLEARM

class SkywardSpine(WeaponEntity):
    name: str = "Skyward Spine"


class TravelersHandySwordCard(WeaponCard):
    id: int = 311501
    name: str = "Traveler's Handy Sword"
    text: str = """The character deals +1 DMG.(Only Sword Characters can equip this. A character can equip a maximum of 1 Weapon)"""
    costs: dict[ElementType, int] = {ElementType.SAME: 2}
    weapon_type: WeaponType = WeaponType.SWORD

class TravelersHandySword(WeaponEntity):
    name: str = "Traveler's Handy Sword"


class SacrificialSwordCard(WeaponCard):
    id: int = 311502
    name: str = "Sacrificial Sword"
    text: str = """The character deals +1 DMG.After the character uses an Elemental Skill: Create 1 Elemental Die of the same Elemental Type as this character. (Once per Round)(Only Sword Characters can equip this. A character can equip a maximum of 1 Weapon)"""
    costs: dict[ElementType, int] = {ElementType.SAME: 3}
    weapon_type: WeaponType = WeaponType.SWORD

class SacrificialSword(WeaponEntity):
    name: str = "Sacrificial Sword"


class AquilaFavoniaCard(WeaponCard):
    id: int = 311503
    name: str = "Aquila Favonia"
    text: str = """The character deals +1 DMG.After the opposing character uses a Skill: If the character with this attached is the active character, heal this character for 1 HP. (Max twice per Round)(Only Sword Characters can equip this. A character can equip a maximum of 1 Weapon)"""
    costs: dict[ElementType, int] = {ElementType.SAME: 3}
    weapon_type: WeaponType = WeaponType.SWORD

class AquilaFavonia(WeaponEntity):
    name: str = "Aquila Favonia"