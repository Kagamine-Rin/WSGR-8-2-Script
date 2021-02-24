from cv2 import TM_CCORR_NORMED
MATCH_METHOD = TM_CCORR_NORMED

POS_NETWORK_YES = (740, 685)
POS_START_BATTLE = (1680, 1000)
POS_GIVE_UP = (1280, 700)
POS_CLICK_TO_CONTINUE = (1780, 1000)
POS_MAP = (1280, 680)
POS_SINGLE_LINE = (1140, 250)
POS_BUFF_2 = (430, 700)

THRESHOLD = 0.99
SLEEP_TIME = 0.2

DETAILED_LOG = True

from enum import Enum, unique

@unique
class state(Enum):
	"""
	Since scripting on WSGR can be seen as a state machine, this
	class is used to record state.
	"""
	select_map = 1
	select_fleet = 2
	go_to_b = 3  # Placeholder
	select_buff = 4
	searching = 5  # Placeholder
	search_complete = 6
	select_shape = 7
	in_battle = 8
	day_battle_end = 9
	battle_result = 10
	mvp = 11
	get_new_ship = 12
	go_further = 13