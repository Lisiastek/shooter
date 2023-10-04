import engine.basic as basic
import sys
import engine.startergui

import math
from pygame.math import Vector2
import pygame

import random
import pktgui

import engine.particles as part

import wavegui
import shop

class Enemy2(basic.PhysicElement):
    isusereach = True

    def hitboxReach(self):

        self.scene.game.player.damage(-1)
        self.kill()
    def loop2(self, *args, **kwargs):
        self.time += 1
        if self.time > 300:
            self.kill()

    def __init__(self,scene,image,cords,group='no', *args, **kwargs):
        super().__init__(scene,image,cords,group='no', *args, **kwargs, collision=False)

        self.air_resistance = 0.99
        self.noclip = True
        self.isgravity = False

        self.maxspeedx = 100000
        self.maxspeedy = 100000

        # mp = self.scene.game.player.pos
        # angle = math.atan2(cords.y - mp.y, cords.x - mp.x)
        # self.vel.x = math.cos(angle) * 30 * -1
        # self.vel.y = math.sin(angle) * 30 * -1

        self.vel = self.help_moveto(self.scene.game.player.pos, 30)

        self.time = 0


class HealSus(basic.AdvancedElement):
    isusereach = True

    def loop2(self, *args, **kwargs):
        self.timer += 1
        if self.timer > 1000:
            self.kill()
            self.scene.pkt -= 1000
    def hitboxReach(self):

        self.scene.game.player.damage(4)
        self.scene.pkt += 400 * self.scene.xpoints
        self.kill()
        self.scene.game.playSound('healsus_sound', 3)
        part.genParticles(self.scene, 'img/hearth_full.png', 60, self.scene.game.player.pos, spreadAreay=200, spreadAreax=200)

    def __init__(self,scene,image,cords,group='no', *args, **kwargs):
        super().__init__(scene,image,cords,group='no', *args, **kwargs, collision=False)

        self.timer = 0

class Heal(basic.AdvancedElement):
    isusereach = True

    def loop2(self, *args, **kwargs):
        self.timer += 1
        if self.timer > 1000:
            self.kill()
            self.scene.pkt -= 100
    def hitboxReach(self):

        self.scene.game.player.damage(1)
        self.scene.pkt += 50 * self.scene.xpoints
        self.kill()
        self.scene.game.playSound('heal_sound', 2)
        part.genParticles(self.scene, 'img/hearth_full.png', 30, self.scene.game.player.pos, spreadAreay=100, spreadAreax=100)



    def __init__(self,scene,image,cords,group='no', *args, **kwargs):
        super().__init__(scene,image,cords,group='no', *args, **kwargs, collision=False)

        self.timer = 0

class Enemy(basic.PhysicElement):
    isusereach = True

    def loop2(self, *args, **kwargs):
        self.timer += 1
        if self.timer > 120:
            self.kill()
    def hitboxReach(self):

        self.scene.game.player.damage(-1)
        self.kill()

    def __init__(self,scene,image,cords,group='no', *args, **kwargs):
        super().__init__(scene,image,cords,group='no', *args, **kwargs, collision=False)
        self.air_resistance = 0.91
        self.noclip = True
        self.isgravity = False

        self.maxspeedx = 100000
        self.maxspeedy = 100000

        self.vel = kwargs['enemy_vel']

        self.timer = 0




class Bullet(basic.PhysicElement):
    def loop2(self, *args, **kwargs):
        self.time += 1
        if self.time > 300:
            self.kill()

        collisions = pygame.sprite.spritecollide(self, self.scene.sprites(), False)
        for i in collisions:
            if isinstance(i, Enemy) or isinstance(i, Enemy2):
                i.kill()
                self.kill()
                part.genParticles(self.scene, 'img/block_break1.png', 30, i.pos, spreadAreay=30,
                                  spreadAreax=30)
                self.scene.pkt += 7 * self.scene.xpoints

    def __init__(self,scene,image,cords,group='no', *args, **kwargs):
        super().__init__(scene,image,cords,group='no', *args, **kwargs, collision=False)

        self.air_resistance = 0.99
        self.noclip = True
        self.isgravity = False

        self.maxspeedx = 100000
        self.maxspeedy = 100000

        # mp = self.scene.game.mouseMap
        # angle = math.atan2(cords.y - mp.y, cords.x - mp.x)
        # self.vel.x = math.cos(angle) * 15 * -1
        # self.vel.y = math.sin(angle) * 15 * -1

        self.vel = self.help_moveto(self.scene.game.mouseMap, 15)

        self.time = 0



