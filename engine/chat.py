import pygame
import sys
from pygame.math import Vector2

import engine.fpscounter as fpscoun

class chat():
    numbering = 0

    # colors
    fromUser = (0,255,0) # Green
    normal = (0,0,255) # blue
    dash = (155, 221, 95)
    error = (255, 0, 0) # red

    chatmsg = []
    chatmsgColors = []

    customcommands = {}

    # command managing
    def addCommand(self, name, command):
        self.customcommands[name] = command
    def removeCommand(self, name):
        del self.customcommands[name]

    # command issues
    def command(self, args):
        args[0] = args[0].lower()
        match args[0]:
            case "/amongus" | "/sus" | "/among" | "/us":
                self.addToChatHistory(self.dash, "-----------------")
                self.addToChatHistory(self.normal, "Credo in amogum et impostores suspectos")
                self.addToChatHistory(self.normal, "Quo fugiam ab eorum spiritibus")
                self.addToChatHistory(self.normal, "")
                self.addToChatHistory(self.normal, "From A Songus Among Us")
                self.addToChatHistory(self.dash, "-----------------")
            case "/version" | "/ver" | "/engine":
                self.addToChatHistory(self.normal, "Engine Version: " + self.game.engineVer
                                      + " (" + str(self.game.engineVerINT) + ") ")
            case '/obj' | "/objects" | "/objnum" | "/objectsnumber":
                self.addToChatHistory(self.normal, "Objects in mainscene: "
                                        + str(len(self.game.mainscene.sprites())))
            case '/volume' | "/vlm" | "/vol":
                if len(args) != 2:
                    self.addToChatHistory(self.error, "Use: /volume <number>")
                    return
                if not args[1].isnumeric():
                    self.addToChatHistory(self.error, "Use: /volume <number>")
                    return
                self.game.changeVolume(float(args[1])/100)
                self.addToChatHistory(self.normal, "Global Volume has been changed")
            case '/god' | "/budha" | "/nodamage" | '/aezakami':
                self.game.player.god = not self.game.player.god
                if self.game.player.god:
                    self.addToChatHistory(self.normal, "God mode is enabled")
                else:
                    self.addToChatHistory(self.normal, "God mode is disabled")
            case "/health" | "/hl" | "/hp":
                if len(args) != 2:
                    self.addToChatHistory(self.error, "Use: /hp <number>")
                    return
                if not args[1].isnumeric():
                    self.addToChatHistory(self.error, "Use: /hp <number>")
                    return
                self.addToChatHistory(self.normal, "player's hp has been set to " + str(args[1]))
                self.game.player.health = int(args[1])

            case "/stop":
                self.game.mainscene.isupdating = not self.game.mainscene.isupdating
            case "/fps":
                if self.game.guiExist('fpscon') == False:
                    self.game.addGui('fpscon', fpscoun.getCounter(self.game))
                    self.game.guiON('fpscon')
                else: self.game.guiChange('fpscon')
            case "/cls" | "/clear" | "/cl":
                self.chatmsg.clear()
                self.chatmsgColors.clear()
                self.addToChatHistory(self.normal, "Done!")
            case "/teleport" | "/tp" | "/goto":
                self.game.player.pos = Vector2(float(args[1]), float(args[2]))
            case "/fs" | "/fullscreen":
                self.game.fullscreen = not self.game.fullscreen
                self.game.repairSURF()
                if self.game.fullscreen:
                    self.addToChatHistory(self.normal, "Fullscreen is now ON")
                else: self.addToChatHistory(self.normal, "Fullscreen is now OFF")
            case "/quit" | "/exit" | "/close" | "/stopgame" | "/shutdown":
                self.game.running = False
            case "/nc" | "/noclip":
                if self.game.player.noclip:
                    self.game.player.noclip = False
                    self.game.player.fly = False
                    self.game.player.isgravity = True
                    self.addToChatHistory(self.normal, "Noclip is now OFF")
                else:
                    self.game.player.noclip = True
                    self.game.player.fly = True
                    self.game.player.isgravity = False
                    self.addToChatHistory(self.normal, "Noclip is now ON")
            case _:
                if args[0][1:] in self.customcommands:
                    temp = args[0][1:]
                    try:
                        self.customcommands[temp](self,args)
                    except Exception as ex:
                        self.addToChatHistory(self.error, "Error with using "+str(args[0]))
                        self.addToChatHistory(self.error, "Error: " + str(ex))
                else:
                    self.addToChatHistory(self.error, "Command not found, use /help")

    # sending a message by user
    def send(self, msg):
        if msg == "":
            return

        self.addToChatHistory(self.fromUser, msg)
        args = []
        argsnum = 1
        temp_msg = msg
        while True:
            if not temp_msg.count(" "):
                args.append(temp_msg)
                break
            else:
                temp = temp_msg.find(" ")
                args.append(temp_msg[:temp])
                temp_msg = temp_msg[temp+1:]
                argsnum += 1

        if args[0][0] == "/":
            self.command(args)

        # if args[0] == "/exit":
        #     self.game.running = False
        # if args[0] == "/help":
        #     self.addToChatHistory("--------------------")
        #     self.addToChatHistory("/help <- This")
        #     self.addToChatHistory("/noclip <- noclip")
        #     self.addToChatHistory("/edit <- edit map")
        #     self.addToChatHistory("/fs <- toogle fullscreen")
        #     self.addToChatHistory("/rs <- toogle resizable")
        #     self.addToChatHistory("/cr <1> <2> <- change resolution")
        #     self.addToChatHistory("Page 1/1")
        #     self.addToChatHistory("--------------------")
        # if args[0] == "/of":
        #     if argsnum != 3:
        #         self.addToChatHistory("Uzyj /of <1> <2>")
        #     else: self.game.mainscene.offset = Vector2(float(args[1]), float(args[2]))
        # if args[0] == "/cr":
        #     if argsnum != 3:
        #         self.addToChatHistory("Uzyj /cr <1> <2>")
        #     else: self.game.repairSURF((int(args[1]), int(args[2])))
        # if args[0] == "/fs":
        #     self.game.fullscreen = not self.game.fullscreen
        #     self.game.repairSURF()
        # if args[0] == "/rs":
        #     self.game.resizable = not self.game.resizable
        #     self.game.repairSURF()
        # if args[0] == "/ng":
        #     self.game.player.isgravity = not self.game.player.isgravity
        # if args[0] == "/fly":
        #     self.game.player.fly = not self.game.player.fly
        # if args[0] == "/noclip":
        #     if self.game.player.noclip:
        #         self.game.player.noclip = False
        #         self.game.player.fly = False
        #         self.game.player.isgravity = True
        #         self.addToChatHistory("Noclip is now OFF")
        #     else:
        #         self.game.player.noclip = True
        #         self.game.player.fly = True
        #         self.game.player.isgravity = False
        #         self.addToChatHistory("Noclip is now ON")
        # if args[0] == "/tp":
        #     if argsnum == 3:
        #         self.game.player.pos = Vector2(float(args[1]), float(args[2]))
        #         self.game.player.update()
        # # for number, argument in enumerate(args):
        # #     if


    # add something to add history
    def addToChatHistory(self, color, msg):
        self.chatmsg.append(msg)
        index = len(self.chatmsg)-1
        self.chatmsgColors.append(color)


    def preloop(self):
        if self.active:
            if self.numbering > 10:
                self.numbering = 0
                self.addReady = not self.addReady
            else:
                self.numbering += 1

    def draw(self):
        self.game.screen.blit(self.textbox_img, self.textbox_rect)
        self.linebyline()
        # self.game.screen.blit(self.oldchat_img, self.oldchat_rect)
    def loop(self, events):
        self.repairlines()

        for event in events:
            if event.type == pygame.KEYUP:
                # chat writting
                if self.active:
                    if event.key == pygame.K_BACKSPACE:
                        self.textbox = self.textbox[:-1]
                    elif event.key == pygame.K_RETURN:
                        self.send(self.textbox)
                        self.textbox = ""
                        self.active = self.addReady = False
                        self.textbox_img = self.game.unifontBIG.render("", False,
                                                                       (0, 255, 0)).convert_alpha()
                    else:
                        self.textbox += event.unicode

                    # activing chat
                else:
                    if event.key == pygame.K_RETURN:
                        self.active = True
                        self.addReady = False




    def update(self):
        self.textbox_temp = self.textbox
        if self.addReady:
            self.textbox_temp += "❚"


        self.textbox_img = self.game.unifontBIG.render(self.textbox_temp, False, (0, 255,0)).convert_alpha()
        self.textbox_rect = self.textbox_img.get_rect(x = self.textbox_loc.x, y = self.textbox_loc.y)


        # self.oldchat_img = self.game.unifontBIG.render(self.acchatmsg, False, (0, 255, 0)).convert_alpha()
        # self.oldchat_loc = Vector2(pygame.display.get_surface().get_size()[0] * 0.005,
        #                            pygame.display.get_surface().get_size()[1] * 0.20)
        # self.oldchat_rect = self.oldchat_img.get_rect(x=self.oldchat_loc.x, y=self.oldchat_loc.y)




    def keys(self, keys):
        pass

    def repairlines(self):
        while len(self.chatmsg) > 10:
            self.chatmsg.pop(0)
            self.chatmsgColors.pop(0)


    def linebyline(self):
        self.oldchat_loc = Vector2(self.game.screen.get_size()[0] * 0.005,
                                   self.game.screen.get_size()[1] * 0.20)
        for key, tempchat in enumerate(self.chatmsg):
            color = self.chatmsgColors[key]
            self.oldchat_img = self.game.unifontBIG.render(tempchat, False, color).convert_alpha()
            self.oldchat_rect = self.oldchat_img.get_rect(x=self.oldchat_loc.x, y=self.oldchat_loc.y)
            self.game.screen.blit(self.oldchat_img, self.oldchat_rect)
            self.oldchat_loc.y += 40

    # def getAcChatMsg(self):
    #     if len(self.chatmsg) > 100:
    #         self.chatmsg.remove(0, len(self.chatmsg)-100)
    #
    #     self.acchatmsg = ""
    #
    #     for i, msgn in enumerate(self.chatmsg):
    #         if i > 10:
    #             break
    #         self.acchatmsg += msgn + "\n"


    def update_locs(self):
        self.textbox_loc = Vector2(self.game.screen.get_size()[0] * 0.005,
                                   self.game.screen.get_size()[1] * 0.75)
        self.oldchat_loc = Vector2(self.game.screen.get_size()[0] * 0.005,
                                   self.game.screen.get_size()[1] * 0.20)
    def __init__(self, game):
        self.game = game
        self.active = False
        self.textbox = ""
        self.textbox_temp = ""
        self.acchatmsg = ""
        self.addReady = False
        self.update_locs()
        self.update()

