#!/usr/bin/python

import cv2
import os
from collections import deque

options = {
        1048683: 'keep',
        1048674: 'best',
        1048676: 'delete',
        1048693: 'undecided',
        }

WIN_HEIGHT = 720
WIN_WIDTH = 1280

def fetch(pic):
    if pic['img'] == None:
        pic['img'] = cv2.imread(pic['fileName'])

def show(pic):
    cv2.imshow('pic_win', pic['img'])


def nextPicture(current, pictures):
    if current != None:
        print 'push'
        pictures.append(current)

    try:
        current = pictures.popleft()
    except IndexError:
        return None

    fetch(current)
    show(current)

    return current


def previousPicture(current, pictures):
    if current != None:
        pictures.appendleft(current)

    try:
        current = pictures.pop()
    except StopIteration:
        return None

    fetch(current)
    show(current)

    return current

pictures = deque()

for fileName in os.listdir('.'):
    if any(fileName.endswith(ext) for ext in ['jpg', 'jpeg', 'JPG', 'JPEG']):
        pictures.append({ 'fileName': fileName,
                          'img': None })
print pictures

current = None

cv2.namedWindow('pic_win', cv2.WINDOW_NORMAL);
cv2.resizeWindow('pic_win', WIN_WIDTH, WIN_HEIGHT)

while True:
    key = cv2.waitKey(0)

    if key == 1048603: # ESC
        break
    elif key in options.keys():
        print options[key]
    elif key == 1113939: # Right
        print 'next'
        current = nextPicture(current, pictures)
    elif key == 1113937: # Left
        print 'previous'
        current = previousPicture(current, pictures)
    else:
        print key

cv2.destroyAllWindows()


