from random import randint, choice

from DummyPlayer import DummyPlayer
from SeaGrid import SeaGrid
from constants import GRID_SIZE

DIRECTIONS = {'N', 'E', 'S', 'W'}


class Bot(DummyPlayer):
    def __init__(self, grid: SeaGrid, turn_switch_func):
        super().__init__(grid, turn_switch_func)
        self.__attack_grid = None
        self.__attack_result = 0
        self.__target = None
        self.__target_streak = 0

    def perform_attack(self):
        # if attack result = 0 -> Miss
        # if attack result = 1 -> Hit
        # if attack result = 2 -> Destroy

        # If there is no target -> attack random point
        if self.__target is None:
            # Choose random cell and attack it
            x_index, y_index = randint(0, GRID_SIZE - 1), randint(0, GRID_SIZE - 1)
            cell = self.__attack_grid.get_cell_by_indices(x_index, y_index)
            attack_result = self.__attack_grid.try_attack_cell(cell)

            # If this cell is cannot be attacked, choose another cell
            while attack_result == -1:
                x_index, y_index = randint(0, GRID_SIZE - 1), randint(0, GRID_SIZE - 1)
                cell = self.__attack_grid.get_cell_by_indices(x_index, y_index)
                attack_result = self.__attack_grid.try_attack_cell(cell)

            result = attack_result
            if result == 1:
                self.__target = cell
                self.__target_streak = 1

        # If there is a target
        else:
            hit_or_miss = randint(0, 1)

            cells_around = self.__attack_grid.get_empty_cells_around(self.__target)

            # Make bot miss the shoot
            if hit_or_miss == 0 and len(cells_around) != 0:
                cell = choice(cells_around)
            # Make bot hit the player
            else:
                ship_cell = self.__target.get_warship().get_ship_closest_cell(self.__target)
                self.__target_streak += 1
                cell = ship_cell

            # If the target was destroyed - search for new target
            result = self.__attack_grid.try_attack_cell(cell)
            if result == 2:
                self.__target_streak = 0
                self.__target = None

        # parameter: should this player repeat its turn
        self.action_done(result != 0, cell)

    def place_all_warships(self):
        stock = len(self.get_player_warship_stock())
        grid = self.get_player_grid()
        while stock != 0:
            warship = self.get_first_warship()
            x_index, y_index = randint(0, GRID_SIZE - 1), randint(0, GRID_SIZE - 1)
            # generate indices until find free cell
            while grid.is_cell_occupied(x_index, y_index):
                x_index, y_index = randint(0, GRID_SIZE - 1), randint(0, GRID_SIZE - 1)

            cell = grid.get_cell_by_indices(x_index, y_index)

            attempts = 0
            while attempts < 4:
                warship.rotate_direction()
                placed_successfully = self.try_place_ship(cell, warship)
                if placed_successfully:
                    break
                attempts += 1

            stock = len(self.get_player_warship_stock())

    def set_player_grid(self, grid):
        self.__attack_grid = grid
