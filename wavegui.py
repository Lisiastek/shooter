import pygame.font

import engine.gui as gui
from pygame.math import Vector2

class TextInWaveGui(gui.PhysicsGuiElement):
    def loop2(self, *args, **kwargs):

        if self.pos.y > self.gui.game.height // 2:
            self.waiter -= 1
        else: self.pos.y += 20
        if self.waiter < 0:
            self.kill()
    def __init__(self,scene,image,cords,group='no', *args, **kwargs):
        super().__init__(scene,image,cords,group='no', *args, **kwargs)

        self.text = kwargs['text']
        self.color = kwargs['textcolor']
        self.image = self.gui.font.render(self.text, False, (self.color))
        self.update()

        self.waiter = kwargs['textwaiter']





class WaveGui(gui.BasicGUI):
    def gen_text(self, text, color, time):
        t = TextInWaveGui(self, '', Vector2(self.game.width / 2, 0), text=text, textcolor=color, textwaiter=time)
    def __init__(self, game):
        super().__init__(game)

        self.font = pygame.font.SysFont('couriernew', 40)

        gui.BasicGuiElement(self, '', Vector2(0, self.game.height//2), visible=False, imagex=self.game.width)


