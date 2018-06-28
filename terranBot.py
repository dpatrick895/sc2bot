import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from sc2.constants import *

class terranBot(sc2.BotAI):

	async def on_step(self, interation):
		await self.distribute_workers()
		await self.build_workers()
		await self.build_supply_depot()
		await self.build_refinery()
		await self.expand()

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

	async def build_refinery(self):
		for cc in self.units(COMMANDCENTER).ready:
			vespenes = self.state.vespene_geyser.closer_than(25.0, cc)
			for vespene in vespenes:
				if not self.can_afford(REFINERY):
					break
				worker = self.select_build_worker(vespene.position)
				if worker is None:
					break
				if not self.units(REFINERY).closer_than(1.0, vespene).exists:
					await self.do(worker.build(REFINERY, vespene))

	async def expand(self):
		if self.units(COMMANDCENTER).amount < 2 and self.can_afford(COMMANDCENTER):
			await self.expand_now()


run_game(maps.get("CactusValleyLE"), [
    Bot(Race.Terran, terranBot()),
    Computer(Race.Terran, Difficulty.Easy)
], realtime=True)
