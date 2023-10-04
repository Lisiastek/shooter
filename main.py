import pygame.font

import engine.main as engine


import menu



engine = engine.Engine((1280, 720), 20, 9999, caption='Shooter')


engine.addScene('menu', menu.Menu(engine))
engine.setMainScene('menu')
engine.removeGui('hearths')

# engine.changeVolume(0.1)





engine.run()