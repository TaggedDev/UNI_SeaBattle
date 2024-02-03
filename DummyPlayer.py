from Cell import Cell
from SeaGrid import SeaGrid
from Warship import Warship, get_shift_by_direction


class DummyPlayer:
    def __init__(self, grid: SeaGrid, turn_switch_func):
        self.__grid = grid

        self.__warships_in_stock = []
        self.__warships_list = []
        self.__initialize_stock()
        self.__action_done_function = turn_switch_func
        self.__last_action = ''

        # preparing, game, finished
        self.__current_state = 'preparing'

    def has_alive_ships(self):
        for warship in self.__warships_list:
            if not warship.is_destroyed():
                return True
        return False

    def action_done(self, repeat_turn, current_cell: Cell):
        x, y = current_cell.get_cell_indices()
        self.__action_done_function(repeat_turn, f'{"ABCDEFGHJI"[x]}{y+1}')

    def get_player_grid(self):
        return self.__grid

    def get_player_warship_stock(self):
        return self.__warships_in_stock

    def get_first_warship(self):
        if len(self.__warships_in_stock) == 0:
            return None
        return self.__warships_in_stock[0]

    def try_place_ship(self, cell, warship: Warship):
        x, y = cell.get_cell_indices()

        direction = warship.get_direction()
        slots = warship.get_slots()

        # If placing a ship is unable on specific slot with certain direction -> show player the error message
        if not Warship.can_be_placed(self.__grid, x, y, direction, slots):
            return False

        # Otherwise occupy all required cells
        warship = self.__warships_in_stock[0]

        dx, dy = get_shift_by_direction(direction)
        newly_occupied = []
        for slot_i in range(warship.get_slots()):
            slot_x = x + dx * slot_i
            slot_y = y + dy * slot_i

            cell = self.__grid.get_cell_by_indices(slot_x, slot_y)
            cell.occupy_cell('SHIP')
            cell.assign_warship(warship)
            newly_occupied.append(cell)

        warship.set_ship_cells(newly_occupied)
        for occupied_cell in newly_occupied:
            self.__grid.try_occupy_around(occupied_cell)

        self.__warships_list.append(self.__warships_in_stock[0])
        del self.__warships_in_stock[0]
        return True

    def rotate_warship(self):
        warship = self.__warships_in_stock[0]
        warship.rotate_direction()

    def __initialize_stock(self):
        slots = [4] + [3, 3] + [2, 2, 2] + [1, 1, 1, 1]
        for slot in slots:
            self.__warships_in_stock.append(Warship(slot))
