import os
from io import BytesIO

import requests
from PIL import Image, ImageDraw, ImageFont, ImageColor


def make_ticket(id, from_, to, date):
    im = Image.open("make_fly_ticket/ticket_template.png")
    font_path = os.path.join("make_fly_ticket/fonts", "ofont_ru_MurreyC.ttf")
    font_text = ImageFont.truetype(font_path, size=30)
    font_data = ImageFont.truetype(font_path, size=25)

    draw = ImageDraw.Draw(im)
    x = 40
    draw.text((x, 190), from_, font=font_text, fill=ImageColor.colormap['blue'])
    draw.text((x, 255), to, font=font_text, fill=ImageColor.colormap['blue'])
    draw.text((x + 250, 260), date, font=font_data, fill=ImageColor.colormap['blue'])

    response = requests.get(url=f'https://api.adorable.io/avatars/285/{id}@adorable.png')
    avatar_file_like = BytesIO(response.content)
    avatar = Image.open(avatar_file_like)
    avatar_resize = avatar.resize((120, 120), Image.ANTIALIAS)
    im.paste(avatar_resize, (150, 160))

    temp_file = BytesIO()
    im.save(temp_file, 'png')
    temp_file.seek(0)
    return temp_file

