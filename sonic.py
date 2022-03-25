"""sonic class"""
from entity import Entity
from register import height
class Sonic(Entity):
    """init sonic"""
    def __init__(self, rect):
        Entity.__init__(self, rect)
        self.health = 3
        self.speed = (0,0)
        self.position = self.rect.topleft

    def sonic_pos_restriction(self,zone):
        """restriction of sonic"""
        pos_x,pos_y = self.position
        idk = self.rect.size[1]
        if pos_y + idk > zone.bottom:
            pos_y = zone.bottom - idk
            self.speed = (0,0)
        if pos_y < zone.top:
            pos_y = zone.top
        self.position = (pos_x,pos_y)
        self.rect.topleft = self.position

    def on_floor(self):
        """check if sonic is on floor or not"""
        return self.position[1] == height - 200 - 144
