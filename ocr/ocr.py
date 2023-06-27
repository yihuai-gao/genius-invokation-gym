#暂不支持须弥共鸣和开局换牌


def merge_lists(lists):
    # lists = [[1, 2, 2, 3], [2, 3, 4], [3, 4, 5]]
    # result = merge_lists(lists)
    # print(result)  # 输出: [1, 2, 2, 3, 4, 5]
    merged_list = []
    
    # 将所有子列表合并为一个列表
    merged_occured_num = {}
    for sublist in lists:
        occured_num = {}
        for item in sublist:
            occured_num[item] = occured_num.get(item, 0) + 1
        for item in occured_num:
            if item not in merged_occured_num:
                merged_occured_num[item] = occured_num[item]
            else:
                merged_occured_num[item] = max(merged_occured_num[item], occured_num[item])
    
    # 还原回列表
    for item in merged_occured_num:
        merged_list += [item] * merged_occured_num[item]
    return merged_list

# 每个函数一旦发现是非空都会join，直到发现返回为空列表为止。然后把这段时间内的观察到的return结果集合返回。
# 对结果集合的处理是取并集。
# 为这个功能写一个装饰器
def join_func(func):
    def wrapper(*args, **kw):
        result = []
        while True:
            if not (func_result := func(*args, **kw)):
                break
            else:
                result.append(func_result)
        return merge_lists(result)
    return wrapper

@join_func
def I_am_drawing_card(frame):
    # if not drawing card, return False
    # if drawing card, return [Card]
    # only judge whether it is drawing card at current time
    #TODO
    pass

@join_func
def I_am_playing_card(frame):
    # if not playing card, return False
    # if playing card, return [Card]
    # only judge whether it is drawing card at current time
    #TODO
    pass


@join_func
def I_am_discarding_card(frame):
    # if not discarding card, return False
    # if discarding card, return [Card]
    # only judge whether it is drawing card at current time
    #TODO
    pass

# def opponent_is_drawing_card(frame):
#     # if not drawing card, return False
#     # if drawing card, return [Card_unknown]

# def opponent_is_playing_card(frame):
#     # if not playing card, return False
#     # if playing card, return Card

# def opponent_is_discarding_card(frame):
#     # if not discarding card, return False
#     # if discarding card, return Card_unknown

def removelist(l1, l2):
    for i in l2:
        l1.remove(i)
    return l1

def read_deck(deck_file):
    #读入卡组预览导出的照片，然后识别出来，然后返回一个列表
    #TODO
    pass


def start_program(frame) -> bool:
    # 必须在换完牌以后才开始 program，因为现在还不支持换牌识别。
    #TODO
    pass


def get_frame():
    # should be a yield function
    #TODO
    pass

deck = read_deck(deck_file)
use_card = []

frames = iter(get_frame())

while True:
    if start_program(next(frames)):
        break
while True:
    frame = next(frames)
    if cards := I_am_drawing_card(frame):
        removelist(deck, cards)
        print("I am drawing card", cards)
    if cards := I_am_playing_card(frame):
        use_card += card
        print("I am playing card", cards)
    if cards := I_am_discarding_card(frame):
        use_card += card
        print("I am discarding card", cards)