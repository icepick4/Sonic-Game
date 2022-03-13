class Entity:
    def __init__(self,rect):
        self.rect = rect
        self.speed = (0,0)
        self.position = self.rect.topleft 
    
    def changeSpeed(self, acceleration):
        speedX, speedY = self.speed
        aX, aY = acceleration
        self.speed = (speedX + aX, speedY + aY)

    def changePosition(self,time):
        speedX, speedY = self.speed
        x,y = self.position
        x -= speedX * time
        y -= speedY * time
        self.position = (x,y)
        self.rect.bottomleft = self.position

        
        
    

