import pygame.font

import engine.gui as gui
from pygame.math import Vector2



class GuiGlobal(gui.BasicGUI):
    def loop(self):
        self.info.image = self.font.render(str(self.game.mainscene.pkt) + ' PKT', False, (255,255,255))
        self.ammo.image = self.font.render(str(self.game.mainscene.magazine) + '/' + str(self.game.mainscene.ammo), False, (255,255,255))
        self.info.update()
    def __init__(self, game):
        super().__init__(game)
        self.info = gui.BasicGuiElement(self, '', Vector2(80, 30))
        self.ammo = gui.BasicGuiElement(self, '', Vector2(100, 700))
        self.font = pygame.font.SysFont('comicsansms', 25)




