"""mother class entity"""
class Entity:
    """init an entity"""
    def __init__(self,rect):
        self.rect = rect
        self.speed = (0,0)
        self.position = self.rect.topleft

    def change_speed(self, acceleration):
        """changing the speed of the entity"""
        speed_x, speed_y = self.speed
        a_x, a_y = acceleration
        self.speed = (speed_x + a_x, speed_y + a_y)

    def change_position(self,time):
        """changing the position of the entity"""
        speed_x, speed_y = self.speed
        pos_x,pos_y = self.position
        pos_x -= speed_x * time
        pos_y -= speed_y * time
        self.position = (pos_x,pos_y)
        self.rect.bottomleft = self.position
