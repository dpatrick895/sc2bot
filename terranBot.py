import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from sc2.constants import *

class terranBot(sc2.BotAI):

	async def on_step(self, interation):
		await self.distribute_workers()
		await self.build_workers()
		await self.build_supply_depot()

	async def build_workers(self):
		for cc in self.units(COMMANDCENTER).ready.noqueue:
			if self.can_afford(SCV):
				await self.do(cc.train(SCV))

	async def build_supply_depot(self):
		if self.supply_left < 5 and not self.already_pending(SUPPLYDEPOT):
			cc = self.units(COMMANDCENTER).ready
			if cc.exists:
				if self.can_afford(SUPPLYDEPOT):
					await self.build(SUPPLYDEPOT, near=cc.first)


run_game(maps.get("CactusValleyLE"), [
    Bot(Race.Terran, terranBot()),
    Computer(Race.Terran, Difficulty.Easy)
], realtime=True)
