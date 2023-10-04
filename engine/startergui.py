import pygame.font
from pygame.math import Vector2
import pygame

import engine.gui as gui

import sys



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


class StarterGUI(gui.BasicGUI):
    def loop(self, *args, **kwargs):
        if self.wait > self.game.tickrate:


            self.removeAllObjects()

            full, rest = self.game.player.howManyParties(4)

            start_pos = self.h_startpos.copy()


            if rest == 0:
                start_pos.x -= 40 * (full - full // 6 * 6 + full // 6)
            else:
                start_pos.x -= 40 * (full + 1 - full // 6 * 6 + full // 6)

            while full >= 6:
                full -= 6
                gui.BasicGuiElement(self, "img/hearth_gold.png", (start_pos.x, start_pos.y), imagex=32, imagey=32)
                start_pos.x += 40

            for i in range(full):
                gui.BasicGuiElement(self,"img/hearth_full.png", (start_pos.x,start_pos.y), imagex=32, imagey=32)
                start_pos.x += 40

            match rest:
                case 3:
                    gui.BasicGuiElement(self, "img/hearth_75.png", (start_pos.x,start_pos.y), imagex=32, imagey=32)
                case 2:
                    gui.BasicGuiElement(self, "img/hearth_half.png", (start_pos.x,start_pos.y), imagex=32, imagey=32)
                case 1:
                    gui.BasicGuiElement(self, "img/hearth_25.png", (start_pos.x,start_pos.y), imagex=32, imagey=32)
                case _:
                    pass


        else: self.wait += 1
    def __init__(self, game):
        super().__init__(game)
        self.offset = Vector2(0,0)

        self.h_startpos = Vector2(self.game.width * 0.97, self.game.height * 0.97)
        self.wait = 0




