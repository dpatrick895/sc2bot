import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from sc2.constants import HATCHERY, DRONE

class zergBot(sc2.BotAI):

	async def on_step(self, iteration):
		#what to do every step
		await self.distribute_workers()
		await self.build_workers()

	async def build_workers(self):
		# hatchery is the zerg command center
		for hatchery in self.units(HATCHERY).ready.noqueue:
			if self.can_afford(DRONE):
				await self.do(hatchery.train(DRONE))


run_game(maps.get("AbyssalReefLE"), [
	Bot(Race.Zerg, zergBot()),
	Computer(Race.Terran, Difficulty.Easy)]
	, realtime=True)

