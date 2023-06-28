import requests as req
from PIL import Image
from io import BytesIO
import json

#该代码说明了如何获取id-卡图的字典并存为pickle文件

def get_image(url):
    response = req.get(url)
    image = Image.open(BytesIO(response.content))
    return image
cards_file = json.load(open('cards_images.json', 'r', encoding='utf-8'))
leixie = {'114031':get_image(cards_file['114031'])}
constructable_cards = {k:get_image(v) for k,v in cards_file.items() if '200000' <= k < '400000'}
pickle.dump(leixie, open('leixie.pkl', 'wb'))
pickle.dump(constructable_cards, open('constructable_cards.pkl', 'wb'))
