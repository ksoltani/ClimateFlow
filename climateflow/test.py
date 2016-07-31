"""
Basic Pygame menu script

"""

import sys, pygame
import pygame
from support import *
 
pygame.init()
 
class Menu(object):
    def __init__(self, screen, items, bg_color=(0,0,0), font_color=(255,255,255)): 
        self.screen = screen
        self.bg_color = bg_color
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 12)
        self.font_color = font_color
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height

        self.items = []
        for index, item in enumerate(items):
            label = self.font.render(item, 1, font_color)
            width = label.get_rect().width
            height = label.get_rect().height
            t_h = len(items) * height # Total text block height
            
            posx = (self.scr_width / 2) - (width / 2)
            posy = (self.scr_height / 2) - (t_h / 2) + (index * height)
            
            self.items.append([item, label, (width, height), (posx, posy)])
 
    def run(self):
        mainloop = True
        while mainloop:
            # Limit frame speed to 50 FPS
            self.clock.tick(30)
 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False

            # Redraw the background
            self.screen.fill(self.bg_color)

            # Draw the menu
            for name, label, (width, height), (posx, posy) in self.items:
                self.screen.blit(label, (posx, posy))

            pygame.display.flip()
        return
 
if __name__ == "__main__":
    # Creating the screen
    menuitems = ("Start", "Quit")
    screen = pygame.display.set_mode((640, 480), 0, 32)
    pygame.display.set_caption('Game Menu')
    gm = Menu(screen, menuitems)
    gm.run()
