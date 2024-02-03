import tkinter
from tkinter import RIGHT, Y, Text
from tkinter.ttk import Scrollbar

Y_OFFSET = 30


class ReadOnlyTextField(tkinter.Text):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.config(state=tkinter.DISABLED)

    def set_text(self, text):
        self.config(state=tkinter.NORMAL)
        self.delete(1.0, tkinter.END)
        self.insert(tkinter.END, text)
        self.config(state=tkinter.DISABLED)


class GameHistory:
    def __init__(self, canvas, x_left, y_top):
        self.__history_size = 20
        self.__history_offset = 0
        self.__title_id = None
        self.__canvas = canvas
        self.__title_text = 'История ходов'
        self.__x_left = x_left
        self.__y_top = y_top
        self.__initialize_text()
        self.__turns = []
        self.__text = ''

    def __initialize_text(self):
        self.__title_id = self.__canvas.create_text(self.__x_left, self.__y_top, text=self.__title_text,
                                                    font=('Arial', 16), anchor='nw')

        init_body_text = 'История пуста, сделайте первый ход'
        self.__body_id = self.__canvas.create_text(self.__x_left, self.__y_top + Y_OFFSET, text=init_body_text,
                                                   font=('Arial', 12), anchor='nw')

    def handle_user_scroll(self, event):
        if event.delta < 0:
            return self.scroll_history(1)
        return self.scroll_history(-1)

    def scroll_history(self, delta):
        if len(self.__turns) < self.__history_size:
            return

        if (self.__history_offset == 0 and delta == -1
                or self.__history_offset == self.__history_size and delta == 1):
            return

        self.__history_offset += delta
        self.show_history_text()

    def show_history_text(self):
        if len(self.__turns) > 20:
            self.__text = '\n'.join(self.__turns[self.__history_offset: self.__history_offset + self.__history_size])

        self.__canvas.itemconfig(self.__body_id, text=self.__text)

    def add_turn(self, author, turn):
        self.__text += f'{author}: {turn}\n'
        self.__turns.append(f'{author}: {turn}')
        self.show_history_text()
        self.scroll_history(1)
