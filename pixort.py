#!/usr/bin/python

import cv2
import os
import shutil
import errno
from collections import deque

WIN_HEIGHT = 720
WIN_WIDTH = 1280

options = [
    { 'key': 1048683, 'act': 'mv', 'dir': 'keep' },
    { 'key': 1048674, 'act': 'mv', 'dir': 'best' },
    { 'key': 1048676, 'act': 'mv', 'dir': 'delete' },
    { 'key': 1048693, 'act': 'undo' },
    { 'key': 1048690, 'act': 'mv', 'dir': 'retouche' },
    { 'key': 1048685, 'act': 'cp', 'dir': 'misc' },
]

def fetch(pic):
    if pic['img'] is None:
        pic['img'] = cv2.imread(pic['fileName'])


def show(pic):
    cv2.imshow('pic_win', pic['img'])
    print(pic['fileName'])


def nextPicture(current, pictures):
    if current is not None:
        pictures.append(current)

    try:
        current = pictures.popleft()
    except IndexError:
        return None

    fetch(current)
    show(current)

    return current


def previousPicture(current, pictures):
    if current is not None:
        pictures.appendleft(current)

    try:
        current = pictures.pop()
    except IndexError:
        return None

    fetch(current)
    show(current)

    return current


def moveToDirectory(current, pictures, dir, stack):
    if current is None:
        return None

    try:
        os.makedirs(dir)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(dir):
            pass
        else:
            raise

    base = os.path.splitext(current['fileName'])
    for fileName in os.listdir('.'):
        if fileName.startswith(base):
            os.rename(fileName, dir + '/' + fileName)
            print('moved ' + fileName + ' to ' + dir)

    stack.append({
        'change': 'moveToDirectory',
        'fileName': current['fileName'],
        'directory': dir
        })

    return nextPicture(None, pictures)


def undoMoveToDirectory(current, pictures, change):
    base = os.path.splitext(change['fileName'])
    dir = change['directory']

    for fileName in os.listdir(dir):
        if fileName.startswith(base):
            os.rename(dir + '/' + fileName, fileName)
            print('moved back ' + fileName)

    pictures.append({ 'fileName': change['fileName'],
                      'img': None })

    return previousPicture(current, pictures)


def copyToDirectory(current, pictures, dir):
    if current is None:
        return None
    
    try:
        os.makedirs(dir)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(dir):
            pass
        else:
            raise

    base = os.path.splitext(current['fileName'])
    for fileName in os.listdir('.'):
        if fileName.startswith(base):
            shutil.copy2(fileName, dir + '/' + fileName)
            print('copied picture to ' + dir)

    return nextPicture(None, pictures)


def undo(current, pictures, stack):
    try:
        change = stack.pop()
    except IndexError:
        print('no change to cancel')
        return current

    if change['change'] == 'moveToDirectory':
        return undoMoveToDirectory(current, pictures, change)


# Here it begins ...

# Deque containing all pictures to treate
pictures = deque()
# List of moves (used to cancel actions)
stack = list()

for fileName in sorted(os.listdir('.')):
    if any(fileName.endswith(ext) for ext in ['jpg', 'jpeg', 'JPG', 'JPEG']):
        pictures.append({ 'fileName': fileName,
                          'img': None })
print(pictures)

cv2.namedWindow('pic_win', cv2.WINDOW_NORMAL);
cv2.resizeWindow('pic_win', WIN_WIDTH, WIN_HEIGHT)

current = nextPicture(None, pictures)

while True:
    if current == None:
        print('all done ;)')
        break
    key = cv2.waitKey(0)

    if key == 1048603: # ESC
        break
    elif key == 1113939: # Right
        print('next')
        current = nextPicture(current, pictures)
    elif key == 1113937: # Left
        print('previous')
        current = previousPicture(current, pictures)
    elif any(opt['key'] == key for opt in options):
        opt = next((opt for opt in options if opt['key'] == key), None)
        if opt['act'] == 'mv':
	    current = moveToDirectory(current, pictures, opt['dir'], stack)
        elif opt['act'] == 'cp':
	    current = copyToDirectory(current, pictures, opt['dir'])
        elif opt['act'] == 'undo':
            current = undo(current, pictures, stack)
    else:
        print('wrong command:')
        print(key)

cv2.destroyAllWindows()


# vim: set ts=4 sw=4 expandtab
