#!/usr/bin/python3

from os import environ, system
import json
from io import BytesIO
from datetime import time, datetime

import requests
from PIL import Image

IMG_DIR = environ['HOME']
DAY_IMG_PATH = '/Users/yuan/.himawari8/cowboy.jpg'

def gen_img():
    config_url = 'http://himawari8-dl.nict.go.jp/himawari8/img/D531106/latest.json'
    base_img_url = 'http://himawari8-dl.nict.go.jp/himawari8/img/D531106/2d/550/'
    # example: http://himawari8-dl.nict.go.jp/himawari8/img/D531106/2d/550/2016/01/08/035000_0_0.png

    curr_date = json.loads(requests.get(config_url).text)['date']
    # example: {"date":"2017-07-22 04:50:00","file":"PI_H08_20170722_0450_TRC_FLDK_R10_PGPFD.png"}
    format_date = curr_date.replace('-', '/').replace(' ', '/').replace(
        ':', '')
    # from 2017-07-22 04:50:00 to 2017/07/22/045000

    # four pieces of the earth image
    urls = [
        base_img_url + format_date + '_0_0.png',
        base_img_url + format_date + '_1_0.png',
        base_img_url + format_date + '_0_1.png',
        base_img_url + format_date + '_1_1.png'
    ]
    img_lis = []
    for url in urls:
        r = requests.get(url).content
        i = Image.open(BytesIO(r))
        img_lis.append(i)

    # create a image and comine four pieces
    img = Image.new('RGB', (2134, 1200), 'black')
    img.paste(img_lis[0], (517, 50))
    img.paste(img_lis[1], (1067, 50))
    img.paste(img_lis[2], (517, 600))
    img.paste(img_lis[3], (1067, 600))

    img_path = IMG_DIR + '/.' + curr_date.replace(' ', '-').replace(':', '-') + '.png'
    img.save(img_path)
    return img_path

def set_desktop(img_path):
    system(
        "osascript -e 'tell application \"Finder\" to set desktop picture to \"{}\" as POSIX file'".
        format(img_path))
def in_range(t1, t2):
    '''
    t1, t2 are time range in where script doen not run
    in that range the desktop will be set to another image
    t1, t2 are tuple
    24 hour mode
    10:24 --> (10, 24)
    '''
    now = datetime.now()
    now_time = now.time()
    if now_time >= time(t1[0], t1[1]) and now_time <= time(t2[0], t2[1]):
        return True
    else:
        return False


if __name__ == '__main__':
    if in_range((7,0), (17,0)):
        set_desktop(DAY_IMG_PATH)
    else:
        img_path = gen_img()
        set_desktop(img_path)