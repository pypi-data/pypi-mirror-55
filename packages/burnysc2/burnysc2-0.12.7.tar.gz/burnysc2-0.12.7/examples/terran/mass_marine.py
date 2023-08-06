"""
A bot that goes up to 3 rax and masses marines while it keeps expanding.

Bot made by Burny
"""

from typing import List, Set, Dict, Union, Optional, Iterable

import random
import numpy as np
import heapq

import sc2
from sc2 import Race, Difficulty
from sc2.constants import *
from sc2.position import Point2, Point3
from sc2.unit import Unit
from sc2.player import Bot, Computer
from sc2.player import Human
from sc2.bot_ai import BotAI

from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId
from sc2.ids.upgrade_id import UpgradeId
from sc2.ids.buff_id import BuffId
from sc2.ids.effect_id import EffectId

from sc2.unit import Unit
from sc2.units import Units
from sc2.game_info import Ramp


def save_array_to_png(array: np.ndarray, file_name: str):
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    # ax = fig.add_subplot(111)
    ax.imshow(array)
    ax.invert_yaxis()
    fig.savefig(f"{file_name}.png", dpi=1000)
    # plt.show()

# test = np.asarray([
#     [0, 1, 2],
#     [3, 4, 5],
#     [6, 7, 8]
# ])
# save_array_to_png(test, "test2")

class NydusBot(BotAI):
    async def on_step(self, iteration):
        # Build scvs
        # Build marines
        # Build depots
        # Build barracks
        # Build addons
        # Build ebays
        # Build factory
        # Build armory
        # Build refinery
        # Morph to orbital
        # Research upgrades
        # Distribute workers
        # Micro marines
        color = Point3((0, 0, 255))
        for worker in self.bot.workers:
            self.bot._client.debug_box2_out(worker.position3d, half_vertex_length=0.25, color=color)

        pass

    async def on_start(self):
        # Split workers
        self.split_workers()
        # Calculate areas of expansions
        area_numpy_array, areas = self.generate_voronoi_array()
        # Calculate building grid for all bases

        pass

    def split_workers(self):
        townhall = self.townhalls.random
        used_workers: Set[int] = set()
        mineral_fields = self.mineral_field.closer_than(15, townhall)
        mineral_fields = mineral_fields.sorted_by_distance_to(townhall)

        # There will be 8 mineral fields at the start location, order workers to mine at those 8 based on their distance
        for mf in mineral_fields:
            workers = self.workers.tags_not_in(used_workers)
            closest_worker = workers.closest_to(mf)
            self.do(closest_worker.gather(mf))
            used_workers.add(closest_worker.tag)

        # Send the remaining 4 workers to mine on the closest mineral field to their position
        for worker in self.workers.tags_not_in(used_workers):
            mf = mineral_fields.closest_to(worker)
            self.do(worker.gather(mf))

    def generate_voronoi_array(self, allow_diagonal=True):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        if not allow_diagonal:
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        # A heapq, where the array will be sorted
        open_list = []
        color_dict = {}
        sqrt2 = 2 ** 0.5

        starting_points: List[Point2] = list(self.expansion_locations.keys())

        # Create starting condition
        for color, point in enumerate(starting_points, start=1):
            # Contains tuple of (y, x, dist_to_start, color, terrain_height_origin)
            x, y = point.rounded
            heapq.heappush(open_list, (0, y, x, color, self.game_info.terrain_height.data_numpy[y, x]))

        # Loop over all points, pop the shortest to any starting point
        while open_list:
            current = heapq.heappop(open_list)
            dist_to_start, y, x, color, terrain_height = current

            # Position was already checked
            if (y, x) in color_dict:
                continue

            color_dict[(y, x)] = color
            for dir_index, direction in enumerate(directions):
                new_y, new_x = (y + direction[0], x + direction[1])
                # Discard point that has different starting terrain height
                # Discard point that is not in placement grid
                if (
                    self.game_info.terrain_height.data_numpy[new_y, new_x] != terrain_height
                    or self.game_info.placement_grid.data_numpy[new_y, new_x] == 0
                ):
                    continue
                new_distance = dist_to_start + (sqrt2 if dir_index > 3 else 1)
                heapq.heappush(open_list, (new_distance, new_y, new_x, color, terrain_height))

        # Create new numpy array with the colors as value
        return_array = np.zeros_like(self.game_info.pathing_grid.data_numpy, dtype=np.uint8)
        for p, color in color_dict.items():
            # print(p, color)
            return_array[p] = color

        areas: Dict[int, Area] = {}
        for (y, x), color in np.ndenumerate(return_array):
            # Create "Area" objects and add points to them
            if color not in areas:
                areas[color] = Area(bot_object=self)
                areas[color].area_color = color
            areas[color].add(Point2((x, y)))

        # save_array_to_png(return_array, "test")
        expansion_color_dict: Dict[Point2, int] = {}
        color_expansion_dict: Dict[int, Point2] = {}

        # Add expansion location to area
        for expansion in self.expansion_locations:
            x, y = expansion.rounded
            color = return_array[y, x]
            assert color != 0, f"Only locations that are outside of pathing grid should be 1"
            # print(x, y, color, return_array[y-1:y+2, x-1:x+2])
            assert areas[color].expansion_position is None, f"Trying to apply an expansion position to an area more than once: x: {x}, y: {y}, old color: {areas[color].expansion_position}, new color: {color}"
            areas[color].expansion_position = expansion
            expansion_color_dict[expansion] = color
            color_expansion_dict[color] = expansion

        # TODO mark ramps
        # TODO mark areas that are unreachable by expansions but are pathable

        return return_array, areas


