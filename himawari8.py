#!/usr/bin/python3

from os import environ, system
import json
from io import BytesIO
from time import sleep

import requests
from PIL import Image

IMG_DIR = environ['HOME'] + '/himawari8_img.png'


def gen_img():
    config_url = 'http://himawari8-dl.nict.go.jp/himawari8/img/D531106/latest.json'
    base_img_url = 'http://himawari8-dl.nict.go.jp/himawari8/img/D531106/2d/550/'
    # example: http://himawari8-dl.nict.go.jp/himawari8/img/D531106/2d/550/2016/01/08/035000_0_0.png

    curr_date = json.loads(requests.get(config_url).text)['date']
    # example: {"date":"2017-07-22 04:50:00","file":"PI_H08_20170722_0450_TRC_FLDK_R10_PGPFD.png"}
    tmp_path = '/tmp/earth.png'
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

    img.save(IMG_DIR)


def set_desktop():
    system(
        "osascript -e 'tell application \"Finder\" to set desktop picture to \"{}\" as POSIX file'".
        format(IMG_DIR))


if __name__ == '__main__':
    while True:
        sleep(600)
        gen_img()
        set_desktop()