class ArenaBorder(basic.AdvancedElement):
    isusereach = True

    def hitboxReach(self):
        self.scene.game.player.pos = Vector2(200,200)

    def __init__(self,scene,image,cords,group='no', *args, **kwargs):
        super().__init__(scene,image,cords,group='no', *args, **kwargs)


def die(player):
    player.game.addScene('gameover', GameOver(player.game, player.game.mainscene.pkt))
    player.game.mainscene.removePlayerFromScene()
    player.game.removeScene(player.game.mainsceneNAME)
    player.game.removeGui('hearts')
    player.game.removeGui('pkt')
    player.game.removeGui('wavegui')
    player.game.removeGui('shopgui')
    player.game.setMainScene('gameover')
    player.game.tempVarsRepair()



class Arena(basic.Scene):
    def loop(self):
        self.waiter_bullet += 1
        self.waiter_changeLoc += 1
        self.waiter_pkt += 1
        self.waiter_heal += 1
        self.waiter_wave += 1
        self.waiter_shot += 1


        match self.wave:
            case 2:
                if self.waiter_shot > 100:
                    self.waiter_shot = 0
                    temp = random.randint(1,4)
                    match temp:
                        case 1: pos = Vector2(0,0)
                        case 2: pos = Vector2(1280,0)
                        case 3: pos = Vector2(1280,720)
                        case 4: pos = Vector2(0,720)

                    Enemy2(self, 'img/block.png', pos)
            case 3:
                if self.waiter_shot > 20:
                    self.waiter_shot = 0
                    loc = random.randint(30, 1200)
                    Enemy(self, 'img/block.png', Vector2(loc, 10), enemy_vel=Vector2(0, 30))
            case 4:
                if self.waiter_shot > 40:
                    self.waiter_shot = 0
                    loc = random.randint(30, 1200)
                    Enemy(self, 'img/block.png', Vector2(loc, 10), enemy_vel=Vector2(0, 30))



            case 5:
                if self.waiter_shot > 100:
                    self.waiter_shot = 0
                    loc = random.randint(30, 1200)
                    Enemy(self, 'img/block.png', Vector2(loc, 10), enemy_vel=Vector2(0, 30))
                    loc = random.randint(30, 1200)
                    Enemy(self, 'img/block.png', Vector2(loc, 10), enemy_vel=Vector2(0, 30))
                    loc = random.randint(30, 1200)
                    Enemy(self, 'img/block.png', Vector2(loc, 10), enemy_vel=Vector2(0, 30))

                    temp = random.randint(1,4)
                    match temp:
                        case 1: pos = Vector2(0,0)
                        case 2: pos = Vector2(1280,0)
                        case 3: pos = Vector2(1280,720)
                        case 4: pos = Vector2(0,720)

                    Enemy2(self, 'img/block.png', pos)
            case 6:
                if self.waiter_shot > 200:
                    self.waiter_shot = 0
                    temp = random.randint(1,4)
                    match temp:
                        case 1: pos = Vector2(0,0)
                        case 2: pos = Vector2(1280,0)
                        case 3: pos = Vector2(1280,720)
                        case 4: pos = Vector2(0,720)

                    Enemy2(self, 'img/block.png', pos)

                    temp = random.randint(1,4)
                    match temp:
                        case 1: pos = Vector2(0,0)
                        case 2: pos = Vector2(1280,0)
                        case 3: pos = Vector2(1280,720)
                        case 4: pos = Vector2(0,720)

                    Enemy2(self, 'img/block.png', pos)
            case 7 | 8:
                if self.waiter_shot > 300:

                    loc = random.randint(30, 1200)
                    Enemy(self, 'img/block.png', Vector2(loc, 10), enemy_vel=Vector2(0, 30))

                    loc = random.randint(720, 1200)
                    Enemy(self, 'img/block.png', Vector2(loc, 10), enemy_vel=Vector2(0, 30))

                    self.waiter_shot = 0
                    temp = random.randint(1, 4)
                    match temp:
                        case 1:
                            pos = Vector2(0, 0)
                        case 2:
                            pos = Vector2(1280, 0)
                        case 3:
                            pos = Vector2(1280, 720)
                        case 4:
                            pos = Vector2(0, 720)

                    Enemy2(self, 'img/block.png', pos)

                    temp = random.randint(1, 4)
                    match temp:
                        case 1:
                            pos = Vector2(0, 0)
                        case 2:
                            pos = Vector2(1280, 0)
                        case 3:
                            pos = Vector2(1280, 720)
                        case 4:
                            pos = Vector2(0, 720)

                    Enemy2(self, 'img/block.png', pos)
            case 9 | 10:
                if self.waiter_shot > 300:

                    loc = random.randint(30, 1200)
                    Enemy(self, 'img/block.png', Vector2(loc, 10), enemy_vel=Vector2(0, 30))

                    loc = random.randint(720, 1200)
                    Enemy(self, 'img/block.png', Vector2(loc, 10), enemy_vel=Vector2(0, 30))

                    loc = random.randint(10, 720)
                    Enemy(self, 'img/block.png', Vector2(10, loc), enemy_vel=Vector2(0, 30))

                    loc = random.randint(10,720)
                    Enemy(self, 'img/block.png', Vector2(10,loc), enemy_vel=Vector2(0, 30))


                    self.waiter_shot = 0
                    temp = random.randint(1, 4)
                    match temp:
                        case 1:
                            pos = Vector2(0, 0)
                        case 2:
                            pos = Vector2(1280, 0)
                        case 3:
                            pos = Vector2(1280, 720)
                        case 4:
                            pos = Vector2(0, 720)

                    Enemy2(self, 'img/block.png', pos)

                    temp = random.randint(1, 4)
                    match temp:
                        case 1:
                            pos = Vector2(0, 0)
                        case 2:
                            pos = Vector2(1280, 0)
                        case 3:
                            pos = Vector2(1280, 720)
                        case 4:
                            pos = Vector2(0, 720)

                    Enemy2(self, 'img/block.png', pos)

                    temp = random.randint(1, 4)
                    match temp:
                        case 1:
                            pos = Vector2(0, 0)
                        case 2:
                            pos = Vector2(1280, 0)
                        case 3:
                            pos = Vector2(1280, 720)
                        case 4:
                            pos = Vector2(0, 720)

                    Enemy2(self, 'img/block.png', pos)
            case _:
                pass

        match self.waiter_wave:
            case 55:
                self.wavegui.gen_text('FALA 1', (30, 30, 255), 40)
            case 1600:
                self.wavegui.gen_text('FALA 2', (30, 30, 255), 40)
                self.wave = 2
                self.pkt += 400 * self.xpoints
                self.game.playSound('nextwave_sound', 1)

                pos = Vector2(random.randint(100, 1100), random.randint(30, 650))
                Heal(self, 'img/hearth_full.png', pos)
                pos = Vector2(random.randint(100, 1100), random.randint(30, 650))
                Heal(self, 'img/hearth_full.png', pos)
                pos = Vector2(random.randint(100, 1100), random.randint(30, 650))
                Heal(self, 'img/hearth_full.png', pos)
            case 4000:
                self.wavegui.gen_text('FALA 3', (30, 30, 255), 40)
                self.wave = 3
                self.pkt += 400 * self.xpoints
                self.game.playSound('nextwave_sound', 1)

                pos = Vector2(random.randint(100, 1100), random.randint(30, 650))
                Heal(self, 'img/hearth_full.png', pos)
            case 4800:
                self.wavegui.gen_text('FALA 4', (30, 30, 255), 40)
                self.wave = 4
                self.pkt += 400 * self.xpoints
                self.game.playSound('nextwave_sound', 1)

                pos = Vector2(random.randint(100, 1100), random.randint(30, 650))
                Heal(self, 'img/hearth_full.png', pos)
                pos = Vector2(random.randint(100, 1100), random.randint(30, 650))
                Heal(self, 'img/hearth_full.png', pos)
                pos = Vector2(random.randint(100, 1100), random.randint(30, 650))
                Heal(self, 'img/hearth_full.png', pos)
            case 6000:
                self.wavegui.gen_text('FALA 5', (30, 30, 255), 40)
                self.wave = 5
                self.pkt += 600 * self.xpoints
                self.game.playSound('nextwave_sound', 1)



                pos = Vector2(random.randint(100, 1100), random.randint(30, 650))
                Heal(self, 'img/hearth_full.png', pos)
                pos = Vector2(random.randint(100, 1100), random.randint(30, 650))
                Heal(self, 'img/hearth_full.png', pos)
                pos = Vector2(random.randint(100, 1100), random.randint(30, 650))
                Heal(self, 'img/hearth_full.png', pos)
                pos = Vector2(random.randint(100, 1100), random.randint(30, 650))
                Heal(self, 'img/hearth_full.png', pos)
                pos = Vector2(random.randint(100, 1100), random.randint(30, 650))
                Heal(self, 'img/hearth_full.png', pos)
                pos = Vector2(random.randint(100, 1100), random.randint(30, 650))
                Heal(self, 'img/hearth_full.png', pos)
            case 9000:
                self.wavegui.gen_text('FALA 6', (30, 30, 255), 40)
                self.wave = 6
                self.pkt += 1000 * self.xpoints
                self.game.playSound('nextwave_sound', 1)


                pos = Vector2(random.randint(100, 1100), random.randint(30, 650))
                Heal(self, 'img/hearth_full.png', pos)
                pos = Vector2(random.randint(100, 1100), random.randint(30, 650))
                Heal(self, 'img/hearth_full.png', pos)
                pos = Vector2(random.randint(100, 1100), random.randint(30, 650))
                Heal(self, 'img/hearth_full.png', pos)
            case 10000:
                self.wavegui.gen_text('FALA 7', (30, 30, 255), 40)
                self.wave = 7
                self.pkt += 1500 * self.xpoints
                self.game.playSound('nextwave_sound', 1)

                pos = Vector2(random.randint(100, 1100), random.randint(30, 650))
                Heal(self, 'img/hearth_full.png', pos)
                pos = Vector2(random.randint(100, 1100), random.randint(30, 650))
                Heal(self, 'img/hearth_full.png', pos)
                pos = Vector2(random.randint(100, 1100), random.randint(30, 650))
                Heal(self, 'img/hearth_full.png', pos)
                pos = Vector2(random.randint(100, 1100), random.randint(30, 650))
                Heal(self, 'img/hearth_full.png', pos)
                pos = Vector2(random.randint(100, 1100), random.randint(30, 650))
                Heal(self, 'img/hearth_full.png', pos)
                pos = Vector2(random.randint(100, 1100), random.randint(30, 650))
                Heal(self, 'img/hearth_full.png', pos)
            case 11200:
                self.wavegui.gen_text('FALA 8', (30, 30, 255), 40)
                self.wave = 8
                self.pkt += 2000 * self.xpoints
                self.game.playSound('nextwave_sound', 1)

                pos = Vector2(random.randint(100, 1100), random.randint(30, 650))
                Heal(self, 'img/hearth_full.png', pos)
                pos = Vector2(random.randint(100, 1100), random.randint(30, 650))
                Heal(self, 'img/hearth_full.png', pos)
                pos = Vector2(random.randint(100, 1100), random.randint(30, 650))
                Heal(self, 'img/hearth_full.png', pos)
                pos = Vector2(random.randint(100, 1100), random.randint(30, 650))
                HealSus(self, 'img/sus.png', pos)
                pos = Vector2(random.randint(100, 1100), random.randint(30, 650))
                HealSus(self, 'img/sus.png', pos)

            case 14400:
                self.wavegui.gen_text('FALA 9', (30, 30, 255), 40)
                self.wave = 9
                self.pkt += 2000 * self.xpoints
                pygame.mixer.Sound.play(self.nextwave_sound)

                pos = Vector2(random.randint(100, 1100), random.randint(30, 650))
                Heal(self, 'img/hearth_full.png', pos)
                pos = Vector2(random.randint(100, 1100), random.randint(30, 650))
                Heal(self, 'img/hearth_full.png', pos)
                pos = Vector2(random.randint(100, 1100), random.randint(30, 650))
                Heal(self, 'img/hearth_full.png', pos)
                pos = Vector2(random.randint(100, 1100), random.randint(30, 650))
                HealSus(self, 'img/sus.png', pos)
                pos = Vector2(random.randint(100, 1100), random.randint(30, 650))
                HealSus(self, 'img/sus.png', pos)

            case 18800:
                self.wavegui.gen_text('FALA INFINITY', (30, 30, 255), 40)
                self.wave = 10
                self.pkt += 3000 * self.xpoints
                self.game.playSound('nextwave_sound', 1)
                # pygame.mixer.Sound.play(self.nextwave_sound)

                pos = Vector2(random.randint(100, 1100), random.randint(30, 650))
                Heal(self, 'img/hearth_full.png', pos)
                pos = Vector2(random.randint(100, 1100), random.randint(30, 650))
                Heal(self, 'img/hearth_full.png', pos)
                pos = Vector2(random.randint(100, 1100), random.randint(30, 650))
                Heal(self, 'img/hearth_full.png', pos)
                pos = Vector2(random.randint(100, 1100), random.randint(30, 650))
                HealSus(self, 'img/sus.png', pos)
                pos = Vector2(random.randint(100, 1100), random.randint(30, 650))
                HealSus(self, 'img/sus.png', pos)

        if self.waiter_heal > 1000:
            self.waiter_heal = 0
            pos = Vector2(random.randint(100, 1100), random.randint(30, 650))
            Heal(self, 'img/hearth_full.png', pos)
            Heal(self, 'img/hearth_full.png', pos)
            if self.wave == 10:
                Heal(self, 'img/hearth_full.png', pos)
                HealSus(self, 'img/sus.png', pos)
                HealSus(self, 'img/sus.png', pos)


        if self.waiter_pkt > 10:
            self.waiter_pkt = 0
            self.pkt += (1 * self.xpoints)

        if self.waiter_changeLoc > 200:
            self.waiter_changeLoc = 0
            self.enemy_loc = random.randint(1,4)


        if self.waiter_enemy > 10:
            self.waiter_enemy = 0
            match self.enemy_loc:
                case 1:
                    loc = random.randint(30, 1200)
                    Enemy(self, 'img/block.png', Vector2(loc, 10), enemy_vel=Vector2(0, 30))
                case 2:
                    loc = random.randint(30, 1200)
                    Enemy(self, 'img/block.png', Vector2(loc, 720), enemy_vel=Vector2(0, -30))
                case 3:
                    loc = random.randint(20, 700)
                    Enemy(self, 'img/block.png', Vector2(10,loc), enemy_vel=Vector2(30, 0))
                case 4:
                    loc = random.randint(20, 700)
                    Enemy(self, 'img/block.png', Vector2(1280,loc), enemy_vel=Vector2(-30, 0))


        else: self.waiter_enemy += 1


        # reload system

        if self.waiter_reload > 0: self.waiter_reload -= 1
        if self.waiter_reload == 0:
            self.waiter_reload -= 1
            temp_ = abs(self.maxmagazine - self.magazine)

            if temp_ > self.ammo:
                temp_ = self.ammo

            self.ammo -= temp_
            self.magazine += temp_

            # temp_ = self.maxmagazine
            # temp_remove = self.maxmagazine
            #
            # if(self.maxmagazine < self.ammo):
            #     temp_ = abs(self.ammo)
            #     temp_remove = abs(self.ammo)
            #
            # if self.magazine + temp_ > self.maxmagazine:
            #     temp2_ = temp_ + self.magazine - self.maxmagazine
            #     self.ammo += temp2_
            #
            #     temp_ = self.maxmagazine
            #     # temp_remove = selftemp2_)
            #
            #
            # self.ammo -= temp_remove
            # self.magazine = temp_


    def leftClick(self, *args, **kwargs):
        # basic.basicElement(self, '', Vector2(self.game.mouseMap), )



        if self.waiter_bullet > 2:
            if self.magazine > 0 and self.waiter_reload <= 0:
                self.game.playSound('shoot_sound', 0)
                # pygame.mixer.Sound.play(self.shoot_sound)
                self.waiter_bullet = 0
                Bullet(self, 'img/bullet.png', self.game.player.pos, layer=4)
                self.magazine -= 1
            else:
                self.game.playSound('cantshoot_sound', 0)



    def keys2(self, keys):
        if keys[pygame.K_r] and self.waiter_reload <= 0:
            self.game.playSound('reload_sound', 0)
            self.waiter_reload = abs(self.reloadTime)

    def __init__(self, game):
        super().__init__(game)
        basic.basicElement(self, 'img/txt.png', Vector2(0,0), layer=0,topleft=True, imagex=1280, imagey=720, collision=False)
        self.addplayerToScene()
        self.game.player.isgravity = False
        self.game.player.maxspeedx = 20
        self.game.player.pos = Vector2(200,200)

        self.game.addGui('hearts', engine.startergui.StarterGUI(self.game))
        self.game.addGui('pkt', pktgui.GuiGlobal(self.game))
        self.wavegui = self.game.addGui('wavegui', wavegui.WaveGui(self.game))
        self.game.addGui('shopgui', shop.ShopGlobal(self.game))

        self.wavegui.gen_text('START!', (30,30,30), 40)

        self.game.keylist['player_jump'] = -1
        self.game.keylist['player_up'] = pygame.K_w
        self.game.keylist['player_down'] = pygame.K_s

        self.game.player.addskin('down', 'img/cat/new_down.png')
        self.game.player.addskin('up', 'img/cat/new_up.png')
        self.game.player.addskin('left', 'img/cat/new_left.png')
        self.game.player.addskin('right', 'img/cat/new_right.png')

        if self.game.player.animationExist('left'):
            self.game.player.removeAnimation('left')
            self.game.player.removeAnimation('right')

        self.game.player.setskin('down')
        self.game.player.health = 4


        ArenaBorder(self, '', Vector2(-10, 0), imagex=1300, imagey=10,topleft=True, visible=False)
        ArenaBorder(self, '', Vector2(0, -10), imagex=10, imagey=1300, topleft=True, visible=False)
        ArenaBorder(self, '', Vector2(1280, -10), imagex=10, imagey=1300, topleft=True, visible=False)
        ArenaBorder(self, '', Vector2(-10, 720), imagex=1300, imagey=10, topleft=True, visible=False)


        self.game.addSound('shoot_sound', '/sounds/shoot.wav')
        self.game.addSound('heal_sound', '/sounds/heal.mp3')
        self.game.addSound('healsus_sound', '/sounds/healsus.mp3')
        self.game.addSound('nextwave_sound', '/sounds/nextwave.mp3')
        self.game.addSound('cantshoot_sound', 'sounds/cannot.wav')
        self.game.addSound('reload_sound', 'sounds/reload.mp3')
        self.game.addSound('uwu_sound', 'sounds/uwu.mp3')
        self.game.addSound('mariocoin_sound', 'sounds/mariocoin.mp3')
        self.game.addSound('button_sound', 'sounds/button.mp3')
        self.game.addSound('dooropen_sound', 'sounds/dooropen.mp3')



        # self.shoot_sound = pygame.mixer.Sound("assets/sounds/shoot.wav")
        # self.heal_sound = pygame.mixer.Sound("assets/sounds/heal.mp3")
        # self.healsus_sound = pygame.mixer.Sound("assets/sounds/healsus.mp3")
        # self.nextwave_sound = pygame.mixer.Sound("assets/sounds/nextwave.mp3")




        self.waiter_bullet = 0
        self.waiter_enemy = 0
        self.waiter_changeLoc = 0
        self.waiter_pkt = 0
        self.waiter_heal = 0
        self.waiter_shot = 0
        self.enemy_loc = 1

        self.wave = 1
        self.waiter_wave = 0
        self.waiter_reload = 0


        self.pkt = 0
        self.ammo = 300
        self.maxmagazine = 25
        self.magazine = 20
        self.reloadTime = 60
        self.xpoints = 1


        self.game.player.maxhealth = 900
        self.game.player.setAfterDieMethod(die)


