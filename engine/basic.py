# BASIC IS FOR BASIC CLASSES LIKE BASIC SPRITES AND SCENE


# Imports others
import os.path
import json
import abc
import copy
import sys
import math

# pygame imports


import pygame
from pygame.math import Vector2


# ULTRA BASIC CLASS, DOING NOTHING BUT NOT CRASHING
# ITS SHOW WHAT FUNCTIONS INSIDE CLASS DO YOU NEED TO 80% CLASSES
class ultraBasic():

    # type of your object
    type = 'none'

    def loop(self, *args, **kwargs):
        pass
    def keys(self, keys):
        pass
    def update(self, *args, **kwargs):
        pass
    def draw(self):
        pass


# basic scene class
class Scene(pygame.sprite.Group):

    # informations
    type = "SCENE"


    # Not used Yet
    isonly = True

    # # Camera Types:
    # # 0 - Normal Rendering
    # # 1 - Player Center Rendering
    # cameraType = 1


    # For Rendering
    offset = Vector2(0,0)

    # collision


    # mouse detection


    # not looping mouse detection
    @abc.abstractmethod
    def rightClickOnce(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def leftClickOnce(self, *args, **kwargs):
        pass

    #looping detection
    @abc.abstractmethod
    def rightClick(self, *args, **kwargs):
        pass
    @abc.abstractmethod
    def leftClick(self, *args, **kwargs):
        pass

    # get id




    # Offset editing

    def centerOffsetToObj(self, obj, **kwargs):
        addx = addy = 0
        for key, value in kwargs.items():
            match key:
                case "staticx":
                    staticx = value
                case "staticy":
                    staticy = value
                case "addx":
                    addx = value
                case "addy":
                    addy = value

        if 'staticx' in locals():
            self.offset.x = staticx
        else: self.offset.x = obj.pos.x - (self.game.res[0] // 2) + addx
        if 'staticy' in locals():
            self.offset.y = staticy
        else: self.offset.y = obj.pos.y - (self.game.res[1] // 2) + addy


    # Easy Function to just leave from a game, you can just change variable running against using this function
    @abc.abstractmethod
    def exitFromGame(self):
        self.game.running = False

    # function for delete all objects from scene
    def removeAllObjects(self):
        self.empty()
        self.collisionGroup.empty()
        self.L_0.empty()
        self.L_1.empty()
        self.L_2.empty()
        self.L_3.empty()
        self.L_4.empty()
        if self.game.player.scene == self:
            self.addplayerToScene()


    # Function that makes you able to Create Entities by Table
    def CreateByTable(self, table, startcords, tilesize):
        for y, temp_tile in enumerate(table):
            for x, tile in enumerate(temp_tile):


                # temp_cords = copy.deepcopy(tilesize)
                temp_cords = tilesize.copy()
                temp_cords.y *= y
                temp_cords.x *= x
                temp_cords += startcords

                temp_cords.y = temp_cords.y + (tilesize.y / 2)
                temp_cords.x = temp_cords.x + (tilesize.x / 2)

                if not tile == "-" or not tile == " ":
                    self.gen_addTile(tile, temp_cords)

    # Abstract Function that you have to define in child class before use CreateByTable Function

    @abc.abstractmethod
    def gen_addtile(self, tile, temp_cords):
        pass

    # Functions for add player to Scene or Remove from Scene (BE CAREFULLY WITH THAT!)
    # Player has to be maximum on one scene in the same time
    @abc.abstractmethod
    def addplayerToScene(self):
        if not isinstance(self.game.player.scene,str):
            self.game.player.scene.removePlayerFromScene()
        self.add(self.game.player)
        self.game.player.scene = self

    @abc.abstractmethod
    def removePlayerFromScene(self):
        # for entity in self.sprites():
        #     if isinstance(entity, Player):
        #         self.remove(entity)
        self.remove(self.game.player)
        self.game.player.scene = "UNSET"

    # Functions for managing keys systems in game
    # Be carefully with edititing keys() function, if you define it wrong
    # propably your sprites cant detect keys
    # better way is to redefine keys2() function
    @abc.abstractmethod
    def keys(self, keys):
        if self.isupdating == False:
            return
        for entity in self.sprites():
            if entity.isusekeys:
                entity.keys(keys)
        self.keys2(keys)

    @abc.abstractmethod
    def keys2(self, keys):
        pass

    # editable by user loop function (Engine runs this function by definied tickrate)
    @abc.abstractmethod
    def loop(self):
        pass

    # draw function (Be carefully with editing that)
    @abc.abstractmethod
    def draw(self, *args, **kwargs):
        if self.isdrawing:
            if self.layerRender:
                for entity in self.L_0.sprites():
                    entity.draw(self.offset)
                for entity in self.L_1.sprites():
                    entity.draw(self.offset)
                for entity in self.L_2.sprites():
                    entity.draw(self.offset)
                if self.game.player.scene == self: self.game.player.draw(self.offset)
                for entity in self.L_3.sprites():
                    entity.draw(self.offset)
                for entity in self.L_4.sprites():
                    entity.draw(self.offset)
            else:
                for entity in self.sprites():
                    entity.draw(self.offset)



    # Not editable update function (Engine runs this function by definied tickrate)
    def update(self, *args, **kwargs):
        if self.isupdating == False:
            return
        for entity in self.sprites():
            entity.loop()
            entity.update()


    def __init__(self, game):
        super().__init__()
        self.game = game
        self.isupdating = True
        self.isdrawing = True


        # layers

        self.L_0 = pygame.sprite.Group()
        self.L_1 = pygame.sprite.Group()
        self.L_2 = pygame.sprite.Group()
        self.L_3 = pygame.sprite.Group()
        self.L_4 = pygame.sprite.Group()
        self.collisionGroup = pygame.sprite.Group()


        self.layerRender = True



# basic object element
class basicElement(pygame.sprite.Sprite):

    # is this object using keys(self, keys) function?
    isusekeys = False
    isusereach = False

    # is object have to draw?
    visible = True

    # For Player Collision

    @abc.abstractmethod
    def fromUp(self, *args, **kwargs):
        pass
    @abc.abstractmethod
    def fromDown(self, *args, **kwargs):
        pass
    @abc.abstractmethod
    def fromRight(self, *args, **kwargs):
        pass
    @abc.abstractmethod
    def fromLeft(self, *args, **kwargs):
        pass


    def getId(self):
        return hash(self)

    # update rect function and another basic things
    @abc.abstractmethod
    def update(self, *args, **kwargs):
        self.rect = self.image.get_rect(center=self.pos)



    # function to use keys
    @abc.abstractmethod
    def keys(self, keys):
        pass


    # function to draw this object
    @abc.abstractmethod
    def draw(self, offset=Vector2(0,0)):
        if not self.scene == "UNSET" and self.visible != False:

            self.scene.game.screen.blit(self.image, self.rect.topleft - offset)


            # pygame.draw.rect(self.scene.game.screen, (255,255,255), temprect2)


    # function to in-tick loop (default: 20 per sec)
    @abc.abstractmethod
    def loop(self, *args, **kwargs):
        pass

    # not used yet loop2 function
    @abc.abstractmethod
    def loop2(self, *args, **kwargs):
        pass

    def __init__(self, scene, image, cords, group="NO", *args, **kwargs):

        self.scene = scene


        if not isinstance(cords, Vector2):
            cords = Vector2(cords)


        # additional group if we want
        if group != "NO":
            if not scene == "UNSET":
                super().__init__(group, scene)
            else:
                super().__init__()
        else:
            if not scene == "UNSET":
                super().__init__(scene)
            else:
                super().__init__()


        # pos
        self.pos = cords

        # object image
        image = "assets/" + image
        try:
            self.image = pygame.image.load(image)
        except:
            # if we cannot get image then try get error image
            try:
                self.image = pygame.image.load("assets/img/errortexture.png")
            except:
                print("Failed to load errortexture")


        # temp vars for kwargs reading
        imagex = self.image.get_width()
        imagey = self.image.get_height()
        resized = False
        collision = True

        for key, value in kwargs.items():
            # resizing image
            if key == "imagex":
                resized = True
                imagex = int(value)
            if key == "imagey":
                resized = True
                imagey = int(value)

            # collision disabling
            if key == "collision" and value == False:
                collision = False

        self.tempimgx = imagex
        self.tempimgy = imagey

        # if collision and scene set add to collision group
        if collision and self.scene != "UNSET":
            self.scene.collisionGroup.add(self)

        # resizing
        if resized:
            self.image = pygame.transform.scale(self.image, (imagex, imagey))


        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect(center=self.pos)


        if 'topleft' in kwargs:
            if kwargs['topleft']:
                self.pos.x = cords.x + (self.image.get_width() / 2)
                self.pos.y = cords.y + (self.image.get_height() / 2)

        if 'visible' in kwargs:
            if not kwargs['visible']:
                self.visible = False

        # layers
        if 'layer' in kwargs: self.layerNum = kwargs['layer']
        else: self.layerNum = 2


        match self.layerNum:
            case -1:
                pass
            case 0:
                self.scene.L_0.add(self)
            case 1:
                self.scene.L_1.add(self)
            case 2:
                self.scene.L_2.add(self)
            case 3:
                self.scene.L_3.add(self)
            case 4:
                self.scene.L_4.add(self)
            case _:
                pass

    def _loadimg(self, image, imagex=0, imagey=0):
        try:
            self.image = pygame.image.load(image)
        except:
            # if we cannot get image then try get error image
            try:
                self.image = pygame.image.load("assets/img/errortexture.png")
                print("Failed to load texture: " + str(image))
            except:
                print("Failed to load errortexture")

        t = False
        if imagex == 0:
            imagex = self.image.get_width()
            t = True
        if imagey == 0:
            imagey = self.image.get_width()
            t = True

        if t:
            self.image = pygame.transform.scale(self.image, (imagex, imagey))

    def _loadimgV(self, image, imagex=0, imagey=0, **kwargs):
        try:
            image = pygame.image.load(image)
        except:
            # if we cannot get image then try get error image
            try:
                image = pygame.image.load("assets/img/errortexture.png")
                print("Failed to load texture: " + str(image))
            except:
                print("Failed to load errortexture")

        # if imagex in locals():
        #     t = True
        # if imagey in locals():
        #     t = True

        t = False
        if imagex == 0:
            imagex = image.get_width()
            t = True
        if imagey == 0:
            imagey = image.get_height()
            t = True

        if t:
            image = pygame.transform.scale(image, (imagex, imagey))

        try:
            if kwargs['res'] == True: return image, imagex, imagey
            else: return image
        except:
            return image


class AdvancedElement(basicElement):


    # skins dictionary
    skins = {
        "main":"test.png"
    }

    # animations dictionary
    animations = {

    }

    anim_isOn = False
    anim_name = ''

    # idk whats for it
    helpSkinLinks = {

    }

    # current skin set
    currentskin = "main"

    # you know
    onRightClickEnabled = False
    onLeftClickEnabled = False
    onPlayerCollision = True


    # hitbox player reach
    @abc.abstractmethod
    def hitboxReach(self):
        pass


    # hitbox for clicking
    def update_hitbox(self):
        self.hitboxrect = self.rect.copy()

    # click tester
    def clicktester(self):
        if self.onRightClickEnabled and self.hitboxrect.collidepoint(self.scene.game.mouseMap) and pygame.mouse.get_pressed()[2]:
            self.onRightClick()
        if self.onLeftClickEnabled and self.hitboxrect.collidepoint(self.scene.game.mouseMap) and pygame.mouse.get_pressed()[0]:
            self.onLeftClick()

    # for user clicking
    @abc.abstractmethod
    def onRightClick(self):
        pass

    @abc.abstractmethod
    def onLeftClick(self):
        pass

    # animations managing


    def animationExist(self, name):
        if name in self.animations:
            return True
        else: return False

    def removeAnimation(self, name):
        if name in self.animations:
            del self.animations[name]
        else:
            raise Exception('Animation in ' + str(self) + 'named ' + str(name) + 'not found!')

    def generateAnimByFile(self, name, file_link):
        file_link = "assets/" + file_link
        if os.path.isfile(file_link):
            with open(file_link, "r") as file:
                temp_json = json.load(file)


                if not 'imagex' in temp_json or not 'imagex' in temp_json:
                    search = True
                else:
                    search = False
                    imagex = temp_json['imagex']
                    imagey = temp_json['imagey']


                temp_anim = {}
                frames = 0

                for key, in temp_json['animationfiles']:
                    frames += 1

                    if search:
                        temp_anim[int(key)], imagex, imagey = self._loadimgV("assets/"+temp_json['animationfiles'][key], res=True)
                        search = False
                    else:
                        temp_anim[int(key)] = self._loadimgV("assets/"+temp_json['animationfiles'][key], imagex, imagey)

                self.animations[name] = [temp_json['delay'], frames, temp_anim]


        else: return False

    def playAnimation(self, name, **kwargs):
        if name in self.animations:
            self.anim_delay = self.animations[name][0]
            self.anim_frames = self.animations[name][1]
            self.anim_isOn = True

            if not self.anim_name == name:
                self.anim_tick = 0
                self.anim_acframe = 0
                self.image = self.animations[name][2][0]

            self.anim_name = name




        else:
            raise Exception("Animation named " + str(name) + "doesnt exist!")

    def animationTick(self):

        if self.anim_isOn == False: return

        if self.anim_tick > self.anim_delay:
            self.anim_acframe += 1

            if self.anim_acframe >= self.anim_frames:
                self.anim_acframe = 0

            self.image = self.animations[self.anim_name][2][self.anim_acframe]

            self.anim_tick = 0




        else:
            self.anim_tick += 1

    def stopAnimation(self):
        self.anim_isOn = False


    # skin managing
    def setskin(self, skinname):
        if skinname in self.skins:
            currentskin = skinname
            # self.image = pygame.image.load(self.skins[skinname])
            self._loadimg(self.skins[skinname], self.tempimgx, self.tempimgy)
            self.update()

        else:
            print("error")
            return False

    def addskin(self, name, where):
        self.skins[name] = "assets/" + where

    def removeskin(self, name):
        del self.skins[name]


    @abc.abstractmethod
    def update(self, *args, **kwargs):
        self.rect = self.image.get_rect(center=self.pos)
        self.update_hitbox()

    @abc.abstractmethod
    def loop(self, *args, **kwargs):
        self.clicktester()
        self.animationTick()
        self.loop2()









    def __init__(self, scene, image, cords, group="NO", *args, **kwargs):
        super().__init__(scene, image, cords, group="NO", *args, **kwargs)
        self.addskin("main", image)
        self.update_hitbox()



# class AbstractSpriteR(pygame.sprite.Sprite):
#     def updateV2(self):
#         self.image = pygame.Surface([width, height])
#         self.rect = self.image.get_rect(center=V2)
#     def __init__(self, rect, V2):
#         super().__init__()
#         self.image = pygame.Surface([width, height])
#         self.rect = self.image.get_rect(center=V2)



# Defacto Temp vars

class AbstractSprite(pygame.sprite.Sprite):
    def __init__(self, width, height, V2):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect(center=V2)

class AbstractRect():
    def __init__(self, rect):
        self.rect = rect


# Object with Physics attributes

class PhysicElement(AdvancedElement):

    # Basic Physics
    speed = 0
    gravity = Vector2()
    isgravity = False
    noclip = False
    collisionType = 0

    # function to set self.pos based on self.rect
    def fixPosToRect(self):
        self.pos = Vector2(self.rect.center)

    # old collision system, not working currently

    # def trymove(self, **kwargs):
    #     x, y = 0.0
    #     for key, value in kwargs:
    #         match key:
    #             case "x":
    #                 x = value
    #             case "y":
    #                 y = value
    #     # temp_rect = pygame.Rect()


    # def trymove(self, V2):
    #     temp_vec = self.pos + V2
    #     temp_sprite = AbstractSprite(self.rect.width, self.rect.height, temp_vec)
    #     # temp_vec_topleftx = temp_vec.y - (self.rect.width /2)
    #     # temp_vec_toplefty = temp_vec.y - (self.rect.height / 2)
    #     # temp_vec_topleft = Vector2(temp_vec_topleftx, temp_vec_toplefty)
    #     # temp_rect = pygame.Rect(temp_vec_topleft, (self.rect.height, self.rect.width))
    #     # temp_sprite = pygame.sprite.Sprite(temp_rect)
    #     hits = pygame.sprite.spritecollide(temp_sprite, self.scene.collisionGroup, False)
    #     for entity in hits:
    #         pass




    # def collisionTester(self):
    #     for entity in self.scene.sprites():
    #         # y range
    #         if self.rect.bottom < entity.rect.top and self.rect.top < entity.rect.bottom:
    #             print("g")
    #             if self.vel.y > 0:
    #                 self.rect.bottom = entity.rect.top
    #                 self.vel.y = 0.0
    #                 self.acc.y = 0.0
    #                 self.fixPosToRect()
    #             # if self.rect.bottom > entity.rect.top:
    #             #     if self.vel.y > 0:
    #             #         self.rect.bottom = entity.rect.top
    #             #         # self.pos.y -= 1
    #             #         self.vel.y = self.acc.y = 0.0
    #             #         self.canjump = True
    #                     # self.pos.y -= self.rect.bottom - entity.rect.top - 0.5
    #             # if abs(entity.rect.bottom - self.rect.top) < 15:
    #             #     if self.vel.y < 0:
    #             #         self.rect.top = entity.rect.bottom
    #             #         self.vel.y = self.acc.y = 0.0
    #             # if abs(entity.rect.left - self.rect.right) < 15:
    #             #     if self.vel.x > 0:
    #             #         # self.pos.x -= self.rect.right - entity.rect.left
    #             #         self.rect.right = entity.rect.left
    #             #         self.vel.x = self.acc.x = 0.0
    #             # if  self.rect.left - entity.rect.right:
    #             #     if self.vel.x < 0:
    #             #         self.rect.left = entity.rect.right
    #             #         self.vel.x = self.acc.x = 0.0



    @abc.abstractmethod
    def loop(self, *args, **kwargs):
        self.Physics()
        self.clicktester()
        self.update()
        self.animationTick()
        self.loop2(*args, *kwargs)

    # trying move to specificy direction (returning new rect and velocity)
    def Physics_move(self, rect, vel):

        # position x
        rect.x += vel.x



        t = AbstractRect(rect.copy())

        if vel.x > 0:
            t.rect.x += 1
        elif vel.x < 0:
            t.rect.x -= 1

        collisions = self.collisionTest(t, self.scene.collisionGroup.sprites())
        for obj in collisions:
            if vel.x > 0:
                obj.fromRight()

                rect.right = obj.rect.left -1
                vel.x = 0
                break
            else:
                obj.fromLeft()

                rect.left = obj.rect.right +1
                vel.x = 0
                break



        # position y

        rect.y += vel.y



        tt = AbstractRect(rect.copy())

        if self.vel.y > 0:
            tt.rect.y += 1
        elif self.vel.y < 0:
            tt.rect.y -= 1


        collisions = self.collisionTest(tt, self.scene.collisionGroup.sprites())
        for obj in collisions:
            if vel.y > 0:
                self.canjump = True
                rect.bottom = obj.rect.top -1
                vel.y = 0

                obj.fromUp()

                if abs(vel.x) < 3:
                    vel.x *= 0.56
                else: vel.x *= 0.80

                break
            elif vel.y < 0:
                obj.fromDown()

                rect.top = obj.rect.bottom +1
                vel.y = 0
                break
        return rect, vel

    # function to returning all object what collide with this object
    def collisionTest(self, obj_rect, layer):
        forreturn = []
        for tile in layer:
            if pygame.sprite.collide_rect(tile, obj_rect):
                if not obj_rect.rect == self.rect:
                    forreturn.append(tile)
        return forreturn




    # for help Physics (for code, not engine)

    def help_moveto(self, to, speed):

        angle = math.atan2(self.pos.y - to.y, self.pos.x - to.x)
        x = math.cos(angle) * speed * -1
        y = math.sin(angle) * speed * -1
        return Vector2(x,y)

    # main Physics function
    def Physics(self):

        # gravity




        if self.isgravity:
            self.acc += self.gravity

        self.vel += self.acc
        self.vel = self.vel * self.air_resistance





        # fixing vel

        self.vel = Vector2(round(self.vel.x, 2), round(self.vel.y, 2))



        if self.vel.x == self.fixer.x and self.acc.x == 0.0:
            self.vel.x = 0
        if self.vel.y == self.fixer.y and self.acc.x == 0.0:
            self.vel.y = 0


        # self.fixer = copy.deepcopy(self.vel)
        self.fixer = self.vel.copy()



        # max speed
        if abs(self.vel.x) > self.maxspeedx:
            if self.vel.x > 0: self.vel.x = self.maxspeedx
            else: self.vel.x = self.maxspeedx * -1
        if abs(self.vel.y) > self.maxspeedy:
            if self.vel.y > 0: self.vel.y = self.maxspeedy
            else: self.vel.y = self.maxspeedy * -1



        # noclip (defacto just for players)
        if not self.noclip:
            self.rect, self.vel = self.Physics_move(self.rect, self.vel)
            self.fixPosToRect()
        else: self.pos += self.vel




        # restarting self.acc
        self.acc = Vector2(0, 0)






        # max y
        if self.pos.y > 2000:
            self.pos = Vector2(0,0)
            self.update()







    def __init__(self, scene, image, cords, group="NO", *args, **kwargs):
        super().__init__(scene, image, cords, group="NO", *args, **kwargs)
        self.vel = Vector2(0,0)
        self.acc = Vector2(0,0)
        self.fixer = Vector2(0,0)
        self.maxspeedx = 9999999
        self.maxspeedy = 9999999
        self.air_resistance = 0.94
        self.g = 0

        if 'gravity' in kwargs:
            self.gravity = kwargs['gravity']





# Basic character
class Character(PhysicElement):
    isgravity = True
    gravity = Vector2(0, 1)
    animationSET = {}


    def loop(self, *args, **kwargs):
        self.Physics()
        self.clicktester()
        self.update()
        self.animationTick()

        if not self.isalive():
            self.afterDie(self)
            self.kill()

        self.loop2(*args, *kwargs)


    @abc.abstractmethod
    def afterDie(self, player):
        pass

    def setAfterDieMethod(self, method):
        self.afterDie = method

    def isalive(self):
        return self.health <= 0

    def damage(self, hp):
        if hp < 0:
            # god mode
            if self.god:
                return

            self.health += hp
            if self.health < 0:
                self.health = 0
        elif hp > 0:
            self.health += hp
            if self.health > self.maxhealth:
                self.health = self.maxhealth

    def howManyParties(self, howmany):

        full = self.health // howmany
        rest = self.health - full * howmany

        return full, rest

    def __init__(self, scene, image, cords, group="NO", *args, **kwargs):
        super().__init__(scene, image, cords, group="NO", *args, **kwargs)
        self.health = 22
        self.maxhealth = 20
        self.god = False



# just players
class Player(Character):
    # what player can use
    isusekeys = True
    canjump = True
    fly = False
    speed = 1.5

    def hitboxReachTester(self):
        collisions = pygame.sprite.spritecollide(self, self.scene.sprites(), False)
        for i in collisions:
            if i.isusereach == True:
                i.hitboxReach()


    def loop(self, *args, **kwargs):
        self.Physics()
        self.clicktester()
        self.update()
        self.animationTick()
        self.hitboxReachTester()


        if self.isalive():
            self.afterDie(self)

        self.loop2(*args, *kwargs)

    def keys(self, keys):
        if self.fly:
            self.canjump = True

        if keys[self.game.keylist['player_right']]:
            self.acc.x += self.speed
            # self.setskin('right')
            if 'right' in self.animations:
                self.playAnimation('right')
            else:
                self.setskin('right')
        elif keys[self.game.keylist['player_left']]:
            self.acc.x -= self.speed
            # self.setskin('left')
            if 'left' in self.animations:
                self.playAnimation('left')
            else:
                self.setskin('left')

        if keys[self.game.keylist['player_up']]:
            self.acc.y -= self.speed
            # self.setskin('right')
            if 'up' in self.animations:
                self.playAnimation('up')
            else:
                self.setskin('up')
        elif keys[self.game.keylist['player_down']]:
            self.acc.y += self.speed
            # self.setskin('left')
            if 'down' in self.animations:
                self.playAnimation('down')
            else: self.setskin('down')

        if keys[self.game.keylist['player_jump']] and self.canjump:
            self.canjump = False
            if self.fly:
                self.acc.y -= 1
            else:
                self.acc.y -= self.jumprange

        if keys[self.game.keylist['player_sneak']] and self.fly:
            self.acc.y += 1

        if keys[self.game.keylist['returnPlayerTo0x0']]:
            self.pos = Vector2(0,0)
            self.vel = Vector2(0,0)
            self.update()



    def __init__(self, engine , cords, group="NO", *args, **kwargs):
        super().__init__("UNSET", "img/cat/right.png", cords, group=group, *args, layer=-1, **kwargs)
        self.game = engine
        self.maxspeedx = 20
        self.maxspeedy = 999999
        self.jumprange = 20

        # animations

        self.addskin('left', 'img/cat/left.png')
        self.addskin('right', 'img/cat/right.png')

        self.generateAnimByFile('left', "img/cat/leftanimation.json")
        self.generateAnimByFile('right', "img/cat/rightanimation.json")

        self.animationSET['left'] = 'left'