class CustomRamp(set):
    def __init__(self, points: Iterable[Point2] = None, bot_object: BotAI = None):
        if points is None:
            points = set()
        set.__init__(self, points)
        self._bot_object: BotAI = bot_object
        self.adjacent_areas: List[Area] = []
        self.ramp_color: int = -1

    """
    Properties:
    Get all upper points of a ramp
    Get all lower points of a ramp
    Get top center point of a ramp
    Get bottom center point of a ramp   
    
    Methods:
    Get all neighboring areas
    Enemy has vision to the top -> bool
    """


class Area(set):
    def __init__(self, points: Iterable[Point2] = None, bot_object: BotAI = None):
        """
        Each area is defined for an expansion location.
        TODO: Areas that have no expansions but are cut off via ramps might be added as areas later.

        A helper class for army movement to decide whether enemy units can be ignored or if units need to be sent to defend an expansion.

        :param points:
        :param bot_object:
        """
        if points is None:
            points = set()
        set.__init__(self, points)
        self._bot_object: BotAI = bot_object
        self.adjacent_areas: List[Area] = []
        self.adjacent_ramps: List[CustomRamp] = []
        self.area_color: int = -1

        # 0: Unclaimed, 1: Mine, 2: Enemy
        self.area_ownership: int = 0

        self.expansion_position: Optional[Point2] = None
        # Point that is between expansion position and the mineral fields
        self.mineral_line_center: Optional[Point2] = None

    """
    Properties:
    area_belongs_to_nobody -> bool
    area_belongs_to_me -> bool
    area_belongs_to_enemy -> bool
    
    Methods:    
    Get all adjacent ramps
    Get all adjacent areas
    Get all adjacent areas that are connected through a ramp
    
    Get all edge points (points that lie on the outside of the area, which form the border)
    Get all points that are connected to a certain ramp (intersection)
    
    Get all my units in that area
    Get all enemy units in that area
    
    Get point from area that is closest to a unit
    Get point in mineral line for ranged-units to retreat from enemy melee-units
    
    Test if point is in area (to check if a unit is leaving an area or if an area of ours is under attack)
    Test if a rectangle of points is in an area (to be able to plant a nydus, or have enough space for a drop)
    
    Mark area as "ours" or "neutral" or "belongs to enemy", based on that: send troops to defend, ignore or attack
    """

def main(player1, player2, _map, realtime):
    sc2.run_game(
        sc2.maps.get(_map),
        [player1, player2],
        realtime=realtime,
        # Force same spawn every game
        random_seed=1000,
    )


if __name__ == '__main__':
    bot = sc2.player.Bot(sc2.Race.Terran, NydusBot())
    # human = sc2.player.Human(sc2.Race.Terran)

    # fixed race seems to use different strats than sc2.Race.Random
    race = random.choice([sc2.Race.Zerg, sc2.Race.Terran, sc2.Race.Protoss, sc2.Race.Random])
    build = random.choice(
        [
            # sc2.AIBuild.RandomBuild,
            sc2.AIBuild.Rush,
            sc2.AIBuild.Timing,
            sc2.AIBuild.Power,
            sc2.AIBuild.Macro,
            sc2.AIBuild.Air,
        ]
    )
    build = sc2.AIBuild.Macro
    race = Race.Terran
    builtin_bot = sc2.player.Computer(race, sc2.Difficulty.Medium, build)
    # builtin_bot = sc2.player.Computer(race, sc2.Difficulty.CheatInsane, build)

    map_ = random.choice(
        [
            "AutomatonLE",
            "BlueshiftLE",
            "CeruleanFallLE",
            "DarknessSanctuary",
            "KairosJunctionLE",
            "ParaSiteLE",
            "PortAleksanderLE",
            # "StasisLE",
            "Bandwidth",
            "Ephemeron",
            "PrimusQ9",
            "Reminiscence",
            "Sanglune",
            "TheTimelessVoid",
            "Urzagol",
            "Acropolis",
            "Artana",
            "CrystalCavern",
            "DigitalFrontier",
            "OldSunshine",
            "Treachery",
            "Triton",
        ]
    )
    map_ = "Triton"
    # human = sc2.player.Human(sc2.Race.Terran)
    main(bot, builtin_bot, map_, realtime=False)
