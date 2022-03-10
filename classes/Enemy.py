from classes.Entity import Entity

class Enemy(Entity):
    def __init__(self, rect, type):
        Entity.__init__(self, rect)
        self.type = type 

    def enemyRestriction(self):
        x,y = self.position
        w = self.rect.size[0]
        if self.type == "grass":
            if x + w < 0:
                return True
        else:
            if x + w < 0:
                return True
        return False
    