from os import system
from math import floor
import cv2 as cv
from time import sleep
from constants import MATCH_METHOD, THRESHOLD, SLEEP_TIME


def tap(pos, x_offset=0, scale=1):
	'''
	Tap position pos = (x, y) (based on 1920x1080 scale).
	If actual scale is not 1, then given (x, y) will be scaled.
	If screen is not 16:9 (most commonly, 2160x1080), then
	adjust x_offset (in this case, 120).
	Note x_offset is applied before scale.
	'''
	actual_x = floor((pos[0] + x_offset) * scale)
	actual_y = floor(pos[1] * scale)
	system(f'adb shell input tap {actual_x} {actual_y}')

def capture():
	'''
	Capture screen and save that image to './temp.png'.
	Then, read it and returns an OpenCV image.
	'''
	system('adb exec-out screencap -p > temp.png')
	return cv.imread('temp.png')

def match(source, target) -> bool:
	'''
	Use "minMaxLoc" to find target image on source image.
	Input values are all OpenCV images.
	Return value represents similarity; Greater value means greater similarity.
	'''
	result = cv.matchTemplate(source, target, MATCH_METHOD)
	_, max_val, _, _ = cv.minMaxLoc(result)
	return max_val > THRESHOLD

def wait():
	'''
	Wait for a few time. Time is defined in constants.py
	'''
	sleep(SLEEP_TIME)