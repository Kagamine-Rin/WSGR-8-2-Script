import cv2 as cv
import logging
import utils
from constants import state
import constants

if constants.DETAILED_LOG:
	logging.basicConfig(level = logging.INFO, format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
else:
	logging.basicConfig(level = logging.WARN, format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class bot():
	'''
	The bot class. Controls all steps.
	'''

	def __init__(self, curr_ship = 450, max_ship = 500, scale = 1, offs = 0):
		'''
		Initalize the bot.
		Params: "curr_ship" -> how many ships you have;
				"max_ship" -> how many ships can you hold at most.
		'''

		# init logger
		self.log = logging.getLogger('bot')

		# init image resources
		self.MapInfo = cv.imread('assets/8-2.jpg')
		self.BattleResult = cv.imread('assets/BattleResult.jpg')
		self.GainedExp = cv.imread('assets/GainedExp.jpg')
		self.GetShip = cv.imread('assets/GetShip.jpg')
		self.NightBattleYesNo = cv.imread('assets/NightBattleYesNo.jpg')
		self.NoNetwork = cv.imread('assets/NoNetwork.jpg')
		self.ReadyForCombat = cv.imread('assets/ReadyForCombat.jpg')
		self.SelectBuff = cv.imread('assets/SelectBuff.jpg')
		self.StartBattle = cv.imread('assets/StartBattle.jpg')
		self.SelectShape = cv.imread('assets/SelectShape.jpg')
		self.ABC = cv.imread('assets/ABC.jpg')

		# init counter
		self.counter = 0
		self.counter_max = max_ship - curr_ship

		self.scale = scale
		self.offset = offs

		# State machine default
		self.state = state.select_map


	def tap(self, pos):
		utils.tap(pos, self.offset, self.scale)

	def loop(self):
		try:
			while True:
				self.run()
		except Exception as e:
			print(e)

	def run(self):

		src = utils.capture()

		if self.state == state.select_map:
			if utils.match(src, self.MapInfo):
				self.state = state.select_fleet
				self.log.info(f'Round {self.counter + 1}')
				self.log.info('Selecting Fleet......')
				self.tap(constants.POS_MAP)
			else:
				utils.wait()
		elif self.state == state.select_fleet:
			if utils.match(src, self.ReadyForCombat):
				self.state = state.go_to_b
				self.log.info('Going into the map......')
				self.tap(constants.POS_START_BATTLE)
			else:
				utils.wait()
		elif self.state == state.go_to_b:
			if utils.match(src, self.ReadyForCombat):
				self.state = state.select_buff
				self.log.info('Go to Point B.')
				self.tap(constants.POS_MAP)
			else:
				utils.wait()
		elif self.state == state.select_buff:
			if utils.match(src, self.SelectBuff):
				self.state = state.select_shape
				self.log.info('Begin searching......')
				self.tap(constants.POS_BUFF_2)
			else:
				utils.wait()
		elif self.state == state.searching:
			pass
		elif self.state == state.select_shape:
			if utils.match(src, self.StartBattle):
				self.log.info('Search success!')
				self.tap(constants.POS_START_BATTLE)
				utils.wait()
				self.tap(constants.POS_SINGLE_LINE)
				self.state = state.in_battle
			elif utils.match(src, self.SelectShape):
				self.log.info('Search fail ...')
				self.tap(constants.POS_SINGLE_LINE)
				self.state = state.in_battle
			else:
				utils.wait()
		elif self.state == state.in_battle:
			if utils.match(src, self.NightBattleYesNo):
				self.state = state.day_battle_end
				self.log.info('Day battle complete!')
				self.tap(constants.POS_GIVE_UP)
			else:
				utils.wait()
		elif self.state == state.day_battle_end:
			if utils.match(src, self.BattleResult):
				self.state = state.mvp
				self.log.info('What grade do you get?')
				self.tap(constants.POS_CLICK_TO_CONTINUE)
			else:
				utils.wait()
		elif self.state == state.mvp:
			if utils.match(src, self.GainedExp):
				self.state = state.get_new_ship
				self.log.info('MVP should belong to CV')
				self.tap(constants.POS_CLICK_TO_CONTINUE)
			else:
				utils.wait()
		elif self.state == state.get_new_ship:
			# 1. C/D fail, directly to state 1
			if utils.match(src, self.MapInfo):
				self.state = state.select_map
				self.log.info('It seems you failed the last battle...')
			# 2. Win, but no ship got
			elif utils.match(src, self.NightBattleYesNo):
				self.state = state.select_map
				self.log.info('It seems you won without ship..')
				self.tap(constants.POS_GIVE_UP)
			# 3. Win, and got ship
			elif utils.match(src, self.GetShip):
				self.state = state.go_further
				self.log.info('Got ship!')
				self.tap(constants.POS_MAP)
			else:
				utils.wait()
		elif self.state == state.go_further:
			if utils.match(src, self.NightBattleYesNo):
				self.state = state.select_map
				self.log.info('Go to next round!')
				self.tap(constants.POS_GIVE_UP)
				self.counter += 1
				if self.counter == self.counter_max:
					self.log.error(f"Ship full!")
					raise RuntimeError("ship full")
			else:
				utils.wait()
		else:
			self.log.error(f"Entered unknown state: {self.state}")
			raise RuntimeError("unknown state")
