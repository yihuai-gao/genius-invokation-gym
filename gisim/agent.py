"""Player & agent APIs
"""
from abc import ABC, abstractmethod
import enum
from typing import OrderedDict
from xml.dom.minidom import Element
from gisim.cards.characters.Cryo.KamisatoAyaka import KamisatoAyaka

from gisim.classes.action import (
    Action,
    ChangeCardsAction,
    ChangeCharacterAction,
    DeclareEndAction,
    RollDiceAction,
    UseSkillAction,
)
from gisim.classes.enums import CharPos, ElementType, GamePhase, GameStatus, PlayerID, SkillType
from gisim.game import GameInfo

from .cards.characters.base import CHARACTER_CARDS, CHARACTER_NAME2ID
from .classes.message import ChangeCharacterMsg


class Agent(ABC):
    def __init__(self, player_id: PlayerID):
        self.player_id = player_id

    @abstractmethod
    def take_action(self, game_info: OrderedDict) -> Action:
        pass


class AttackOnlyAgent(Agent):
    def __init__(self, player_id: PlayerID):
        super().__init__(player_id)

    def get_dice_idx_greedy(self, dice:list[ElementType], cost:dict[ElementType, int], char_element:ElementType=ElementType.NONE):
        # First determine whether the current dice are enough
        dice_idx = []
        for key, val in cost.items():
            if 1 <= key.value <= 7:
                # 7 majors elements
                remaining = val
                for idx, die in enumerate(dice):
                    if idx not in dice_idx and die == key:
                        remaining -= 1
                        dice_idx.append(idx)
                        if remaining == 0:
                            break
                if remaining > 0:
                    # Need to take OMNI elements
                    for idx, die in enumerate(dice):
                        if idx not in dice_idx and die == ElementType.OMNI:
                            remaining -= 1
                            dice_idx.append(idx)
                            if remaining == 0:
                                break
                if remaining > 0:
                    # Insufficient dice
                    return []
            elif key.value == ElementType.ANY:
                # Arbitrary element
                remaining = val
                for idx, die in enumerate(dice):
                    if idx not in dice_idx and die != char_element:
                        remaining -= 1
                        dice_idx.append(idx)
                        if remaining == 0:
                            break
                if remaining > 0:
                    # Insufficient unaligned dice: we first use the dice with character element
                    for idx, die in enumerate(dice):
                        if idx not in dice_idx and die == char_element:
                            remaining -= 1
                            dice_idx.append(idx)
                            if remaining == 0:
                                break
                if remaining > 0:
                    # Insufficient unaligned dice: we first use the dice with character element
                    for idx, die in enumerate(dice):
                        if idx not in dice_idx and die == ElementType.OMNI:
                            remaining -= 1
                            dice_idx.append(idx)
                            if remaining == 0:
                                break
                if remaining > 0:
                    return []
        return dice_idx

    def take_action(self, game_info: GameInfo) -> Action:
        if game_info.status == GameStatus.INITIALIZING:
            if game_info.phase == GamePhase.CHANGE_CARD:
                return ChangeCardsAction(cards_idx=[])
            elif game_info.phase == GamePhase.SELECT_ACTIVE_CHARACTER:
                return ChangeCharacterAction(position=CharPos.MIDDLE, dice_idx=[])

        elif game_info.status == GameStatus.RUNNING:
            if game_info.phase == GamePhase.ROLL_DICE:
                player_info = game_info.get_player_info()
                active_pos = player_info.active_character_position
                character_info = player_info.characters[active_pos.value]
                # character_card = CHARACTER_CARDS[
                #     CHARACTER_NAME2ID[character_info.character.name]
                # ]
                character_card = KamisatoAyaka()
                character_element = character_card.element_type
                current_dice = player_info.dice_zone
                reroll_dice_idx = []
                for k, element_type in enumerate(current_dice):
                    if element_type not in [character_element, ElementType.OMNI]:
                        reroll_dice_idx.append(k)
                return RollDiceAction(dice_idx=reroll_dice_idx)
            elif game_info.phase == GamePhase.PLAY_CARDS:
                player_info = game_info.get_player_info()
                active_pos = player_info.active_character_position
                character_info = player_info.characters[active_pos.value]
                # character_card = CHARACTER_CARDS[
                #     CHARACTER_NAME2ID[character_info.character.name]
                # ]
                character_card = KamisatoAyaka()
                if character_info.character.health_point <= 0:
                    alive_positions = [
                        CharPos(k)
                        for k, character in enumerate(player_info.characters)
                        if character.character.alive
                    ]
                    return ChangeCharacterAction(
                        position=alive_positions[0], dice_idx=[]
                    )
                character_element = character_card.element_type
                current_dice = player_info.dice_zone
                skill_names = [skill.name for skill in character_card.skills]                
                elemental_skill = character_card.get_skill(skill_type=SkillType.ELEMENTAL_SKILL)
                dice_idx = self.get_dice_idx_greedy(current_dice, elemental_skill.costs, character_card.element_type)
                if len(dice_idx) > 0:
                    skill_name = elemental_skill.name
                else:
                    # Insufficient dice for elemental skill
                    normal_attack = character_card.get_skill(skill_type=SkillType.NORMAL_ATTACK)
                    dice_idx = self.get_dice_idx_greedy(current_dice, normal_attack.costs, character_card.element_type)
                    if len(dice_idx) > 0:
                        skill_name = normal_attack.name
                    else:
                        # No skill applicable
                        return DeclareEndAction()
                    
                return UseSkillAction(
                    user_position=active_pos,
                    skill_name=skill_name,
                    dice_idx=dice_idx,
                    skill_targets=[
                        (
                            ~self.player_id,
                            game_info.get_opponent_info().active_character_position,
                        )
                    ],
                )

        return DeclareEndAction()
