from tkinter import *

from Bot import Bot
from GameHistory import GameHistory
from Player import Player
from constants import CELL_SIZE, GRID_SIZE, WIDTH, HEIGHT, GRID_Y_OFFSET
from SeaGrid import SeaGrid


class Field:
    def __init__(self):
        self.__window = Tk()
        self.GRID_SIZE = 10
        self.__canvas = Canvas(self.__window, width=WIDTH, height=HEIGHT)
        self.__canvas.pack(expand=True, fill=BOTH)

        self.__init_grid()
        self.__player = Player(self.__player_grids[0], self.__show_error_message,
                               self.__show_successful_placement_message,
                               self.handle_action_turns)
        self.__bot = Bot(self.__player_grids[1], self.handle_action_turns)
        self.__init_header()
        self.__init_history()

        self.__player_turn = True

        self.__window.bind('<Motion>', self.__player.handle_mouse_movement)
        self.__window.bind('<Button-1>', self.__player.handle_mouse_click)

        self.__window.bind('<Key>', self.__player.handle_rotate_button)
        self.__window.bind('<MouseWheel>', self.__history.handle_user_scroll)
        self.__window.mainloop()

    def __init_grid(self):
        """
        Creating two grids of cells
        """
        player1_offset_x = 50
        player1 = SeaGrid(self.__canvas, player1_offset_x, GRID_Y_OFFSET, False)
        player2_offset_x = 100
        player2 = SeaGrid(self.__canvas, player1_offset_x + player2_offset_x + CELL_SIZE * GRID_SIZE, GRID_Y_OFFSET,
                          True)
        self.__player_grids = [player1, player2]

    def __init_header(self):
        """
        Create header text widget
        """
        self.__header_id = self.__canvas.create_text(50, 10, anchor=NW,
                                                     text='Стадия расстановки кораблей',
                                                     font=("Arial", 20))
        self.__subtitle_id = self.__canvas.create_text(50, 50, anchor=NW,
                                                       text='Установка 4 палубного корабля',
                                                       font=('Arial', 16))

    def __show_error_message(self, cell):
        """
        Called to edit header text with placing error message
        :param cell:
        """
        self.__canvas.itemconfig(self.__subtitle_id,
                                 text=f'В клетку {cell.get_cell_indices()} нельзя установить корабль',
                                 fill='red')

    def __switch_to_gaming_state(self):
        """
        Switches game to new state
        """
        self.__canvas.itemconfig(self.__header_id, text=f'Начинается стадия игры',
                                 fill='black')
        self.__canvas.itemconfig(self.__subtitle_id, text=f'Потопите вражеские корабли!',
                                 fill='black')
        lmb_binding = self.__player.get_gaming_lmb_function(self.__player_grids[1])
        self.__bot.set_player_grid(self.__player_grids[0])
        self.__window.bind('<Button-1>', lmb_binding)

    def __show_successful_placement_message(self, next_warship):
        """
        Change display-text on top of the screen
        :param next_warship: Warship object to be placed. Can be None
        """
        if not next_warship:
            self.__implement_bot_ship_placement()
            self.__switch_to_gaming_state()
            return

        self.__canvas.itemconfig(self.__subtitle_id, text=f'Установка {next_warship.get_slots()} палубного корабля',
                                 fill='black')

    def is_game_over(self):
        # If player has no alive ships left -> he is a loser
        if not self.__player.has_alive_ships():
            return True, 2

        # If bot has no alive ships left -> it is a loser
        if not self.__bot.has_alive_ships():
            return True, 1

        # If both bot and player has any alive ships -> no one is a loser
        return False, 0

    def handle_action_turns(self, should_be_repeated, last_turn):
        game_over_result = self.is_game_over()
        is_game_over = game_over_result[0]

        turn_author = 'Бот'
        if self.__player_turn:
            turn_author = 'Игрок'

        self.__history.add_turn(turn_author, last_turn)

        if is_game_over:
            self.__handle_game_ended(game_over_result[1])
            return

        if should_be_repeated:
            if not self.__player_turn:
                self.__bot.perform_attack()
            return

        if self.__player_turn:
            self.__player_turn = False
            self.__window.unbind('<Button-1>')
            self.__bot.perform_attack()

        else:
            self.__player_turn = True
            self.__window.bind('<Button-1>', self.__player.handle_mouse_click_action)

    def __implement_bot_ship_placement(self):
        self.__bot.place_all_warships()

    def __handle_game_ended(self, winner):
        winner_name = 'Бот'
        if winner == 1:
            winner_name = 'Игрок'

        self.__window.unbind('<Button-1>')
        self.__window.unbind('<Motion>')
        self.__canvas.itemconfig(self.__subtitle_id, text=f'{winner_name} победил!', fill='black')
        self.__canvas.itemconfig(self.__header_id, text='Игра окончена', fill='black')

    def __init_history(self):
        self.__history = GameHistory(self.__canvas, 1200, GRID_Y_OFFSET)
