from gisim.classes.enums import *
from gisim.classes.entity import Entity

# 可附着元素列表
can_attachable_element_list = [
    ElementType.CRYO, ElementType.DENDRO, ElementType.ELECTRO, ElementType.HYDRO]


def can_attachable(element: ElementType):
    """是否为可附着元素"""
    return element in can_attachable_element_list

class ElementalReaction(Entity):
    """元素反应"""
    def __init__(self) -> None:
        pass

    def effect(self):
        """反应的效果，比如：
        对目标以外的所有敌方角色造成1点穿透伤害 - 后台伤害
        使目标角色附属[冻结]状态 - 添加角色状态
        生成[燃烧烈焰] - 召唤物
        """
        pass

    def increased_bonuses(self):
        """反应的增益：本伤害+2"""
        pass


if __name__ == "__main__":
    print(can_attachable(ElementType.ANEMO))
