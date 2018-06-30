import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from sc2.constants import *
import random


class terranBot(sc2.BotAI):

	async def on_step(self, interation):
		await self.distribute_workers()
		await self.build_workers()
		await self.build_supply_depot()
		await self.expand()
		await self.build_refinery()
		await self.build_barracks()
		await self.train_marine()
		await self.train_reaper()
		await self.attack()
		

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

	async def build_barracks(self):
		if self.units(SUPPLYDEPOT).ready.exists:
			if self.units(BARRACKS).amount < 2 and self.can_afford(BARRACKS):
				sd = self.units(SUPPLYDEPOT).ready
				if sd.exists:
					await self.build(BARRACKS, near = sd.first)


	async def train_marine(self):
		for bar in self.units(BARRACKS).ready.noqueue:
			if(self.can_afford(MARINE)):
				await self.do(bar.train(MARINE))

	async def train_reaper(self):
		for bar in self.units(BARRACKS).ready.noqueue:
			if(self.can_afford(REAPER)):
				await self.do(bar.train(REAPER))

	def find_target(self, state):
		if len(self.known_enemy_units) > 0:
			return random.choice(self.known_enemy_units)
		elif len(self.known_enemy_structures) > 0:
			return random.choice(self.known_enemy_structures)
		else:
			return self.enemy_start_locations[0]

	async def attack(self):
		if (self.units(REAPER).amount + self.units(MARINE).amount) > 25:
			for s in self.units(REAPER).idle or self.units(MARINE).idle:
				await self.do(s.attack(self.find_target(self.state)))

		elif (self.units(REAPER).amount + self.units(MARINE).amount) > 5:
			if len(self.known_enemy_units) > 0:
				for s in self.units(REAPER).idle or self.units(MARINE).idle:
					await self.do(s.attack(random.choice(self.known_enemy_units)))



run_game(maps.get("CactusValleyLE"), [
    Bot(Race.Terran, terranBot()),
    Computer(Race.Terran, Difficulty.Easy)
], realtime=False)
