import cv2 as cv
import numpy as np

MapInfo = cv.imread('assets/8-2.jpg')
BattleResult = cv.imread('assets/BattleResult.jpg')
GainedExp = cv.imread('assets/GainedExp.jpg')
GetShip = cv.imread('assets/GetShip.jpg')
NightBattleYesNo = cv.imread('assets/NightBattleYesNo.jpg')
NoNetwork = cv.imread('assets/NoNetwork.jpg')
ReadyForCombat = cv.imread('assets/ReadyForCombat.jpg')
SelectBuff = cv.imread('assets/SelectBuff.jpg')
StartBattle = cv.imread('assets/StartBattle.jpg')

md = cv.TM_CCORR_NORMED

tpl = NightBattleYesNo

cv.namedWindow('template image', cv.WINDOW_NORMAL)
cv.imshow("template image", tpl)

for i in range(1, 12):
    target = cv.imread('raw/%d.jpg' % i)
    th, tw = tpl.shape[:2]
    result = cv.matchTemplate(target, tpl, md)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
    print(max_val, max_loc)
    tl = max_loc
    br = (tl[0] + tw, tl[1] + th)  # br是矩形右下角的点的坐标
    cv.rectangle(target, tl, br, (0, 0, 255), 2)
    cv.namedWindow("match-" + np.str(md), cv.WINDOW_NORMAL)
    cv.imshow("match-" + np.str(md), target)
    cv.waitKey(0)
    cv.destroyAllWindows()
