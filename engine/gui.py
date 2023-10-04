import pygame
import abc

from pygame.math import Vector2

import engine.basic as bb

class BasicGUI(bb.Scene):

    type = "GUI"
    offset = Vector2(0,0)

    @abc.abstractmethod
    def draw(self, *args, **kwargs):
        if self.visible == False:
            return
        for e in self.sprites():
            e.draw(self.offset)

    def addplayerToScene(self):
        raise Exception("You cannot add player to GUI!")

    def removePlayerFromScene(self):
        raise Exception("You cannot remove player from GUI!")

    def __init__(self, game):
        super().__init__(game)

        self.visible = True

# class BasicGUI(pygame.sprite.Group):
#
#     @abc.abstractmethod
#     def keys2(self, keys):
#         pass
#     @abc.abstractmethod
#     def loop2(self, keys):
#         pass
#
#     @abc.abstractmethod
#     def keys(self, keys):
#         for e in self.sprites():
#             e.keys(keys)
#         self.keys2(keys)
#
#     @abc.abstractmethod
#     def loop(self, *args, **kwargs):
#         for e in self.sprites():
#             e.loop(*args, **kwargs)
#         self.loop2()
#
#     @abc.abstractmethod
#     def update(self, *args, **kwargs):
#         for e in self.sprites():
#             e.update(*args, **kwargs)
#
#     @abc.abstractmethod
#     def draw(self, *args, **kwargs):
#         if self.visible == False:
#             return
#
#         for e in self.sprites():
#             e.loop(*args, **kwargs)
#
#     def __init__(self, scene):
#         self.scene = scene
#         self.visible = True




class BasicGuiElement(bb.basicElement):
    def __init__(self, gui, image, pos, *args, **kwargs):
        super().__init__(gui, image, pos, *args, **kwargs)
        self.gui = gui
        self.scene = self.gui
        self.gui.add(self)

class AdvancedGuiElement(bb.AdvancedElement):
    def __init__(self, gui, image, pos, *args, **kwargs):
        super().__init__(gui, image, pos, *args, **kwargs)
        self.gui = gui
        self.scene = self.gui
        self.gui.add(self)


class PhysicsGuiElement(bb.PhysicElement):
    def __init__(self, gui, image, pos, *args, **kwargs):
        super().__init__(gui, image, pos, *args, **kwargs)
        self.gui = gui
        self.scene = self.gui
        self.gui.add(self)


