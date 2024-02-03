from tkinter import Canvas

from Warship import Warship
from colors import *
from constants import CELL_SIZE


class Cell:
    def __init__(self, x_offset, y_offset, x, y, canvas: Canvas, is_hidden):
        self.__canvas = canvas
        self.__x_index = x
        self.__y_index = y
        self.__grid_offset_x = x_offset
        self.__grid_offset_y = y_offset
        x1 = self.__grid_offset_x + self.__x_index * CELL_SIZE
        y1 = self.__grid_offset_y + self.__y_index * CELL_SIZE
        self.__coords = (x1, y1, x1 + CELL_SIZE, y1 + CELL_SIZE)

        self.__warship = None
        self.__hit_type = None
        self.__is_occupied = False
        self.__occupation_type = None
        self.__is_color_permanent = False
        self.__is_hidden = is_hidden

        self.__initialize_cell()

    def get_warship(self):
        return self.__warship

    def get_hit_type(self):
        return self.__hit_type

    def set_hit_type(self, value):
        if self.__hit_type == 'WARSHIP':
            return

        self.__hit_type = value
        self.__is_color_permanent = True
        if value == 'WARSHIP':
            self.__canvas.itemconfig(self.__id, outline=CELL_DESTROYED_COLOR_OUTLINE, fill=CELL_DESTROYED_COLOR)
        elif value == 'NEAR':
            self.__canvas.itemconfig(self.__id, outline=CELL_DESTROYED_COLOR_NEAR_OUTLINE,
                                     fill=CELL_DESTROYED_COLOR_NEAR)
        elif value == 'MISSED':
            self.__canvas.itemconfig(self.__id, outline=CELL_MISSED_COLOR_OUTLINE,
                                     fill=CELL_MISSED_COLOR)
        else:
            raise ValueError(f'Value must be WARSHIP or NEAR. Given: {value}')

    def __initialize_cell(self):
        """
        Draw a rectangle on the coordinates in __init__ function
        :return:
        """
        x1, y1, x2, y2 = self.__coords
        self.__id = self.__canvas.create_rectangle(x1, y1, x2, y2, width=3, outline=CELL_COLOR_OUTLINE, fill=CELL_COLOR)

    def on_cell_hovered(self):
        """
        Event is called when the player hovered a cell
        """
        if self.__is_color_permanent:
            return

        self.__canvas.itemconfig(self.__id, outline=CELL_HOVER_COLOR_OUTLINE, fill=CELL_HOVER_COLOR)

    def on_cell_hovered_off(self):
        """
        Event is called when the mouse ended hovering a cell
        """
        if self.__is_color_permanent:
            return

        self.__canvas.itemconfig(self.__id, outline=CELL_COLOR_OUTLINE, fill=CELL_COLOR)
        if self.__is_hidden:
            return

        if self.__is_occupied:
            if self.__occupation_type == 'SHIP':
                self.__canvas.itemconfig(self.__id, outline=CELL_OCCUPIED_COLOR_OUTLINE, fill=CELL_OCCUPIED_COLOR)
            elif self.__occupation_type == 'NEAR':
                self.__canvas.itemconfig(self.__id, outline=CELL_NEAR_OCCUPIED_COLOR_OUTLINE,
                                         fill=CELL_NEAR_OCCUPIED_COLOR)


    def on_cell_hovered_ghost(self, is_available) -> None:
        """
        Changes color for this cell based on is_available parameter
        :param is_available: Can ship fit the whole cells
        """
        fill = CELL_INCORRECT_COLOR
        outline = CELL_INCORRECT_COLOR_OUTLINE
        if is_available:
            fill = CELL_PLACING_COLOR
            outline = CELL_PLACING_COLOR_OUTLINE

        self.__canvas.itemconfig(self.__id, fill=fill, outline=outline)

    def get_cell_coords(self):
        """
        Gets the coordinates of this cell on canvas
        :return: x1, y1, x2, y2 tuple
        """
        return self.__coords

    def get_cell_indices(self):
        """
        Get cell x, y indices of the grid
        :return: tuple of (x,y)
        """
        return self.__x_index, self.__y_index

    def is_cell_occupied(self) -> bool:
        """
        Getter for __is_occupied method
        :return: self.__is_occupied
        """
        return self.__is_occupied

    def handle_miss(self):
        self.set_hit_type('MISSED')

    def occupy_cell(self, occupation_type: str):
        """
        Tries to occupy the cell with given occupation_type. Does not overwrite the values for already occupied cells
        :param occupation_type: Possible options: SHIP - there is a ship in the cell, NEAR - there is a ship nearby
        of this cell
        """
        if self.__is_occupied:
            return

        self.__is_occupied = True
        self.__occupation_type = occupation_type

        if self.__is_hidden:
            return

        if occupation_type == 'SHIP':
            self.__canvas.itemconfig(self.__id, outline=CELL_OCCUPIED_COLOR_OUTLINE, fill=CELL_OCCUPIED_COLOR)
        elif occupation_type == 'NEAR':
            self.__canvas.itemconfig(self.__id, outline=CELL_NEAR_OCCUPIED_COLOR_OUTLINE, fill=CELL_NEAR_OCCUPIED_COLOR)
        else:
            self.__is_occupied = None
            raise ValueError(f"occupation_type must be SHIP or NEAR. Can't be {occupation_type}")

    def assign_warship(self, warship: Warship):
        self.__warship = warship
