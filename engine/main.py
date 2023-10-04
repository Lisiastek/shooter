#######################################################
#          TEST PYTHON ENGINE BASED ON PYGAME         #
# Orginally Created by Patryk Łata                    #
#######################################################
import copy

import pygame
import sys
from pygame.math import Vector2
from engine.basic import Player as PP
import engine.chat
import engine.startergui as startergui
import engine.fpscounter as fpc

if __name__ == '__main__':
    print("You should use this python files using import!")
    raise Exception("You should use this python files using import!")
    sys.exit()

version = "ALPH3.83"
versionINT = 00003.83

def Version():
    return version
def VersionINT():
    return versionINT

class notmain():
    def ERROR(self):
        raise Exception('Engine: mainscene isnt set!')
    def loop(self, *args, **kwargs):
        self.ERROR()
    def draw(self, *args, **kwargs):
        self.ERROR()
    def keys(self, *args, **kwargs):
        self.ERROR()
    def update(self, *args, **kwargs):
        self.ERROR()

class Engine:

    scenes = {}
    tempscenes = {}
    mainscene = "none"
    mainsceneNAME = "none"

    guis = {}
    tempguis = {}

    numberingTEMP = 0



    engineVer = version
    engineVerINT = versionINT

    running = True
    delta = 0
    enginestopped = False

    sounds = {

    }

    keylist = {
        "player_jump":pygame.K_UP,

        "player_right":pygame.K_d,
        "player_left":pygame.K_a,
        "player_up": -1,
        'player_down': -1,

        "player_sneak": pygame.K_DOWN,
        "returnPlayerTo0x0":pygame.K_l
    }


    # sound managing

    def addSound(self, name, link):
        self.sounds[name] = pygame.mixer.Sound("assets/" + link)

    def isSoundExist(self, name):
        if name in self.sounds: return True
        else: return False

    def removeSound(self, name):
        if name in self.sounds:
            del self.sounds[name]
        else:
            raise Exception('Sound named '+str(name) + ' doesnt exist!')

    def playSound(self, name, channel):
        pygame.mixer.Channel(channel).play(self.sounds[name])

    def changeVolume(self, volume):
        for i in range(pygame.mixer.get_num_channels()):
            pygame.mixer.Channel(i).set_volume(volume)

    # scenes managing

    def addScene(self, name, scene):
        if self.mainsceneNAME == name:
            raise Exception("Scene with name "+str(name)+" is currently used!\n"
                            "You cannot change scene with the same ID what already used!")
        else:
            self.scenes[name] = scene
            self._sceneup()

    def removeScene(self, name):
        if name in self.scenes:
            if self.mainsceneNAME == name:
                self.mainsceneNAME = ''
                self.mainscene = notmain()
                self.player.scene = ''
            del self.scenes[name]
            self._sceneup()
        else:
            raise Exception("Scene with name "+str(name)+" doesnt exist!")

    def isSceneExist(self, name):
        if name in self.scenes: return True
        else: return False

    def getScene(self, name):
        if name in self.scenes:
            return self.scenes[name]
        else:
            raise Exception("Scene with name "+str(name)+" doesnt exist!")

    def setMainScene(self, name):
        if name in self.scenes:
            self.mainsceneNAME = name
            self.mainscene = self.scenes[name]
            self._sceneup()
        else:
            raise Exception("Scene with name " + str(name) + " doesnt exist!")





    # guis managing
    def guiExist(self, name):
        if name in self.guis:
            return True
        else: return False
    def addGui(self, name, gui):
        self.guis[name] = gui
        self._sceneup()
        return gui
    def removeGui(self, name):
        del self.guis[name]
        self._sceneup()
    def guiON(self, name):
        self.guis[name].visible = True
        self.guis[name].isupdating = True
        self._sceneup()
    def guiOFF(self, name):
        self.guis[name].visible = False
        self.guis[name].isupdating = False
        self._sceneup()
    def guiChange(self, name):
        if self.guis[name].isupdating == True:
            self.guis[name].visible = False
            self.guis[name].isupdating = False
            self._sceneup()
        else:
            self.guis[name].visible = True
            self.guis[name].isupdating = True
            self._sceneup()
    def getGui(self, name):
        return self.guis[name]




    def engine_changestatus(self):
        self.gamestopped = not self.gamestopped


    def tempVarsRepair(self):
        self._sceneup()
    # function to make temps vars depends of "normal" vars
    def _sceneup(self):
        self.tempscenes.clear()
        self.tempguis.clear()

        for key in self.scenes.keys():
            self.tempscenes[key] = self.scenes[key]
        for key in self.guis.keys():
            self.tempguis[key] = self.guis[key]
        # self.tempscenes = self.scenes.copy()
        # self.tempguis = self.tempguis.copy()




    def loop(self):

        if self.numberingTEMP > 90:
            self.numberingTEMP = 0
            self._sceneup()
        else: self.numberingTEMP += 1

        for i in self.tempscenes.values():
            if i.isupdating:
                i.loop()
                i.update()

        for i in self.tempguis.values():
            i.loop()
            i.update()

        # self.mainscene.loop()
        # self.mainscene.update()
        if self.chat.active: self.chat.update()



        # print(self.mouseMap, self.crc)
    def draw(self):
        self.screen.fill((0, 0, 0))
        self.mainscene.draw()



        for value in self.guis.values():
            value.draw()

        if self.chat.active: self.chat.draw()

        # pygame.draw.rect(self.screen, (0, 255, 0), self.mainscene.newpicture.hitboxrect)
        # temp = self.player.rect.center - self.mainscene.offset
        temp_ = pygame.transform.scale(self.screen, pygame.display.get_surface().get_size())
        self.surf.blit(temp_, (0,0))
        pygame.display.flip()
    def keys(self, keys):
        for i in self.scenes.values():
            i.keys(keys)

        # self.mainscene.keys(keys)
        for value in self.guis.values():
            value.keys(keys)
        self.chat.keys(keys)
    def run(self):
        # basic checking

        if self.mainscene == "none":
            raise Exception('Engine: MainScene is not initiated!\n'
                            'Please use something like:\n'
                            'en.mainscene = YOURSCENE \n'
                            'or en.setMainScene("scenename")'
                            'en = Your Variable For Engine')
            sys.exit()

        while self.running:
            # print(self.crc)
            #print(pygame.mouse.get_pos()[0]*self.crc.x,pygame.mouse.get_pos()[1]*self.crc.y)
            self.draw()
            self.delta += self.clock.tick(self.maxfps)


            while self.delta > self.tickrate:
                self.delta -= self.tickrate
                events = pygame.event.get()

                self.chat.preloop()
                self.chat.loop(events)


                for Event in events:

                    if Event.type == pygame.QUIT:
                        self.running = False
                    elif Event.type == pygame.VIDEORESIZE:
                        # self.screen = pygame.surface.Surface(pygame.display.set_mode(Event.dict['size']))
                        self.repairSURF(Event.dict['size'])

                    elif Event.type == pygame.MOUSEBUTTONUP:
                        if not isinstance(self.mainscene, notmain):
                            if _tempBUTTONS[0]:
                                self.mainscene.leftClickOnce()
                            elif _tempBUTTONS[2]:
                                self.mainscene.rightClickOnce()

                self.mouseMap = Vector2(pygame.mouse.get_pos()[0] / self.crc.x + self.mainscene.offset.x,
                                        pygame.mouse.get_pos()[1] / self.crc.y + self.mainscene.offset.y)

                _tempBUTTONS = pygame.mouse.get_pressed()
                if not isinstance(self.mainscene, notmain):
                    if _tempBUTTONS[0]:
                        if _tempBUTTONS[0]:
                            if self.mainscene.isupdating: self.mainscene.leftClick()
                        elif _tempBUTTONS[2]:
                            if self.mainscene.isupdating: self.mainscene.rightClick()

                if self.enginestopped:
                    continue
                keys = pygame.key.get_pressed()
                if not self.chat.active: self.keys(keys)
                self.loop()

    def repairSURF(self, res="no"):
        argsZ = self.generateArgsForSURF()

        if res != "no": self.scaleres = Vector2(res)

        self.surf = pygame.display.set_mode(self.scaleres, *argsZ)
        self.crc.x = self.scaleres.x / self.res.x
        self.crc.y = self.scaleres.y / self.res.y

    def generateArgsForSURF(self):
        args = []
        if self.fullscreen:
            args.append(pygame.FULLSCREEN)
        if self.resizable:
            args.append(pygame.RESIZABLE)
        if self.noframe:
            args.append(pygame.NOFRAME)

        if not self.fullscreen: args.append(pygame.DOUBLEBUF)
        # if self.graphiccard:
        #     args.append(pygame.DOUBLEBUF)
        #     args.append(pygame.HWSURFACE)
        return args

    def getFps(self):
        return self.clock.get_fps()
    def getMs(self):
        return self.clock.get_time()

    def __init__(self, res, tickrate, maxfps, *args, **kwargs):

        self.res = Vector2(float(res[0]), float(res[1]))
        self.width, self.height = self.res
        self.scaleres = copy.deepcopy(self.res)
        self.crc = Vector2(0.1,0.1)
        self.mouseMap = Vector2(0,0)
        self.tickrate = tickrate
        self.maxfps = maxfps
        self.screen = pygame.surface.Surface(res)
        self.surf = pygame.display.set_mode(res, pygame.RESIZABLE)
        self.clock = pygame.time.Clock()

        pygame.mixer.pre_init(44100, -16, 20)
        pygame.init()
        pygame.font.init()


        self.globalfont = pygame.font.SysFont("arial", 14)
        self.unifontBIG = pygame.font.SysFont("segoe-ui-symbol", 35)

        self.resizable = True
        self.savelogs = False
        self.fullscreen = False
        self.noframe = False
        self.graphiccard = False

        for key, value in kwargs.items():
            key = key.lower()
            match key:
                case "resizable":
                    if value == False:
                        self.resizable = False

                case "logs":
                    if value == True:
                        self.savelogs = True
                case "scaleres":
                    self.scaleres = Vector2(value)
                case "fullscreen":
                    if value == True:
                        self.fullscreen = True
                case "noframe":
                    if value == True:
                        self.noframe = True
                case "graphiccard":
                    if value == True:
                        self.graphiccard = True
                case "caption":
                    pygame.display.set_caption(str(value))
        # argsZ = self.generateArgsForSURF()
        # self.surf = pygame.display.set_mode(self.scaleres, *argsZ)
        self.repairSURF()

        self.chat = engine.chat.chat(self)

        self.player = PP(self, Vector2(0,0))
        self.addGui('hearths', startergui.StarterGUI(self))
        self.guiON('hearths')
        # self.addGui('fpscon', fpc.getCounter(self))
        # self.guiON('fpscon')

