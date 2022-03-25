"""Class enemy"""
from random import randint, choice
from entity import Entity


class Enemy(Entity):
    """init an enemy"""
    def __init__(self, rect, surface, category):
        Entity.__init__(self, rect)
        self.category = category
        self.surface = surface
        self.speed = (0,0)
        self.position = self.rect.topleft

    def enemy_restriction(self):
        """return true if enemy left his rect restriction"""
        height,_ = self.position
        width = self.rect.size[0]
        if self.category == "grass":
            if height + width < 0:
                return True
        else:
            if height + width < 0:
                return True
        return False

    def display(self, screen):
        """displaying the enemy"""
        screen.blit(self.surface, self.rect)

    def moving(self):
        """verif if moving"""
        return self.speed != (0,0)

    def run(self ,speed):
        """animate the mob"""
        if self.category == "flyingMob":
            self.change_speed(
                        (
                        speed + speed*0.05,choice([randint(int(-400+speed * 0.3),
                        int(-300+speed * 0.3)
                        ),
                        randint(
                                int(-120+speed * 0.1),
                                int(100+speed * 0.1))]
                            )
                        )
                    )
        elif self.category == "heart":
            self.change_speed((speed + randint(0,500),0))
        elif self.category == "mediumMob":
            self.change_speed((speed + speed*0.05,0))
        else:
            self.change_speed((speed,0))
    