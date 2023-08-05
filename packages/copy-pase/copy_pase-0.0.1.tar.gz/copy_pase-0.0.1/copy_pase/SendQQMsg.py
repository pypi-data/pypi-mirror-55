# coding:utf-8
import os
import time
import win32api
import win32gui
import win32con
import win32clipboard as w
from PIL import Image
from io import BytesIO

# 窗口名字
name = "购物优惠群"

# 获取窗口句柄
handle = win32gui.FindWindow(None, name)


def get_msg(file):
    global msg
    files = os.listdir(file)
    for fileName in files:
        file_path = os.path.join(file, fileName)
        if not os.path.isdir(fileName) and os.path.getsize(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                msg = """\n{0}""".format(f.read())
            with open(file_path, 'w') as fb:
                fb.truncate()
        else:
            msg = ''


def get_img(file):
    global image_path
    files = os.listdir(file)
    for fileName in files:
        file_path = os.path.join(file, fileName)
        if not os.path.isdir(fileName):
            image_path = file_path
        else:
            image_path = ''


def get_dir(path):
    files = os.listdir(path)
    for file in files:
        abs_path = os.path.join(path + "\\" + file)
        if os.path.isdir(abs_path) and file == 'content':
            get_msg(abs_path)
        elif os.path.isdir(abs_path) and file == 'image':
            get_img(abs_path)


def get_img_data(path):
    global data
    image = Image.open(path)
    output = BytesIO()
    image.convert('RGB').save(output, 'BMP')
    data = output.getvalue()[14:]
    output.close()


def copy_img(data):
    # 将图片复制到剪切板中
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardData(win32con.CF_DIB, data)
    w.CloseClipboard()
    # win32gui.SendMessage(handle, 770, 0, 0)
    win32api.PostMessage(handle, win32con.WM_PASTE, 0, 0)


def copy_msg(msg):
    # 将信息复制到剪切板中
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardData(win32con.CF_UNICODETEXT, msg)
    w.CloseClipboard()
    # win32gui.SendMessage(handle, 770, 0, 0)
    win32api.PostMessage(handle, win32con.WM_PASTE, 0, 0)


if __name__ == "__main__":
    # 文案目录
    BaseUrl = 'C:\\文案'
    msg = ''
    image_path = ''
    data = ''

    get_dir(BaseUrl)
    if len(image_path) > 0 and len(msg) > 0:
        get_img_data(image_path)
        copy_img(data)
        time.sleep(1)
        copy_msg(msg)
        time.sleep(1)
        win32gui.SendMessage(handle, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
        os.remove(image_path)
