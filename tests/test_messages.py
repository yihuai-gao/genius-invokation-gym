from gisim.classes.enums import CharPos, ElementType, PlayerID, RegionType
from gisim.classes.message import PayCardCostMsg


msg = PayCardCostMsg(card_idx=0, card_user_pos=CharPos.ACTIVE, 
                     sender_id=PlayerID.PLAYER1, required_cost={ElementType.ANY:3})

print(msg)