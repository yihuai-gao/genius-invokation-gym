"""
This files will generate character cards from "gisim/resources/cards_20221205_en-us.json"
"""
from gisim.classes.enums import ElementType, Nation, SkillType, WeaponType
from gisim.cards.characters.base import CharacterCard, CharacterSkill
from typing import Type
from collections import defaultdict
import re
import os
import json
all_role_card = [
    {
        "id": 1101,
        "name": "Ganyu",
        "element_type": "ETIce",
        "rank_id": 1101,
        "role_skill_infos": [
            {
                "skill_text": "Deals 2 <color=#FFFFFFFF>Physical DMG</color>.",
                "skill_costs": [
                    {
                        "cost_num": "1",
                        "cost_icon": "11"
                    },
                    {
                        "cost_num": "2",
                        "cost_icon": "10"
                    }
                ],
                "type": [
                    "Normal Attack",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/5d510bb74d2c14e2fe53edbdfc955ba4.png",
                "name": "Liutian Archery",
                "id": "11011"
            },
            {
                "skill_text": "Deals 1 <color=#99FFFFFF>Cryo DMG</color>, creates 1 <color=#FFFFFFFF>Ice Lotus</color>.",
                "skill_costs": [
                    {
                        "cost_num": "3",
                        "cost_icon": "11"
                    },
                    {
                        "cost_num": "",
                        "cost_icon": ""
                    }
                ],
                "type": [
                    "Elemental Skill",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/80d61bdb70eef0d57ca877bb39dbb0d9.png",
                "name": "Trail of the Qilin",
                "id": "11012"
            },
            {
                "skill_text": "Deals 2 <color=#99FFFFFF>Cryo DMG</color>, deals <color=#FFFFFFFF>2 <color=#FFFFFFFF>Piercing DMG</color></color> to all opposing characters on standby.",
                "skill_costs": [
                    {
                        "cost_num": "5",
                        "cost_icon": "11"
                    },
                    {
                        "cost_num": "",
                        "cost_icon": ""
                    }
                ],
                "type": [
                    "Normal Attack",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/5d510bb74d2c14e2fe53edbdfc955ba4.png",
                "name": "Frostflake Arrow",
                "id": "11013"
            },
            {
                "skill_text": "Deals 1 <color=#99FFFFFF>Cryo DMG</color>, deals <color=#FFFFFFFF>1 <color=#FFFFFFFF>Piercing DMG</color></color> to all opposing characters on standby, summons 1 <color=#FFFFFFFF>Sacred Cryo Pearl</color>.",
                "skill_costs": [
                    {
                        "cost_num": "3",
                        "cost_icon": "11"
                    },
                    {
                        "cost_num": "2",
                        "cost_icon": "1"
                    }
                ],
                "type": [
                    "Elemental Burst",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/fcda5c89f7d783e8bff69719c0d30692.png",
                "name": "Celestial Shower",
                "id": "11014"
            }
        ],
        "weapon": "Bow",
        "belong_to": [
            "Liyue",
            "",
            ""
        ],
        "hp": "10",
        "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/dec5ba575fc5720ec15b8964a826f2b5.png"
    },
    {
        "id": 1102,
        "name": "Diona",
        "element_type": "ETIce",
        "rank_id": 1102,
        "role_skill_infos": [
            {
                "skill_text": "Deals 2 <color=#FFFFFFFF>Physical DMG</color>.",
                "skill_costs": [
                    {
                        "cost_num": "1",
                        "cost_icon": "11"
                    },
                    {
                        "cost_num": "2",
                        "cost_icon": "10"
                    }
                ],
                "type": [
                    "Normal Attack",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/5d510bb74d2c14e2fe53edbdfc955ba4.png",
                "name": "Kätzlein Style",
                "id": "11021"
            },
            {
                "skill_text": "Deals 2 <color=#99FFFFFF>Cryo DMG</color>, creates 1 <color=#FFFFFFFF>Cat-Claw Shield</color>.",
                "skill_costs": [
                    {
                        "cost_num": "3",
                        "cost_icon": "11"
                    },
                    {
                        "cost_num": "",
                        "cost_icon": ""
                    }
                ],
                "type": [
                    "Elemental Skill",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/90c513d6b26cc20a6ce30fb82750f2e7.png",
                "name": "Icy Paws",
                "id": "11022"
            },
            {
                "skill_text": "Deals 1 <color=#99FFFFFF>Cryo DMG</color>, heals this character for 2 HP, summons 1 <color=#FFFFFFFF>Drunken Mist</color>.",
                "skill_costs": [
                    {
                        "cost_num": "3",
                        "cost_icon": "11"
                    },
                    {
                        "cost_num": "3",
                        "cost_icon": "1"
                    }
                ],
                "type": [
                    "Elemental Burst",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/6ab5e0c2e95117950515b23a875006c0.png",
                "name": "Signature Mix",
                "id": "11023"
            }
        ],
        "weapon": "Bow",
        "belong_to": [
            "Mondstadt",
            "",
            ""
        ],
        "hp": "10",
        "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/7c8b166b3254b11d33a5bc1b78fb3034.png"
    },
    {
        "id": 1103,
        "name": "Kaeya",
        "element_type": "ETIce",
        "rank_id": 1103,
        "role_skill_infos": [
            {
                "skill_text": "Deals 2 <color=#FFFFFFFF>Physical DMG</color>.",
                "skill_costs": [
                    {
                        "cost_num": "1",
                        "cost_icon": "11"
                    },
                    {
                        "cost_num": "2",
                        "cost_icon": "10"
                    }
                ],
                "type": [
                    "Normal Attack",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/3d73149ed08fc08529476d7f1b4a5db2.png",
                "name": "Ceremonial Bladework",
                "id": "11031"
            },
            {
                "skill_text": "Deals 3 <color=#99FFFFFF>Cryo DMG</color>.",
                "skill_costs": [
                    {
                        "cost_num": "3",
                        "cost_icon": "11"
                    },
                    {
                        "cost_num": "",
                        "cost_icon": ""
                    }
                ],
                "type": [
                    "Elemental Skill",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/de0abe0fb5f2904c8695d4207f472cdb.png",
                "name": "Frostgnaw",
                "id": "11032"
            },
            {
                "skill_text": "Deals 1 <color=#99FFFFFF>Cryo DMG</color>, creates 1 <color=#FFFFFFFF>Icicle</color>.",
                "skill_costs": [
                    {
                        "cost_num": "4",
                        "cost_icon": "11"
                    },
                    {
                        "cost_num": "2",
                        "cost_icon": "1"
                    }
                ],
                "type": [
                    "Elemental Burst",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/f9e5cb46ba3bf6d4ec2f9e4455dc6238.png",
                "name": "Glacial Waltz",
                "id": "11033"
            }
        ],
        "weapon": "Sword",
        "belong_to": [
            "Mondstadt",
            "",
            ""
        ],
        "hp": "10",
        "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/877beb9d2fa9201737f43b12b68a7c41.png"
    },
    {
        "id": 1104,
        "name": "Chongyun",
        "element_type": "ETIce",
        "rank_id": 1104,
        "role_skill_infos": [
            {
                "skill_text": "Deals 2 <color=#FFFFFFFF>Physical DMG</color>.",
                "skill_costs": [
                    {
                        "cost_num": "1",
                        "cost_icon": "11"
                    },
                    {
                        "cost_num": "2",
                        "cost_icon": "10"
                    }
                ],
                "type": [
                    "Normal Attack",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/1f2774a0570701e52f573952cd3436ce.png",
                "name": "Demonbane",
                "id": "11041"
            },
            {
                "skill_text": "Deals 3 <color=#99FFFFFF>Cryo DMG</color>, creates 1 <color=#FFFFFFFF>Chonghua Frost Field</color>.",
                "skill_costs": [
                    {
                        "cost_num": "3",
                        "cost_icon": "11"
                    },
                    {
                        "cost_num": "",
                        "cost_icon": ""
                    }
                ],
                "type": [
                    "Elemental Skill",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/e023be3e82b38b50202ecf4d4fb0fa81.png",
                "name": "Chonghua's Layered Frost",
                "id": "11042"
            },
            {
                "skill_text": "Deals 7 <color=#99FFFFFF>Cryo DMG</color>.",
                "skill_costs": [
                    {
                        "cost_num": "3",
                        "cost_icon": "11"
                    },
                    {
                        "cost_num": "3",
                        "cost_icon": "1"
                    }
                ],
                "type": [
                    "Elemental Burst",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/153a77400dc95c9b51733d0d0d9a4ac0.png",
                "name": "Cloud-Parting Star",
                "id": "11043"
            }
        ],
        "weapon": "Claymore",
        "belong_to": [
            "Liyue",
            "",
            ""
        ],
        "hp": "10",
        "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/5e61c140b9a2e5bed18c09c8d1115150.png"
    },
    {
        "id": 1105,
        "name": "Kamisato Ayaka",
        "element_type": "ETIce",
        "rank_id": 1105,
        "role_skill_infos": [
            {
                "skill_text": "Deals 2 <color=#FFFFFFFF>Physical DMG</color>.",
                "skill_costs": [
                    {
                        "cost_num": "1",
                        "cost_icon": "11"
                    },
                    {
                        "cost_num": "2",
                        "cost_icon": "10"
                    }
                ],
                "type": [
                    "Normal Attack",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/3d73149ed08fc08529476d7f1b4a5db2.png",
                "name": "Kamisato Art: Kabuki",
                "id": "11051"
            },
            {
                "skill_text": "Deals 3 <color=#99FFFFFF>Cryo DMG</color>.",
                "skill_costs": [
                    {
                        "cost_num": "3",
                        "cost_icon": "11"
                    },
                    {
                        "cost_num": "",
                        "cost_icon": ""
                    }
                ],
                "type": [
                    "Elemental Skill",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/7b59308313512c3c7350eb6a92b3ea27.png",
                "name": "Kamisato Art: Hyouka",
                "id": "11052"
            },
            {
                "skill_text": "Deals 4 <color=#99FFFFFF>Cryo DMG</color>, summons 1 <color=#FFFFFFFF>Frostflake Seki no To</color>.",
                "skill_costs": [
                    {
                        "cost_num": "3",
                        "cost_icon": "11"
                    },
                    {
                        "cost_num": "3",
                        "cost_icon": "1"
                    }
                ],
                "type": [
                    "Elemental Burst",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/3668bb20f0b7fb4cfb1fb4162d6fa28f.png",
                "name": "Kamisato Art: Soumetsu",
                "id": "11053"
            },
            {
                "skill_text": "(Passive) When switched to be the active character, this character gains <color=#FFFFFFFF>Cryo Elemental Infusion</color>.",
                "skill_costs": [
                    {
                        "cost_num": "",
                        "cost_icon": ""
                    },
                    {
                        "cost_num": "",
                        "cost_icon": ""
                    }
                ],
                "type": [
                    "Passive Skill",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/959584488f20484942c1403df073f954.png",
                "name": "Kamisato Art: Senho",
                "id": "11054"
            }
        ],
        "weapon": "Sword",
        "belong_to": [
            "Inazuma",
            "",
            ""
        ],
        "hp": "10",
        "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/3c864f3a914d0de0a416e25f0234fe89.png"
    },
    {
        "id": 1201,
        "name": "Barbara",
        "element_type": "ETWater",
        "rank_id": 1201,
        "role_skill_infos": [
            {
                "skill_text": "Deals 1 <color=#80C0FFFF>Hydro DMG</color>.",
                "skill_costs": [
                    {
                        "cost_num": "1",
                        "cost_icon": "12"
                    },
                    {
                        "cost_num": "2",
                        "cost_icon": "10"
                    }
                ],
                "type": [
                    "Normal Attack",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/a51c9140615f7682c79e6dd2af3366e4.png",
                "name": "Whisper of Water",
                "id": "12011"
            },
            {
                "skill_text": "Deals 1 <color=#80C0FFFF>Hydro DMG</color>, summons 1 <color=#FFFFFFFF>Melody Loop</color>.",
                "skill_costs": [
                    {
                        "cost_num": "3",
                        "cost_icon": "12"
                    },
                    {
                        "cost_num": "",
                        "cost_icon": ""
                    }
                ],
                "type": [
                    "Elemental Skill",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/63c2345902423b25788f104985348cfd.png",
                "name": "Let the Show Begin♪",
                "id": "12012"
            },
            {
                "skill_text": "Heals all of your characters for 4 HP.",
                "skill_costs": [
                    {
                        "cost_num": "3",
                        "cost_icon": "12"
                    },
                    {
                        "cost_num": "3",
                        "cost_icon": "1"
                    }
                ],
                "type": [
                    "Elemental Burst",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/8da9eff0a67380b83cb6c3360e509695.png",
                "name": "Shining Miracle♪",
                "id": "12013"
            }
        ],
        "weapon": "Catalyst",
        "belong_to": [
            "Mondstadt",
            "",
            ""
        ],
        "hp": "10",
        "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/9e4098dbdaac941957fb3af0e34bac6e.png"
    },
    {
        "id": 1202,
        "name": "Xingqiu",
        "element_type": "ETWater",
        "rank_id": 1202,
        "role_skill_infos": [
            {
                "skill_text": "Deals 2 <color=#FFFFFFFF>Physical DMG</color>.",
                "skill_costs": [
                    {
                        "cost_num": "1",
                        "cost_icon": "12"
                    },
                    {
                        "cost_num": "2",
                        "cost_icon": "10"
                    }
                ],
                "type": [
                    "Normal Attack",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/3d73149ed08fc08529476d7f1b4a5db2.png",
                "name": "Guhua Style",
                "id": "12021"
            },
            {
                "skill_text": "Deals 2 <color=#80C0FFFF>Hydro DMG</color>, grants this character <color=#80C0FFFF>Hydro Application</color>, creates 1 <color=#FFFFFFFF>Rain Sword</color>.",
                "skill_costs": [
                    {
                        "cost_num": "3",
                        "cost_icon": "12"
                    },
                    {
                        "cost_num": "",
                        "cost_icon": ""
                    }
                ],
                "type": [
                    "Elemental Skill",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/5578cdac2dd8187149544e0898ddf1fd.png",
                "name": "Fatal Rainscreen",
                "id": "12022"
            },
            {
                "skill_text": "Deals 1 <color=#80C0FFFF>Hydro DMG</color>, grants this character <color=#80C0FFFF>Hydro Application</color>, creates 1 <color=#FFFFFFFF>Rainbow Bladework</color>.",
                "skill_costs": [
                    {
                        "cost_num": "3",
                        "cost_icon": "12"
                    },
                    {
                        "cost_num": "2",
                        "cost_icon": "1"
                    }
                ],
                "type": [
                    "Elemental Burst",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/41d0bb68b4558ff4583b48268b5ecb1b.png",
                "name": "Raincutter",
                "id": "12023"
            }
        ],
        "weapon": "Sword",
        "belong_to": [
            "Liyue",
            "",
            ""
        ],
        "hp": "10",
        "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/4fed2d8054aa757b8081d5cfc8dbc5e5.png"
    },
    {
        "id": 1203,
        "name": "Mona",
        "element_type": "ETWater",
        "rank_id": 1203,
        "role_skill_infos": [
            {
                "skill_text": "Deals 1 <color=#80C0FFFF>Hydro DMG</color>.",
                "skill_costs": [
                    {
                        "cost_num": "1",
                        "cost_icon": "12"
                    },
                    {
                        "cost_num": "2",
                        "cost_icon": "10"
                    }
                ],
                "type": [
                    "Normal Attack",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/a51c9140615f7682c79e6dd2af3366e4.png",
                "name": "Ripple of Fate",
                "id": "12031"
            },
            {
                "skill_text": "Deals 1 <color=#80C0FFFF>Hydro DMG</color>, summons 1 <color=#FFFFFFFF>Reflection</color>.",
                "skill_costs": [
                    {
                        "cost_num": "3",
                        "cost_icon": "12"
                    },
                    {
                        "cost_num": "",
                        "cost_icon": ""
                    }
                ],
                "type": [
                    "Elemental Skill",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/c821ff150eb08b2512e3bfa39c19b20d.png",
                "name": "Mirror Reflection of Doom",
                "id": "12032"
            },
            {
                "skill_text": "Deals 4 <color=#80C0FFFF>Hydro DMG</color>, creates 1 <color=#FFFFFFFF>Illusory Bubble</color>.",
                "skill_costs": [
                    {
                        "cost_num": "3",
                        "cost_icon": "12"
                    },
                    {
                        "cost_num": "3",
                        "cost_icon": "1"
                    }
                ],
                "type": [
                    "Elemental Burst",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/bd9c6c5db4f7cfd3ce555aaa00a4a1dd.png",
                "name": "Stellaris Phantasm",
                "id": "12033"
            },
            {
                "skill_text": "(Passive) <color=#FFFFFFFF>When you perform \"Switch Character\" while Mona is your active character:</color> This switch is considered a <color=#FFFFFFFF>Fast Action</color> instead of a <color=#FFFFFFFF>Combat Action</color>. (Once per Round)",
                "skill_costs": [
                    {
                        "cost_num": "",
                        "cost_icon": ""
                    },
                    {
                        "cost_num": "",
                        "cost_icon": ""
                    }
                ],
                "type": [
                    "Passive Skill",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/6c924aed33d3b0cbdcd6b280c2b52631.png",
                "name": "Illusory Torrent",
                "id": "12034"
            }
        ],
        "weapon": "Catalyst",
        "belong_to": [
            "Mondstadt",
            "",
            ""
        ],
        "hp": "10",
        "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/e6031f667a1da4f83bc75ab5a5e868a0.png"
    },
    {
        "id": 1301,
        "name": "Diluc",
        "element_type": "ETFire",
        "rank_id": 1301,
        "role_skill_infos": [
            {
                "skill_text": "Deals 2 <color=#FFFFFFFF>Physical DMG</color>.",
                "skill_costs": [
                    {
                        "cost_num": "1",
                        "cost_icon": "13"
                    },
                    {
                        "cost_num": "2",
                        "cost_icon": "10"
                    }
                ],
                "type": [
                    "Normal Attack",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/1f2774a0570701e52f573952cd3436ce.png",
                "name": "Tempered Sword",
                "id": "13011"
            },
            {
                "skill_text": "Deals 3 <color=#FF9999FF>Pyro DMG</color>. For the third use of this Skill each Round, deals +2 DMG.",
                "skill_costs": [
                    {
                        "cost_num": "3",
                        "cost_icon": "13"
                    },
                    {
                        "cost_num": "",
                        "cost_icon": ""
                    }
                ],
                "type": [
                    "Elemental Skill",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/31863c524d54277f038d60c77c8a85ef.png",
                "name": "Searing Onslaught",
                "id": "13012"
            },
            {
                "skill_text": "Deals 8 <color=#FF9999FF>Pyro DMG</color>. This character gains <color=#FFFFFFFF>Pyro Infusion</color>.",
                "skill_costs": [
                    {
                        "cost_num": "4",
                        "cost_icon": "13"
                    },
                    {
                        "cost_num": "3",
                        "cost_icon": "1"
                    }
                ],
                "type": [
                    "Elemental Burst",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/441499b2202e58aa6df0ebbd21bb4f67.png",
                "name": "Dawn",
                "id": "13013"
            }
        ],
        "weapon": "Claymore",
        "belong_to": [
            "Mondstadt",
            "",
            ""
        ],
        "hp": "10",
        "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/c00f19ba52c4497b81f1654c705240b8.png"
    },
    {
        "id": 1302,
        "name": "Xiangling",
        "element_type": "ETFire",
        "rank_id": 1302,
        "role_skill_infos": [
            {
                "skill_text": "Deals 2 <color=#FFFFFFFF>Physical DMG</color>.",
                "skill_costs": [
                    {
                        "cost_num": "1",
                        "cost_icon": "13"
                    },
                    {
                        "cost_num": "2",
                        "cost_icon": "10"
                    }
                ],
                "type": [
                    "Normal Attack",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/eff1794fed54da5f9132873f84b6f41c.png",
                "name": "Dough-Fu",
                "id": "13021"
            },
            {
                "skill_text": "Summons 1 <color=#FFFFFFFF>Guoba</color>.",
                "skill_costs": [
                    {
                        "cost_num": "3",
                        "cost_icon": "13"
                    },
                    {
                        "cost_num": "",
                        "cost_icon": ""
                    }
                ],
                "type": [
                    "Elemental Skill",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/5a6d6002064487f449b61a96300a79b8.png",
                "name": "Guoba Attack",
                "id": "13022"
            },
            {
                "skill_text": "Deals 2 <color=#FF9999FF>Pyro DMG</color>, creates 1 <color=#FFFFFFFF>Pyronado</color>.",
                "skill_costs": [
                    {
                        "cost_num": "4",
                        "cost_icon": "13"
                    },
                    {
                        "cost_num": "2",
                        "cost_icon": "1"
                    }
                ],
                "type": [
                    "Elemental Burst",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/4a5ced0f3db7bd4a0553f837544ecb99.png",
                "name": "Pyronado",
                "id": "13023"
            }
        ],
        "weapon": "Polearm",
        "belong_to": [
            "Liyue",
            "",
            ""
        ],
        "hp": "10",
        "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/f6f310d5276e6d7656eb5b42913ec8b0.png"
    },
    {
        "id": 1303,
        "name": "Bennett",
        "element_type": "ETFire",
        "rank_id": 1303,
        "role_skill_infos": [
            {
                "skill_text": "Deals 2 <color=#FFFFFFFF>Physical DMG</color>.",
                "skill_costs": [
                    {
                        "cost_num": "1",
                        "cost_icon": "13"
                    },
                    {
                        "cost_num": "2",
                        "cost_icon": "10"
                    }
                ],
                "type": [
                    "Normal Attack",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/3d73149ed08fc08529476d7f1b4a5db2.png",
                "name": "Strike of Fortune",
                "id": "13031"
            },
            {
                "skill_text": "Deals 3 <color=#FF9999FF>Pyro DMG</color>.",
                "skill_costs": [
                    {
                        "cost_num": "3",
                        "cost_icon": "13"
                    },
                    {
                        "cost_num": "",
                        "cost_icon": ""
                    }
                ],
                "type": [
                    "Elemental Skill",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/3b102a63444d271b250d9b199568bd79.png",
                "name": "Passion Overload",
                "id": "13032"
            },
            {
                "skill_text": "Deals 2 <color=#FF9999FF>Pyro DMG</color>, creates 1 <color=#FFFFFFFF>Inspiration Field</color>.",
                "skill_costs": [
                    {
                        "cost_num": "4",
                        "cost_icon": "13"
                    },
                    {
                        "cost_num": "2",
                        "cost_icon": "1"
                    }
                ],
                "type": [
                    "Elemental Burst",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/a0063dea821a2e70e3ad6d8731e65c44.png",
                "name": "Fantastic Voyage",
                "id": "13033"
            }
        ],
        "weapon": "Sword",
        "belong_to": [
            "Mondstadt",
            "",
            ""
        ],
        "hp": "10",
        "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/6d539b8c4ec001cf0e651bf2af3b828d.png"
    },
    {
        "id": 1305,
        "name": "Yoimiya",
        "element_type": "ETFire",
        "rank_id": 1305,
        "role_skill_infos": [
            {
                "skill_text": "Deals 2 <color=#FFFFFFFF>Physical DMG</color>.",
                "skill_costs": [
                    {
                        "cost_num": "1",
                        "cost_icon": "13"
                    },
                    {
                        "cost_num": "2",
                        "cost_icon": "10"
                    }
                ],
                "type": [
                    "Normal Attack",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/5d510bb74d2c14e2fe53edbdfc955ba4.png",
                "name": "Firework Flare-Up",
                "id": "13051"
            },
            {
                "skill_text": "This character gains <color=#FFFFFFFF>Niwabi Enshou</color>. (This Skill does not grant Energy)",
                "skill_costs": [
                    {
                        "cost_num": "1",
                        "cost_icon": "13"
                    },
                    {
                        "cost_num": "",
                        "cost_icon": ""
                    }
                ],
                "type": [
                    "Elemental Skill",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/bd53cae9bde22c0efae9e696adf58b3b.png",
                "name": "Niwabi Fire-Dance",
                "id": "13052"
            },
            {
                "skill_text": "Deals 4 <color=#FF9999FF>Pyro DMG</color>, creates 1 <color=#FFFFFFFF>Aurous Blaze</color>.",
                "skill_costs": [
                    {
                        "cost_num": "4",
                        "cost_icon": "13"
                    },
                    {
                        "cost_num": "3",
                        "cost_icon": "1"
                    }
                ],
                "type": [
                    "Elemental Burst",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/a7ce012f5ae1e409862e6b98c3367391.png",
                "name": "Ryuukin Saxifrage",
                "id": "13053"
            }
        ],
        "weapon": "Bow",
        "belong_to": [
            "Inazuma",
            "",
            ""
        ],
        "hp": "10",
        "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/55c408c3b086c396d35a734e0ac61691.png"
    },
    {
        "id": 1306,
        "name": "Klee",
        "element_type": "ETFire",
        "rank_id": 1306,
        "role_skill_infos": [
            {
                "skill_text": "Deals 1 <color=#FF9999FF>Pyro DMG</color>.",
                "skill_costs": [
                    {
                        "cost_num": "1",
                        "cost_icon": "13"
                    },
                    {
                        "cost_num": "2",
                        "cost_icon": "10"
                    }
                ],
                "type": [
                    "Normal Attack",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/a51c9140615f7682c79e6dd2af3366e4.png",
                "name": "Kaboom!",
                "id": "13061"
            },
            {
                "skill_text": "Deals 3 <color=#FF9999FF>Pyro DMG</color>. This character gains <color=#FFFFFFFF>Explosive Spark</color>.",
                "skill_costs": [
                    {
                        "cost_num": "3",
                        "cost_icon": "13"
                    },
                    {
                        "cost_num": "",
                        "cost_icon": ""
                    }
                ],
                "type": [
                    "Elemental Skill",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/b6c61b3c6f8bba28a55db50de81707bd.png",
                "name": "Jumpy Dumpty",
                "id": "13062"
            },
            {
                "skill_text": "Deals 3 <color=#FF9999FF>Pyro DMG</color>, creates 1 <color=#FFFFFFFF>Sparks 'n' Splash</color> at the opponent's play area.",
                "skill_costs": [
                    {
                        "cost_num": "3",
                        "cost_icon": "13"
                    },
                    {
                        "cost_num": "3",
                        "cost_icon": "1"
                    }
                ],
                "type": [
                    "Elemental Burst",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/3128faa41c9d7b52c3df95b34d29057a.png",
                "name": "Sparks 'n' Splash",
                "id": "13063"
            }
        ],
        "weapon": "Catalyst",
        "belong_to": [
            "Mondstadt",
            "",
            ""
        ],
        "hp": "10",
        "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/795f644590f0079f119b36638d81e7e5.png"
    },
    {
        "id": 1401,
        "name": "Fischl",
        "element_type": "ETThunder",
        "rank_id": 1401,
        "role_skill_infos": [
            {
                "skill_text": "Deals 2 <color=#FFFFFFFF>Physical DMG</color>.",
                "skill_costs": [
                    {
                        "cost_num": "1",
                        "cost_icon": "14"
                    },
                    {
                        "cost_num": "2",
                        "cost_icon": "10"
                    }
                ],
                "type": [
                    "Normal Attack",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/5d510bb74d2c14e2fe53edbdfc955ba4.png",
                "name": "Bolts of Downfall",
                "id": "14011"
            },
            {
                "skill_text": "Deals 1 <color=#FFACFFFF>Electro DMG</color>, summons 1 <color=#FFFFFFFF>Oz</color>.",
                "skill_costs": [
                    {
                        "cost_num": "3",
                        "cost_icon": "14"
                    },
                    {
                        "cost_num": "",
                        "cost_icon": ""
                    }
                ],
                "type": [
                    "Elemental Skill",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/4b4b654a14e8ca726e105af1666f4fc4.png",
                "name": "Nightrider",
                "id": "14012"
            },
            {
                "skill_text": "Deals 4 <color=#FFACFFFF>Electro DMG</color>, deals 2 <color=#FFFFFFFF><color=#FFFFFFFF>Piercing DMG</color></color> to all opposing characters on standby.",
                "skill_costs": [
                    {
                        "cost_num": "3",
                        "cost_icon": "14"
                    },
                    {
                        "cost_num": "3",
                        "cost_icon": "1"
                    }
                ],
                "type": [
                    "Elemental Burst",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/a51f354b2f813bfc1de68460be40d435.png",
                "name": "Midnight Phantasmagoria",
                "id": "14013"
            }
        ],
        "weapon": "Bow",
        "belong_to": [
            "Mondstadt",
            "",
            ""
        ],
        "hp": "10",
        "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/b9dbb5a2cf9c0ceb63443f7409d19fe7.png"
    },
    {
        "id": 1402,
        "name": "Razor",
        "element_type": "ETThunder",
        "rank_id": 1402,
        "role_skill_infos": [
            {
                "skill_text": "Deals 2 <color=#FFFFFFFF>Physical DMG</color>.",
                "skill_costs": [
                    {
                        "cost_num": "1",
                        "cost_icon": "14"
                    },
                    {
                        "cost_num": "2",
                        "cost_icon": "10"
                    }
                ],
                "type": [
                    "Normal Attack",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/1f2774a0570701e52f573952cd3436ce.png",
                "name": "Steel Fang",
                "id": "14021"
            },
            {
                "skill_text": "Deals 3 <color=#FFACFFFF>Electro DMG</color>.",
                "skill_costs": [
                    {
                        "cost_num": "3",
                        "cost_icon": "14"
                    },
                    {
                        "cost_num": "",
                        "cost_icon": ""
                    }
                ],
                "type": [
                    "Elemental Skill",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/efb029187262b0892b0a85a7be3c81c6.png",
                "name": "Claw and Thunder",
                "id": "14022"
            },
            {
                "skill_text": "Deals 5 <color=#FFACFFFF>Electro DMG</color>. This character gains <color=#FFFFFFFF>The Wolf Within</color>.",
                "skill_costs": [
                    {
                        "cost_num": "3",
                        "cost_icon": "14"
                    },
                    {
                        "cost_num": "3",
                        "cost_icon": "1"
                    }
                ],
                "type": [
                    "Elemental Burst",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/43720b9540661d37f397adddc08f984d.png",
                "name": "Lightning Fang",
                "id": "14023"
            }
        ],
        "weapon": "Claymore",
        "belong_to": [
            "Mondstadt",
            "",
            ""
        ],
        "hp": "10",
        "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/00e87c7e7518713e3bc65c12068c598a.png"
    },
    {
        "id": 1403,
        "name": "Keqing",
        "element_type": "ETThunder",
        "rank_id": 1403,
        "role_skill_infos": [
            {
                "skill_text": "Deals 2 <color=#FFFFFFFF>Physical DMG</color>.",
                "skill_costs": [
                    {
                        "cost_num": "1",
                        "cost_icon": "14"
                    },
                    {
                        "cost_num": "2",
                        "cost_icon": "10"
                    }
                ],
                "type": [
                    "Normal Attack",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/3d73149ed08fc08529476d7f1b4a5db2.png",
                "name": "Yunlai Swordsmanship",
                "id": "14031"
            },
            {
                "skill_text": "Deals 3 <color=#FFACFFFF>Electro DMG</color>, creates 1 <color=#FFFFFFFF>Lightning Stiletto</color>.",
                "skill_costs": [
                    {
                        "cost_num": "3",
                        "cost_icon": "14"
                    },
                    {
                        "cost_num": "",
                        "cost_icon": ""
                    }
                ],
                "type": [
                    "Elemental Skill",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/eb94518489d930ab5fa02434b64b206e.png",
                "name": "Stellar Restoration",
                "id": "14032"
            },
            {
                "skill_text": "Deals 4 <color=#FFACFFFF>Electro DMG</color>, deals <color=#FFFFFFFF>3 <color=#FFFFFFFF>Piercing DMG</color></color> to all opposing characters on standby.",
                "skill_costs": [
                    {
                        "cost_num": "4",
                        "cost_icon": "14"
                    },
                    {
                        "cost_num": "3",
                        "cost_icon": "1"
                    }
                ],
                "type": [
                    "Elemental Burst",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/4caa9b938cb1e72fa2cf4dca79b51fb8.png",
                "name": "Starward Sword",
                "id": "14033"
            }
        ],
        "weapon": "Sword",
        "belong_to": [
            "Liyue",
            "",
            ""
        ],
        "hp": "10",
        "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/f6f3d3d3b183e676f9912dfec572b237.png"
    },
    {
        "id": 1404,
        "name": "Cyno",
        "element_type": "ETThunder",
        "rank_id": 1404,
        "role_skill_infos": [
            {
                "skill_text": "Deals 2 <color=#FFFFFFFF>Physical DMG</color>.",
                "skill_costs": [
                    {
                        "cost_num": "1",
                        "cost_icon": "14"
                    },
                    {
                        "cost_num": "2",
                        "cost_icon": "10"
                    }
                ],
                "type": [
                    "Normal Attack",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/eff1794fed54da5f9132873f84b6f41c.png",
                "name": "Invoker's Spear",
                "id": "14041"
            },
            {
                "skill_text": "Deals 3 <color=#FFACFFFF>Electro DMG</color>.",
                "skill_costs": [
                    {
                        "cost_num": "3",
                        "cost_icon": "14"
                    },
                    {
                        "cost_num": "",
                        "cost_icon": ""
                    }
                ],
                "type": [
                    "Elemental Skill",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/70d35fde5a93ea9706b5c82e223ed57c.png",
                "name": "Secret Rite: Chasmic Soulfarer",
                "id": "14042"
            },
            {
                "skill_text": "Deals 4 <color=#FFACFFFF>Electro DMG</color>.\\n<color=#FFFFFFFF>Pactsworn Pathclearer</color>'s Indwelling Level +2.",
                "skill_costs": [
                    {
                        "cost_num": "4",
                        "cost_icon": "14"
                    },
                    {
                        "cost_num": "2",
                        "cost_icon": "1"
                    }
                ],
                "type": [
                    "Elemental Burst",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/df77d411c3039ab4c7455f62aa0fe43c.png",
                "name": "Sacred Rite: Wolf's Swiftness",
                "id": "14043"
            },
            {
                "skill_text": "(Passive) When the battle begins, this character gains <color=#FFFFFFFF>Pactsworn Pathclearer</color>.",
                "skill_costs": [
                    {
                        "cost_num": "",
                        "cost_icon": ""
                    },
                    {
                        "cost_num": "",
                        "cost_icon": ""
                    }
                ],
                "type": [
                    "Passive Skill",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/3fee355d6f0090f9079b6a8bd15dd839.png",
                "name": "Lawful Enforcer",
                "id": "14044"
            }
        ],
        "weapon": "Polearm",
        "belong_to": [
            "Sumeru",
            "",
            ""
        ],
        "hp": "10",
        "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/1c0359bdc24635a0808ca2046f00793f.png"
    },
    {
        "id": 1405,
        "name": "Beidou",
        "element_type": "ETThunder",
        "rank_id": 1405,
        "role_skill_infos": [
            {
                "skill_text": "Deals 2 <color=#FFFFFFFF>Physical DMG</color>.",
                "skill_costs": [
                    {
                        "cost_num": "1",
                        "cost_icon": "14"
                    },
                    {
                        "cost_num": "2",
                        "cost_icon": "10"
                    }
                ],
                "type": [
                    "Normal Attack",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/1f2774a0570701e52f573952cd3436ce.png",
                "name": "Oceanborne",
                "id": "14051"
            },
            {
                "skill_text": "This character gains a <color=#FFFFFFFF>Tidecaller: Surf Embrace</color>. <color=#FFFFFFFF>Prepare Skill</color>: <color=#FFFFFFFF>Wavestrider</color>.",
                "skill_costs": [
                    {
                        "cost_num": "3",
                        "cost_icon": "14"
                    },
                    {
                        "cost_num": "",
                        "cost_icon": ""
                    }
                ],
                "type": [
                    "Elemental Skill",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/4a89d425a7012848bd53b30a07db0767.png",
                "name": "Tidecaller",
                "id": "14052"
            },
            {
                "skill_text": "Deals 3 <color=#FFACFFFF>Electro DMG</color>, creates 1 <color=#FFFFFFFF>Thunderbeast's Targe</color>.",
                "skill_costs": [
                    {
                        "cost_num": "4",
                        "cost_icon": "14"
                    },
                    {
                        "cost_num": "3",
                        "cost_icon": "1"
                    }
                ],
                "type": [
                    "Elemental Burst",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/bcacde02f6f83c377022ae8789ece544.png",
                "name": "Stormbreaker",
                "id": "14053"
            },
            {
                "skill_text": "(Prepare for 1 turn)\\nDeals 2 <color=#FFACFFFF>Electro DMG</color>.",
                "skill_costs": [
                    {
                        "cost_num": "",
                        "cost_icon": ""
                    },
                    {
                        "cost_num": "",
                        "cost_icon": ""
                    }
                ],
                "type": [
                    "Elemental Skill",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/4a89d425a7012848bd53b30a07db0767.png",
                "name": "Wavestrider",
                "id": "14054"
            }
        ],
        "weapon": "Claymore",
        "belong_to": [
            "Liyue",
            "",
            ""
        ],
        "hp": "10",
        "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/d4de10020e7ab22dfa52375e20c97590.png"
    },
    {
        "id": 1501,
        "name": "Sucrose",
        "element_type": "ETWind",
        "rank_id": 1501,
        "role_skill_infos": [
            {
                "skill_text": "Deals 1 <color=#80FFD7FF>Anemo DMG</color>.",
                "skill_costs": [
                    {
                        "cost_num": "1",
                        "cost_icon": "17"
                    },
                    {
                        "cost_num": "2",
                        "cost_icon": "10"
                    }
                ],
                "type": [
                    "Normal Attack",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/a51c9140615f7682c79e6dd2af3366e4.png",
                "name": "Wind Spirit Creation",
                "id": "15011"
            },
            {
                "skill_text": "Deals 3 <color=#80FFD7FF>Anemo DMG</color>, the target is forcibly switched to the previous character.",
                "skill_costs": [
                    {
                        "cost_num": "3",
                        "cost_icon": "17"
                    },
                    {
                        "cost_num": "",
                        "cost_icon": ""
                    }
                ],
                "type": [
                    "Elemental Skill",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/6c091fa8a5b6e71ad8b876dd1e45e407.png",
                "name": "Astable Anemohypostasis Creation - 6308",
                "id": "15012"
            },
            {
                "skill_text": "Deals 1 <color=#80FFD7FF>Anemo DMG</color>, summons 1 <color=#FFFFFFFF>Large Wind Spirit</color>.",
                "skill_costs": [
                    {
                        "cost_num": "3",
                        "cost_icon": "17"
                    },
                    {
                        "cost_num": "2",
                        "cost_icon": "1"
                    }
                ],
                "type": [
                    "Elemental Burst",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/38cc0d7de9627cf89d3f19c326d2e890.png",
                "name": "Forbidden Creation - Isomer 75 / Type II",
                "id": "15013"
            }
        ],
        "weapon": "Catalyst",
        "belong_to": [
            "Mondstadt",
            "",
            ""
        ],
        "hp": "10",
        "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/0bef56ba7c462ad8c593096ba6e3af81.png"
    },
    {
        "id": 1502,
        "name": "Jean",
        "element_type": "ETWind",
        "rank_id": 1502,
        "role_skill_infos": [
            {
                "skill_text": "Deals 2 <color=#FFFFFFFF>Physical DMG</color>.",
                "skill_costs": [
                    {
                        "cost_num": "1",
                        "cost_icon": "17"
                    },
                    {
                        "cost_num": "2",
                        "cost_icon": "10"
                    }
                ],
                "type": [
                    "Normal Attack",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/3d73149ed08fc08529476d7f1b4a5db2.png",
                "name": "Favonius Bladework",
                "id": "15021"
            },
            {
                "skill_text": "Deals 3 <color=#80FFD7FF>Anemo DMG</color>, the target is forcibly switched to the next character.",
                "skill_costs": [
                    {
                        "cost_num": "3",
                        "cost_icon": "17"
                    },
                    {
                        "cost_num": "",
                        "cost_icon": ""
                    }
                ],
                "type": [
                    "Elemental Skill",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/906be849304f62b87b34122e050333b8.png",
                "name": "Gale Blade",
                "id": "15022"
            },
            {
                "skill_text": "Heals all your characters for 2 HP, summons 1 <color=#FFFFFFFF>Dandelion Field</color>.",
                "skill_costs": [
                    {
                        "cost_num": "4",
                        "cost_icon": "17"
                    },
                    {
                        "cost_num": "3",
                        "cost_icon": "1"
                    }
                ],
                "type": [
                    "Elemental Burst",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/dfc823559c0cfa4f6febda9d9ea32d60.png",
                "name": "Dandelion Breeze",
                "id": "15023"
            }
        ],
        "weapon": "Sword",
        "belong_to": [
            "Mondstadt",
            "",
            ""
        ],
        "hp": "10",
        "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/1a51029f206394310232b449839464be.png"
    },
    {
        "id": 1601,
        "name": "Ningguang",
        "element_type": "ETRock",
        "rank_id": 1601,
        "role_skill_infos": [
            {
                "skill_text": "Deals 1 <color=#FFE699FF>Geo DMG</color>.",
                "skill_costs": [
                    {
                        "cost_num": "1",
                        "cost_icon": "15"
                    },
                    {
                        "cost_num": "2",
                        "cost_icon": "10"
                    }
                ],
                "type": [
                    "Normal Attack",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/a51c9140615f7682c79e6dd2af3366e4.png",
                "name": "Sparkling Scatter",
                "id": "16011"
            },
            {
                "skill_text": "Deals 2 <color=#FFE699FF>Geo DMG</color>, creates 1 <color=#FFFFFFFF>Jade Screen</color>.",
                "skill_costs": [
                    {
                        "cost_num": "3",
                        "cost_icon": "15"
                    },
                    {
                        "cost_num": "",
                        "cost_icon": ""
                    }
                ],
                "type": [
                    "Elemental Skill",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/2bd0da27a460a5cd1b552c13180ecb5e.png",
                "name": "Jade Screen",
                "id": "16012"
            },
            {
                "skill_text": "Deals 6 <color=#FFE699FF>Geo DMG</color>. If <color=#FFFFFFFF>Jade Screen</color> is on the field, deals +2 DMG.",
                "skill_costs": [
                    {
                        "cost_num": "3",
                        "cost_icon": "15"
                    },
                    {
                        "cost_num": "3",
                        "cost_icon": "1"
                    }
                ],
                "type": [
                    "Elemental Burst",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/e7fcd17292e0f2c5c3aa10434f454f0a.png",
                "name": "Starshatter",
                "id": "16013"
            }
        ],
        "weapon": "Catalyst",
        "belong_to": [
            "Liyue",
            "",
            ""
        ],
        "hp": "10",
        "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/be2f95433c64c62c9788b081f8115ec5.png"
    },
    {
        "id": 1602,
        "name": "Noelle",
        "element_type": "ETRock",
        "rank_id": 1602,
        "role_skill_infos": [
            {
                "skill_text": "Deals 2 <color=#FFFFFFFF>Physical DMG</color>.",
                "skill_costs": [
                    {
                        "cost_num": "1",
                        "cost_icon": "15"
                    },
                    {
                        "cost_num": "2",
                        "cost_icon": "10"
                    }
                ],
                "type": [
                    "Normal Attack",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/1f2774a0570701e52f573952cd3436ce.png",
                "name": "Favonius Bladework - Maid",
                "id": "16021"
            },
            {
                "skill_text": "Deals 1 <color=#FFE699FF>Geo DMG</color>, creates 1 <color=#FFFFFFFF>Full Plate</color>.",
                "skill_costs": [
                    {
                        "cost_num": "3",
                        "cost_icon": "15"
                    },
                    {
                        "cost_num": "",
                        "cost_icon": ""
                    }
                ],
                "type": [
                    "Elemental Skill",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/46096c958f0cce3073cac75e540eec9d.png",
                "name": "Breastplate",
                "id": "16022"
            },
            {
                "skill_text": "Deals 4 <color=#FFE699FF>Geo DMG</color>. This character gains <color=#FFFFFFFF>Sweeping Time</color>.",
                "skill_costs": [
                    {
                        "cost_num": "4",
                        "cost_icon": "15"
                    },
                    {
                        "cost_num": "2",
                        "cost_icon": "1"
                    }
                ],
                "type": [
                    "Elemental Burst",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/2a78695dc2147234a2bb70c6fa13543c.png",
                "name": "Sweeping Time",
                "id": "16023"
            }
        ],
        "weapon": "Claymore",
        "belong_to": [
            "Mondstadt",
            "",
            ""
        ],
        "hp": "10",
        "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/5f52fdb0a80066e8ba65578962fc305e.png"
    },
    {
        "id": 1701,
        "name": "Collei",
        "element_type": "ETGrass",
        "rank_id": 1701,
        "role_skill_infos": [
            {
                "skill_text": "Deals 2 <color=#FFFFFFFF>Physical DMG</color>.",
                "skill_costs": [
                    {
                        "cost_num": "1",
                        "cost_icon": "16"
                    },
                    {
                        "cost_num": "2",
                        "cost_icon": "10"
                    }
                ],
                "type": [
                    "Normal Attack",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/5d510bb74d2c14e2fe53edbdfc955ba4.png",
                "name": "Supplicant's Bowmanship",
                "id": "17011"
            },
            {
                "skill_text": "Deals 3 <color=#7EC236FF>Dendro DMG</color>.",
                "skill_costs": [
                    {
                        "cost_num": "3",
                        "cost_icon": "16"
                    },
                    {
                        "cost_num": "",
                        "cost_icon": ""
                    }
                ],
                "type": [
                    "Elemental Skill",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/31c6bae6d30b2389e9717f5aa00bb617.png",
                "name": "Floral Brush",
                "id": "17012"
            },
            {
                "skill_text": "Deals 2 <color=#7EC236FF>Dendro DMG</color>, summons 1 <color=#FFFFFFFF>Cuilein-Anbar</color>.",
                "skill_costs": [
                    {
                        "cost_num": "3",
                        "cost_icon": "16"
                    },
                    {
                        "cost_num": "2",
                        "cost_icon": "1"
                    }
                ],
                "type": [
                    "Elemental Burst",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/aeb8db26f8f3fe637353801bdf1407c7.png",
                "name": "Trump-Card Kitty",
                "id": "17013"
            }
        ],
        "weapon": "Bow",
        "belong_to": [
            "Sumeru",
            "",
            ""
        ],
        "hp": "10",
        "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/efddc4c03c5f0997fbe5ef31ac70a505.png"
    },
    {
        "id": 2201,
        "name": "Rhodeia of Loch",
        "element_type": "ETWater",
        "rank_id": 2201,
        "role_skill_infos": [
            {
                "skill_text": "Deals 1 <color=#80C0FFFF>Hydro DMG</color>.",
                "skill_costs": [
                    {
                        "cost_num": "1",
                        "cost_icon": "12"
                    },
                    {
                        "cost_num": "2",
                        "cost_icon": "10"
                    }
                ],
                "type": [
                    "Normal Attack",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/a51c9140615f7682c79e6dd2af3366e4.png",
                "name": "Surge",
                "id": "22011"
            },
            {
                "skill_text": "Randomly summons 1 <color=#FFFFFFFF>Oceanid Mimic</color> (Prioritizes summoning a different type from preexisting ones).",
                "skill_costs": [
                    {
                        "cost_num": "3",
                        "cost_icon": "12"
                    },
                    {
                        "cost_num": "",
                        "cost_icon": ""
                    }
                ],
                "type": [
                    "Elemental Skill",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/f25ce524e9fb01340a45dcf85c72b6f2.png",
                "name": "Oceanid Mimic Summoning",
                "id": "22012"
            },
            {
                "skill_text": "Randomly summons 2 <color=#FFFFFFFF>Oceanid Mimic</color> (Prioritizes summoning different types).",
                "skill_costs": [
                    {
                        "cost_num": "5",
                        "cost_icon": "12"
                    },
                    {
                        "cost_num": "",
                        "cost_icon": ""
                    }
                ],
                "type": [
                    "Elemental Skill",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/62bc1e938e36a78b18a85f7b2f7ed3b0.png",
                "name": "The Myriad Wilds",
                "id": "22013"
            },
            {
                "skill_text": "Deals 2 <color=#80C0FFFF>Hydro DMG</color>. For each friendly Summon on the field, deals +2 additional DMG.",
                "skill_costs": [
                    {
                        "cost_num": "3",
                        "cost_icon": "12"
                    },
                    {
                        "cost_num": "3",
                        "cost_icon": "1"
                    }
                ],
                "type": [
                    "Elemental Burst",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/0f148384285f60cf949d5d9b34f8fa92.png",
                "name": "Tide and Torrent",
                "id": "22014"
            }
        ],
        "weapon": "Other Weapons",
        "belong_to": [
            "Monster",
            "",
            ""
        ],
        "hp": "10",
        "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/90422150d3267bdf9ec9a6535a7b001f.png"
    },
    {
        "id": 2202,
        "name": "Mirror Maiden",
        "element_type": "ETWater",
        "rank_id": 2202,
        "role_skill_infos": [
            {
                "skill_text": "Deals 1 <color=#80C0FFFF>Hydro DMG</color>.",
                "skill_costs": [
                    {
                        "cost_num": "1",
                        "cost_icon": "12"
                    },
                    {
                        "cost_num": "2",
                        "cost_icon": "10"
                    }
                ],
                "type": [
                    "Normal Attack",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/a51c9140615f7682c79e6dd2af3366e4.png",
                "name": "Water Ball",
                "id": "22021"
            },
            {
                "skill_text": "Deals 3 <color=#80C0FFFF>Hydro DMG</color>. The target character receives <color=#FFFFFFFF>Refraction</color>.",
                "skill_costs": [
                    {
                        "cost_num": "3",
                        "cost_icon": "12"
                    },
                    {
                        "cost_num": "",
                        "cost_icon": ""
                    }
                ],
                "type": [
                    "Elemental Skill",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/02e8a759adb9dd6f7862f18a638cefcb.png",
                "name": "Influx Blast",
                "id": "22022"
            },
            {
                "skill_text": "Deals 5 <color=#80C0FFFF>Hydro DMG</color>.",
                "skill_costs": [
                    {
                        "cost_num": "3",
                        "cost_icon": "12"
                    },
                    {
                        "cost_num": "2",
                        "cost_icon": "1"
                    }
                ],
                "type": [
                    "Elemental Burst",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/e968bcf122be55187bd11a6bc3ce8c7f.png",
                "name": "Rippled Reflection",
                "id": "22023"
            }
        ],
        "weapon": "Other Weapons",
        "belong_to": [
            "Fatui",
            "",
            ""
        ],
        "hp": "10",
        "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/9ffdee8d345bec9dca1946902df5969a.png"
    },
    {
        "id": 2301,
        "name": "Fatui Pyro Agent",
        "element_type": "ETFire",
        "rank_id": 2301,
        "role_skill_infos": [
            {
                "skill_text": "Deals 2 <color=#FFFFFFFF>Physical DMG</color>.",
                "skill_costs": [
                    {
                        "cost_num": "1",
                        "cost_icon": "13"
                    },
                    {
                        "cost_num": "2",
                        "cost_icon": "10"
                    }
                ],
                "type": [
                    "Normal Attack",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/f667af23ed9c0f26bd5b1cf676dae52c.png",
                "name": "Thrust",
                "id": "23011"
            },
            {
                "skill_text": "Deals 1 <color=#FF9999FF>Pyro DMG</color>. This character gains <color=#FFFFFFFF>Stealth</color>.",
                "skill_costs": [
                    {
                        "cost_num": "3",
                        "cost_icon": "13"
                    },
                    {
                        "cost_num": "",
                        "cost_icon": ""
                    }
                ],
                "type": [
                    "Elemental Skill",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/4b3d7470c2443c3438fcc7e86ff69dcc.png",
                "name": "Prowl",
                "id": "23012"
            },
            {
                "skill_text": "Deals 5 <color=#FF9999FF>Pyro DMG</color>.",
                "skill_costs": [
                    {
                        "cost_num": "3",
                        "cost_icon": "13"
                    },
                    {
                        "cost_num": "2",
                        "cost_icon": "1"
                    }
                ],
                "type": [
                    "Elemental Burst",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/f58850c0fa15b11271c164ae7e249785.png",
                "name": "Blade Ablaze",
                "id": "23013"
            },
            {
                "skill_text": "(Passive) When the battle begins, this character gains <color=#FFFFFFFF>Stealth</color>.",
                "skill_costs": [
                    {
                        "cost_num": "",
                        "cost_icon": ""
                    },
                    {
                        "cost_num": "",
                        "cost_icon": ""
                    }
                ],
                "type": [
                    "Passive Skill",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/52db57120e52fb2584a696c34b38aac9.png",
                "name": "Stealth Master",
                "id": "23014"
            }
        ],
        "weapon": "Other Weapons",
        "belong_to": [
            "Fatui",
            "",
            ""
        ],
        "hp": "10",
        "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/95bd6d63973f827cf93db1ca11886b44.png"
    },
    {
        "id": 2501,
        "name": "Maguu Kenki",
        "element_type": "ETWind",
        "rank_id": 2501,
        "role_skill_infos": [
            {
                "skill_text": "Deals 2 <color=#FFFFFFFF>Physical DMG</color>.",
                "skill_costs": [
                    {
                        "cost_num": "1",
                        "cost_icon": "17"
                    },
                    {
                        "cost_num": "2",
                        "cost_icon": "10"
                    }
                ],
                "type": [
                    "Normal Attack",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/f667af23ed9c0f26bd5b1cf676dae52c.png",
                "name": "Ichimonji",
                "id": "25011"
            },
            {
                "skill_text": "Summons 1 <color=#FFFFFFFF>Shadowsword: Lone Gale</color>.",
                "skill_costs": [
                    {
                        "cost_num": "3",
                        "cost_icon": "17"
                    },
                    {
                        "cost_num": "",
                        "cost_icon": ""
                    }
                ],
                "type": [
                    "Elemental Skill",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/697861409887f41bf4b5c90f2f3815ff.png",
                "name": "Blustering Blade",
                "id": "25012"
            },
            {
                "skill_text": "Summons 1 <color=#FFFFFFFF>Shadowsword: Galloping Frost</color>.",
                "skill_costs": [
                    {
                        "cost_num": "3",
                        "cost_icon": "11"
                    },
                    {
                        "cost_num": "",
                        "cost_icon": ""
                    }
                ],
                "type": [
                    "Elemental Skill",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/95c0d647c78c6058bfbd352a44fd4911.png",
                "name": "Frosty Assault",
                "id": "25013"
            },
            {
                "skill_text": "Deals 4 <color=#80FFD7FF>Anemo DMG</color>, triggers the effect(s) of all your <color=#FFFFFFFF>Shadowsword</color> Summon(s). (Does not consume their Usages)",
                "skill_costs": [
                    {
                        "cost_num": "3",
                        "cost_icon": "17"
                    },
                    {
                        "cost_num": "3",
                        "cost_icon": "1"
                    }
                ],
                "type": [
                    "Elemental Burst",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/51a851b66792a160e211ff84020d3610.png",
                "name": "Pseudo Tengu Sweeper",
                "id": "25014"
            }
        ],
        "weapon": "Other Weapons",
        "belong_to": [
            "Monster",
            "",
            ""
        ],
        "hp": "10",
        "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/efad8cd6d5bd6907341115e050f69b86.png"
    },
    {
        "id": 2601,
        "name": "Stonehide Lawachurl",
        "element_type": "ETRock",
        "rank_id": 2601,
        "role_skill_infos": [
            {
                "skill_text": "Deals 2 <color=#FFFFFFFF>Physical DMG</color>.",
                "skill_costs": [
                    {
                        "cost_num": "1",
                        "cost_icon": "15"
                    },
                    {
                        "cost_num": "2",
                        "cost_icon": "10"
                    }
                ],
                "type": [
                    "Normal Attack",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/f667af23ed9c0f26bd5b1cf676dae52c.png",
                "name": "Plama Lawa",
                "id": "26011"
            },
            {
                "skill_text": "Deals 3 <color=#FFFFFFFF>Physical DMG</color>.",
                "skill_costs": [
                    {
                        "cost_num": "3",
                        "cost_icon": "15"
                    },
                    {
                        "cost_num": "",
                        "cost_icon": ""
                    }
                ],
                "type": [
                    "Elemental Skill",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/dba642d3d9f4dc42820168db15b95de2.png",
                "name": "Movo Lawa",
                "id": "26012"
            },
            {
                "skill_text": "Deals 5 <color=#FFFFFFFF>Physical DMG</color>.",
                "skill_costs": [
                    {
                        "cost_num": "3",
                        "cost_icon": "15"
                    },
                    {
                        "cost_num": "2",
                        "cost_icon": "1"
                    }
                ],
                "type": [
                    "Elemental Burst",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/418ae77cc4622a67d6286b4be44ff910.png",
                "name": "Upa Shato",
                "id": "26013"
            },
            {
                "skill_text": "(Passive) When the battle begins, this character gains <color=#FFFFFFFF>Stonehide</color> and <color=#FFFFFFFF>Stone Force</color>.",
                "skill_costs": [
                    {
                        "cost_num": "",
                        "cost_icon": ""
                    },
                    {
                        "cost_num": "",
                        "cost_icon": ""
                    }
                ],
                "type": [
                    "Passive Skill",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/058b86d139526b2518ce20e3badbb4ef.png",
                "name": "Infused Stonehide",
                "id": "26014"
            }
        ],
        "weapon": "Other Weapons",
        "belong_to": [
            "Monster",
            "Hilichurl",
            ""
        ],
        "hp": "8",
        "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/721a409699b498d66b64bdc212a21c74.png"
    },
    {
        "id": 2701,
        "name": "Jadeplume Terrorshroom",
        "element_type": "ETGrass",
        "rank_id": 2701,
        "role_skill_infos": [
            {
                "skill_text": "Deals 2 <color=#FFFFFFFF>Physical DMG</color>.",
                "skill_costs": [
                    {
                        "cost_num": "1",
                        "cost_icon": "16"
                    },
                    {
                        "cost_num": "2",
                        "cost_icon": "10"
                    }
                ],
                "type": [
                    "Normal Attack",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/f667af23ed9c0f26bd5b1cf676dae52c.png",
                "name": "Majestic Dance",
                "id": "27011"
            },
            {
                "skill_text": "Deals 3 <color=#7EC236FF>Dendro DMG</color>.",
                "skill_costs": [
                    {
                        "cost_num": "3",
                        "cost_icon": "16"
                    },
                    {
                        "cost_num": "",
                        "cost_icon": ""
                    }
                ],
                "type": [
                    "Elemental Skill",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/121e09032218105e54a51cbd1c2ce731.png",
                "name": "Volatile Spore Cloud",
                "id": "27012"
            },
            {
                "skill_text": "Deals 4 <color=#7EC236FF>Dendro DMG</color>, then consumes all <color=#FFFFFFFF>Radical Vitality</color> stacks. For each stack consumed, this instance deals +1 DMG.",
                "skill_costs": [
                    {
                        "cost_num": "3",
                        "cost_icon": "16"
                    },
                    {
                        "cost_num": "2",
                        "cost_icon": "1"
                    }
                ],
                "type": [
                    "Elemental Burst",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/f7843567c0056ab7fe1132d9875d2c26.png",
                "name": "Feather Spreading",
                "id": "27013"
            },
            {
                "skill_text": "(Passive) When the battle begins, this character gains <color=#FFFFFFFF>Radical Vitality</color>.",
                "skill_costs": [
                    {
                        "cost_num": "",
                        "cost_icon": ""
                    },
                    {
                        "cost_num": "",
                        "cost_icon": ""
                    }
                ],
                "type": [
                    "Passive Skill",
                    ""
                ],
                "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/fc3e95c05191996151a572a15b3a99fb.png",
                "name": "Radical Vitality",
                "id": "27014"
            }
        ],
        "weapon": "Other Weapons",
        "belong_to": [
            "Monster",
            "",
            ""
        ],
        "hp": "10",
        "resource": "https://webstatic.hoyoverse.com/hk4e/e20221205drawcard/picture/bd089cefb123e25131de1932395dde26.png"
    }
]

ts_zhcn = {
    "Talent": "天赋",
    "Combat Action": "战斗行动",
    "<color=#FFFFFFFF>Combat Action</color>: When your active character is <color=#FFFFFFFF>Ganyu</color>, equip this card.\\nAfter Ganyu equips this card, immediately use <color=#FFD780FF>Frostflake Arrow</color> once.\\nWhen your Ganyu, who has this card equipped, uses <color=#FFFFFFFF>Frostflake Arrow</color>: <color=#99FFFFFF>Cryo DMG</color> dealt by this Skill +1 if this Skill has been used before during this match, and it now deals 3 <color=#FFFFFFFF>Piercing DMG</color> to all opposing characters on standby instead.\\n(You must have Ganyu in your deck to add this card to your deck.)": "<color=#FFFFFFFF>战斗行动</color>：我方出战角色为<color=#FFFFFFFF>甘雨</color>时，装备此牌。\\n甘雨装备此牌后，立刻使用一次<color=#FFD780FF>霜华矢</color>。\\n装备有此牌的甘雨使用<color=#FFFFFFFF>霜华矢</color>时：如果此技能在本场对局中曾经被使用过，则其造成的<color=#99FFFFFF>冰元素伤害</color>+1，并且改为对敌方后台角色造成3点<color=#FFFFFFFF>穿透伤害</color>。\\n（牌组中包含甘雨，才能加入牌组）",
    "Undivided Heart": "唯此一心",
    "<color=#FFFFFFFF>Combat Action</color>: When your active character is <color=#FFFFFFFF>Diona</color>, equip this card.\\nAfter Diona equips this card, immediately use <color=#FFD780FF>Icy Paws</color> once.\\nWhen your Diona, who has this card equipped, creates a <color=#FFFFFFFF>Cat-Claw Shield</color>, its <color=#FFFFFFFF>Shield</color> points +1.\\n(You must have Diona in your deck to add this card to your deck.)": "<color=#FFFFFFFF>战斗行动</color>：我方出战角色为<color=#FFFFFFFF>迪奥娜</color>时，装备此牌。\\n迪奥娜装备此牌后，立刻使用一次<color=#FFD780FF>猫爪冻冻</color>。\\n装备有此牌的迪奥娜生成的<color=#FFFFFFFF>猫爪护盾</color>，所提供的<color=#FFFFFFFF>护盾</color>值+1。\\n（牌组中包含迪奥娜，才能加入牌组）",
    "Shaken, Not Purred": "猫爪冰摇",
    "<color=#FFFFFFFF>Combat Action</color>: When your active character is <color=#FFFFFFFF>Kaeya</color>, equip this card.\\nAfter Kaeya equips this card, immediately use <color=#FFD780FF>Frostgnaw</color> once.\\nAfter your Kaeya, who has this card equipped, uses <color=#FFFFFFFF>Frostgnaw</color>, he heals himself for 2 HP. (Once per Round)\\n(You must have Kaeya in your deck to add this card to your deck.)": "<color=#FFFFFFFF>战斗行动</color>：我方出战角色为<color=#FFFFFFFF>凯亚</color>时，装备此牌。\\n凯亚装备此牌后，立刻使用一次<color=#FFD780FF>霜袭</color>。\\n装备有此牌的凯亚使用<color=#FFFFFFFF>霜袭</color>后：治疗自身2点。（每回合1次）\\n（牌组中包含凯亚，才能加入牌组）",
    "Cold-Blooded Strike": "冷血之剑",
    "<color=#FFFFFFFF>Combat Action</color>: When your active character is <color=#FFFFFFFF>Chongyun</color>, equip this card.\\nAfter Chongyun equips this card, immediately use <color=#FFD780FF>Chonghua's Layered Frost</color> once.\\nWhen your Chongyun, who has this card equipped, creates a <color=#FFFFFFFF>Chonghua Frost Field</color>, it will have the following effects: Starting <color=#FFFFFFFF>Duration (Rounds)</color> +1, will cause your Sword, Claymore, and Polearm-wielding characters' <color=#FFFFFFFF>Normal Attacks</color> to deal +1 DMG.\\n(You must have Chongyun in your deck to add this card to your deck.)": "<color=#FFFFFFFF>战斗行动</color>：我方出战角色为<color=#FFFFFFFF>重云</color>时，装备此牌。\\n重云装备此牌后，立刻使用一次<color=#FFD780FF>重华叠霜</color>。\\n装备有此牌的重云生成的<color=#FFFFFFFF>重华叠霜领域</color>获得以下效果：\\n初始<color=#FFFFFFFF>持续回合</color>+1，并且使我方单手剑、双手剑或长柄武器角色的<color=#FFFFFFFF>普通攻击</color>伤害+1。\\n（牌组中包含重云，才能加入牌组）",
    "Steady Breathing": "吐纳真定",
    "The <color=#FFFFFFFF>Cryo Elemental Infusion</color> created by your <color=#FFFFFFFF>Kamisato Ayaka</color>, who has this card equipped, allows the character to which it is attached to deal +1 <color=#99FFFFFF><color=#99FFFFFF>Cryo DMG</color></color>.\\nWhen you switch to Kamisato Ayaka, who has this card equipped: Spend 1 less Elemental Die. (Once per Round)\\n(You must have Kamisato Ayaka in your deck to add this card to your deck.)": "装备有此牌的<color=#FFFFFFFF>神里绫华</color>生成的<color=#FFFFFFFF>冰元素附魔</color>会使所附属角色造成的<color=#99FFFFFF><color=#99FFFFFF>冰元素伤害</color></color>+1。\\n切换到装备有此牌的神里绫华时：少花费1个元素骰。（每回合1次）\\n（牌组中包含神里绫华，才能加入牌组）",
    "Kanten Senmyou Blessing": "寒天宣命祝词",
    "<color=#FFFFFFFF>Combat Action</color>: When your active character is <color=#FFFFFFFF>Barbara</color>, equip this card.\\nAfter Barbara equips this card, immediately use <color=#FFD780FF>Let the Show Begin♪</color> once.\\nWhen your Barbara, who has this card equipped, is on the field, <color=#FFFFFFFF>Melody Loop</color> will allow you to spend 1 less Elemental Die the next time you use \"Switch Character.\" (Once per round)\\n(You must have Barbara in your deck to add this card to your deck.)": "<color=#FFFFFFFF>战斗行动</color>：我方出战角色为<color=#FFFFFFFF>芭芭拉</color>时，装备此牌。\\n芭芭拉装备此牌后，立刻使用一次<color=#FFD780FF>演唱，开始♪</color>。\\n装备有此牌的芭芭拉在场时，<color=#FFFFFFFF>歌声之环</color>会使我方执行「切换角色」行动时少花费1个元素骰。（每回合1次）\\n（牌组中包含芭芭拉，才能加入牌组）",
    "Glorious Season": "光辉的季节",
    "<color=#FFFFFFFF>Combat Action</color>: When your active character is <color=#FFFFFFFF>Xingqiu</color>, equip this card.\\nAfter Xingqiu equips this card, immediately use <color=#FFD780FF>Fatal Rainscreen</color> once.\\nWhen your Xingqiu, who has this card equipped, creates a <color=#FFFFFFFF>Rain Sword</color>, its starting <color=#FFFFFFFF>Usage(s)</color> +1.\\n(You must have Xingqiu in your deck to add this card to your deck.)": "<color=#FFFFFFFF>战斗行动</color>：我方出战角色为<color=#FFFFFFFF>行秋</color>时，装备此牌。\\n行秋装备此牌后，立刻使用一次<color=#FFD780FF>画雨笼山</color>。\\n装备有此牌的行秋生成的<color=#FFFFFFFF>雨帘剑</color>，初始<color=#FFFFFFFF>可用次数</color>+1。\\n（牌组中包含行秋，才能加入牌组）",
    "The Scent Remained": "重帘留香",
    "<color=#FFFFFFFF>Combat Action</color>: When your active character is <color=#FFFFFFFF>Mona</color>, equip this card.\\nWhen Mona equips this card, immediately use <color=#FFD780FF>Stellaris Phantasm</color> once.\\nWhen your Mona, who has this card equipped, is the active character, the <color=#80C0FFFF>Hydro-Related Reactions</color> you trigger deal +2 additional DMG.\\n(You must have Mona in your deck to add this card to your deck.)": "<color=#FFFFFFFF>战斗行动</color>：我方出战角色为<color=#FFFFFFFF>莫娜</color>时，装备此牌。\\n莫娜装备此牌后，立刻使用一次<color=#FFD780FF>星命定轨</color>。\\n装备有此牌的莫娜出战期间，我方引发的<color=#80C0FFFF>水元素相关反应</color>伤害额外+2。\\n（牌组中包含莫娜，才能加入牌组）",
    "Prophecy of Submersion": "沉没的预言",
    "<color=#FFFFFFFF>Combat Action</color>: When your active character is <color=#FFFFFFFF>Diluc</color>, equip this card.\\nAfter Diluc equips this card, immediately use <color=#FFD780FF>Searing Onslaught</color> once.\\nWhen your Diluc, who has this card equipped, uses <color=#FFFFFFFF>Searing Onslaught</color> for the second time in one Round, spend 1 less <color=#FF9999FF>Pyro Die</color>.\\n(You must have Diluc in your deck to add this card to your deck.)": "<color=#FFFFFFFF>战斗行动</color>：我方出战角色为<color=#FFFFFFFF>迪卢克</color>时，装备此牌。\\n迪卢克装备此牌后，立刻使用一次<color=#FFD780FF>逆焰之刃</color>。\\n装备有此牌的迪卢克每回合第2次使用<color=#FFFFFFFF>逆焰之刃</color>时，少花费1个<color=#FF9999FF>火元素</color>。\\n（牌组中包含迪卢克，才能加入牌组）",
    "Flowing Flame": "流火焦灼",
    "<color=#FFFFFFFF>Combat Action</color>: When your active character is <color=#FFFFFFFF>Xiangling</color>, equip this card.\\nAfter Xiangling equips this card, immediately use <color=#FFD780FF>Guoba Attack</color> once.\\nWhen your Xiangling, who has this card equipped, uses <color=#FFFFFFFF>Guoba Attack</color>, she will also deal 1 <color=#FF9999FF>Pyro DMG</color>.\\n(You must have Xiangling in your deck to add this card to your deck.)": "<color=#FFFFFFFF>战斗行动</color>：我方出战角色为<color=#FFFFFFFF>香菱</color>时，装备此牌。\\n香菱装备此牌后，立刻使用一次<color=#FFD780FF>锅巴出击</color>。\\n装备有此牌的香菱施放<color=#FFFFFFFF>锅巴出击</color>时，自身也会造成1点<color=#FF9999FF>火元素伤害</color>。\\n（牌组中包含香菱，才能加入牌组）",
    "Crossfire": "交叉火力",
    "<color=#FFFFFFFF>Combat Action</color>: When your active character is <color=#FFFFFFFF>Bennett</color>, equip this card.\\nAfter Bennett equips this card, immediately use <color=#FFD780FF>Fantastic Voyage</color> once.\\nWhen your Bennett, who has this card equipped, creates an <color=#FFFFFFFF>Inspiration Field</color>, its DMG Bonus is now always active and will no longer have an HP restriction.\\n(You must have Bennett in your deck to add this card to your deck.)": "<color=#FFFFFFFF>战斗行动</color>：我方出战角色为<color=#FFFFFFFF>班尼特</color>时，装备此牌。\\n班尼特装备此牌后，立刻使用一次<color=#FFD780FF>美妙旅程</color>。\\n装备有此牌的班尼特生成的<color=#FFFFFFFF>鼓舞领域</color>，其伤害提升效果改为总是生效，不再具有生命值限制。\\n（牌组中包含班尼特，才能加入牌组）",
    "Grand Expectation": "冒险憧憬",
    "<color=#FFFFFFFF>Combat Action</color>: When your active character is <color=#FFFFFFFF>Yoimiya</color>, equip this card.\\nAfter Yoimiya equips this card, immediately use <color=#FFD780FF>Niwabi Fire-Dance</color> once.\\nAfter your Yoimiya, who has this card equipped, triggers <color=#FFFFFFFF>Niwabi Enshou</color>: Deal 1 additional <color=#FF9999FF>Pyro DMG</color>.\\n(You must have Yoimiya in your deck to add this card to your deck.)": "<color=#FFFFFFFF>战斗行动</color>：我方出战角色为<color=#FFFFFFFF>宵宫</color>时，装备此牌。\\n宵宫装备此牌后，立刻使用一次<color=#FFD780FF>焰硝庭火舞</color>。\\n装备有此牌的宵宫触发<color=#FFFFFFFF>庭火焰硝</color>后：额外造成1点<color=#FF9999FF>火元素伤害</color>。\\n（牌组中包含宵宫，才能加入牌组）",
    "Naganohara Meteor Swarm": "长野原龙势流星群",
    "<color=#FFFFFFFF>Combat Action</color>: When your active character is <color=#FFFFFFFF>Klee</color>, equip this card.\\nAfter Klee equips this card, immediately use <color=#FFD780FF>Jumpy Dumpty</color> once.\\nWhen your Klee, who has this card equipped, creates an <color=#FFFFFFFF>Explosive Spark</color>, its <color=#FFFFFFFF>Usage(s)</color> +1.\\n(You must have Klee in your deck to add this card to your deck.)": "<color=#FFFFFFFF>战斗行动</color>：我方出战角色为<color=#FFFFFFFF>可莉</color>时，装备此牌。\\n可莉装备此牌后，立刻使用一次<color=#FFD780FF>蹦蹦炸弹</color>。\\n装备有此牌的可莉生成的<color=#FFFFFFFF>爆裂火花</color>的<color=#FFFFFFFF>可用次数</color>+1。\\n（牌组中包含可莉，才能加入牌组）",
    "Pounding Surprise": "砰砰礼物",
    "<color=#FFFFFFFF>Combat Action</color>: When your active character is <color=#FFFFFFFF>Fischl</color>, equip this card.\\nAfter Fischl equips this card, immediately use <color=#FFD780FF>Nightrider</color> once.\\nWhen your Fischl, who has this card equipped, creates an <color=#FFFFFFFF>Oz</color>, and after Fischl uses a <color=#FFFFFFFF>Normal Attack</color>: Deal 2 <color=#FFACFFFF>Electro DMG</color>. (Consumes <color=#FFFFFFFF>Usage(s)</color>)\\n(You must have Fischl in your deck to add this card to your deck.)": "<color=#FFFFFFFF>战斗行动</color>：我方出战角色为<color=#FFFFFFFF>菲谢尔</color>时，装备此牌。\\n菲谢尔装备此牌后，立刻使用一次<color=#FFD780FF>夜巡影翼</color>。\\n装备有此牌的菲谢尔生成的<color=#FFFFFFFF>奥兹</color>，会在菲谢尔<color=#FFFFFFFF>普通攻击</color>后造成2点<color=#FFACFFFF>雷元素伤害</color>。（需消耗<color=#FFFFFFFF>可用次数</color>）\\n（牌组中包含菲谢尔，才能加入牌组）",
    "Stellar Predator": "噬星魔鸦",
    "<color=#FFFFFFFF>Combat Action</color>: When your active character is <color=#FFFFFFFF>Razor</color>, equip this card.\\nAfter Razor equips this card, immediately use <color=#FFD780FF>Claw and Thunder</color> once.\\nAfter your Razor, who has this card equipped, uses <color=#FFFFFFFF>Claw and Thunder</color>: 1 of your Electro characters gains 1 Energy. (Active Character prioritized)\\n(You must have Razor in your deck to add this card to your deck.)": "<color=#FFFFFFFF>战斗行动</color>：我方出战角色为<color=#FFFFFFFF>雷泽</color>时，装备此牌。\\n雷泽装备此牌后，立刻使用一次<color=#FFD780FF>利爪与苍雷</color>。\\n装备有此牌的雷泽使用<color=#FFFFFFFF>利爪与苍雷</color>后：使我方一个雷元素角色获得1点充能。（出战角色优先）\\n（牌组中包含雷泽，才能加入牌组）",
    "Awakening": "觉醒",
    "<color=#FFFFFFFF>Combat Action</color>: When your active character is <color=#FFFFFFFF>Keqing</color>, equip this card.\\nAfter Keqing equips this card, immediately use <color=#FFD780FF>Stellar Restoration</color> once.\\nWhen your Keqing, who has this card equipped, creates an <color=#FFFFFFFF>Electro Elemental Infusion</color>, it will have the following effects:\\nStarting <color=#FFFFFFFF>Duration (Rounds)</color> +1, <color=#FFACFFFF>Electro DMG</color> dealt by the attached character +1.\\n(You must have Keqing in your deck to add this card to your deck.)": "<color=#FFFFFFFF>战斗行动</color>：我方出战角色为<color=#FFFFFFFF>刻晴</color>时，装备此牌。\\n刻晴装备此牌后，立刻使用一次<color=#FFD780FF>星斗归位</color>。\\n装备有此牌的刻晴生成的<color=#FFFFFFFF>雷元素附魔</color>获得以下效果：\\n初始<color=#FFFFFFFF>持续回合</color>+1，并且会使所附属角色造成的<color=#FFACFFFF>雷元素伤害</color>+1。\\n（牌组中包含刻晴，才能加入牌组）",
    "Thundering Penance": "抵天雷罚",
    "<color=#FFFFFFFF>Combat Action</color>: When your active character is <color=#FFFFFFFF>Cyno</color>, equip this card.\\nAfter Cyno equips this card, immediately use <color=#FFD780FF>Secret Rite: Chasmic Soulfarer</color> once.\\nWhen your Cyno, who has this card equipped, uses <color=#FFFFFFFF>Secret Rite: Chasmic Soulfarer</color> with 3 or 5 levels of <color=#FFFFFFFF>Pactsworn Pathclearer</color>'s Indwelling effect, deal +1 additional DMG.\\n(You must have Cyno in your deck to add this card to your deck.)": "<color=#FFFFFFFF>战斗行动</color>：我方出战角色为<color=#FFFFFFFF>赛诺</color>时，装备此牌。\\n赛诺装备此牌后，立刻使用一次<color=#FFD780FF>秘仪·律渊渡魂</color>。\\n装备有此牌的赛诺在<color=#FFFFFFFF>启途誓使</color>的「凭依」级数为3或5时使用<color=#FFFFFFFF>秘仪·律渊渡魂</color>时，造成的伤害额外+1。\\n（牌组中包含赛诺，才能加入牌组）",
    "Featherfall Judgment": "落羽的裁择",
    "<color=#FFFFFFFF>Combat Action</color>: When your active character is <color=#FFFFFFFF>Beidou</color>, equip this card.\\nAfter Beidou equips this card, immediately use <color=#FFD780FF>Tidecaller</color> once.\\nWhen Beidou, who has this card equipped, uses <color=#FFFFFFFF>Wavestrider</color>: If DMG is taken while <color=#FFFFFFFF>Prepare Skill</color> is active, Beidou's Normal Attacks this Round will cost 1 less <color=#FFFFFFFF>Unaligned Element</color>. (Can be triggered 2 times)\\n(You must have Beidou in your deck to add this card to your deck.)": "<color=#FFFFFFFF>战斗行动</color>：我方出战角色为<color=#FFFFFFFF>北斗</color>时，装备此牌。\\n北斗装备此牌后，立刻使用一次<color=#FFD780FF>捉浪</color>。\\n装备有此牌的北斗使用<color=#FFFFFFFF>踏潮</color>时：如果<color=#FFFFFFFF>准备技能</color>期间受到过伤害，则使北斗本回合内「普通攻击」少花费1个<color=#FFFFFFFF>无色元素</color>。（最多触发2次）\\n（牌组中包含北斗，才能加入牌组）",
    "Lightning Storm": "霹雳连霄",
    "<color=#FFFFFFFF>Combat Action</color>: When your active character is <color=#FFFFFFFF>Sucrose</color>, equip this card.\\nAfter Sucrose equips this card, immediately use <color=#FFD780FF>Forbidden Creation - Isomer 75 / Type II</color> once.\\nAfter the <color=#FFFFFFFF>Large Wind Spirit</color> created by your Sucrose, who had this card equipped, has converted to another Elemental Type: Deal +1 DMG of this Elemental Type.\\n(You must have Sucrose in your deck to add this card to your deck.)": "<color=#FFFFFFFF>战斗行动</color>：我方出战角色为<color=#FFFFFFFF>砂糖</color>时，装备此牌。\\n砂糖装备此牌后，立刻使用一次<color=#FFD780FF>禁·风灵作成·柒伍同构贰型</color>。\\n装备有此牌的砂糖生成的<color=#FFFFFFFF>大型风灵</color>已转换成另一种元素后：我方造成的此类元素伤害+1。\\n（牌组中包含砂糖，才能加入牌组）",
    "Chaotic Entropy": "混元熵增论",
    "<color=#FFFFFFFF>Combat Action</color>: When your active character is <color=#FFFFFFFF>Jean</color>, equip this card.\\nAfter Jean equips this card, immediately use <color=#FFD780FF>Dandelion Breeze</color> once.\\nWhen your Jean, who has this card equipped, is on the field, <color=#FFFFFFFF>Dandelion Field</color> will cause you to deal +1 <color=#80FFD7FF><color=#80FFD7FF>Anemo DMG</color></color>.\\n(You must have Jean in your deck to add this card to your deck.)": "<color=#FFFFFFFF>战斗行动</color>：我方出战角色为<color=#FFFFFFFF>琴</color>时，装备此牌。\\n琴装备此牌后，立刻使用一次<color=#FFD780FF>蒲公英之风</color>。\\n装备有此牌的琴在场时，<color=#FFFFFFFF>蒲公英领域</color>会使我方造成的<color=#80FFD7FF><color=#80FFD7FF>风元素伤害</color></color>+1。\\n（牌组中包含琴，才能加入牌组）",
    "Lands of Dandelion": "蒲公英的国土",
    "<color=#FFFFFFFF>Combat Action</color>: When your active character is <color=#FFFFFFFF>Ningguang</color>, equip this card.\\nAfter Ningguang equips this card, immediately use <color=#FFD780FF>Jade Screen</color> once.\\nWhen your Ningguang, who has this card equipped, is on the field, <color=#FFFFFFFF>Jade Screen</color> will cause you to deal +1 <color=#FFE699FF><color=#FFE699FF>Geo DMG</color></color>.\\n(You must have Ningguang in your deck to add this card to your deck.)": "<color=#FFFFFFFF>战斗行动</color>：我方出战角色为<color=#FFFFFFFF>凝光</color>时，装备此牌。\\n凝光装备此牌后，立刻使用一次<color=#FFD780FF>璇玑屏</color>。\\n装备有此牌的凝光在场时，<color=#FFFFFFFF>璇玑屏</color>会使我方造成的<color=#FFE699FF><color=#FFE699FF>岩元素伤害</color></color>+1。\\n（牌组中包含凝光，才能加入牌组）",
    "Strategic Reserve": "储之千日，用之一刻",
    "<color=#FFFFFFFF>Combat Action</color>: When your active character is <color=#FFFFFFFF>Noelle</color>, equip this card.\\nAfter Noelle equips this card, immediately use <color=#FFD780FF>Breastplate</color> once.\\nWhen your Noelle, who has this card equipped, creates a <color=#FFFFFFFF>Full Plate</color>, it will heal all your characters for 1 HP after Noelle uses a <color=#FFFFFFFF>Normal Attack</color>. (Once per Round)\\n(You must have Noelle in your deck to add this card to your deck.)": "<color=#FFFFFFFF>战斗行动</color>：我方出战角色为<color=#FFFFFFFF>诺艾尔</color>时，装备此牌。\\n诺艾尔装备此牌后，立刻使用一次<color=#FFD780FF>护心铠</color>。\\n装备有此牌的诺艾尔生成的<color=#FFFFFFFF>护体岩铠</color>，会在诺艾尔使用<color=#FFFFFFFF>普通攻击</color>后，治疗我方所有角色1点。（每回合1次）\\n（牌组中包含诺艾尔，才能加入牌组）",
    "I Got Your Back": "支援就交给我吧",
    "<color=#FFFFFFFF>Combat Action</color>: When your active character is <color=#FFFFFFFF>Collei</color>, equip this card.\\nAfter Collei equips this card, immediately use <color=#FFD780FF>Floral Brush</color> once.\\nAfter your Collei, who has this card equipped, <color=#FFFFFFFF>uses Floral Brush</color>, during this Round, when your characters' Skills trigger <color=#7EC236FF>Dendro-Related Reactions</color>: Deal 1 <color=#7EC236FF>Dendro DMG</color>. (Once per Round)\\n(You must have Collei in your deck to add this card to your deck.)": "<color=#FFFFFFFF>战斗行动</color>：我方出战角色为<color=#FFFFFFFF>柯莱</color>时，装备此牌。\\n柯莱装备此牌后，立刻使用一次<color=#FFD780FF>拂花偈叶</color>。\\n装备有此牌的柯莱使用了<color=#FFFFFFFF>拂花偈叶</color>的回合中，我方角色的技能引发<color=#7EC236FF>草元素相关反应</color>后：造成1点<color=#7EC236FF>草元素伤害</color>。（每回合1次）\\n（牌组中包含柯莱，才能加入牌组）",
    "Floral Sidewinder": "飞叶迴斜",
    "<color=#FFFFFFFF>Combat Action</color>: When your active character is <color=#FFFFFFFF>Rhodeia of Loch</color>, equip this card.\\nAfter Rhodeia of Loch equips this card, immediately use <color=#FFD780FF>Tide and Torrent</color> once.\\nWhen your Rhodeia of Loch, who has this card equipped, uses <color=#FFFFFFFF>Tide and Torrent</color>, all of your Summon(s) gain +1 <color=#FFFFFFFF>Usage(s)</color>.\\n(You must have Rhodeia of Loch in your deck to add this card to your deck.)": "<color=#FFFFFFFF>战斗行动</color>：我方出战角色为<color=#FFFFFFFF>纯水精灵·洛蒂娅</color>时，装备此牌。\\n纯水精灵·洛蒂娅装备此牌后，立刻使用一次<color=#FFD780FF>潮涌与激流</color>。\\n装备有此牌的纯水精灵·洛蒂娅施放<color=#FFFFFFFF>潮涌与激流</color>时，使我方所有召唤物<color=#FFFFFFFF>可用次数</color>+1。\\n（牌组中包含纯水精灵·洛蒂娅，才能加入牌组）",
    "Streaming Surge": "百川奔流",
    "<color=#FFFFFFFF>Combat Action</color>: When your active character is <color=#FFFFFFFF>Mirror Maiden</color>, equip this card.\\nAfter Mirror Maiden equips this card, immediately use <color=#FFD780FF>Influx Blast</color> once.\\nWhen your Mirror Maiden, who has this card equipped, creates a <color=#FFFFFFFF>Refraction</color>, it will have the following effects:\\nStarting <color=#FFFFFFFF>Duration (Rounds)</color> +1, will increase the Elemental Dice Cost of switching from the character to which this is attached to another character by 1.\\n(You must have Mirror Maiden in your deck to add this card to your deck.)": "<color=#FFFFFFFF>战斗行动</color>：我方出战角色为<color=#FFFFFFFF>愚人众·藏镜仕女</color>时，装备此牌。\\n愚人众·藏镜仕女装备此牌后，立刻使用一次<color=#FFD780FF>潋波绽破</color>。\\n装备有此牌的愚人众·藏镜仕女生成的<color=#FFFFFFFF>水光破镜</color>获得以下效果：\\n初始<color=#FFFFFFFF>持续回合</color>+1，并且会使所附属角色切换到其他角色时元素骰费用+1。\\n（牌组中包含愚人众·藏镜仕女，才能加入牌组）",
    "Mirror Cage": "镜锢之笼",
    "<color=#FFFFFFFF>Combat Action</color>: When your active character is <color=#FFFFFFFF>Fatui Pyro Agent</color>, equip this card.\\nAfter Fatui Pyro Agent equips this card, immediately use <color=#FFD780FF>Prowl</color> once.\\nWhen your Fatui Pyro Agent, who has this card equipped, creates a <color=#FFFFFFFF>Stealth</color>, it will have the following effects:\\nStarting <color=#FFFFFFFF>Usage(s)</color> +1, the <color=#FFFFFFFF>Physical DMG</color> the attached character deals will be converted to <color=#FF9999FF>Pyro DMG</color>.\\n(You must have Fatui Pyro Agent in your deck to add this card to your deck.)": "<color=#FFFFFFFF>战斗行动</color>：我方出战角色为<color=#FFFFFFFF>愚人众·火之债务处理人</color>时，装备此牌。\\n愚人众·火之债务处理人装备此牌后，立刻使用一次<color=#FFD780FF>伺机而动</color>。\\n装备有此牌的愚人众·火之债务处理人生成的<color=#FFFFFFFF>潜行</color>获得以下效果：\\n初始<color=#FFFFFFFF>可用次数</color>+1，并且使所附属角色造成的<color=#FFFFFFFF>物理伤害</color>变为<color=#FF9999FF>火元素伤害</color>。\\n（牌组中包含愚人众·火之债务处理人，才能加入牌组）",
    "Paid in Full": "悉数讨回",
    "<color=#FFFFFFFF>Combat Action</color>: When your active character is <color=#FFFFFFFF>Maguu Kenki</color>, equip this card.\\nAfter Maguu Kenki equips this card, immediately use <color=#FFD780FF>Blustering Blade</color> once.\\nAfter your Maguu Kenki, who has this card equipped, uses <color=#FFFFFFFF>Blustering Blade</color>, you will switch to your next character. You will switch to your previous character when your Maguu Kenki, who has this card equipped, uses <color=#FFFFFFFF>Frosty Assault</color>.\\n(You must have Maguu Kenki in your deck to add this card to your deck.)": "<color=#FFFFFFFF>战斗行动</color>：我方出战角色为<color=#FFFFFFFF>魔偶剑鬼</color>时，装备此牌。\\n魔偶剑鬼装备此牌后，立刻使用一次<color=#FFD780FF>孤风刀势</color>。\\n装备有此牌的魔偶剑鬼施放<color=#FFFFFFFF>孤风刀势</color>后，我方切换到后一个角色；施放<color=#FFFFFFFF>霜驰影突</color>后，我方切换到前一个角色。\\n（牌组中包含魔偶剑鬼，才能加入牌组）",
    "Transcendent Automaton": "机巧神通",
    "<color=#FFFFFFFF>Combat Action</color>: When your active character is <color=#FFFFFFFF>Stonehide Lawachurl</color>, equip this card.\\nAfter Stonehide Lawachurl equips this card, immediately use <color=#FFD780FF>Upa Shato</color> once.\\nWhen your Stonehide Lawachurl, who has this card equipped, defeats an opposing character: Stonehide Lawachurl will re-attach <color=#FFFFFFFF>Stonehide</color> and <color=#FFFFFFFF>Stone Force</color>.\\n(You must have Stonehide Lawachurl in your deck to add this card to your deck.)": "<color=#FFFFFFFF>战斗行动</color>：我方出战角色为<color=#FFFFFFFF>丘丘岩盔王</color>时，装备此牌。\\n丘丘岩盔王装备此牌后，立刻使用一次<color=#FFD780FF>Upa Shato</color>。\\n装备有此牌的丘丘岩盔王击倒敌方角色后；丘丘岩盔王重新附属<color=#FFFFFFFF>岩盔</color>和<color=#FFFFFFFF>坚岩之力</color>。\\n（牌组中包含丘丘岩盔王，才能加入牌组）",
    "Stonehide Reforged": "重铸：岩盔",
    "<color=#FFFFFFFF>Combat Action</color>: When your active character is <color=#FFFFFFFF>Jadeplume Terrorshroom</color>, equip this card.\\nAfter Jadeplume Terrorshroom equips this card, immediately use <color=#FFD780FF>Volatile Spore Cloud</color> once.\\nYour Jadeplume Terrorshroom, who has this card equipped, can accumulate 1 more stack of Radical Vitality.\\n(You must have Jadeplume Terrorshroom in your deck to add this card to your deck.)": "<color=#FFFFFFFF>战斗行动</color>：我方出战角色为<color=#FFFFFFFF>翠翎恐蕈</color>时，装备此牌。\\n翠翎恐蕈装备此牌后，立刻使用一次<color=#FFD780FF>不稳定孢子云</color>。\\n装备有此牌的翠翎恐蕈，可累积的「活化激能」层数+1。\\n（牌组中包含翠翎恐蕈，才能加入牌组）",
    "Proliferating Spores": "孢子增殖",
    "Weapon": "武器",
    "Catalyst": "法器",
    "<color=#FFFFFFFF>The character deals +1 DMG</color>.\\n(<color=#FFFFFFFF>Only Catalyst Characters</color> can equip this. A character can equip a maximum of 1 Weapon)": "<color=#FFFFFFFF>角色造成的伤害+1</color>。\\n（<color=#FFFFFFFF>「法器」角色</color>才能装备。角色最多装备1件「武器」）",
    "Magic Guide": "魔导绪论",
    "<color=#FFFFFFFF>The character deals +1 DMG</color>.\\n<color=#FFFFFFFF>After the character uses an Elemental Skill:</color> Create 1 Elemental Die of the same Elemental Type as this character. (Once per Round)\\n(<color=#FFFFFFFF>Only Catalyst Characters</color> can equip this. A character can equip a maximum of 1 Weapon)": "<color=#FFFFFFFF>角色造成的伤害+1</color>。\\n<color=#FFFFFFFF>角色使用「元素战技」后：</color>生成1个此角色类型的元素骰。（每回合1次）\\n（<color=#FFFFFFFF>「法器」角色</color>才能装备。角色最多装备1件「武器」）",
    "Sacrificial Fragments": "祭礼残章",
    "<color=#FFFFFFFF>The character deals +1 DMG</color>.\\n<color=#FFFFFFFF>Once per Round:</color> This character's Normal Attacks deal +1 additional DMG.\\n(<color=#FFFFFFFF>Only Catalyst Characters</color> can equip this. A character can equip a maximum of 1 Weapon)": "<color=#FFFFFFFF>角色造成的伤害+1</color>。\\n<color=#FFFFFFFF>每回合1次：</color>角色使用「普通攻击」造成的伤害额外+1。\\n（<color=#FFFFFFFF>「法器」角色</color>才能装备。角色最多装备1件「武器」）",
    "Skyward Atlas": "天空之卷",
    "Bow": "弓",
    "<color=#FFFFFFFF>The character deals +1 DMG</color>.\\n(<color=#FFFFFFFF>Only Bow Characters</color> can equip this. A character can equip a maximum of 1 Weapon)": "<color=#FFFFFFFF>角色造成的伤害+1</color>。\\n（<color=#FFFFFFFF>「弓」角色</color>才能装备。角色最多装备1件「武器」）",
    "Raven Bow": "鸦羽弓",
    "<color=#FFFFFFFF>The character deals +1 DMG</color>.\\n<color=#FFFFFFFF>After the character uses an Elemental Skill:</color> Create 1 Elemental Die of the same Elemental Type as this character. (Once per Round)\\n(<color=#FFFFFFFF>Only Bow Characters</color> can equip this. A character can equip a maximum of 1 Weapon)": "<color=#FFFFFFFF>角色造成的伤害+1</color>。\\n<color=#FFFFFFFF>角色使用「元素战技」后：</color>生成1个此角色类型的元素骰。（每回合1次）\\n（<color=#FFFFFFFF>「弓」角色</color>才能装备。角色最多装备1件「武器」）",
    "Sacrificial Bow": "祭礼弓",
    "<color=#FFFFFFFF>The character deals +1 DMG</color>.\\n<color=#FFFFFFFF>Once per Round:</color> This character's Normal Attacks deal +1 additional DMG.\\n(<color=#FFFFFFFF>Only Bow Characters</color> can equip this. A character can equip a maximum of 1 Weapon)": "<color=#FFFFFFFF>角色造成的伤害+1</color>。\\n<color=#FFFFFFFF>每回合1次：</color>角色使用「普通攻击」造成的伤害额外+1。\\n（<color=#FFFFFFFF>「弓」角色</color>才能装备。角色最多装备1件「武器」）",
    "Skyward Harp": "天空之翼",
    "Claymore": "双手剑",
    "<color=#FFFFFFFF>The character deals +1 DMG</color>.\\n(<color=#FFFFFFFF>Only Claymore Characters</color> can equip this. A character can equip a maximum of 1 Weapon)": "<color=#FFFFFFFF>角色造成的伤害+1</color>。\\n（<color=#FFFFFFFF>「双手剑」角色</color>才能装备。角色最多装备1件「武器」）",
    "White Iron Greatsword": "白铁大剑",
    "<color=#FFFFFFFF>The character deals +1 DMG</color>.\\n<color=#FFFFFFFF>After the character uses an Elemental Skill:</color> Create 1 Elemental Die of the same Elemental Type as this character. (Once per Round)\\n(<color=#FFFFFFFF>Only Claymore Characters</color> can equip this. A character can equip a maximum of 1 Weapon)": "<color=#FFFFFFFF>角色造成的伤害+1</color>。\\n<color=#FFFFFFFF>角色使用「元素战技」后：</color>生成1个此角色类型的元素骰。（每回合1次）\\n（<color=#FFFFFFFF>「双手剑」角色</color>才能装备。角色最多装备1件「武器」）",
    "Sacrificial Greatsword": "祭礼大剑",
    "<color=#FFFFFFFF>The character deals +1 DMG</color>.\\nDeal +2 additional DMG if the target's remaining HP is equal to or less than 6.\\n(<color=#FFFFFFFF>Only Claymore Characters</color> can equip this. A character can equip a maximum of 1 Weapon)": "<color=#FFFFFFFF>角色造成的伤害+1</color>。\\n攻击剩余生命值不多于6的目标时，伤害额外+2。\\n（<color=#FFFFFFFF>「双手剑」角色</color>才能装备。角色最多装备1件「武器」）",
    "Wolf's Gravestone": "狼的末路",
    "Polearm": "长柄武器",
    "<color=#FFFFFFFF>The character deals +1 DMG</color>.\\n(<color=#FFFFFFFF>Only Polearm Characters</color> can equip this. A character can equip a maximum of 1 Weapon)": "<color=#FFFFFFFF>角色造成的伤害+1</color>。\\n（<color=#FFFFFFFF>「长柄武器」角色</color>才能装备。角色最多装备1件「武器」）",
    "White Tassel": "白缨枪",
    "<color=#FFFFFFFF>The character deals +1 DMG</color>.\\n<color=#FFFFFFFF>When played:</color> For each party member from Liyue, grant <color=#FFFFFFFF>1 <color=#FFFFFFFF>Shield</color> point</color> to the character to which this is attached. (Max 3 points)\\n(<color=#FFFFFFFF>Only Polearm Characters</color> can equip this. A character can equip a maximum of 1 Weapon)": "<color=#FFFFFFFF>角色造成的伤害+1</color>。\\n<color=#FFFFFFFF>入场时：</color>队伍中每有一名「璃月」角色，此牌就为附属的角色提供<color=#FFFFFFFF>1点<color=#FFFFFFFF>护盾</color></color>。（最多3点）\\n（<color=#FFFFFFFF>「长柄武器」角色</color>才能装备。角色最多装备1件「武器」）",
    "Lithic Spear": "千岩长枪",
    "<color=#FFFFFFFF>The character deals +1 DMG</color>.\\n<color=#FFFFFFFF>Once per Round:</color> This character's Normal Attacks deal +1 additional DMG.\\n(<color=#FFFFFFFF>Only Polearm Characters</color> can equip this. A character can equip a maximum of 1 Weapon)": "<color=#FFFFFFFF>角色造成的伤害+1</color>。\\n<color=#FFFFFFFF>每回合1次：</color>角色使用「普通攻击」造成的伤害额外+1。\\n（<color=#FFFFFFFF>「长柄武器」角色</color>才能装备。角色最多装备1件「武器」）",
    "Skyward Spine": "天空之脊",
    "Sword": "单手剑",
    "<color=#FFFFFFFF>The character deals +1 DMG</color>.\\n(<color=#FFFFFFFF>Only Sword Characters</color> can equip this. A character can equip a maximum of 1 Weapon)": "<color=#FFFFFFFF>角色造成的伤害+1</color>。\\n（<color=#FFFFFFFF>「单手剑」角色</color>才能装备。角色最多装备1件「武器」）",
    "Traveler's Handy Sword": "旅行剑",
    "<color=#FFFFFFFF>The character deals +1 DMG</color>.\\n<color=#FFFFFFFF>After the character uses an Elemental Skill:</color> Create 1 Elemental Die of the same Elemental Type as this character. (Once per Round)\\n(<color=#FFFFFFFF>Only Sword Characters</color> can equip this. A character can equip a maximum of 1 Weapon)": "<color=#FFFFFFFF>角色造成的伤害+1</color>。\\n<color=#FFFFFFFF>角色使用「元素战技」后：</color>生成1个此角色类型的元素骰。（每回合1次）\\n（<color=#FFFFFFFF>「单手剑」角色</color>才能装备。角色最多装备1件「武器」）",
    "Sacrificial Sword": "祭礼剑",
    "<color=#FFFFFFFF>The character deals +1 DMG</color>.\\n<color=#FFFFFFFF>After the opposing character uses a Skill:</color> If the character with this attached is the active character, heal this character for 1 HP. (Max twice per Round)\\n(<color=#FFFFFFFF>Only Sword Characters</color> can equip this. A character can equip a maximum of 1 Weapon)": "<color=#FFFFFFFF>角色造成的伤害+1</color>。\\n<color=#FFFFFFFF>对方使用技能后：</color>如果所附属角色为「出战角色」，则治疗该角色1点。（每回合至多2次）\\n（<color=#FFFFFFFF>「单手剑」角色</color>才能装备。角色最多装备1件「武器」）",
    "Aquila Favonia": "风鹰剑",
    "Artifact": "圣遗物",
    "<color=#FFFFFFFF>After a character uses a Normal Attack:</color> Heal self for 1 HP. (Max 3 times per Round)\\n(A character can equip a maximum of 1 Artifact)": "<color=#FFFFFFFF>角色使用「普通攻击」后：</color>治疗自身1点。（每回合至多3次）\\n（角色最多装备1件「圣遗物」）",
    "Adventurer's Bandana": "冒险家头带",
    "<color=#FFFFFFFF>After a character uses an Elemental Skill:</color> Heal self for 2 HP. (Once per Round)\\n(A character can equip a maximum of 1 Artifact)": "<color=#FFFFFFFF>角色使用「元素战技」后：</color>治疗自身2点。（每回合1次）\\n（角色最多装备1件「圣遗物」）",
    "Lucky Dog's Silver Circlet": "幸运儿银冠",
    "<color=#FFFFFFFF>After a character uses an Elemental Burst:</color> Heal all your characters for 1 HP. (Once per Round)\\n(A character can equip a maximum of 1 Artifact)": "<color=#FFFFFFFF>角色使用「元素爆发」后：</color>治疗所有我方角色1点。（每回合1次）\\n（角色最多装备1件「圣遗物」）",
    "Traveling Doctor's Handkerchief": "游医的方巾",
    "<color=#FFFFFFFF>After an opposing character is defeated:</color> If the character this card is attached to is the active character, create <color=#FFFFFFFF>Omni Element</color> ×2.\\n(A character can equip a maximum of 1 Artifact)": "<color=#FFFFFFFF>敌方角色被击倒后：</color>如果所附属角色为「出战角色」，则生成2个<color=#FFFFFFFF>万能元素</color>。\\n（角色最多装备1件「圣遗物」）",
    "Gambler's Earrings": "赌徒的耳环",
    "<color=#FFFFFFFF>After a character triggers an Elemental Reaction:</color> Create 1 Elemental Die that matches this Character's Elemental Type. (Max 3 times per Round)\\n(A character can equip a maximum of 1 Artifact)": "<color=#FFFFFFFF>角色引发元素反应后：</color>生成1个此角色元素类型的元素骰。（每回合至多3次）\\n（角色最多装备1件「圣遗物」）",
    "Instructor's Cap": "教官的帽子",
    "<color=#FFFFFFFF>After a character uses an Elemental Burst:</color> All your characters on standby gain 1 <color=#FFFFFFFF>Energy</color>. (Once per Round)\\n(A character can equip a maximum of 1 Artifact)": "<color=#FFFFFFFF>角色使用元素爆发后：</color>所有我方后台角色获得1点<color=#FFFFFFFF>充能</color>。（每回合1次）\\n（角色最多装备1件「圣遗物」）",
    "Exile's Circlet": "流放者头冠",
    "<color=#FFFFFFFF>When a character uses a Skill or equips a Talent:</color> Spend 1 less <color=#99FFFFFF>Cryo Die</color>. (Once per Round)\\n(A character can equip a maximum of 1 Artifact)": "<color=#FFFFFFFF>角色使用技能或装备「天赋」时：</color>少花费1个<color=#99FFFFFF>冰元素</color>。（每回合1次）\\n（角色最多装备1件「圣遗物」）",
    "Broken Rime's Echo": "破冰踏雪的回音",
    "<color=#FFFFFFFF>When a character uses a Skill or equips a Talent:</color> Spend 1 less <color=#99FFFFFF>Cryo Die</color>. (Once per Round)\\n<color=#FFFFFFFF>Roll Phase:</color> 2 of the starting Elemental Dice you roll are always guaranteed to be <color=#99FFFFFF>Cryo Dice</color>.\\n(A character can equip a maximum of 1 Artifact)": "<color=#FFFFFFFF>角色使用技能或装备「天赋」时：</color>少花费1个<color=#99FFFFFF>冰元素</color>。（每回合1次）\\n<color=#FFFFFFFF>投掷阶段：</color>2个元素骰初始总是投出<color=#99FFFFFF>冰元素</color>。\\n（角色最多装备1件「圣遗物」）",
    "Blizzard Strayer": "冰风迷途的勇士",
    "<color=#FFFFFFFF>When a character uses a Skill or equips a Talent:</color> Spend 1 less <color=#80C0FFFF>Hydro Die</color>. (Once per Round)\\n(A character can equip a maximum of 1 Artifact)": "<color=#FFFFFFFF>角色使用技能或装备「天赋」时：</color>少花费1个<color=#80C0FFFF>水元素</color>。（每回合1次）\\n（角色最多装备1件「圣遗物」）",
    "Wine-Stained Tricorne": "酒渍船帽",
    "<color=#FFFFFFFF>When a character uses a Skill or equips a Talent:</color> Spend 1 less <color=#80C0FFFF>Hydro Die</color>. (Once per Round)\\n<color=#FFFFFFFF>Roll Phase:</color> 2 of the starting Elemental Dice you roll are always guaranteed to be <color=#80C0FFFF>Hydro Dice</color>.\\n(A character can equip a maximum of 1 Artifact)": "<color=#FFFFFFFF>角色使用技能或装备「天赋」时：</color>少花费1个<color=#80C0FFFF>水元素</color>。（每回合1次）\\n<color=#FFFFFFFF>投掷阶段：</color>2个元素骰初始总是投出<color=#80C0FFFF>水元素</color>。\\n（角色最多装备1件「圣遗物」）",
    "Heart of Depth": "沉沦之心",
    "<color=#FFFFFFFF>When a character uses a Skill or equips a Talent:</color> Spend 1 less <color=#FF9999FF>Pyro Die</color>. (Once per Round)\\n(A character can equip a maximum of 1 Artifact)": "<color=#FFFFFFFF>角色使用技能或装备「天赋」时：</color>少花费1个<color=#FF9999FF>火元素</color>。（每回合1次）\\n（角色最多装备1件「圣遗物」）",
    "Witch's Scorching Hat": "焦灼的魔女帽",
    "<color=#FFFFFFFF>When a character uses a Skill or equips a Talent:</color> Spend 1 less <color=#FF9999FF>Pyro Die</color>. (Once per Round)\\n<color=#FFFFFFFF>Roll Phase:</color> 2 of the starting Elemental Dice you roll are always guaranteed to be <color=#FF9999FF>Pyro Dice</color>.\\n(A character can equip a maximum of 1 Artifact)": "<color=#FFFFFFFF>角色使用技能或装备「天赋」时：</color>少花费1个<color=#FF9999FF>火元素</color>。（每回合1次）\\n<color=#FFFFFFFF>投掷阶段：</color>2个元素骰初始总是投出<color=#FF9999FF>火元素</color>。\\n（角色最多装备1件「圣遗物」）",
    "Crimson Witch of Flames": "炽烈的炎之魔女",
    "<color=#FFFFFFFF>When a character uses a Skill or equips a Talent:</color> Spend 1 less <color=#FFACFFFF>Electro Die</color>. (Once per Round)\\n(A character can equip a maximum of 1 Artifact)": "<color=#FFFFFFFF>角色使用技能或装备「天赋」时：</color>少花费1个<color=#FFACFFFF>雷元素</color>。（每回合1次）\\n（角色最多装备1件「圣遗物」）",
    "Thunder Summoner's Crown": "唤雷的头冠",
    "<color=#FFFFFFFF>When a character uses a Skill or equips a Talent:</color> Spend 1 less <color=#FFACFFFF>Electro Die</color>. (Once per Round)\\n<color=#FFFFFFFF>Roll Phase:</color> 2 of the starting Elemental Dice you roll are always guaranteed to be <color=#FFACFFFF>Electro Dice</color>.\\n(A character can equip a maximum of 1 Artifact)": "<color=#FFFFFFFF>角色使用技能或装备「天赋」时：</color>少花费1个<color=#FFACFFFF>雷元素</color>。（每回合1次）\\n<color=#FFFFFFFF>投掷阶段：</color>2个元素骰初始总是投出<color=#FFACFFFF>雷元素</color>。\\n（角色最多装备1件「圣遗物」）",
    "Thundering Fury": "如雷的盛怒",
    "<color=#FFFFFFFF>When a character uses a Skill or equips a Talent:</color> Spend 1 less <color=#80FFD7FF>Anemo Die</color>. (Once per Round)\\n(A character can equip a maximum of 1 Artifact)": "<color=#FFFFFFFF>角色使用技能或装备「天赋」时：</color>少花费1个<color=#80FFD7FF>风元素</color>。（每回合1次）\\n（角色最多装备1件「圣遗物」）",
    "Viridescent Venerer's Diadem": "翠绿的猎人之冠",
    "<color=#FFFFFFFF>When a character uses a Skill or equips a Talent:</color> Spend 1 less <color=#80FFD7FF>Anemo Die</color>. (Once per Round)\\n<color=#FFFFFFFF>Roll Phase:</color> 2 of the starting Elemental Dice you roll are always guaranteed to be <color=#80FFD7FF>Anemo Dice</color>.\\n(A character can equip a maximum of 1 Artifact)": "<color=#FFFFFFFF>角色使用技能或装备「天赋」时：</color>少花费1个<color=#80FFD7FF>风元素</color>。（每回合1次）\\n<color=#FFFFFFFF>投掷阶段：</color>2个元素骰初始总是投出<color=#80FFD7FF>风元素</color>。\\n（角色最多装备1件「圣遗物」）",
    "Viridescent Venerer": "翠绿之影",
    "<color=#FFFFFFFF>When a character uses a Skill or equips a Talent:</color> Spend 1 less <color=#FFE699FF>Geo Die</color>. (Once per Round)\\n(A character can equip a maximum of 1 Artifact)": "<color=#FFFFFFFF>角色使用技能或装备「天赋」时：</color>少花费1个<color=#FFE699FF>岩元素</color>。（每回合1次）\\n（角色最多装备1件「圣遗物」）",
    "Mask of Solitude Basalt": "不动玄石之相",
    "<color=#FFFFFFFF>When a character uses a Skill or equips a Talent:</color> Spend 1 less <color=#FFE699FF>Geo Die</color>. (Once per Round)\\n<color=#FFFFFFFF>Roll Phase:</color> 2 of the starting Elemental Dice you roll are always guaranteed to be <color=#FFE699FF>Geo Dice</color>.\\n(A character can equip a maximum of 1 Artifact)": "<color=#FFFFFFFF>角色使用技能或装备「天赋」时：</color>少花费1个<color=#FFE699FF>岩元素</color>。（每回合1次）\\n<color=#FFFFFFFF>投掷阶段：</color>2个元素骰初始总是投出<color=#FFE699FF>岩元素</color>。\\n（角色最多装备1件「圣遗物」）",
    "Archaic Petra": "悠古的磐岩",
    "<color=#FFFFFFFF>When a character uses a Skill or equips a Talent:</color> Spend 1 less <color=#99FF88FF>Dendro Die</color>. (Once per Round)\\n(A character can equip a maximum of 1 Artifact)": "<color=#FFFFFFFF>角色使用技能或装备「天赋」时：</color>少花费1个<color=#99FF88FF>草元素</color>。（每回合1次）\\n（角色最多装备1件「圣遗物」）",
    "Laurel Coronet": "月桂的宝冠",
    "<color=#FFFFFFFF>When a character uses a Skill or equips a Talent:</color> Spend 1 less <color=#99FF88FF>Dendro Die</color>. (Once per Round)\\n<color=#FFFFFFFF>Roll Phase:</color> 2 of the starting Elemental Dice you roll are always guaranteed to be <color=#99FF88FF>Dendro Dice</color>.\\n(A character can equip a maximum of 1 Artifact)": "<color=#FFFFFFFF>角色使用技能或装备「天赋」时：</color>少花费1个<color=#99FF88FF>草元素</color>。（每回合1次）\\n<color=#FFFFFFFF>投掷阶段：</color>2个元素骰初始总是投出<color=#99FF88FF>草元素</color>。\\n（角色最多装备1件「圣遗物」）",
    "Deepwood Memories": "深林的记忆",
    "Location": "场地",
    "<color=#FFFFFFFF>End Phase:</color> Draw 2 cards.\\n<color=#FFFFFFFF>Usage(s)</color>: 2": "<color=#FFFFFFFF>结束阶段：</color>抓2张牌。\\n<color=#FFFFFFFF>可用次数</color>：2",
    "Liyue Harbor Wharf": "璃月港口",
    "<color=#FFFFFFFF>When played:</color> Select any Elemental Dice to reroll.\\n<color=#FFFFFFFF>Roll Phase:</color> Gain another chance to reroll.": "<color=#FFFFFFFF>入场时：</color>选择任意元素骰重投。\\n<color=#FFFFFFFF>投掷阶段：</color>获得额外一次重投机会。",
    "Knights of Favonius Library": "骑士团图书馆",
    "<color=#FFFFFFFF>Roll Phase:</color> 2 of the starting Elemental Dice you roll are always guaranteed to match the Elemental Type of your active character.": "<color=#FFFFFFFF>投掷阶段：</color>2个元素骰初始总是投出我方出战角色类型的元素。",
    "Jade Chamber": "群玉阁",
    "<color=#FFFFFFFF>When you perform \"Switch Character\":</color> Spend 1 less Elemental Die. (Once per Round)": "<color=#FFFFFFFF>我方执行「切换角色」行动时：</color>少花费1个元素骰。（每回合1次）",
    "Dawn Winery": "晨曦酒庄",
    "<color=#FFFFFFFF>End Phase:</color> Heal the most injured character on standby for 2 HP.\\n<color=#FFFFFFFF><color=#FFFFFFFF>Usage(s)</color>: 2</color>": "<color=#FFFFFFFF>结束阶段：</color>治疗受伤最多的我方后台角色2点。\\n<color=#FFFFFFFF><color=#FFFFFFFF>可用次数</color>：2</color>",
    "Wangshu Inn": "望舒客栈",
    "<color=#FFFFFFFF>End Phase:</color> Heal your active character for 2 HP.\\n<color=#FFFFFFFF><color=#FFFFFFFF>Usage(s)</color>: 2</color>": "<color=#FFFFFFFF>结束阶段：</color>治疗我方出战角色2点。\\n<color=#FFFFFFFF><color=#FFFFFFFF>可用次数</color>：2</color>",
    "Favonius Cathedral": "西风大教堂",
    "Companion": "伙伴",
    "<color=#FFFFFFFF>When Action Phase begins:</color> Create <color=#FFFFFFFF>Omni Element</color> ×2.\\n<color=#FFFFFFFF><color=#FFFFFFFF>Usage(s)</color>: 2</color>": "<color=#FFFFFFFF>行动阶段开始时：</color>生成2点<color=#FFFFFFFF>万能元素</color>。\\n<color=#FFFFFFFF><color=#FFFFFFFF>可用次数</color>：2</color>",
    "Paimon": "派蒙",
    "<color=#FFFFFFFF>When you perform \"Switch Character\":</color> This switch is considered a <color=#FFFFFFFF>Fast Action</color> instead of a <color=#FFFFFFFF>Combat Action</color>. (Once per Round)": "<color=#FFFFFFFF>我方执行「切换角色」行动时：</color>将此次切换视为「<color=#FFFFFFFF>快速行动</color>」而非「<color=#FFFFFFFF>战斗行动</color>」。（每回合1次）",
    "Katheryne": "凯瑟琳",
    "Comes with 2 Transmutation Materials when played.\\n<color=#FFFFFFFF>End Phase:</color> Gain 1 Transmutation Material.\\n<color=#FFFFFFFF>When playing an Artifact Card:</color> If possible, spend Transmutation Materials equal to the total cost of the Artifact and equip this Artifact for free. (Once per Round)": "入场时附带2个「合成材料」。\\n<color=#FFFFFFFF>结束阶段：</color>补充1个「合成材料」。\\n<color=#FFFFFFFF>打出「圣遗物」手牌时：</color>如可能，则支付等同于「圣遗物」总费用数量的「合成材料」，以免费装备此「圣遗物」。（每回合1次）",
    "Timaeus": "蒂玛乌斯",
    "Comes with 2 Forging Billets when played.\\n<color=#FFFFFFFF>End Phase:</color> Gain 1 Forging Billet.\\n<color=#FFFFFFFF>When playing a Weapon Card:</color> If possible, spend Forging Billets equal to the total cost of the Weapon and equip this Weapon for free. (Once per Round)": "入场时附带2个「锻造原胚」。\\n<color=#FFFFFFFF>结束阶段：</color>补充1个「锻造原胚」。\\n<color=#FFFFFFFF>打出「武器」手牌时：</color>如可能，则支付等同于「武器」总费用数量的「锻造原胚」，以免费装备此「武器」。（每回合1次）",
    "Wagner": "瓦格纳",
    "<color=#FFFFFFFF>After playing a Food Event Card:</color> Create 1 random Elemental Die. (Once per Round)": "<color=#FFFFFFFF>打出「料理」事件牌后：</color>生成1个随机基础元素骰。（每回合1次）",
    "Chef Mao": "卯师傅",
    "<color=#FFFFFFFF>When playing a Location Support Card:</color> Spend 2 less Elemental Dice. (Once per Round)": "<color=#FFFFFFFF>打出「场地」支援牌时：</color>少花费2个元素骰。（每回合1次）",
    "Tubby": "阿圆",
    "<color=#FFFFFFFF>Triggers automatically once per Round:</color> This card gains <color=#FFFFFFFF>1 Pigeon</color>.\\nWhen this card gains <color=#FFFFFFFF>3 Pigeons</color>, discard this card, then draw 1 card and create <color=#FFFFFFFF>Omni Element</color> ×1.": "<color=#FFFFFFFF>每回合自动触发1次：</color>此牌累积<color=#FFFFFFFF>1只「鸽子」</color>。\\n如果此牌已累积<color=#FFFFFFFF>3只「鸽子」</color>，则弃置此牌：抓1张牌，生成一点<color=#FFFFFFFF>万能元素</color>。",
    "Timmie": "提米",
    "<color=#FFFFFFFF>End Phase:</color> Collect your unused Elemental Dice (Max 1 of each Elemental Type).\\n<color=#FFFFFFFF>When Action Phase begins:</color> If this card has collected 3 Elemental Dice, draw 2 cards and create <color=#FFFFFFFF>Omni Element</color> ×2, then discard this card.": "<color=#FFFFFFFF>结束阶段：</color>收集我方未使用的元素骰（每种最多1个）。\\n<color=#FFFFFFFF>行动阶段开始时：</color>如果此牌已收集3个元素骰，则抓2张牌，生成2点<color=#FFFFFFFF>万能元素</color>，然后弃置此牌。",
    "Liben": "立本",
    "<color=#FFFFFFFF>After either side uses a Skill:</color> If <color=#FFFFFFFF>Physical DMG</color> or <color=#FFFFFFFF>Piercing DMG</color> was dealt, or an <color=#FFFFFFFF>Elemental Reaction</color> was triggered, this card gains <color=#FFFFFFFF>1 Inspiration</color>.\\nWhen this card gains <color=#FFFFFFFF>3 Inspiration</color>, discard this card, then draw 2 cards.": "<color=#FFFFFFFF>双方角色使用技能后：</color>如果造成了<color=#FFFFFFFF>物理伤害</color>、<color=#FFFFFFFF>穿透伤害</color>或引发了<color=#FFFFFFFF>元素反应</color>，此牌累积<color=#FFFFFFFF>1个「灵感」</color>。\\n如果此牌已累积<color=#FFFFFFFF>3个「灵感」</color>，弃置此牌：抓2张牌。",
    "Chang the Ninth": "常九爷",
    "<color=#FFFFFFFF>When you use a Skill that has already been used in this Round:</color> Spend 1 less Elemental Die. (Once per Round)": "<color=#FFFFFFFF>我方角色使用本回合使用过的技能时：</color>少花费1个元素骰。（每回合1次）",
    "Ellin": "艾琳",
    "<color=#FFFFFFFF>End Phase:</color> One of your characters without maximum Energy gains 1 <color=#FFFFFFFF>Energy</color>. (Active Character prioritized)\\n<color=#FFFFFFFF><color=#FFFFFFFF>Usage(s)</color>: 2</color>": "<color=#FFFFFFFF>结束阶段：</color>我方一名充能未满的角色获得1点<color=#FFFFFFFF>充能</color>。（出战角色优先）\\n<color=#FFFFFFFF><color=#FFFFFFFF>可用次数</color>：2</color>",
    "Iron Tongue Tian": "田铁嘴",
    "<color=#FFFFFFFF>After you switch characters:</color> If the character you switched to does not have <color=#FFFFFFFF>Energy</color>, they will gain 1 <color=#FFFFFFFF>Energy</color>. (Once per Round)\\n<color=#FFFFFFFF><color=#FFFFFFFF>Usage(s)</color>: 2</color>": "<color=#FFFFFFFF>我方切换角色后：</color>如果切换到的角色没有<color=#FFFFFFFF>充能</color>，则使该角色获得1点<color=#FFFFFFFF>充能</color>。（每回合1次）\\n<color=#FFFFFFFF><color=#FFFFFFFF>可用次数</color>：2</color>",
    "Liu Su": "刘苏",
    "Item": "道具",
    "<color=#FFFFFFFF>When either side uses a Skill:</color> If Elemental DMG was dealt, this card gains <color=#FFFFFFFF>1 Qualitative Progress</color>.\\nWhen this card gains <color=#FFFFFFFF>3 Qualitative Progress</color>, discard this card, then create 3 different Basic Elemental Dice.": "<color=#FFFFFFFF>双方角色使用技能后：</color>如果造成了元素伤害，此牌累积<color=#FFFFFFFF>1个「质变进度」</color>。\\n当此牌已累积<color=#FFFFFFFF>3个「质变进度」</color>时，弃置此牌：生成3个不同的基础元素骰子。",
    "Parametric Transformer": "参量质变仪",
    "<color=#FFFFFFFF>When played:</color> Draw 1 Food Event Card from your deck.\\n<color=#FFFFFFFF>When you play a Food Event Card:</color> Draw 1 Food Event Card from your deck. (Once per Round)": "<color=#FFFFFFFF>入场时：</color>从牌组中随机抽取1张「料理」事件。\\n<color=#FFFFFFFF>我方打出「料理」事件牌时：</color>从牌组中随机抽取1张「料理」事件。（每回合1次）",
    "NRE": "便携营养袋",
    "Elemental Resonance": "元素共鸣",
    "Create 1 <color=#99FFFFFF>Cryo Die</color>.\\n(You must have at least 2 <color=#99FFFFFF>Cryo</color> characters in your deck to add this card to your deck.)": "生成1个<color=#99FFFFFF>冰元素骰</color>。\\n（牌组包含至少2个<color=#99FFFFFF>冰元素</color>角色，才能加入牌组）",
    "Elemental Resonance: Woven Ice": "元素共鸣：交织之冰",
    "During this Round, your current active character will deal +2 DMG for the next instance.\\n(You must have at least 2 <color=#99FFFFFF>Cryo</color> characters in your deck to add this card to your deck.)": "本回合中，我方当前出战角色下一次造成的伤害+2。\\n（牌组包含至少2个<color=#99FFFFFF>冰元素</color>角色，才能加入牌组）",
    "Elemental Resonance: Shattering Ice": "元素共鸣：粉碎之冰",
    "Create 1 <color=#80C0FFFF>Hydro Die</color>.\\n(You must have at least 2 <color=#80C0FFFF>Hydro</color> characters in your deck to add this card to your deck.)": "生成1个<color=#80C0FFFF>水元素骰</color>。\\n（牌组包含至少2个<color=#80C0FFFF>水元素</color>角色，才能加入牌组）",
    "Elemental Resonance: Woven Waters": "元素共鸣：交织之水",
    "Heal your active character for 2 HP and all your characters on standby for 1 HP.\\n(You must have at least 2 <color=#80C0FFFF>Hydro</color> characters in your deck to add this card to your deck.)": "治疗我方出战角色2点。然后，治疗所有我方后台角色1点。\\n（牌组包含至少2个<color=#80C0FFFF>水元素</color>角色，才能加入牌组）",
    "Elemental Resonance: Soothing Water": "元素共鸣：愈疗之水",
    "Create 1 <color=#FF9999FF>Pyro Die</color>.\\n(You must have at least 2 <color=#FF9999FF>Pyro</color> characters in your deck to add this card to your deck.)": "生成1个<color=#FF9999FF>火元素骰</color>。\\n（牌组包含至少2个<color=#FF9999FF>火元素</color>角色，才能加入牌组）",
    "Elemental Resonance: Woven Flames": "元素共鸣：交织之火",
    "During this round, the next instance of <color=#FF9999FF>Pyro-Related Reactions</color> your current active character triggers deals +3 DMG.\\n(You must have at least 2 <color=#FF9999FF>Pyro</color> characters in your deck to add this card to your deck.)": "本回合中，我方当前出战角色下一次引发<color=#FF9999FF>火元素相关反应</color>时，造成的伤害+3。\\n（牌组包含至少2个<color=#FF9999FF>火元素</color>角色，才能加入牌组）",
    "Elemental Resonance: Fervent Flames": "元素共鸣：热诚之火",
    "Create 1 <color=#FFACFFFF>Electro Die</color>.\\n(You must have at least 2 <color=#FFACFFFF>Electro</color> characters in your deck to add this card to your deck.)": "生成1个<color=#FFACFFFF>雷元素骰</color>。\\n（牌组包含至少2个<color=#FFACFFFF>雷元素</color>角色，才能加入牌组）",
    "Elemental Resonance: Woven Thunder": "元素共鸣：交织之雷",
    "One of your characters without maximum Energy gains 1 <color=#FFFFFFFF>Energy</color>. (Active Character prioritized)\\n(You must have at least 2 <color=#FFACFFFF>Electro</color> characters in your deck to add this card to your deck.)": "我方一名充能未满的角色获得1点<color=#FFFFFFFF>充能</color>。（出战角色优先）\\n（牌组包含至少2个<color=#FFACFFFF>雷元素</color>角色，才能加入牌组）",
    "Elemental Resonance: High Voltage": "元素共鸣：强能之雷",
    "Create 1 <color=#80FFD7FF>Anemo Die</color>.\\n(You must have at least 2 <color=#80FFD7FF>Anemo</color> characters in your deck to add this card to your deck.)": "生成1个<color=#80FFD7FF>风元素骰</color>。\\n（牌组包含至少2个<color=#80FFD7FF>风元素</color>角色，才能加入牌组）",
    "Elemental Resonance: Woven Winds": "元素共鸣：交织之风",
    "Switch to the target character and create <color=#FFFFFFFF>Omni Element</color> ×1.\\n(You must have at least 2 <color=#80FFD7FF>Anemo</color> characters in your deck to add this card to your deck.)": "切换到目标角色，并生成1点<color=#FFFFFFFF>万能元素</color>。\\n（牌组包含至少2个<color=#80FFD7FF>风元素</color>角色，才能加入牌组）",
    "Elemental Resonance: Impetuous Winds": "元素共鸣：迅捷之风",
    "Create 1 <color=#FFE699FF>Geo Die</color>.\\n(You must have at least 2 <color=#FFE699FF>Geo</color> characters in your deck to add this card to your deck.)": "生成1个<color=#FFE699FF>岩元素骰</color>。\\n（牌组包含至少2个<color=#FFE699FF>岩元素</color>角色，才能加入牌组）",
    "Elemental Resonance: Woven Stone": "元素共鸣：交织之岩",
    "During this round, after your character deals <color=#FFE699FF>Geo DMG</color> next time: Should there be any Combat Status on your side that provides <color=#FFFFFFFF>Shield</color>, grant one such Status with 3 <color=#FFFFFFFF>Shield</color> points. \\n(You must have at least 2 <color=#FFE699FF>Geo</color> characters in your deck to add this card to your deck.)": "本回合中，我方角色下一次造成<color=#FFE699FF>岩元素伤害</color>后：如果我方存在提供「<color=#FFFFFFFF>护盾</color>」的出战状态，则为一个此类出战状态补充3点「<color=#FFFFFFFF>护盾</color>」。\\n（牌组包含至少2个<color=#FFE699FF>岩元素</color>角色，才能加入牌组）",
    "Elemental Resonance: Enduring Rock": "元素共鸣：坚定之岩",
    "Create 1 <color=#99FF88FF>Dendro Die</color>.\\n(You must have at least 2 <color=#99FF88FF>Dendro</color> characters in your deck to add this card to your deck.)": "生成1个<color=#99FF88FF>草元素骰</color>。\\n（牌组包含至少2个<color=#99FF88FF>草元素</color>角色，才能加入牌组）",
    "Elemental Resonance: Woven Weeds": "元素共鸣：交织之草",
    "During this round, the next Elemental Reaction your active character triggers deals +2 DMG.\\nYour <color=#FFFFFFFF>Burning Flame, Dendro Core, and Catalyzing Field</color> gain +1 <color=#FFFFFFFF>Usage(s)</color>.\\n(You must have at least 2 <color=#99FF88FF>Dendro</color> characters in your deck to add this card to your deck.)": "本回合中，我方下一次引发元素反应时，造成的伤害+2。\\n使我方场上的<color=#FFFFFFFF>燃烧烈焰、草原核和激化领域</color>「<color=#FFFFFFFF>可用次数</color>」+1。\\n（牌组包含至少2个<color=#99FF88FF>草元素</color>角色，才能加入牌组）",
    "Elemental Resonance: Sprawling Greenery": "元素共鸣：蔓生之草",
    "Convert the Elemental Dice spent to <color=#FFFFFFFF>Omni Element</color> ×2.": "将所花费的元素骰转换为2个<color=#FFFFFFFF>万能元素</color>。",
    "The Bestest Travel Companion!": "最好的伙伴！",
    "<color=#FFFFFFFF>The next time you perform \"Switch Character\":</color> Spend 1 less Elemental Die.": "<color=#FFFFFFFF>我方下次执行「切换角色」行动时：</color>少花费1个元素骰。",
    "Changing Shifts": "换班时间",
    "Select any Elemental Dice to <color=#FFFFFFFF>reroll</color>. Can reroll 2 times.": "选择任意元素骰<color=#FFFFFFFF>重投</color>，可重投2次。",
    "Toss-Up": "一掷乾坤",
    "Draw 2 cards.": "抓2张牌。",
    "Strategize": "运筹帷幄",
    "Only playable if one of your characters is defeated this Round:\\nCreate <color=#FFFFFFFF>Omni Element</color> ×1 and your current active character gains 1 <color=#FFFFFFFF>Energy</color>.": "本回合有我方角色被击倒，才能打出：\\n生成1个<color=#FFFFFFFF>万能元素</color>，我方当前出战角色获得1点<color=#FFFFFFFF>充能</color>。",
    "I Haven't Lost Yet!": "本大爷还没有输！",
    "<color=#FFFFFFFF>The next time you perform \"Switch Character\":</color> This switch will be considered a <color=#FFFFFFFF>Fast Action</color> instead of a <color=#FFFFFFFF>Combat Action</color>.": "<color=#FFFFFFFF>我方下次执行「切换角色」行动时：</color>将此次切换视为「<color=#FFFFFFFF>快速行动</color>」而非「<color=#FFFFFFFF>战斗行动</color>」。",
    "Leave It to Me!": "交给我吧！",
    "<color=#FFFFFFFF>The next time you use a Skill:</color> Switch your next character in to be the active character.": "<color=#FFFFFFFF>我方下一次使用技能后：</color>将下一个我方后台角色切换到场上。",
    "When the Crane Returned": "鹤归之时",
    "Your current Active Character <color=#FFFFFFFF>gains 1 <color=#FFFFFFFF>Energy</color></color>.": "我方当前出战角色<color=#FFFFFFFF>获得1点<color=#FFFFFFFF>充能</color></color>。",
    "Starsigns": "星天之兆",
    "Shift 1 <color=#FFFFFFFF>Energy</color> from at most 2 of your characters on standby to your active character.": "从最多2个我方后台角色身上，转移1点<color=#FFFFFFFF>充能</color>到我方出战角色。",
    "Calx's Arts": "白垩之术",
    "Shift 1 Weapon Equipment Card that has been equipped to one of your characters to another one of your characters of the same Weapon Type.": "将一个装备在我方角色的「武器」装备牌，转移给另一个武器类型相同的我方角色。",
    "Master of Weaponry": "诸武精通",
    "Shift 1 Artifact Equipment Card that has been equipped to one of your characters to another one of your characters.": "将一个装备在我方角色的「圣遗物」装备牌，转移给另一个我方角色。",
    "Blessing of the Divine Relic's Installation": "神宝迁宫祝词",
    "Choose one Summon on your side and grant it +1 <color=#FFFFFFFF>Usage(s)</color>.": "选择一个我方「召唤物」，使其「<color=#FFFFFFFF>可用次数</color>」+1。",
    "Quick Knit": "快快缝补术",
    "Choose one Summon on the opposing side and destroy it.": "选择一个敌方「召唤物」，将其消灭。",
    "Send Off": "送你一程",
    "Destroy all Summons. (Affects both you and your opponent!)": "消灭所有「召唤物」。（不分敌我！）",
    "Guardian's Oath": "护法之誓",
    "Summon 1 <color=#FFFFFFFF>Random Hilichurl Summon</color>!\\n(You must have at least 2 Monster characters in your deck to add this card to your deck.)": "召唤一个<color=#FFFFFFFF>随机「丘丘人」召唤物</color>！\\n（牌组包含至少2个「魔物」角色，才能加入牌组）",
    "Abyssal Summons": "深渊的呼唤",
    "Food": "料理",
    "During this Round, the target character's next <color=#FFFFFFFF>Normal Attack</color> deals +1 DMG.\\n(A character can consume at most 1 Food per Round)": "本回合中，目标角色下一次<color=#FFFFFFFF>普通攻击</color>造成的伤害+1。\\n（每回合每个角色最多食用1次「料理」）",
    "Jueyun Guoba": "绝云锅巴",
    "During this Round, the target character's next <color=#FFFFFFFF>Elemental Burst</color> deals +3 DMG.\\n(A character can consume at most 1 Food per Round)": "本回合中，目标角色下一次<color=#FFFFFFFF>元素爆发</color>造成的伤害+3。\\n（每回合每个角色最多食用1次「料理」）",
    "Adeptus' Temptation": "仙跳墙",
    "During this Round, the target character takes -3 DMG the next time.\\n(A character can consume at most 1 Food per Round)": "本回合中，目标角色下次受到的伤害-3。\\n（每回合中每个角色最多食用1次「料理」）",
    "Lotus Flower Crisp": "莲花酥",
    "During this Round, the target character's next <color=#FFFFFFFF>Normal Attack</color> costs 1 less <color=#FFFFFFFF>Unaligned Element</color>.\\n(A character can consume at most 1 Food per Round)": "本回合中，目标角色下一次<color=#FFFFFFFF>普通攻击</color>少花费1个<color=#FFFFFFFF>无色元素</color>。\\n（每回合每个角色最多食用1次「料理」）",
    "Northern Smoked Chicken": "北地烟熏鸡",
    "Heal the target character for 1 HP.\\n(A character can consume at most 1 Food per Round)": "治疗目标角色1点。\\n（每回合每个角色最多食用1次「料理」）",
    "Sweet Madame": "甜甜花酿鸡",
    "Heal the target character for 2 HP.\\n(A character can consume at most 1 Food per Round)": "治疗目标角色2点。\\n（每回合每个角色最多食用1次「料理」）",
    "Mondstadt Hash Brown": "蒙德土豆饼",
    "Heal the target character for 1 HP. For the next two Rounds, heal this character for 1 HP again at the End Phase.\\n(A character can consume at most 1 Food per Round)": "治疗目标角色1点，两回合内结束阶段再治疗此角色1点。\\n（每回合每个角色最多食用1次「料理」）",
    "Mushroom Pizza": "烤蘑菇披萨",
    "Before this Round ends, the target character's next 3 <color=#FFFFFFFF>Normal Attacks</color> cost 1 less <color=#FFFFFFFF>Unaligned Element</color>.\\n(A character can consume at most 1 Food per Round)": "目标角色在本回合结束前，之后三次<color=#FFFFFFFF>普通攻击</color>都少花费1个<color=#FFFFFFFF>无色元素</color>。\\n（每回合每个角色最多食用1次「料理」）",
    "Minty Meat Rolls": "兽肉薄荷卷",
    "Ganyu": "甘雨",
    "Liutian Archery": "流天射术",
    "Deals 2 <color=#FFFFFFFF>Physical DMG</color>.": "造成2点<color=#FFFFFFFF>物理伤害</color>。",
    "Trail of the Qilin": "山泽麟迹",
    "Deals 1 <color=#99FFFFFF>Cryo DMG</color>, creates 1 <color=#FFFFFFFF>Ice Lotus</color>.": "造成1点<color=#99FFFFFF>冰元素伤害</color>，生成<color=#FFFFFFFF>冰莲</color>。",
    "Frostflake Arrow": "霜华矢",
    "Deals 2 <color=#99FFFFFF>Cryo DMG</color>, deals <color=#FFFFFFFF>2 <color=#FFFFFFFF>Piercing DMG</color></color> to all opposing characters on standby.": "造成2点<color=#99FFFFFF>冰元素伤害</color>，对所有敌方后台角色造成<color=#FFFFFFFF>2点<color=#FFFFFFFF>穿透伤害</color></color>。",
    "Celestial Shower": "降众天华",
    "Deals 1 <color=#99FFFFFF>Cryo DMG</color>, deals <color=#FFFFFFFF>1 <color=#FFFFFFFF>Piercing DMG</color></color> to all opposing characters on standby, summons 1 <color=#FFFFFFFF>Sacred Cryo Pearl</color>.": "造成1点<color=#99FFFFFF>冰元素伤害</color>，对所有敌方后台角色造成<color=#FFFFFFFF>1点<color=#FFFFFFFF>穿透伤害</color></color>，召唤<color=#FFFFFFFF>冰灵珠</color>。",
    "Diona": "迪奥娜",
    "Kätzlein Style": "猎人射术",
    "Icy Paws": "猫爪冻冻",
    "Deals 2 <color=#99FFFFFF>Cryo DMG</color>, creates 1 <color=#FFFFFFFF>Cat-Claw Shield</color>.": "造成2点<color=#99FFFFFF>冰元素伤害</color>，生成<color=#FFFFFFFF>猫爪护盾</color>。",
    "Signature Mix": "最烈特调",
    "Deals 1 <color=#99FFFFFF>Cryo DMG</color>, heals this character for 2 HP, summons 1 <color=#FFFFFFFF>Drunken Mist</color>.": "造成1点<color=#99FFFFFF>冰元素伤害</color>，治疗此角色2点，召唤<color=#FFFFFFFF>酒雾领域</color>。",
    "Kaeya": "凯亚",
    "Ceremonial Bladework": "仪典剑术",
    "Frostgnaw": "霜袭",
    "Deals 3 <color=#99FFFFFF>Cryo DMG</color>.": "造成3点<color=#99FFFFFF>冰元素伤害</color>。",
    "Glacial Waltz": "凛冽轮舞",
    "Deals 1 <color=#99FFFFFF>Cryo DMG</color>, creates 1 <color=#FFFFFFFF>Icicle</color>.": "造成1点<color=#99FFFFFF>冰元素伤害</color>，生成<color=#FFFFFFFF>寒冰之棱</color>。",
    "Chongyun": "重云",
    "Demonbane": "灭邪四式",
    "Chonghua's Layered Frost": "重华叠霜",
    "Deals 3 <color=#99FFFFFF>Cryo DMG</color>, creates 1 <color=#FFFFFFFF>Chonghua Frost Field</color>.": "造成3点<color=#99FFFFFF>冰元素伤害</color>，生成<color=#FFFFFFFF>重华叠霜领域</color>。",
    "Cloud-Parting Star": "云开星落",
    "Deals 7 <color=#99FFFFFF>Cryo DMG</color>.": "造成7点<color=#99FFFFFF>冰元素伤害</color>。",
    "Kamisato Ayaka": "神里绫华",
    "Kamisato Art: Kabuki": "神里流·倾",
    "Kamisato Art: Hyouka": "神里流·冰华",
    "Kamisato Art: Soumetsu": "神里流·霜灭",
    "Deals 4 <color=#99FFFFFF>Cryo DMG</color>, summons 1 <color=#FFFFFFFF>Frostflake Seki no To</color>.": "造成4点<color=#99FFFFFF>冰元素伤害</color>，召唤<color=#FFFFFFFF>霜见雪关扉</color>。",
    "Kamisato Art: Senho": "神里流·霰步",
    "(Passive) When switched to be the active character, this character gains <color=#FFFFFFFF>Cryo Elemental Infusion</color>.": "【被动】此角色被切换为「出战角色」时，附属<color=#FFFFFFFF>冰元素附魔</color>。",
    "Barbara": "芭芭拉",
    "Whisper of Water": "水之浅唱",
    "Deals 1 <color=#80C0FFFF>Hydro DMG</color>.": "造成1点<color=#80C0FFFF>水元素伤害</color>。",
    "Let the Show Begin♪": "演唱，开始♪",
    "Deals 1 <color=#80C0FFFF>Hydro DMG</color>, summons 1 <color=#FFFFFFFF>Melody Loop</color>.": "造成1点<color=#80C0FFFF>水元素伤害</color>，召唤<color=#FFFFFFFF>歌声之环</color>。",
    "Shining Miracle♪": "闪耀奇迹♪",
    "Heals all of your characters for 4 HP.": "治疗所有我方角色4点。",
    "Xingqiu": "行秋",
    "Guhua Style": "古华剑法",
    "Fatal Rainscreen": "画雨笼山",
    "Deals 2 <color=#80C0FFFF>Hydro DMG</color>, grants this character <color=#80C0FFFF>Hydro Application</color>, creates 1 <color=#FFFFFFFF>Rain Sword</color>.": "造成2点<color=#80C0FFFF>水元素伤害</color>，本角色<color=#80C0FFFF>附着水元素</color>，生成<color=#FFFFFFFF>雨帘剑</color>。",
    "Raincutter": "裁雨留虹",
    "Deals 1 <color=#80C0FFFF>Hydro DMG</color>, grants this character <color=#80C0FFFF>Hydro Application</color>, creates 1 <color=#FFFFFFFF>Rainbow Bladework</color>.": "造成1点<color=#80C0FFFF>水元素伤害</color>，本角色<color=#80C0FFFF>附着水元素</color>，生成<color=#FFFFFFFF>虹剑势</color>。",
    "Mona": "莫娜",
    "Ripple of Fate": "因果点破",
    "Mirror Reflection of Doom": "水中幻愿",
    "Deals 1 <color=#80C0FFFF>Hydro DMG</color>, summons 1 <color=#FFFFFFFF>Reflection</color>.": "造成1点<color=#80C0FFFF>水元素伤害</color>，召唤<color=#FFFFFFFF>虚影</color>。",
    "Stellaris Phantasm": "星命定轨",
    "Deals 4 <color=#80C0FFFF>Hydro DMG</color>, creates 1 <color=#FFFFFFFF>Illusory Bubble</color>.": "造成4点<color=#80C0FFFF>水元素伤害</color>，生成<color=#FFFFFFFF>泡影</color>。",
    "Illusory Torrent": "虚实流动",
    "(Passive) <color=#FFFFFFFF>When you perform \"Switch Character\" while Mona is your active character:</color> This switch is considered a <color=#FFFFFFFF>Fast Action</color> instead of a <color=#FFFFFFFF>Combat Action</color>. (Once per Round)": "【被动】<color=#FFFFFFFF>此角色为出战角色，我方执行「切换角色」行动时：</color>将此次切换视为「<color=#FFFFFFFF>快速行动</color>」而非「<color=#FFFFFFFF>战斗行动</color>」。（每回合1次）",
    "Diluc": "迪卢克",
    "Tempered Sword": "淬炼之剑",
    "Searing Onslaught": "逆焰之刃",
    "Deals 3 <color=#FF9999FF>Pyro DMG</color>. For the third use of this Skill each Round, deals +2 DMG.": "造成3点<color=#FF9999FF>火元素伤害</color>。每回合第三次使用本技能时，伤害+2。",
    "Dawn": "黎明",
    "Deals 8 <color=#FF9999FF>Pyro DMG</color>. This character gains <color=#FFFFFFFF>Pyro Infusion</color>.": "造成8点<color=#FF9999FF>火元素伤害</color>，本角色附属<color=#FFFFFFFF>火元素附魔</color>。",
    "Xiangling": "香菱",
    "Dough-Fu": "白案功夫",
    "Guoba Attack": "锅巴出击",
    "Summons 1 <color=#FFFFFFFF>Guoba</color>.": "召唤<color=#FFFFFFFF>锅巴</color>。",
    "Pyronado": "旋火轮",
    "Deals 2 <color=#FF9999FF>Pyro DMG</color>, creates 1 <color=#FFFFFFFF>Pyronado</color>.": "造成2点<color=#FF9999FF>火元素伤害</color>，生成<color=#FFFFFFFF>旋火轮</color>。",
    "Bennett": "班尼特",
    "Strike of Fortune": "好运剑",
    "Passion Overload": "热情过载",
    "Deals 3 <color=#FF9999FF>Pyro DMG</color>.": "造成3点<color=#FF9999FF>火元素伤害</color>。",
    "Fantastic Voyage": "美妙旅程",
    "Deals 2 <color=#FF9999FF>Pyro DMG</color>, creates 1 <color=#FFFFFFFF>Inspiration Field</color>.": "造成2点<color=#FF9999FF>火元素伤害</color>，生成<color=#FFFFFFFF>鼓舞领域</color>。",
    "Yoimiya": "宵宫",
    "Firework Flare-Up": "烟火打扬",
    "Niwabi Fire-Dance": "焰硝庭火舞",
    "This character gains <color=#FFFFFFFF>Niwabi Enshou</color>. (This Skill does not grant Energy)": "本角色附属<color=#FFFFFFFF>庭火焰硝</color>。（此技能不产生充能）",
    "Ryuukin Saxifrage": "琉金云间草",
    "Deals 4 <color=#FF9999FF>Pyro DMG</color>, creates 1 <color=#FFFFFFFF>Aurous Blaze</color>.": "造成4点<color=#FF9999FF>火元素伤害</color>，生成<color=#FFFFFFFF>琉金火光</color>。",
    "Klee": "可莉",
    "Kaboom!": "砰砰",
    "Deals 1 <color=#FF9999FF>Pyro DMG</color>.": "造成1点<color=#FF9999FF>火元素伤害</color>。",
    "Jumpy Dumpty": "蹦蹦炸弹",
    "Deals 3 <color=#FF9999FF>Pyro DMG</color>. This character gains <color=#FFFFFFFF>Explosive Spark</color>.": "造成3点<color=#FF9999FF>火元素伤害</color>，本角色附属<color=#FFFFFFFF>爆裂火花</color>。",
    "Sparks 'n' Splash": "轰轰火花",
    "Deals 3 <color=#FF9999FF>Pyro DMG</color>, creates 1 <color=#FFFFFFFF>Sparks 'n' Splash</color> at the opponent's play area.": "造成3点<color=#FF9999FF>火元素伤害</color>，在对方场上生成<color=#FFFFFFFF>轰轰火花</color>。",
    "Fischl": "菲谢尔",
    "Bolts of Downfall": "罪灭之矢",
    "Nightrider": "夜巡影翼",
    "Deals 1 <color=#FFACFFFF>Electro DMG</color>, summons 1 <color=#FFFFFFFF>Oz</color>.": "造成1点<color=#FFACFFFF>雷元素伤害</color>，召唤<color=#FFFFFFFF>奥兹</color>。",
    "Midnight Phantasmagoria": "至夜幻现",
    "Deals 4 <color=#FFACFFFF>Electro DMG</color>, deals 2 <color=#FFFFFFFF><color=#FFFFFFFF>Piercing DMG</color></color> to all opposing characters on standby.": "造成4点<color=#FFACFFFF>雷元素伤害</color>，对所有敌方后台角色造成2点<color=#FFFFFFFF><color=#FFFFFFFF>穿透伤害</color></color>。",
    "Razor": "雷泽",
    "Steel Fang": "钢脊",
    "Claw and Thunder": "利爪与苍雷",
    "Deals 3 <color=#FFACFFFF>Electro DMG</color>.": "造成3点<color=#FFACFFFF>雷元素伤害</color>。",
    "Lightning Fang": "雷牙",
    "Deals 5 <color=#FFACFFFF>Electro DMG</color>. This character gains <color=#FFFFFFFF>The Wolf Within</color>.": "造成5点<color=#FFACFFFF>雷元素伤害</color>，本角色附属<color=#FFFFFFFF>雷狼</color>。",
    "Keqing": "刻晴",
    "Yunlai Swordsmanship": "云来剑法",
    "Stellar Restoration": "星斗归位",
    "Deals 3 <color=#FFACFFFF>Electro DMG</color>, creates 1 <color=#FFFFFFFF>Lightning Stiletto</color>.": "造成3点<color=#FFACFFFF>雷元素伤害</color>，生成手牌<color=#FFFFFFFF>雷楔</color>。",
    "Starward Sword": "天街巡游",
    "Deals 4 <color=#FFACFFFF>Electro DMG</color>, deals <color=#FFFFFFFF>3 <color=#FFFFFFFF>Piercing DMG</color></color> to all opposing characters on standby.": "造成4点<color=#FFACFFFF>雷元素伤害</color>，对所有敌方后台角色造成<color=#FFFFFFFF>3点<color=#FFFFFFFF>穿透伤害</color></color>。",
    "Cyno": "赛诺",
    "Invoker's Spear": "七圣枪术",
    "Secret Rite: Chasmic Soulfarer": "秘仪·律渊渡魂",
    "Sacred Rite: Wolf's Swiftness": "圣仪·煟煌随狼行",
    "Deals 4 <color=#FFACFFFF>Electro DMG</color>.\\n<color=#FFFFFFFF>Pactsworn Pathclearer</color>'s Indwelling Level +2.": "造成4点<color=#FFACFFFF>雷元素伤害</color>，\\n<color=#FFFFFFFF>启途誓使</color>的[凭依]级数+2。",
    "Lawful Enforcer": "行度誓惩",
    "(Passive) When the battle begins, this character gains <color=#FFFFFFFF>Pactsworn Pathclearer</color>.": "【被动】战斗开始时，初始附属<color=#FFFFFFFF>启途誓使</color>。",
    "Beidou": "北斗",
    "Oceanborne": "征涛",
    "Tidecaller": "捉浪",
    "This character gains a <color=#FFFFFFFF>Tidecaller: Surf Embrace</color>. <color=#FFFFFFFF>Prepare Skill</color>: <color=#FFFFFFFF>Wavestrider</color>.": "本角色附属<color=#FFFFFFFF>捉浪·涛拥之守</color>并<color=#FFFFFFFF>准备技能</color>：<color=#FFFFFFFF>踏潮</color>。",
    "Stormbreaker": "斫雷",
    "Deals 3 <color=#FFACFFFF>Electro DMG</color>, creates 1 <color=#FFFFFFFF>Thunderbeast's Targe</color>.": "造成3点<color=#FFACFFFF>雷元素伤害</color>，生成<color=#FFFFFFFF>雷兽之盾</color>。",
    "Wavestrider": "踏潮",
    "(Prepare for 1 turn)\\nDeals 2 <color=#FFACFFFF>Electro DMG</color>.": "（需准备1个行动轮）\\n造成2点<color=#FFACFFFF>雷元素伤害</color>。",
    "Sucrose": "砂糖",
    "Wind Spirit Creation": "简式风灵作成",
    "Deals 1 <color=#80FFD7FF>Anemo DMG</color>.": "造成1点<color=#80FFD7FF>风元素伤害</color>。",
    "Astable Anemohypostasis Creation - 6308": "风灵作成·陆叁零捌",
    "Deals 3 <color=#80FFD7FF>Anemo DMG</color>, the target is forcibly switched to the previous character.": "造成3点<color=#80FFD7FF>风元素伤害</color>，使对方强制切换到前一个角色。",
    "Forbidden Creation - Isomer 75 / Type II": "禁·风灵作成·柒伍同构贰型",
    "Deals 1 <color=#80FFD7FF>Anemo DMG</color>, summons 1 <color=#FFFFFFFF>Large Wind Spirit</color>.": "造成1点<color=#80FFD7FF>风元素伤害</color>，召唤<color=#FFFFFFFF>大型风灵</color>。",
    "Jean": "琴",
    "Favonius Bladework": "西风剑术",
    "Gale Blade": "风压剑",
    "Deals 3 <color=#80FFD7FF>Anemo DMG</color>, the target is forcibly switched to the next character.": "造成3点<color=#80FFD7FF>风元素伤害</color>，使对方强制切换到下一个角色。",
    "Dandelion Breeze": "蒲公英之风",
    "Heals all your characters for 2 HP, summons 1 <color=#FFFFFFFF>Dandelion Field</color>.": "治疗所有我方角色2点，召唤<color=#FFFFFFFF>蒲公英领域</color>。",
    "Ningguang": "凝光",
    "Sparkling Scatter": "千金掷",
    "Deals 1 <color=#FFE699FF>Geo DMG</color>.": "造成1点<color=#FFE699FF>岩元素伤害</color>。",
    "Jade Screen": "璇玑屏",
    "Deals 2 <color=#FFE699FF>Geo DMG</color>, creates 1 <color=#FFFFFFFF>Jade Screen</color>.": "造成2点<color=#FFE699FF>岩元素伤害</color>，生成<color=#FFFFFFFF>璇玑屏</color>。",
    "Starshatter": "天权崩玉",
    "Deals 6 <color=#FFE699FF>Geo DMG</color>. If <color=#FFFFFFFF>Jade Screen</color> is on the field, deals +2 DMG.": "造成6点<color=#FFE699FF>岩元素伤害</color>；如果<color=#FFFFFFFF>璇玑屏</color>在场，就使此伤害+2。",
    "Noelle": "诺艾尔",
    "Favonius Bladework - Maid": "西风剑术·女仆",
    "Breastplate": "护心铠",
    "Deals 1 <color=#FFE699FF>Geo DMG</color>, creates 1 <color=#FFFFFFFF>Full Plate</color>.": "造成1点<color=#FFE699FF>岩元素伤害</color>，生成<color=#FFFFFFFF>护体岩铠</color>。",
    "Sweeping Time": "大扫除",
    "Deals 4 <color=#FFE699FF>Geo DMG</color>. This character gains <color=#FFFFFFFF>Sweeping Time</color>.": "造成4点<color=#FFE699FF>岩元素伤害</color>，本角色附属<color=#FFFFFFFF>大扫除</color>。",
    "Collei": "柯莱",
    "Supplicant's Bowmanship": "祈颂射艺",
    "Floral Brush": "拂花偈叶",
    "Deals 3 <color=#7EC236FF>Dendro DMG</color>.": "造成3点<color=#7EC236FF>草元素伤害</color>。",
    "Trump-Card Kitty": "猫猫秘宝",
    "Deals 2 <color=#7EC236FF>Dendro DMG</color>, summons 1 <color=#FFFFFFFF>Cuilein-Anbar</color>.": "造成2点<color=#7EC236FF>草元素伤害</color>，召唤<color=#FFFFFFFF>柯里安巴</color>。",
    "Rhodeia of Loch": "纯水精灵·洛蒂娅",
    "Surge": "翻涌",
    "Oceanid Mimic Summoning": "纯水幻造",
    "Randomly summons 1 <color=#FFFFFFFF>Oceanid Mimic</color> (Prioritizes summoning a different type from preexisting ones).": "随机召唤1种<color=#FFFFFFFF>纯水幻形</color>。（优先生成不同的类型）",
    "The Myriad Wilds": "林野百态",
    "Randomly summons 2 <color=#FFFFFFFF>Oceanid Mimic</color> (Prioritizes summoning different types).": "随机召唤2种<color=#FFFFFFFF>纯水幻形</color>。（优先生成不同的类型）",
    "Tide and Torrent": "潮涌与激流",
    "Deals 2 <color=#80C0FFFF>Hydro DMG</color>. For each friendly Summon on the field, deals +2 additional DMG.": "造成2点<color=#80C0FFFF>水元素伤害</color>；我方每有1个召唤物，再使此伤害+2。",
    "Other Weapons": "其他武器",
    "Mirror Maiden": "愚人众·藏镜仕女",
    "Water Ball": "水弹",
    "Influx Blast": "潋波绽破",
    "Deals 3 <color=#80C0FFFF>Hydro DMG</color>. The target character receives <color=#FFFFFFFF>Refraction</color>.": "造成3点<color=#80C0FFFF>水元素伤害</color>，目标角色附属<color=#FFFFFFFF>水光破镜</color>。",
    "Rippled Reflection": "粼镜折光",
    "Deals 5 <color=#80C0FFFF>Hydro DMG</color>.": "造成5点<color=#80C0FFFF>水元素伤害</color>。",
    "Fatui Pyro Agent": "愚人众·火之债务处理人",
    "Thrust": "突刺",
    "Prowl": "伺机而动",
    "Deals 1 <color=#FF9999FF>Pyro DMG</color>. This character gains <color=#FFFFFFFF>Stealth</color>.": "造成1点<color=#FF9999FF>火元素伤害</color>，本角色附属<color=#FFFFFFFF>潜行</color>。",
    "Blade Ablaze": "焚毁之锋",
    "Deals 5 <color=#FF9999FF>Pyro DMG</color>.": "造成5点<color=#FF9999FF>火元素伤害</color>。",
    "Stealth Master": "潜行大师",
    "(Passive) When the battle begins, this character gains <color=#FFFFFFFF>Stealth</color>.": "【被动】战斗开始时，初始附属<color=#FFFFFFFF>潜行</color>。",
    "Maguu Kenki": "魔偶剑鬼",
    "Ichimonji": "一文字",
    "Blustering Blade": "孤风刀势",
    "Summons 1 <color=#FFFFFFFF>Shadowsword: Lone Gale</color>.": "召唤<color=#FFFFFFFF>剑影·孤风</color>。",
    "Frosty Assault": "霜驰影突",
    "Summons 1 <color=#FFFFFFFF>Shadowsword: Galloping Frost</color>.": "召唤<color=#FFFFFFFF>剑影·霜驰</color>。",
    "Pseudo Tengu Sweeper": "机巧伪天狗抄",
    "Deals 4 <color=#80FFD7FF>Anemo DMG</color>, triggers the effect(s) of all your <color=#FFFFFFFF>Shadowsword</color> Summon(s). (Does not consume their Usages)": "造成4点<color=#80FFD7FF>风元素伤害</color>，触发所有我方<color=#FFFFFFFF>剑影</color>召唤物的效果。（不消耗其可用次数）",
    "Stonehide Lawachurl": "丘丘岩盔王",
    "Deals 3 <color=#FFFFFFFF>Physical DMG</color>.": "造成3点<color=#FFFFFFFF>物理伤害</color>。",
    "Deals 5 <color=#FFFFFFFF>Physical DMG</color>.": "造成5点<color=#FFFFFFFF>物理伤害</color>。",
    "Infused Stonehide": "魔化：岩盔",
    "(Passive) When the battle begins, this character gains <color=#FFFFFFFF>Stonehide</color> and <color=#FFFFFFFF>Stone Force</color>.": "【被动】战斗开始时，初始附属<color=#FFFFFFFF>岩盔</color>和<color=#FFFFFFFF>坚岩之力</color>。",
    "Jadeplume Terrorshroom": "翠翎恐蕈",
    "Majestic Dance": "菌王舞步",
    "Volatile Spore Cloud": "不稳定孢子云",
    "Feather Spreading": "尾羽豪放",
    "Deals 4 <color=#7EC236FF>Dendro DMG</color>, then consumes all <color=#FFFFFFFF>Radical Vitality</color> stacks. For each stack consumed, this instance deals +1 DMG.": "造成4点<color=#7EC236FF>草元素伤害</color>，消耗所有<color=#FFFFFFFF>活化激能</color>层数，每层使此伤害+1。",
    "Radical Vitality": "活化激能",
    "(Passive) When the battle begins, this character gains <color=#FFFFFFFF>Radical Vitality</color>.": "【被动】战斗开始时，初始附属<color=#FFFFFFFF>活化激能</color>。"
  }

_DEFAULT_SKILL_REGEXPS = {
    # Deals 8 Pyro DMG
    "DMG": r"^[dD]eals (\d+) ([a-zA-Z]+) DMG$",
    # deals 1 piercing DMG to all opposing characters on standby
    "DMGAll": r"^[dD]eals (\d+) ([a-zA-Z]+) DMG to all opposing characters on standby$",
    # This character gains Pyro Infusion
    "Infusion": r"^[tT]his character gains ([a-zA-Z]+) (Elemental )?Infusion$",
    # heals this character for 2 HP
    "Heal": r"^[hH]eals this character for (\d+) HP$",
    # heals all of your characters for 4 HP
    "HealAll": r"^[hH]eals all of your characters for (\d+) HP$",
    # summons 1 shadowsword: galloping frost
    "Summon": r"^[Ss]ummons (\d+) ([a-zA-Z: -]+)$",
    # creates 1 pyronado
    "Create": r"^[cC]reates (\d+) ([a-zA-Z: -]+)$",
    # this character gains niwabi enshou
    "Buff": r"^[tT]his character gains ([a-zA-Z: -]+)$",
    # # deals 2 Piercing DMG to all opposing characters on standby
    # "PiercingDMG":r"^[dD]eals (\d+) Piercing DMG to all opposing characters on standby$"
}


CHARACTER_CARDS: dict[int, CharacterCard] = {}
CHARACTER_SKILLS: dict[int, CharacterSkill] = {}
CHARACTER_SKILL_FACTORIES: dict[int, Type[CharacterSkill]] = defaultdict(
    lambda: CharacterSkill
)
CHARACTER_NAME2ID: dict[str, int] = {}


def register_character_card(card: CharacterCard, override: bool = False):
    if override is False and card.id in CHARACTER_CARDS:
        raise ValueError(
            f"Character card {card.id} already exists, use override=True to override it, or use silent=True to silence this warning"
        )

    CHARACTER_CARDS[card.id] = card
    CHARACTER_NAME2ID[card.name] = card.id


def register_character_skill(skill: CharacterSkill, override: bool = False):
    if override is False and skill.id in CHARACTER_SKILLS:
        raise ValueError(
            f"Character skill {skill.id} already exists, use override=True to override it, or use silent=True to silence this warning"
        )

    CHARACTER_SKILLS[skill.id] = skill


def register_character_skill_factory(
    skill_id: int,
):
    if skill_id in CHARACTER_SKILL_FACTORIES:
        raise ValueError(
            f"Character skill factory of skill {skill_id} already exists")

    def decorator(skill_factory: Type[CharacterSkill]):
        CHARACTER_SKILL_FACTORIES[skill_id] = skill_factory
        return skill_factory

    return decorator


_ELEMENT_TYPE_MAP = {
    "ETIce": ElementType.CRYO,
    "ETWater": ElementType.HYDRO,
    "ETFire": ElementType.PYRO,
    "ETThunder": ElementType.ELECTRO,
    "ETRock": ElementType.GEO,
    "ETGrass": ElementType.DENDRO,
    "ETWind": ElementType.ANEMO,
}

_NATION_MAP = {
    "Mondstadt": Nation.Mondstadt,
    "Liyue": Nation.Liyue,
    "Inazuma": Nation.Inazuma,
    "Sumeru": Nation.Sumeru,
    "Monster": Nation.Monster,
    "Fatui": Nation.Fatui,
    "Hilichurl": Nation.Hilichurl,
}

_SKILL_TYPE_MAP = {
    "Normal Attack": SkillType.NORMAL_ATTACK,
    "Elemental Skill": SkillType.ELEMENTAL_SKILL,
    "Elemental Burst": SkillType.ELEMENTAL_BURST,
    "Passive Skill": SkillType.PASSIVE_SKILL,
}

_SKILL_COST_MAP = {
    "1": ElementType.POWER,
    "10": ElementType.ANY,
    "11": ElementType.CRYO,
    "12": ElementType.HYDRO,
    "13": ElementType.PYRO,
    "14": ElementType.ELECTRO,
    "15": ElementType.GEO,
    "16": ElementType.DENDRO,
    "17": ElementType.ANEMO,
}

_WEAPON_TYPE_MAP = {
    "Bow": WeaponType.BOW,
    "Sword": WeaponType.SWORD,
    "Claymore": WeaponType.CLAYMORE,
    "Polearm": WeaponType.POLEARM,
    "Catalyst": WeaponType.CATALYST,
    "Other Weapons": WeaponType.OTHER_WEAPONS,
}


def _process_card(config: dict):
    for skill in config["role_skill_infos"]:
        skill_id = int(skill["id"])
        text = skill["skill_text"]
        text = text.replace("</color>", "")

        # Use regexp to replace all the color tags
        text = re.sub(r"<color=#([0-9a-fA-F]{8})>", "", text)
        skill_instance = CHARACTER_SKILL_FACTORIES[skill_id](
            id=skill_id,
            name=skill["name"],
            type=[_SKILL_TYPE_MAP[i] for i in skill["type"] if i][0],
            text=text,
            costs={
                _SKILL_COST_MAP[j["cost_icon"]]: int(j["cost_num"])
                for j in skill["skill_costs"]
                if j["cost_icon"]
            },
            resource=skill["resource"],
        )
        # 忽略错误
        register_character_skill(skill_instance, override=True)

    skills = [CHARACTER_SKILLS[int(i["id"])]
              for i in config["role_skill_infos"]]
    card = CharacterCard(
        id=int(config["id"]),
        name=config["name"],
        nations=[_NATION_MAP[i] for i in config["belong_to"] if i],
        element_type=_ELEMENT_TYPE_MAP[config["element_type"]],
        health_point=int(config["hp"]),
        resource=config["resource"],
        skills=skills,
        max_power=max(
            [
                skill.costs[ElementType.POWER]
                for skill in skills
                if ElementType.POWER in skill.costs.keys()
            ]
        ),
        weapon_type=_WEAPON_TYPE_MAP[config["weapon"]],
    )

    register_character_card(card, override=True)


def generate_character_cards_and_skills():
    path = os.path.join(
        os.path.dirname(__file__),
        ".",
        "gisim",
        "resources",
        "cards_20221205_en-us.json",
    )

    with open(path, "r", encoding="utf-8") as f:
        cards = json.load(f)["role_card_infos"]

    for i in cards:
        _process_card(i)


def parse_sub_command(sub_command: str):
    for skill_type, regexp in _DEFAULT_SKILL_REGEXPS.items():
        results = re.findall(regexp, sub_command)
        if results:
            return [skill_type, results]
    return [sub_command]


def parse_skill_text(text: str):
    """
    Parse the skill text and execute the skill effect
    """

    effects = []
    for command in text.split("."):
        command = command.strip()
        if not command:
            continue

        # A command is parsable if all of its sub-commands are parsable
        for sub_command in command.split(", "):
            effects.append(parse_sub_command(sub_command))

    return effects


def auto_skil(character_name):
    generate_character_cards_and_skills()
    # character_name = "Ganyu"
    # character_name = "Collei"
    for r in all_role_card:
        if r['name'] is character_name:
            trcard = r
    character_card = CHARACTER_CARDS[CHARACTER_NAME2ID[character_name]]
    print(
        f"Name: {character_card.name}, Nations: {character_card.nations}, Weapon: {character_card.weapon_type}, Element: {character_card.element_type}"
    )
    skills = character_card.skills
    print("Skills:")
    for skill in skills:
        print(
            f"    Name: {skill.name}, type: {skill.type}, cost: {skill.costs}, text: {skill.text}"
        )
        effects = parse_skill_text(skill.text)
        for effect in effects:
            print(f"          {effect}")

    # TODO: Generate text for each CharacterSkill and CharacterCard using KamisatoAyaka.py as a template
    # TODO: Find out all skills that cannot be parsed and mark them at the end of each file
    zh_cn_name = ts_zhcn[character_name]
    with open(f"./autoSkil/{character_name}.py", "w", encoding="utf-8") as f:
        f.write(f'"""{zh_cn_name}"""')
        f.write(
        """
from queue import PriorityQueue
from gisim.cards.characters.base import CharacterCard, CharacterSkill, GenericSkill
from gisim.classes.enums import (
    CharPos,
    ElementType,
    EntityType,
    EquipmentType,
    Nation,
    PlayerID,
    SkillType,
    WeaponType,
)
from gisim.classes.summon import AttackSummon, Summon
from gisim.classes.status import CombatStatusEntity

"""
        )
        indeffect = []
        for skill in skills:
            for sk in trcard['role_skill_infos']:
                if sk['name'] == skill.name:
                    skill_text = sk['skill_text']
                    zh_skill_text = ts_zhcn[skill_text]
                    zh_skill_text = re.sub(r'<.+?>','`',zh_skill_text)
            # skdec = trsk['skill_text']
            effects = parse_skill_text(skill.text)
            skill_name = re.sub(r"[^a-zA-Z]", "", skill.name)
            zhcn_skill_name = ts_zhcn[skill.name] if skill.name in ts_zhcn else skill.name
            f.write(
                f"class {skill_name}(GenericSkill):\n"
                + '    """\n'
                + f"    {zhcn_skill_name}\n"
                + '    '+((len(zhcn_skill_name)) * '~~') + '\n'
                + f"    {zh_skill_text}\n"
                + '    """\n'
                + f"    id: int = {skill.id}\n"
                + f'    name: str = "{skill.name}"\n'
                + f'    text: str = """\n    {skill.text}\n    """\n'
                + f"    type: SkillType = {skill.type}\n"
                + "    costs: dict[ElementType, int] = {"
            )

            for i, cost_icon, cost_num in zip(
                range(len(skill.costs)), skill.costs.keys(), skill.costs.values()
            ):
                f.write(f"ElementType.{cost_icon.name}, {cost_num}")
                if i != len(skill.costs) - 1:
                    f.write(", ")
            f.write("}\n")

            for effect in effects:
                if effect[0] == "DMG":
                    f.write(
                        f"    damage_element: ElementType = ElementType.{effect[1][0][1]}\n"
                        + f"    damage_value: int = {effect[1][0][0]}\n"
                    )
                if effect[0] == "Summon":
                    indeffect.append(effect)
                    for i in range(int(effect[1][0][0])):
                        f.write(
                            f'    summon_name: str = "{effect[1][0][i+1]}"\n')
                if effect[0] == "DMGAll" and effect[1][0][1] in [
                    "Piercing",
                    "piercing",
                ]:
                    # 穿透伤害
                    f.write(
                    f"    piercing_damage_value: int = {effect[1][0][0]}\n"
                    )
                # 战斗行动
                if effect[0] == "Create":
                    indeffect.append(effect)
                    f.write(
                    f'    combat_status_name: str = "{effect[1][0][1]}"\n'
                    )
            f.write("\n\n")
        
        # 添加战斗行动和召唤物
        print(indeffect)
        for indclass in indeffect:
            indclass_name = re.sub(r"[ ]", "", indclass[1][0][1])
            if indclass[0] == 'Create':
                BaseClassType = "CombatStatusEntity"
                zhclasstype = "战斗行动"
                per = "CombatStatu"
            else:
                BaseClassType = "AttackSummon"
                zhclasstype = "召唤物"
                per = "Summon"
            f.write(
            f"class {per}{indclass_name}({BaseClassType}):\n"
            +f'    """\n    {indclass[1][0][1]}\n    ~~~~~~\n    `{zhclasstype}`{indclass[1][0][1]}\n    请完善这个类的效果,应该是召唤物或者战斗效果\n    """\n'
            +f'    name: str = "{indclass[1][0][1]}"\n'
            )
            if BaseClassType == "CombatStatusEntity":
                f.write("\n")
                f.write(
                    '    def msg_handler(self, msg_queue: PriorityQueue) -> bool:\n        """请编写处理函数"""\n        pass\n'
                )
            f.write("\n\n")

        ronation = re.sub(r'[<>:0-9 ]','',str(character_card.nations))
        f.write(
            f'class {character_name.replace(" ", "")}(CharacterCard):\n'
            +f'    """{zh_cn_name}"""\n'
            +f"    id: int = {character_card.id}\n"
            +f'    name: str = "{character_name}"\n'
            +f"    element_type: ElementType = ElementType.{character_card.element_type}\n"
            +f"    nations: list[Nation] = {ronation}\n"
            +f"    health_point: int = {character_card.health_point}\n"
            +f"    power: int = {character_card.power}\n"
            +f"    max_power: int = {character_card.max_power}\n"
            +f"    weapon_type: WeaponType = {character_card.weapon_type}\n"
            +f"    skills: list[CharacterSkill] = [\n"
        )
        for skill in skills:
            skill_name = re.sub(r"[^a-zA-Z]", "", skill.name)
            f.write(f"        {skill_name}(),\n")
        f.write("    ]\n\n")


if __name__ == "__main__":
    for role in all_role_card:
        # print(role)
        name = role["name"]
        auto_skil(name)
        # break
