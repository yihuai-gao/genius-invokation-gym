from typing import List

from gisim.classes.enums import ElementType, ReactionType
from gisim.classes.reaction import (
    can_attachable,
    element_reaction,
    get_reaction_system,
    get_reaction_system_by_type,
    sum_element_reaction,
)

# 获取反应体系 多元素反应

# Character 附着的元素 冰 草
elemental_attachment: List[ElementType] = [ElementType.CRYO, ElementType.DENDRO]

# 受到元素伤害 水
dmg_element: ElementType = ElementType.HYDRO

print(globals())
if __name__ == "__main__":
    # print(can_attachable(ElementType.HYDRO))
    print(f"角色初始附着的元素：{elemental_attachment}\n受到元素攻击：{dmg_element}")
    reaction_name, effect = None, None
    reaction_attachment, reaction = element_reaction(elemental_attachment, dmg_element)
    if reaction_attachment is not None:
        reaction_name, effect = reaction.name, reaction.effect_text

    print(f"发生元素反应：{reaction_name}\n产生了效果：{effect}\n更新附着状态：{reaction_attachment}")
