from gisim.classes.enums import CharacterPosition, ElementType, PlayerID
from gisim.classes.message import PayCardCostMsg


msg = PayCardCostMsg(card_idx=0, card_user_position=CharacterPosition.ACTIVE_CHARACTER, 
                     card_target=[], sender_id=PlayerID.PLAYER1, required_cost={ElementType.ANY:3})

print(msg)