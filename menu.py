import engine.basic as basic
import sys
import arena

from pygame.math import Vector2


class PlayButton(basic.AdvancedElement):
    onLeftClickEnabled = True


    def onLeftClick(self):
        self.scene.game.removeScene('menu')
        self.scene.game.addScene('arena', arena.Arena(self.scene.game))
        self.scene.game.setMainScene('arena')
        self.scene.game.tempVarsRepair()

    def __init__(self, scene, image, cords, group = 'no', *args, **kwargs):
        super().__init__(scene, image, cords, group = 'no', *args, **kwargs)

class Menu(basic.Scene):
    def __init__(self, game):
        super().__init__(game)
        basic.basicElement(self, 'img/background.png', Vector2(0,0), layer=0,imagey=720,imagex=1280, topleft=True)
        PlayButton(self, 'img/start.png', Vector2(200,200), imagex=170, imagey=70)