import pygame
import numpy as np
SCALE = 10

class mass():
    def __init__(self, x, y, mass, init_vx, init_vy):
        self.x = x
        self.y = y
        self.mass = mass
        self.colour = BLACK
        self.radius = 20
        self.vx = init_vx
        self.vy = init_vy
        self.springs = []
    
    def draw(self, win):
        x = self.x * SCALE + (WIDTH / 2)
        y = self.y * SCALE + (HEIGHT / 2)
        pygame.draw.circle(win, self.colour, (x, y), self.radius)
    
    def update(self):
        fx_tot = 0
        fy_tot = 0
        for i in self.springs:
            fx, fy = i.force()
            if self is i.object1:
                fx_tot += fx
                fy_tot += fy
            elif self is i.object2:
                fx_tot -= fx
                fy_tot -= fy
        
        ax = fx_tot / self.mass
        ay = fy_tot / self.mass

        self.vx += ax * TIMESTEP
        self.vy += ay * TIMESTEP

        self.x += self.vx * TIMESTEP
        self.y += self.vy * TIMESTEP





class wall():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.springs = []
    
    def draw(self, win):
        x = self.x * SCALE + (WIDTH / 2)
        y = self.y * SCALE + (HEIGHT / 2)
        pygame.draw.circle(win, BLACK, (x, y), 3)



class spring():
    def __init__(self, object_1, object_2, stiffness, nat_len):
        self.object1 = object_1
        self.object2 = object_2
        self.x1 = object_1.x
        self.x2 = object_2.x
        self.y1 = object_1.y
        self.y2 = object_2.y
        self.stiffness = stiffness
        self.nat_len = nat_len
        self.colour = RED
        object_1.springs.append(self)
        object_2.springs.append(self)

    def draw(self,win):
        x1, x2 = self.x1 * SCALE + (WIDTH / 2), self.x2 * SCALE + (WIDTH / 2)
        y1, y2 = self.y1 * SCALE + (HEIGHT / 2), self.y2 * SCALE + (HEIGHT / 2)
        pygame.draw.line(win, self.colour, (x1, y1), (x2, y2), 5)
    
    def force(self):
        len_x = self.x2 - self.x1
        len_y = self.y2 - self.y1
        len_tot = np.sqrt(len_x**2 + len_y**2)
        dlen = len_tot - self.nat_len
        force = dlen * self.stiffness
        fx = force * (len_x / len_tot)
        fy = force * (len_y / len_tot)
        return fx, fy

    def update(self, object_1, object_2):
        self.x1, self.x2 = object_1.x, object_2.x
        self.y1, self.y2 = object_1.y, object_2.y




pygame.init()
FPS = 60
TIMESTEP = 0.05
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mass-Spring Simulation")


WHITE = ((255, 255, 255))
BLACK = ((0, 0, 0))
RED = ((255, 0, 0))



def main():
    run = True
    clock = pygame.time.Clock()

    mass1 = mass(-3, 0, 20, 0, 1) 
    mass2 = mass(-10, 0, 5, 0, 0)
    masses = [mass1, mass2]   

    wall1 = wall(0,0)
    walls = [wall1]

    spring1 = spring(mass1, wall1, 10, 10)
    spring2 = spring(mass1, mass2, 5, 8)
    spring3 = spring(mass2, wall1, 1, 10)
    springs = [spring1, spring2, spring3]

    while run:
        clock.tick(FPS)
        WIN.fill(WHITE)

        for i in walls:
            i.draw(WIN)

        for i in masses:
            i.update()
            i.draw(WIN)

        for i in springs:
            i.update(i.object1,i.object2)
            i.draw(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        pygame.display.update()

    pygame.quit()


main()