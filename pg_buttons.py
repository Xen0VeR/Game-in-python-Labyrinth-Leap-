import pygame
from os.path import isfile, join

pygame.init()
Main_font = pygame.font.Font(join("Assets","Font","font.ttf"),50)

class Buttons():
    def __init__(self, image, position, text):
        self.image = image
        self.x = position[0]
        self.y = position[1]
        self.text = text
        self.text_out = Main_font.render(self.text,False,"#F8F6E3")
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x,self.y))
        self.text_rect = self.text_out.get_rect(center=(self.x,self.y))

    def update(self,Window):
        if self.image is not None:
            Window.blit(self.image,self.rect)
        Window.blit(self.text_out,self.text_rect)

    def Check_input(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
        
    def Hover_over(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text_out = Main_font.render(self.text,False,"#97E7E1")
        else:
            self.text_out = Main_font.render(self.text,False,"#F8F6E3")

