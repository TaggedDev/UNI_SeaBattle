from Cell import Cell
from Warship import get_shift_by_direction
from constants import GRID_SIZE, AXIS_OFFSET, CELL_SIZE


def mouse_in_between(mouse_x, mouse_y, coords):
    is_in_x = coords[0] <= mouse_x <= coords[2]
    is_in_y = coords[1] <= mouse_y <= coords[3]
    return is_in_y and is_in_x


class SeaGrid:
    def __init__(self, canvas, x_offset, y_offset, hide_ships):
        self.__cells = []
        self.__canvas = canvas
        self.__hide_ships = hide_ships
        self.__initialize_cells(x_offset, y_offset)
        self.__initialize_axis(x_offset, y_offset)
        self.__saved_cell = None

    def get_saved_cell(self) -> Cell:
        """
        Getter for self.__saved_cell (currently hovered cell)
        :return: Saved cell
        """
        return self.__saved_cell

    def show_ship_ghost(self, slots: int, direction: str) -> None:
        """
        Displays a ghost for a possible ship placement
        :param slots: Amount of slots a warship takes
        :param direction: A direction from where target is moving. Possible options in [N, S, W, E]
        """
        dx, dy = get_shift_by_direction(direction)
        cells = []
        x, y = self.__saved_cell.get_cell_indices()
        all_cells_available = True

        for i in range(slots):
            cell = self.get_cell_by_indices(x + dx * i, y + dy * i)
            if cell is None:
                all_cells_available = False
            cells.append(cell)

        for cell in cells:
            if cell is None:
                continue

            is_cell_occupied = cell.is_cell_occupied()
            is_available = (not is_cell_occupied) and all_cells_available
            cell.on_cell_hovered_ghost(is_available)

    def update_cells_colors(self, mouse_x, mouse_y) -> None:
        """
        Updates hover effects for each cell
        :param mouse_x: Mouse position X
        :param mouse_y: Mouse position Y
        """

        # for each cell disable selection
        self.__saved_cell = None
        for row in self.__cells:
            for cell in row:
                cell.on_cell_hovered_off()

                is_cell_under_hover = mouse_in_between(mouse_x, mouse_y, cell.get_cell_coords())
                if is_cell_under_hover:
                    self.__saved_cell = cell

        # but for the one player is hovering right now turn it on
        if self.__saved_cell is None:
            return
        self.__saved_cell.on_cell_hovered()

    def get_cell_by_indices(self, x, y):
        """
        Returns cell on given coordinates of 2D-array
        :param x: x index of the cell
        :param y: y index of the cell
        :return: None if x or y is out of bounds. Otherwise: cell object
        """
        if x >= GRID_SIZE or x < 0 or y < 0 or y >= GRID_SIZE:
            return None
        return self.__cells[x][y]

    def __initialize_cells(self, x_offset, y_offset):
        """
        Instantiating cells in grid
        :param x_offset: offset in pixels for the grid (x) on canvas
        :param y_offset: offset in pixels for the grid (y) on canvas
        """
        for x in range(GRID_SIZE):
            row = []
            for y in range(GRID_SIZE):
                cell = Cell(x_offset, y_offset, x, y, self.__canvas, self.__hide_ships)
                row.append(cell)
            self.__cells.append(row)

    def try_attack_cell(self, cell):
        """
        Implements attempt to attack cell
        :param cell: Cell object to attack
        :return:
        -1 - unable to implement attack (destroyed cell)
        0 - miss
        1 - hit
        2 - destroy
        """
        if cell.get_hit_type() in ['NEAR', 'WARSHIP', 'MISSED']:
            return -1

        if not cell.get_warship():
            cell.handle_miss()
            return 0

        warship = cell.get_warship()
        warship.handle_hit()
        cell.set_hit_type('WARSHIP')

        if warship.is_destroyed():
            self.display_destroyed_ship(warship)
            return 2
        return 1

    def gather_cells_around_cell(self, cell):
        x, y = cell.get_cell_indices()
        cells = []
        for x_i in range(x - 1, x + 2):
            for y_i in range(y - 1, y + 2):
                if x_i < 0 or y_i < 0 or y_i >= GRID_SIZE or x_i >= GRID_SIZE:
                    continue
                cells.append(self.__cells[x_i][y_i])
        return cells

    def display_destroyed_ship(self, warship):
        for warship_cell in warship.get_ship_cells():
            targets = self.gather_cells_around_cell(warship_cell)
            for cell in targets:
                cell.set_hit_type('NEAR')

    def is_cell_occupied(self, x_index, y_index):
        """
        Check whether cell on given index is occupied NEAR/SHIP on given coordinates
        :param x_index: x_index of the array
        :param y_index: y_index of the array
        :return: True if cell is occupied of any kind. False if cell is free
        """
        if self.__cells[x_index][y_index].is_cell_occupied():
            return True
        return False

    def get_empty_cells_around(self, cell):
        x, y = cell.get_cell_indices()
        indices = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        cells = [self.get_cell_by_indices(index[0], index[1]) for index in indices]

        result = []
        for cell in cells:
            if (cell is not None) and (cell.get_hit_type() is None) and (cell.get_warship() is None):
                result.append(cell)
        return result

    def try_occupy_around(self, cell):
        """
        Tries to occupy (NEAR) every free slot around given one
        :param cell:
        :return:
        """
        targets = self.gather_cells_around_cell(cell)
        for target in targets:
            target.occupy_cell('NEAR')

    def __initialize_axis(self, x_offset, y_offset):
        # Horizontal
        y_0 = y_offset + CELL_SIZE // 2
        x_0 = x_offset - AXIS_OFFSET
        for i in range(GRID_SIZE):
            x, y = x_0, y_0 + i * CELL_SIZE
            self.__canvas.create_text(x, y, text=str(i+1), font=('Arial', 20))

        # Vertical
        y_0 = y_offset - AXIS_OFFSET
        x_0 = x_offset + CELL_SIZE // 2
        abc = 'ABCDEFGHIJ'
        for i in range(GRID_SIZE):
            x, y = x_0 + i * CELL_SIZE, y_0
            self.__canvas.create_text(x, y, text=abc[i], font=('Arial', 20))