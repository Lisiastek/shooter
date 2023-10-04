import pygame.font
import pygame

import engine.gui as gui
from pygame.math import Vector2


class ShopButton(gui.AdvancedGuiElement):
    onLeftClickEnabled = True
    def loop2(self, *args, **kwargs):
        if self.waiter > 0: self.waiter -= 1
    def onLeftClick(self):
        if self.gui.shopOpen:
            if self.waiter <= 0:
                self.waiter = 20
                match self.typeBShop:
                    case 1:
                        if self.gui.game.mainscene.pkt >= 3500:
                            self.gui.game.playSound('uwu_sound', 1)
                            self.gui.game.mainscene.pkt -= 3500
                            self.gui.game.player.damage(2)
                    case 2:
                        if self.gui.game.mainscene.pkt >= 6500:
                            self.gui.game.playSound('uwu_sound', 1)
                            self.gui.game.mainscene.pkt -= 6500
                            self.gui.game.player.damage(6)
                    case 3:
                        if self.gui.game.mainscene.pkt >= 13000:
                            self.gui.game.playSound('uwu_sound', 1)
                            self.gui.game.mainscene.pkt -= 13000
                            self.gui.game.player.damage(15)
                    case 4:
                        if self.gui.game.mainscene.pkt >= 200:
                            self.gui.game.playSound('button_sound', 1)
                            self.gui.game.mainscene.pkt -= 200
                            self.gui.game.mainscene.ammo += 1000
                    case 5:
                        match self.gui.game.mainscene.maxmagazine:
                            case 25:
                                if self.gui.game.mainscene.pkt >= 100:
                                    self.gui.game.playSound('button_sound', 1)
                                    self.gui.game.mainscene.pkt -= 100
                                    self.gui.game.mainscene.maxmagazine = 50
                                    self.image = pygame.image.load("assets/img/shop_mag2.png")
                            case 50:
                                if self.gui.game.mainscene.pkt >= 600:
                                    self.gui.game.playSound('button_sound', 1)
                                    self.gui.game.mainscene.pkt -= 600
                                    self.gui.game.mainscene.maxmagazine = 100
                                    self.image = pygame.image.load("assets/img/shop_mag3.png")
                            case 100:
                                if self.gui.game.mainscene.pkt >= 2000:
                                    self.gui.game.playSound('button_sound', 1)
                                    self.gui.game.mainscene.pkt -= 2000
                                    self.gui.game.mainscene.maxmagazine = 200
                                    self.image = pygame.image.load("assets/img/shop_mag4.png")
                            case 200:
                                if self.gui.game.mainscene.pkt >= 6000:
                                    self.gui.game.playSound('button_sound', 1)
                                    self.gui.game.mainscene.pkt -= 6000
                                    self.gui.game.mainscene.maxmagazine = 400
                                    self.image = pygame.image.load("assets/img/shop_mag5.png")
                            case 400:
                                if self.gui.game.mainscene.pkt >= 9000:
                                    self.gui.game.playSound('button_sound', 1)
                                    self.gui.game.mainscene.pkt -= 9000
                                    self.gui.game.mainscene.maxmagazine = 800
                                    self.image = pygame.image.load("assets/img/shop_mag6.png")
                            case 800:
                                if self.gui.game.mainscene.pkt >= 30000:
                                    self.gui.game.playSound('button_sound', 1)
                                    self.gui.game.mainscene.pkt -= 30000
                                    self.gui.game.mainscene.maxmagazine = 1400
                                    self.image = pygame.image.load("assets/img/shop_mag7.png")
                            case 1400:
                                if self.gui.game.mainscene.pkt >= 65000:
                                    self.gui.game.playSound('button_sound', 1)
                                    self.gui.game.mainscene.pkt -= 65000
                                    self.gui.game.mainscene.maxmagazine = 9999999999
                                    self.image = pygame.image.load("assets/img/shop_mag8.png")
                    case 6:
                        match self.gui.game.mainscene.xpoints:
                            case 1:
                                if self.gui.game.mainscene.pkt >= 2500:
                                    self.gui.game.playSound('mariocoin_sound', 1)
                                    self.gui.game.mainscene.pkt -= 2500
                                    self.gui.game.mainscene.xpoints = 1.25
                                    self.image = pygame.image.load("assets/img/shop_coin2.png")
                            case 1.25:
                                if self.gui.game.mainscene.pkt >= 5000:
                                    self.gui.game.playSound('mariocoin_sound', 1)
                                    self.gui.game.mainscene.pkt -= 5000
                                    self.gui.game.mainscene.xpoints = 2
                                    self.image = pygame.image.load("assets/img/shop_coin3.png")
                            case 2:
                                if self.gui.game.mainscene.pkt >= 15000:
                                    self.gui.game.playSound('mariocoin_sound', 1)
                                    self.gui.game.mainscene.pkt -= 15000
                                    self.gui.game.mainscene.xpoints = 3
                                    self.image = pygame.image.load("assets/img/shop_coin4.png")
                            case 3:
                                if self.gui.game.mainscene.pkt >= 30000:
                                    self.gui.game.playSound('mariocoin_sound', 1)
                                    self.gui.game.mainscene.pkt -= 30000
                                    self.gui.game.mainscene.xpoints = 4
                                    self.image = pygame.image.load("assets/img/shop_coin5.png")
                            case 4:
                                if self.gui.game.mainscene.pkt >= 60000:
                                    self.gui.game.playSound('mariocoin_sound', 1)
                                    self.gui.game.mainscene.pkt -= 60000
                                    self.gui.game.mainscene.xpoints = 5
                                    self.image = pygame.image.load("assets/img/shop_coin6.png")


    def __init__(self,scene,image,cords,group='no', *args, **kwargs):
        super().__init__(scene,image,cords,group='no', *args, **kwargs)

        self.typeBShop = kwargs['typeBShop']
        self.waiter = 0


