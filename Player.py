from DummyPlayer import DummyPlayer
from SeaGrid import SeaGrid


class Player(DummyPlayer):
    def __init__(self, grid: SeaGrid, error_func, success_func, switch_turn_func):
        super().__init__(grid, switch_turn_func)

        self.__selection_grid = grid

        self.__error_message_callback = error_func
        self.__successful_placement_func = success_func

        # preparing, game, finished
        self.__current_state = 'preparing'

    def handle_rotate_button(self, event):
        """
        Handles player pressing rotation button R
        :param event: Event of pressed button
        """
        if event.char not in ['к', 'К', 'r', 'R']:
            return

        if self.__current_state != 'preparing':
            return

        self.rotate_warship()
        self.handle_mouse_movement(event)

    def handle_mouse_movement(self, event):
        """
        Event called every time the mouse is moved
        :param event: Information of current mouse movement
        """

        self.__selection_grid.update_cells_colors(event.x, event.y)

        cell = self.__selection_grid.get_saved_cell()
        if cell is None:
            return

        if self.__current_state != 'preparing':
            return

        ws = self.get_first_warship()
        self.__selection_grid.show_ship_ghost(ws.get_slots(), ws.get_direction())

    def handle_mouse_click(self, event):
        """
        Event is called every time LMB is pressed
        :param event: Information about mouse click position
        """
        if self.__current_state not in ['preparing', 'game', 'finished']:
            raise ValueError(f'__current_state of Field is not in list. Given: {self.__current_state}. Must be:'
                             f'{["preparing", "game", "finished"]}')

        current_cell = self.__selection_grid.get_saved_cell()
        if current_cell is None:
            return

        # if preparing -> try place current ship
        if self.__current_state == 'preparing':
            self.try_place_ship(current_cell, self.get_first_warship())
            self.check_current_player_state()
            self.handle_mouse_movement(event)

    def check_current_player_state(self):
        next = self.get_first_warship()
        if len(self.get_player_warship_stock()) == 0:
            self.__current_state = 'game'
            self.__successful_placement_func(None)
            return

        self.__successful_placement_func(next)

    def handle_mouse_click_action(self, event):
        current_cell = self.__selection_grid.get_saved_cell()

        if current_cell is None:
            return

        result = self.__selection_grid.try_attack_cell(current_cell)
        if result == -1:
            return
        self.action_done(result != 0, current_cell)

    def get_gaming_lmb_function(self, enemy_grid):
        """
        Returns link to LMB handler in action phase
        :param enemy_grid: A link to an object of enemy grid
        :return:
        """
        self.__selection_grid = enemy_grid
        return self.handle_mouse_click_action
