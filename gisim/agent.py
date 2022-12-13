"""Player & agent APIs
"""
from abc import ABC, abstractmethod
from typing import OrderedDict

from cards.characters.base import CHARACTER_CARDS, CHARACTER_NAME2ID
from classes.message import ChangeCharacterMsg

from gisim.classes.action import Action, ChangeCardsAction, ChangeCharacterAction, DeclareEndAction, RollDiceAction, UseSkillAction
from gisim.classes.enums import CharacterPosition, ElementType, GameStatus, GamePhase, PlayerID
from gisim.game import GameInfo


class Agent(ABC):
    def __init__(self, player_id: PlayerID):
        self.player_id = player_id

    @abstractmethod
    def take_action(self, game_info: OrderedDict) -> Action:
        pass


class AttackOnlyAgent(Agent):
    def __init__(self, player_id: PlayerID):
        super().__init__(player_id)

    def take_action(self, game_info: GameInfo) -> Action:
        if game_info.status == GameStatus.INITIALIZING:
            if game_info.phase == GamePhase.CHANGE_CARD:
                return ChangeCardsAction([])
            elif game_info.phase == GamePhase.SELECT_ACTIVE_CHARACTER:
                return ChangeCharacterAction(CharacterPosition.MIDDLE)
            elif game_info.phase == GamePhase.ROLL_DICE:
                return RollDiceAction([])
            
        elif game_info.status == GameStatus.RUNNING:
            if game_info.phase == GamePhase.ROLL_DICE:
                return RollDiceAction([])
            elif game_info.phase == GamePhase.PLAY_CARDS:
                player_info = game_info.get_player_info()
                active_pos = player_info.active_character_position
                character_info = player_info.character_zone[active_pos.value]
                character_card = CHARACTER_CARDS[CHARACTER_NAME2ID[character_info.name]]
                character_element = character_card.element_type
                current_dice = player_info.element_zone
                skill_names = [skill.name for skill in character_card.skills]
                if len(current_dice) >= 3 and current_dice.count(character_element) + current_dice.count(ElementType.OMNI) >= 1:
                    correct = []
                    omni = []
                    unaligned = []
                    for k, die in enumerate(current_dice):
                        if die == character_element:
                            correct.append(k)
                        elif die == ElementType.OMNI:
                            omni.append(k)
                        else:
                            unaligned.append(k)
                    if len(unaligned) >= 2:
                        dice_idx = [correct[0] if len(correct)>1 else omni[0], unaligned[0], unaligned[1]]  
                    else:
                        dice_idx = unaligned + (correct+omni)[:3-len(unaligned)]
                    return UseSkillAction(active_pos, skill_names[0], dice_idx, game_info.get_opponent_info().active_character_position)

                else:
                    return DeclareEndAction()
            elif game_info.phase == GamePhase.SELECT_ACTIVE_CHARACTER:
                player_info = game_info.get_player_info()
                characters = player_info.character_zone
                alive_positions = [CharacterPosition(k) for k, character in enumerate(characters) if character.alive]
                return ChangeCharacterAction(alive_positions[0])     






        
