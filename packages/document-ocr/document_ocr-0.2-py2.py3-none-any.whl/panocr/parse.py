import re
import os
import sys
import pytesseract
import cv2
import json
import numpy as np
import multiprocessing as mp

from functools import reduce
from collections import OrderedDict
from datetime import datetime

STOPWORDS = ['Permanent', 'Account', 'Number', 'GOVT', 'INDIA', 'INCOME', 'TAX', 'DEPARTMENT', 'OF']
config = '-l eng --oem 1 --psm 3'

result_dict = OrderedDict()


def _get_detail(data):
    resp = {
        'pan': None,
        'name': None,
        'father/spouse_name': None
    }

    try:
        # pan Number
        pan_index = None
        ind = 0
        for key, val in data.items():
            if re.fullmatch("[A-Z]{5}[0-9]{4}[A-Z]{1}", key) is not None:
                resp['pan'] = key
                pan_index = ind
                break
            ind += 1

        # filter alpha num
        data_copy = data.copy()
        for key, val in data_copy.items():
            if re.fullmatch("[A-Z.]+", key.replace(' ', '')) is None:
                del data[key]

        final_dict = sorted(data.items(), key=lambda x: x[1], reverse=True)

        if len(final_dict) > 2:
            if final_dict[0][1] == final_dict[1][1]:
                if final_dict[2][1] == final_dict[1][1]:
                    max_val = final_dict[0][1]
                    final_dict = list(filter(lambda x: x[1] == max_val, final_dict))[:2]
                else:
                    keyy = list(data.keys())
                    item = list(data.items())

                    minn = min(keyy.index(final_dict[0][0]), keyy.index(final_dict[1][0]))
                    maxx = max(keyy.index(final_dict[0][0]), keyy.index(final_dict[1][0]))

                    keyyy = list(data_copy.keys())
                    minnn = min(keyyy.index(final_dict[0][0]), keyyy.index(final_dict[1][0]))
                    maxxx = max(keyyy.index(final_dict[0][0]), keyyy.index(final_dict[1][0]))

                    if minnn < pan_index < maxxx:
                        resp['name'] = item[maxx][0]
                        resp['father/spouse_name'] = item[minn][0]
                    else:
                        resp['name'] = item[minn][0]
                        resp['father/spouse_name'] = item[maxx][0]

            else:
                if final_dict[2][1] == final_dict[1][1]:
                    keyy = list(data.keys())
                    item = list(data.items())

                    minn = min(keyy.index(final_dict[0][0]), keyy.index(final_dict[1][0]))
                    maxx = max(keyy.index(final_dict[0][0]), keyy.index(final_dict[1][0]))

                    resp['name'] = item[minn][0]
                    resp['father/spouse_name'] = item[maxx][0]
                else:
                    keyy = list(data.keys())
                    item = list(data.items())

                    minn = min(keyy.index(final_dict[0][0]), keyy.index(final_dict[1][0]))
                    maxx = max(keyy.index(final_dict[0][0]), keyy.index(final_dict[1][0]))

                    keyyy = list(data_copy.keys())
                    minnn = min(keyyy.index(final_dict[0][0]), keyyy.index(final_dict[1][0]))
                    maxxx = max(keyyy.index(final_dict[0][0]), keyyy.index(final_dict[1][0]))

                    if minnn < pan_index < maxxx:
                        resp['name'] = item[maxx][0]
                        resp['father/spouse_name'] = item[minn][0]
                    else:
                        resp['name'] = item[minn][0]
                        resp['father/spouse_name'] = item[maxx][0]

        if len(final_dict) == 2:
            keyy = list(data.keys())
            item = list(data.items())

            minn = min(keyy.index(final_dict[0][0]), keyy.index(final_dict[1][0]))
            maxx = max(keyy.index(final_dict[0][0]), keyy.index(final_dict[1][0]))

            keyyy = list(data_copy.keys())
            minnn = min(keyyy.index(final_dict[0][0]), keyyy.index(final_dict[1][0]))
            maxxx = max(keyyy.index(final_dict[0][0]), keyyy.index(final_dict[1][0]))

            if minnn < pan_index < maxxx:
                resp['name'] = item[maxx][0]
                resp['father/spouse_name'] = item[minn][0]
            else:
                resp['name'] = item[minn][0]
                resp['father/spouse_name'] = item[maxx][0]

        if len(final_dict) < 2:
            raise ValueError("Bad Resolution")

    except:
        pass

    return resp


def __parse__(rot, img):
    result_dic = OrderedDict()
    steps = [50, 60, 70, 80, 90, 100]
    for thresh in steps:
        im_bw = cv2.threshold(img, thresh, 255, cv2.THRESH_BINARY)[1]
        texts = pytesseract.image_to_string(im_bw, config=config)

        if len(texts.split("\n")) < 5:
            continue

        for text in texts.split("\n"):
            text = text.strip()
            if not text.isspace():
                if re.fullmatch("[a-zA-Z0-9\s.]+", text) is not None:
                    if len(text) > 5:
                        if not text.isnumeric():
                            if text.isupper():
                                if not reduce(lambda x, y: x if x is True else y.upper() in text.upper(), STOPWORDS):
                                    result_dic.update({text: result_dic.get(text, 0) + 1})

    return result_dic


def collect_result(result):
    global result_dict
    result_dict.update(result)


def parse(imPath):
    im = cv2.imread(imPath)

    global result_dict
    result_dict = OrderedDict()

    pool = mp.Pool(2)
    for i in range(0, 2):
        pool.apply_async(__parse__, args=(i, im), callback=collect_result)
        im = np.rot90(im)

    pool.close()
    pool.join()

    detail = _get_detail(result_dict)
    return detail
