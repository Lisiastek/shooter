import pygame.font
from pygame.math import Vector2
import pygame

import engine.gui as gui


class textOBJ(gui.BasicGuiElement):


    def changeText(self, color, text):
        self.text = text
        self.image = self.font.render(str(text), False, color)
        self.rect = self.image.get_rect(center=self.pos)

    def __init__(self, gui, font, pos, color, text):
        super().__init__(gui, "z", pos)
        self.gui = gui
        self.wait = 0
        self.font = font
        self.text = text

        self.changeText(color, text)


class TextGUI(gui.BasicGUI):
    def __init__(self, game, pos, font, color, text):
        super().__init__(game)
        self.offset = Vector2(0,0)

        self.text = textOBJ(self, font, pos, color, text)


def getTextGui(game, pos, font, color, text):
    return TextGUI(game, pos, font, color, text)