class ExitShopButton(gui.AdvancedGuiElement):
    onLeftClickEnabled = True
    def onLeftClick(self):
        if self.gui.shopOpen:
            self.gui.grayBackGround.visible = False
            self.gui.pktInShop.visible = False
            self.gui.exitShop.visible = False
            self.gui.hp1.visible = False
            self.gui.hp2.visible = False
            self.gui.hp3.visible = False
            self.gui.ammo.visible = False
            self.gui.magazine.visible = False
            self.gui.coin.visible = False

            self.gui.game.mainscene.isupdating = True
            self.gui.shopOpen = False

    def __init__(self,scene,image,cords,group='no', *args, **kwargs):
        super().__init__(scene,image,cords,group='no', *args, **kwargs)

class ShopOpenButton(gui.AdvancedGuiElement):
    onLeftClickEnabled = True

    def onLeftClick(self):
        self.gui.shopChange()


    def __init__(self,scene,image,cords,group='no', *args, **kwargs):
        super().__init__(scene,image,cords,group='no', *args, **kwargs)


class ShopGlobal(gui.BasicGUI):
    def keys2(self, keys):
        if keys[pygame.K_e]:
            self.shopChange()
    def shopChange(self):
        if self.waiter <= 0:
            self.waiter = 20

            if self.shopOpen:
                self.grayBackGround.visible = False
                self.pktInShop.visible = False
                self.exitShop.visible = False
                self.hp1.visible = False
                self.hp2.visible = False
                self.hp3.visible = False
                self.ammo.visible = False
                self.magazine.visible = False
                self.coin.visible = False

                self.game.mainscene.isupdating = True
            else:
                self.grayBackGround.visible = True
                self.pktInShop.visible = True
                self.exitShop.visible = True
                self.hp1.visible = True
                self.hp2.visible = True
                self.hp3.visible = True
                self.ammo.visible = True
                self.magazine.visible = True
                self.coin.visible = True
                self.game.playSound('dooropen_sound', 6)

                self.game.mainscene.isupdating = False

            self.shopOpen = not self.shopOpen

    def loop(self):
        if self.waiter > 0:
            self.waiter -= 1

        if self.shopOpen:
            self.pktInShop.image = self.font.render(str(self.game.mainscene.pkt)+' PKT', False, (255,255,255))
        # self.info.update()
    def __init__(self, game):
        super().__init__(game)

        self.shopButton = ShopOpenButton(self, 'img/shopbutton.png', Vector2(self.game.width * 0.98,self.game.height * 0.80))


        self.grayBackGround = gui.BasicGuiElement(self, 'img/gray.png',
                                                  Vector2(self.game.width // 10, self.game.height * 0.02),
                                                  topleft=True, imagex=self.game.width * 0.80,
                                                  imagey=self.game.height * 0.90, visible=False)

        self.pktInShop = gui.BasicGuiElement(self, '', Vector2(180,50), layer=3, visible=False)

        self.exitShop = ExitShopButton(self, 'img/x.png', Vector2(1100, 50), layer=3, visible=False)



        self.hp1 = ShopButton(self, 'img/shop_hp1.png', Vector2(250, 150), layer=3, visible=False, typeBShop=1)
        self.hp2 = ShopButton(self, 'img/shop_hp2.png', Vector2(480, 150), layer=3, visible=False, typeBShop=2)
        self.hp3 = ShopButton(self, 'img/shop_hp3.png', Vector2(730, 150), layer=3, visible=False, typeBShop=3)

        self.ammo = ShopButton(self, 'img/shop_ammo.png', Vector2(250, 330), layer=3, visible=False, typeBShop=4)
        self.magazine = ShopButton(self, 'img/shop_mag1.png', Vector2(480, 330), layer=3, visible=False, typeBShop=5)


        self.coin = ShopButton(self, 'img/shop_coin1.png', Vector2(250, 540), layer=3, visible=False, typeBShop=6)


        self.waiter = 0
        self.shopOpen = False

        # self.info = gui.BasicGuiElement(self, '', Vector2(80, 30))
        self.font = pygame.font.SysFont('comicsansms', 25)




