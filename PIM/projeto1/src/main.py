import os
import cv2
import time
import numpy as np
from pynput import keyboard

IMAGES_FOLDER = os.path.join(os.path.abspath(
    os.path.dirname(__file__)), "../images/")
WATER_MARK = os.path.join(os.path.abspath(
    os.path.dirname(__file__)), "../water_mark/water_mark.png")
WATER_MARK_SIZE = 50
DELAY_SLIDE = 2
DELAY_FADE = 1
IMAGE_SIZE = 150
BORDER_SIZE = 20
BORDER_COLOR = [200, 200, 200]
EXIT = False


def main():
    with keyboard.Listener(on_press=on_press) as listener:
        slides()
        listener.join()


def on_press(key):
    global EXIT
    if ord(key.char) == ord('q'):
        print('Q pressed')
        EXIT = True
        exit(0)


def slides():
    imgs_name = os.listdir(IMAGES_FOLDER)
    size = len(imgs_name)
    i = 0
    while(not EXIT):
        img = getImage(imgs_name[i])
        next = i = (0) if (i == size - 1) else (i + 1)
        img2 = getImage(imgs_name[next])
        fade(img, img2)
        cv2.imshow('slide', img2)
        delay(DELAY_SLIDE)


def fade(img1, img2):
    for IN in range(0, 10):
        fadein = IN/10.0
        dst = cv2.addWeighted(img1, 1-fadein, img2, fadein, 1)
        cv2.imshow('slide', dst)
        delay(DELAY_FADE/10)


def delay(seconds):
    cv2.waitKey(1)
    time.sleep(seconds)


def getImage(img):
    img = cv2.imread(IMAGES_FOLDER + img)
    h, w = img.shape[:2]
    img = waterMark(np.dstack([img, np.ones((h, w), dtype="uint8") * 255]))
    img = cv2.copyMakeBorder(img, BORDER_SIZE, BORDER_SIZE, BORDER_SIZE,
                             BORDER_SIZE, cv2.BORDER_CONSTANT,
                             value=BORDER_COLOR)
    return cv2.resize(img, (IMAGE_SIZE, IMAGE_SIZE))


def waterMark(img):
    overlay = img.copy()
    wm = loadWaterMark()
    overlay[0:WATER_MARK_SIZE, 0:WATER_MARK_SIZE] = wm
    return cv2.addWeighted(img, 0.7, overlay, 0.3, 1)


def loadWaterMark():
    img = cv2.imread(WATER_MARK, cv2.IMREAD_UNCHANGED)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGRA)
    return cv2.resize(img, (WATER_MARK_SIZE, WATER_MARK_SIZE))


if __name__ == "__main__":
    main()
