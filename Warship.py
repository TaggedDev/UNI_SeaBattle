from constants import GRID_SIZE

DIRECTIONS = ['N', 'E', 'S', 'W']


def get_shift_by_direction(direction: str) -> tuple:
    """
    Returns a shift for 2d-array indexing based on a string-value direction
    :param direction: Possible options: [S, N, W, E]
    :return: dx, dy for the indexing
    """
    if direction == 'S':
        return 0, 1
    elif direction == 'N':
        return 0, -1
    elif direction == 'W':
        return -1, 0
    elif direction == 'E':
        return 1, 0
    else:
        raise ValueError(f'Direction must be in [S,N,W,E]. The given one is {direction}')


class Warship:
    def __init__(self, slots=1, direction='N'):
        self.__slots = slots
        self.__x_pos = None
        self.__y_pos = None
        self.__face_direction = direction
        self.__face_direction_index = 0
        self.__hp = slots
        self.__cells = []

    def set_ship_cells(self, value):
        if len(value) != self.__slots:
            raise ValueError(f'Given slot list is not the same size as slots. Given {value}. Should be: {self.__slots}')
        self.__cells = value

    def get_ship_cells(self):
        return self.__cells

    def get_ship_closest_cell(self, cell):
        min_distance = float('inf')
        closest_cell = None
        cell_x, cell_y = cell.get_cell_indices()

        for other_cell in self.__cells:
            if not (other_cell.get_hit_type() is None):
                continue

            other_x, other_y = other_cell.get_cell_indices()
            distance = abs(cell_x - other_x) + abs(cell_y - other_y)
            if distance < min_distance:
                min_distance = distance
                closest_cell = other_cell

        return closest_cell

    def handle_hit(self):
        self.__hp -= 1

    def is_destroyed(self):
        return self.__hp == 0

    def get_slots(self):
        return self.__slots

    def get_position(self):
        return self.__x_pos, self.__y_pos

    def get_direction(self):
        return self.__face_direction

    def rotate_direction(self):
        new_index = (self.__face_direction_index + 1) % 4
        self.__face_direction = DIRECTIONS[new_index]
        self.__face_direction_index = new_index

    @staticmethod
    def can_be_placed(grid, x: int, y: int, direction: str, slots: int) -> bool:
        """
        Does a check whether a ship can or not be placed on a specific x, y with specific direction (rotation)
        :param grid: A grid-owner
        :param x: x = [0,9] - index for column
        :param y: y = [0,9] - index for row
        :param direction: A direction defined by [N, S, W, E]. The ship will face there
        :param slots: Amount of slots this ship occupies
        :return: A bool value true or false: can this ship be placed or not
        """
        # Check if (x,y) is occupied
        if grid.is_cell_occupied(x, y):
            return False

        # Check if of other ship cells in given direction are occupied
        dx, dy = get_shift_by_direction(direction)
        for slot_i in range(slots):
            slot_x = x + dx * slot_i
            slot_y = y + dy * slot_i

            # if slot is going out of bounds -> return false
            if slot_x < 0 or slot_y < 0 or slot_x >= GRID_SIZE or slot_y >= GRID_SIZE:
                return False

            # or this slot is occupied -> return false
            if grid.is_cell_occupied(slot_x, slot_y):
                return False

        # Check if all other slots of this ship are not near the existing one (не в плотную)
        return True
