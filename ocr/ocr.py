from PIL import Image,ImageGrab,ImageChops
import numpy as np
from skimage.metrics import mean_squared_error as mse
import keyboard
import pynput
import pickle
import time

#暂不支持须弥共鸣和开局换牌
#根据你屏幕的缩放率修改ZOOM值。如果你的屏幕缩放率为150%，则将ZOOM值修改为1.5。
ZOOM = 1.5



#所有构筑中可能出现的牌。不含雷楔。
All_cards = pickle.load(open('constructable_cards.pkl','rb'))

def similarity(image1, image2):
    # 将图片调整为相同尺寸
    width, height = max(image1.width, image2.width), max(image1.height, image2.height)
    image1 = image1.resize((width, height), Image.ANTIALIAS)
    image2 = image2.resize((width, height), Image.ANTIALIAS)
    
    image1 = image1.convert('RGB')
    image2 = image2.convert('RGB')
    
    # 将图像数据转换为NumPy数组
    image1 = np.array(image1)
    image2 = np.array(image2)
    
    # 计算相似度
    similarity = mse(image1, image2)
    
    return similarity

def recognize_card(image):
    # return card or None
    to_return = None
    similarities = {}
    #FIXME 这步的缓慢可能成为bug来源
    for k,v in All_cards.items():
        similarities[k] = similarity(image, v)
    first_min = min(similarities.values())
    second_min = sorted(similarities.values())[1]
    avg = sum(similarities.values()) / len(similarities)
    # print('first min = ', first_min, 'second_min =', second_min, 'ratio = ', (avg - first_min) / (avg - second_min), 'min key =', min(similarities, key=similarities.get), 'second_min_key =', min(similarities, key=lambda x: similarities[x] if similarities[x] != first_min else 100000000))
    #FIXME 这步的不精确可能成为bug来源
    if avg - first_min > 1.2 * (avg - second_min):
        to_return = min(similarities, key=similarities.get)
    return to_return

class Box:
    def __init__(self, box):
        self.box = box
        self.previous_image = None
        self.current_image = None
    def crop(self, frame):
        box = self.box
        cropped_image = frame.crop((box[0], box[2], box[1], box[3]))
        self.current_image = cropped_image
        return cropped_image

    def recognize_card(self, frame):
        self.crop(frame)
        if self.previous_image and similarity(self.current_image, self.previous_image) < 2700:
            # 如果该区域改变和上一次相比不大，则不再遍历比较，直接认为什么卡都没看见。
            self.previous_image = self.current_image
            return None
        else:
            self.previous_image = self.current_image
            return recognize_card(self.current_image)
# (x1, y1, x2, y2)
upright_keypoint = (2370,137)
downleft_keypoint = (350,1202)
# upright_keypoint = (2559,0)
# downleft_keypoint = (0,1599)
# One_draw_box = [(, , , )]
Two_draw_box = [Box((827,1065,594,1004)),Box((1497,1734,594,1004))]
Three_draw_box = [Box((660,897,594,1004)),Box((1162,1400,594,1004)),Box((1663,1902,594,1004))]
Play_card_box = Box((471,768,409,920))
Opponent_play_card_box = Box((1791,2087,409,920))
myscreensize = Box((0,2599,0,1599))


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






# Global_remember = None
@join_func
def I_am_drawing_card(frame):
    # if not drawing card, return False
    # if drawing card, return [Card]
    # only judge whether it is drawing card at current time
    three_draw = [i.recognize_card(frame) for i in Three_draw_box]
    if three_draw[0] and three_draw[1] and three_draw[2]:
        return three_draw
    two_draw = [i.recognize_card(frame) for i in Two_draw_box]
    if two_draw[0] and two_draw[1]:
        return two_draw
    # 好像没有只抽一张的情况？
    return []

@join_func
def I_am_playing_card(frame):
    # if not playing card, return False
    # if playing card, return [Card]
    # only judge whether it is drawing card at current time
    one_draw = [Play_card_box.recognize_card(frame)]
    if one_draw[0]:
        return one_draw
    return []


@join_func
def I_am_discarding_card(frame):
    # if not discarding card, return False
    # if discarding card, return [Card]
    # only judge whether it is drawing card at current time
    #TODO
    return []

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

def join_until_receive_signal():
    keyboard.wait('c')
    return

def read_deck(deck_file):
    #读入卡组预览导出的照片，然后识别出来，然后返回一个列表
    #TODO
    pass



def initialize_screen_place():
    
    mouse = pynput.mouse.Controller()
    #print mouse position
    join_until_receive_signal()
    upright_keypoint_personal = mouse.position
    upright_keypoint_personal = (upright_keypoint_personal[0] * ZOOM, upright_keypoint_personal[1] * ZOOM)
    join_until_receive_signal()
    downleft_keypoint_personal = mouse.position
    downleft_keypoint_personal = (downleft_keypoint_personal[0] * ZOOM, downleft_keypoint_personal[1] * ZOOM)
    return upright_keypoint_personal, downleft_keypoint_personal

def ImgOffSet(Img,xoff,yoff):
    width, height = Img.size
    c = ImageChops.offset(Img,xoff,yoff)
    c.paste((0,0,0),(0,0,xoff,height))
    c.paste((0,0,0),(0,0,width,yoff))
    return c

def get_frame(screen_place_personal, screen_place = (upright_keypoint, downleft_keypoint)):
    # screen_place_personal * scale + offset = screen_place
    image = ImageGrab.grab()
    xscale = (screen_place[0][0] - screen_place[1][0]) / (screen_place_personal[0][0] - screen_place_personal[1][0])
    yscale = (screen_place[0][1] - screen_place[1][1]) / (screen_place_personal[0][1] - screen_place_personal[1][1])
    new_width = int(image.width * xscale)
    new_height = int(image.height * yscale)
    image = image.resize((new_width, new_height), Image.ANTIALIAS)
    image = ImgOffSet(image, int(screen_place[0][0] - xscale * screen_place_personal[0][0]), int(screen_place[0][1] - yscale * screen_place_personal[0][1]))
    return image
    




# deck = read_deck(deck_file)
use_card = []

screen_place_personal = initialize_screen_place()


join_until_receive_signal()

while True:
    frame = get_frame(screen_place_personal)
    if cards := I_am_drawing_card(frame):
        # removelist(deck, cards)
        print("I am drawing card", cards)
    if cards := I_am_playing_card(frame):
        use_card += card
        print("I am playing card", cards)
    if cards := I_am_discarding_card(frame):
        use_card += card
        print("I am discarding card", cards)