class RestartButton(basic.AdvancedElement):
    onLeftClickEnabled = True

    def onLeftClick(self):
        self.scene.game.removeScene(self.scene.game.mainsceneNAME)
        self.scene.game.addScene('arena', Arena(self.scene.game))
        self.scene.game.setMainScene('arena')

    def __init__(self,scene,image,cords,group='no', *args, **kwargs):
        super().__init__(scene,image,cords,group='no', *args, **kwargs)



class GameOver(basic.Scene):
    def __init__(self, game, pkt):
        super().__init__(game)

        # self.gameover_sound = pygame.mixer.Sound("assets/sounds/gameover.mp3")
        self.game.addSound('gameover_sound', 'sounds/gameover.mp3')
        self.game.playSound('gameover_sound', 2)

        self.title = basic.basicElement(self, '', Vector2(640, 160))
        self.info =  basic.basicElement(self, '', Vector2(640, 260))
        self.restart = RestartButton(self, 'img/repeat.png', Vector2(640, 400), imagex=120, imagey=120)

        self.font_title = pygame.font.SysFont('comicsansms', 60)
        self.font_info = pygame.font.SysFont('comicsansms', 20)

        self.title.image = self.font_title.render('GameOver', False, (255,0,0))
        self.info.image = self.font_info.render('PKT: ' + str(pkt), False, (255,40,0))



