import pygame.font
from pygame.math import Vector2
import pygame

import engine.gui as gui


class FPS(gui.BasicGuiElement):


    def loop(self, *args, **kwargs):
        if self.wait > self.gui.game.tickrate / 2:
            self.wait = 0
            self.image = self.font.render(str(int(self.gui.game.getFps()))+"FPS"+
                                          " "+str(int(self.gui.game.getMs()))+"MS", False, (255, 255, 255))
        else: self.wait += 1

    def __init__(self, gui):
        super().__init__(gui, "z", Vector2(50,0))
        self.gui = gui
        self.wait = 0
        self.font = pygame.font.SysFont("arial", 20)

        self.loop()
        self.update()


class CounterGUI(gui.BasicGUI):
    def __init__(self, game):
        super().__init__(game)
        self.offset = Vector2(-20,-10)

        self.counter = FPS(self)


def getCounter(game):
    return CounterGUI(game)



