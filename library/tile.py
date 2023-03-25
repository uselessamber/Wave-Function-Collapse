import random
import pygame

class tile:
    #bit:
    #0001 - up (y - 1)
    #0010 - right (x + 1)
    #0100 - down (y + 1)
    #1000 - left (x - 1)
    def __init__(self, tile = 0, size = 10, skin = "connector"):
        self.skin = skin
        self.tile = tile
        self.tile_size = size
        self.restriction_rule = 0 #the value of the restricted bits
        self.restriction_bit = 0 #the positions of the restricted bits
        self.collapsed = False
        self.update_image()

    def add_restriction(self, bit_pos, bit_value):
        bit_value &= 1
        self.restriction_bit |= (1 << bit_pos)
        self.restriction_rule &= ~(1 << bit_pos)
        self.restriction_rule |= (bit_value << bit_pos)

    def apply_restriction(self, value):
        #idea: Value & ~the positions of the restriction bits, reversing 0 -> 1 and 1 -> 0 --> bits at positions that are unrestricted will not be collapsed to 0, bits that are restricted got collapsed to 0. The value then perform operation Or with the restriction rule, setting the restricted bits to the rule. The rule is also & with the restriction bits to avoid noise data (if exist)
        return (value & ~(self.restriction_bit)) | (self.restriction_rule & self.restriction_bit)

    def collapse(self):
        if not self.collapsed:
            self.tile = random.randint(0, 15)
            self.tile = self.apply_restriction(self.tile)
            self.collapsed = True
            self.update_image()
    
    def update_image(self):
        self.image = pygame.image.load(f"tiles/{self.skin}/{self.tile & 15}.png")
        self.image = pygame.transform.scale(self.image, (self.tile_size, self.tile_size))
        self.rect = self.image.get_rect()

    def get_entropy(self):
        return 2 ** (4 - self.restriction_bit.bit_count())

    def return_image(self):
        return self.image, self.rect