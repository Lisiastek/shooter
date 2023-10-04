# NOT CREATED YET!


import pygame.font
from pygame.math import Vector2
import pygame

import engine.gui as gui


class FPS(gui.BasicGuiElement):


    def loop(self, *args, **kwargs):
        pass

    def __init__(self, gui):
        y = self.scene.game.height * 0.15
        x = self.scene.game.width
        super().__init__(gui, "z", Vector2(50,0), imagey=y, imagex=x)
        self.gui = gui
        self.loop()
        self.update()


class DialogueManager(gui.BasicGUI):
    def __init__(self, game):
        super().__init__(game)
        self.offset = Vector2(-20,-10)

        self.counter = FPS(self)


def getCounter(game):
    return DialogueManager(game)



